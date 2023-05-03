import socket
MAX_SIZE = 2048

def client_socket():
    host = socket.gethostname()  # only works when the server and the client are working on the same machine
    port = int(input("Chose a port number: (careful, the port number must be the same as the server's one!)"))  # socket server port number
    if port == "" or port < 1024:
        port = 5000
    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    message = input("Message à transmettre : ")  # take input

    while message.lower().strip() != 'quit':
        client_socket.send(message.encode())  # send message
        data = client_socket.recv(MAX_SIZE).decode()  # receive response

        print('Received from server: ' + data)  # show in terminal

        message = input(" Message à transmettre ")  # again take input

    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_socket()
