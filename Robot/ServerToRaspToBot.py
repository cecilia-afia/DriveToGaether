import serial
import sys
import time

if __name__ == '__main__':
	ser = serial.Serial('/dev/ttyUSB0',9600,timeout=1)
	ser.reset_input_buffer()
	is_executed = False
	test = "move"
	while not(is_executed):
		ser.write(test.encode())
		time.sleep(1)
		line = ser.readline().decode('utf-8').rstrip()
		print(line)
		if "O" in line or "N" in line:
			is_executed = True
			
			
		
	
