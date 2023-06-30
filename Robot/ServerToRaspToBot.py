import serial
import sys
import time

if __name__ == '__main__':
	ser = serial.Serial('/dev/ttyUSB0',9600,timeout=1)
	ser.reset_input_buffer()
	is_executed = False
	ser.write(sys.argv[1].encode())
	start_time = time.time()
	timeout = 5
	
	while True:
		if ser.in_waiting > 5:
			line = ser.readline().decode('utf-8').rstrip()
			print(line)
			break
		if time.time() - start_time > timeout:
			print("Wot")
			break	
		
	
