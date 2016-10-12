import ctypes
import time
import win32con
dd = ctypes.WinDLL("DD32.dll")
#dd.DD_mov(0, 0)
#time.sleep(2)
print win32con.VK_ESCAPE

print win32con.VK_RSHIFT
#print dd.DD_todc(win32con.VK_RSHIFT)
#dd.DD_str("dfajdklADJKFA")

