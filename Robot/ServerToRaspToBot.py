import serial
import sys
import time

if __name__ == '__main__':
	ser = serial.Serial('/dev/ttyUSB0',9600,timeout=1)
	ser.reset_input_buffer()
	
	while True:
		ser.write(sys.argv[1].encode())
		line = ser.readline().decode('utf-8').rstrip()
		print(line)
		time.sleep(1)
	
