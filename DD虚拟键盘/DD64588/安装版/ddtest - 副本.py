import ctypes
import time
import win32con
import logging

#dd = ctypes.WinDLL("DD32.dll")
#dd.DD_mov(0, 0)
#time.sleep(2)
#print win32con.VK_ESCAPE

#print win32con.VK_RSHIFT
#print dd.DD_todc(win32con.VK_RSHIFT)
#dd.DD_str("dfajdklADJKFA")

def main():
	logging.error("1111111111111111")
	try:
		logging.info("11111111111111112")
	except Exception,e:
		logging.error("error 111111111111112")

if __name__ == '__main__':
	try:
		print win32con.VK_ESCAPE
		main()
	except Exception,e:
		logging.error("error 111111111111112")
