# coding: utf-8

import os
import select
import socket
import struct
import sys
import time
import logging

if sys.platform.startswith("win32"):
    # On Windows, the best timer is time.clock()
    default_timer = time.clock
else:
    # On most other platforms the best timer is time.time()
    default_timer = time.time

# ICMP parameters
ICMP_ECHOREPLY = 0 # Echo reply (per RFC792)
ICMP_ECHO = 8 # Echo request (per RFC792)
ICMP_MAX_RECV = 2048 # Max size of incoming buffer

MAX_SLEEP = 1000


def _calculate_checksum(source_string):
    """
    A port of the functionality of in_cksum() from ping.c
    Ideally this would act on the string as a series of 16-bit ints (host
    packed), but this works.
    Network data is big-endian, hosts are typically little-endian
    """
    countTo = (int(len(source_string) / 2)) * 2
    sum = 0
    count = 0

    # Handle bytes in pairs (decoding as short ints)
    loByte = 0
    hiByte = 0
    while count < countTo:
        if (sys.byteorder == "little"):
            loByte = source_string[count]
            hiByte = source_string[count + 1]
        else:
            loByte = source_string[count + 1]
            hiByte = source_string[count]
        sum = sum + (ord(hiByte) * 256 + ord(loByte))
        count += 2

    # Handle last byte if applicable (odd-number of bytes)
    # Endianness should be irrelevant in this case
    if countTo < len(source_string): # Check for odd length
        loByte = source_string[len(source_string) - 1]
        sum += ord(loByte)
    
    # Truncate sum to 32 bits (a variance from ping.c, which
    # uses signed ints, but overflow is unlikely in ping)
    sum &= 0xffffffff 

    sum = (sum >> 16) + (sum & 0xffff)    # Add high 16 bits to low 16 bits
    sum += (sum >> 16)                    # Add carry from above (if any)
    answer = ~sum & 0xffff                # Invert and truncate to 16 bits
    answer = socket.htons(answer)

    return answer

def _is_valid_ip4_address(addrl):

    parts = addrl.split(".")
    if not len(parts) == 4:
        return False
    for part in parts:
        try:
            number = int(part)
        except ValueError:
            return False
        if number > 255:
            return False
    return True

def _to_ip(addr):
    if _is_valid_ip4_address(addr):
        return addr
    return socket.gethostbyname(addr)
        
def _header2dict(names, struct_format, data):
    """ unpack the raw received IP and ICMP header informations to a dict """
    unpacked_data = struct.unpack(struct_format, data)
    return dict(zip(names, unpacked_data))
        
def _send_pings(current_socket,dest_ip_list,own_id,seq_number,packet_size):
    """
    Send ICMP ECHO_REQUEST
    """
    # Header is type (8), code (8), checksum (16), id (16), sequence (16)
    checksum = 0

    # Make a dummy header with a 0 checksum.
    header = struct.pack(
        "!BBHHH", ICMP_ECHO, 0, checksum, own_id, seq_number
    )

    padBytes = []
    startVal = 0x42
    for i in range(startVal, startVal + (packet_size)):
        padBytes += [(i & 0xff)]  # Keep chars in the 0-255 range
#         data = bytes(padBytes) # For python3
     
    data = ''
    for byt in padBytes:
        data += chr(byt) # python2.7 sendto() need a string 

    # Calculate the checksum on the data and the dummy header.
    checksum = _calculate_checksum(header + data) # Checksum is in network order

    # Now that we have the right checksum, we put that in. It's just easier
    # to make up a new header than to stuff it into the dummy.
    header = struct.pack(
        "!BBHHH", ICMP_ECHO, 0, checksum, own_id, seq_number
    )

    packet = header + data
    send_time = {}

    try:
        for dest_ip in dest_ip_list:
            send_time[dest_ip] = default_timer()
            current_socket.sendto(packet, (dest_ip, 1)) # Port number is irrelevant for ICMP
    except socket.error as e:
        current_socket.close()
        return
    return send_time

def _receive_pings(current_socket,src_ip_list,timeout,own_id):
    """
    Receive the ping from the socket. timeout = in ms
    """
    timeout = timeout / 1000.0
    receive_time = {}
    while True: # Loop while waiting for packet or timeout
        select_start = default_timer()
        inputready, outputready, exceptready = select.select([current_socket], [], [], timeout)
        select_duration = (default_timer() - select_start)
        if inputready == []: # timeout
            return receive_time

        rec_time = default_timer()

        packet_data, address = current_socket.recvfrom(ICMP_MAX_RECV)
    
        icmp_header = _header2dict(
            names=["type", "code", "checksum",
                   "packet_id", "seq_number"],
            struct_format="!BBHHH",
            data=packet_data[20:28])
    
        if icmp_header["packet_id"] == own_id: # Our packet
            ip_header = _header2dict(
                names=["version", "type", "length",
                    "id", "flags", "ttl", "protocol",
                    "checksum", "src_ip", "dest_ip"],
                struct_format="!BBHHHBBHII",
                data=packet_data[:20])
            
            packet_size = len(packet_data) - 28
            src_ip = socket.inet_ntoa(struct.pack("!I", ip_header["src_ip"]))
            # XXX: Why not ip = address[0] ???
            
            if src_ip in src_ip_list:
                receive_time[src_ip] = rec_time

        timeout = timeout - select_duration
        if timeout <= 0:
            return receive_time
#     return receive_time

def pings(destination, timeout=1000, packet_size=55, own_id=None):
    '''
    If you use pings(), the destination must be a list. 
    Return a dictionary for destination and receive time.
    For example:
    {'192.168.1.13': False,'www.qq.com': 0.007228921158497624}
    '''
    
    seq_number = 0
    dstips = {}
    result = {}
    
    if isinstance(destination, list):
        for dest in destination:
            dest_ip = _to_ip(dest)
            dstips[dest_ip] = dest
            result[dest] = False
            
    else:
        typ = str(type(destination))[1:-1]
        err_msg = "The destination must be a 'list', not %s"%typ
        logging.error(err_msg)
        raise TypeError,err_msg   
    
    if own_id is None:
        own_id = os.getpid() #& 0xFFFF
    else:
        own_id = own_id

    dest_ip_list = dstips.keys()
    current_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname("icmp"))
    send_time = _send_pings(current_socket,dest_ip_list,own_id,seq_number,packet_size)
    receive_time = _receive_pings(current_socket,dest_ip_list,timeout,own_id)
    current_socket.close()
    
    for ip in receive_time.keys():
        result[dstips[ip]] = receive_time[ip]-send_time[ip]
   
    return result

def _send_a_ping(current_socket,dest_ip,own_id,seq_number,packet_size):
    """
    Send one ICMP ECHO_REQUEST
    """
    # Header is type (8), code (8), checksum (16), id (16), sequence (16)
    checksum = 0

    # Make a dummy header with a 0 checksum.
    print 1
    print ICMP_ECHO,checksum,own_id,seq_number
    header = struct.pack(
        "!BBHHH", ICMP_ECHO, 0, checksum, own_id, seq_number
    )

    padBytes = []
    startVal = 0x42
    for i in range(startVal, startVal + (packet_size)):
        padBytes += [(i & 0xff)]  # Keep chars in the 0-255 range
#         data = bytes(padBytes) # For python3
     
    data = ''
    for byt in padBytes:
        data += chr(byt) # python2.7 sendto() need a string 

    # Calculate the checksum on the data and the dummy header.
    checksum = _calculate_checksum(header + data) # Checksum is in network order

    # Now that we have the right checksum, we put that in. It's just easier
    # to make up a new header than to stuff it into the dummy.
    header = struct.pack(
        "!BBHHH", ICMP_ECHO, 0, checksum, own_id, seq_number
    )

    packet = header + data
    
    send_time = default_timer()
    try:    
        current_socket.sendto(packet, (dest_ip, 1)) # Port number is irrelevant for ICMP
    except socket.error as e:
        current_socket.close()
        return
    return send_time

def _receive_a_ping(current_socket,src_ip,timeout,own_id):
    """
    Receive the ping from the socket. timeout = in ms
    """
    timeout = timeout / 1000.0
    receive_time = None
    while True: # Loop while waiting for packet or timeout
        select_start = default_timer()
        inputready, outputready, exceptready = select.select([current_socket], [], [], timeout)
        select_duration = (default_timer() - select_start)
        if inputready == []: # timeout
            return receive_time

        receive_time = default_timer()

        packet_data, address = current_socket.recvfrom(ICMP_MAX_RECV)
    
        icmp_header = _header2dict(
            names=["type", "code", "checksum",
                   "packet_id", "seq_number"],
            struct_format="!BBHHH",
            data=packet_data[20:28])
    
        if icmp_header["packet_id"] == own_id: # Our packet
            ip_header = _header2dict(
                names=["version", "type", "length",
                    "id", "flags", "ttl", "protocol",
                    "checksum", "src_ip", "dest_ip"],
                struct_format="!BBHHHBBHII",
                data=packet_data[:20])
            
            packet_size = len(packet_data) - 28
            ip = socket.inet_ntoa(struct.pack("!I", ip_header["src_ip"]))
            # XXX: Why not ip = address[0] ???
            if ip == src_ip:
                return receive_time

        timeout = timeout - select_duration
        if timeout <= 0:
            return receive_time
#     return receive_time

def ping(destination, timeout=1000, packet_size=55, own_id=None):
    '''
    If you use ping(), the destination must be string.
    '''
    seq_number = 0
    
    if isinstance(destination, str):
        dest_ip = _to_ip(destination)
      
    else:
        typ = str(type(destination))[1:-1]
        err_msg = "The destination must be a 'str', not %s"%typ
        logging.error(err_msg)
        raise TypeError,err_msg   
    
    if own_id is None:
        own_id = os.getpid() & 0xFFFF
    else:
        own_id = own_id

    current_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname("icmp"))
    send_time = _send_a_ping(current_socket,dest_ip,own_id,seq_number,packet_size)
    receive_time = _receive_a_ping(current_socket,dest_ip,timeout,own_id)
    current_socket.close()
    
    if receive_time:
        rec_time = receive_time-send_time
        return rec_time
    else:
        return False
    
def ping_ip_list_and_print(iplist,timeout=1000):
    '''
    If you use this function, we will print the result in the logging.
    Do not return anything.
    '''
    packet_size = 64
    seq_number = 0
    
    if isinstance(iplist, list):
        pass
    else:
        typ = str(type(iplist))[1:-1]
        err_msg = "The iplist must be a 'list', not %s"%typ
        logging.error(err_msg)
        raise TypeError,err_msg 
    
    own_id = os.getpid() #& 0xFFFF
    
    current_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname("icmp"))
    _send_pings(current_socket,iplist,own_id,seq_number,packet_size)
    
    timeout = timeout / 1000.0
    
    while True: # Loop while waiting for packet or timeout
        select_start = default_timer()
        inputready, outputready, exceptready = select.select([current_socket], [], [], timeout)
        select_duration = (default_timer() - select_start)
        if inputready == []: # timeout
            break 

        receive_time = default_timer()

        packet_data, address = current_socket.recvfrom(ICMP_MAX_RECV)
    
        icmp_header = _header2dict(
            names=["type", "code", "checksum",
                   "packet_id", "seq_number"],
            struct_format="!BBHHH",
            data=packet_data[20:28])
    
        if icmp_header["packet_id"] == own_id: # Our packet
            ip_header = _header2dict(
                names=["version", "type", "length",
                    "id", "flags", "ttl", "protocol",
                    "checksum", "src_ip", "dest_ip"],
                struct_format="!BBHHHBBHII",
                data=packet_data[:20])
            
            packet_size = len(packet_data) - 28
            ipr = socket.inet_ntoa(struct.pack("!I", ip_header["src_ip"]))
            
            if ipr in iplist:
                logging.info('Ping %s ok!'%ipr)
                iplist.remove(ipr)
                
        timeout = timeout - select_duration
        if timeout <= 0:
            break
        
    for ip in sorted(iplist):
        logging.error('Ping %s failed!'%ip)
        
    current_socket.close()
    
     
if __name__ == '__main__':
#     t = time.clock()
#     iplist = 1
#     iplist = ['192.168.1.1','172.168.8.85','www.qq.com','www.baidu.com','www.163.com']
    iplist = ['192.168.1.1','172.168.8.85','192.168.1.13','192.168.1.14','172.168.8.81']
    sorted(iplist)
#     ip = '192.168.1.1'
#     iplist = ['www.qq.com','www.baidu.com','www.163.com','192.168.1.11','192.168.1.1','172.168.8.81','192.168.1.13','172.168.8.82',]
#     r = ping(iplist,count=1)
#     print pings(iplist)
#     print ping(ip)
    ping_ip_list_and_print(iplist)

#     print time.clock() - t
#     time.sleep(3)
#     ip = 'www.qq.com'
#     r = ping(ip,count=1)
#     print r.min_rtt
