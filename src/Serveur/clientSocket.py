import socket
MAX_SIZE = 2048

def client_function():
    #host = socket.gethostname()  # only works when the server and the client are working on the same machine
    #host = input("Choose the name of the host (you can find it once the server is launched) : ")
    host = "25.26.61.36"
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

    message = input("Message to be transmitted : ")  # first message that'll be send

    while message.lower().strip() != 'quit': # better than a devastating Ctrl + C 
        client_socket.send(message.encode())  # send message
        data = client_socket.recv(MAX_SIZE).decode()  # receive response

        print('Received from server: ' + data)  # show in terminal

        message = input(" Message to be transmitted : ")  # send a new message

    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_function()
