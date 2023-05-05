import socket
import sys

MAX_SIZE = 2048

def client_function(hostip):
    
    #host = socket.gethostname()  # only works when the server and the client are working on the same machine
    host = hostip
    port = input("Choose a port number (you can find it once the server is launched): ")  # socket server port number

    print(host)

    ## TESTING PORT ##
    if port == '':
        port = 5000 # arbitrary number, was used during previous experiment
        print("Port initialized with 5000: can't be NULL")

    elif int(port) < 1024:
        port = 5000 # arbitrary number, was used during previous experiment
        print("Port initialized with 5000: port can't be >= 1024")

    
    port = int(port)
    ## END TESTING PORT ##

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # try to connect to the server

    message = ""
    while message.lower().strip() != 'quit': # better than a devastating Ctrl + C 
        recv = client_socket.recv(MAX_SIZE).decode()
        print("Received from server: %s" %recv)  # show in terminal

        message = input("Message to be transmitted : ")  # message that'll be send
        client_socket.send(message.encode())  # send message

    client_socket.close()  # close the connection


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage : python3 %s <server_ipv4>"%sys.argv[0])
        exit(1)
    client_function(sys.argv[1])
