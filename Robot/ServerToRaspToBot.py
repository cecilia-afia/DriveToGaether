import serial
import sys
import time

if __name__ == '__main__':
	ser = serial.Serial('/dev/ttyUSB0',9600,timeout=1)
	ser.reset_input_buffer()
	command = sys.argv[1]
	nb = ser.write("Wake up command".encode()) #create a connexion with the bot, allowing the real command to be received
	time.sleep(5) # we give some time to the bot
	nb = ser.write(command.encode()) # send the real command
	print(ser.readline().decode('utf-8'))
	ser.close()
