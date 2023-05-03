import socket
nb_players = 10
MAX_SIZE = 2048

def server_socket():
    host = socket.gethostname() #get the name of host's machine
    port = int(input("Chose a port number : ")) # arbitrary number, was used during previous experiment
    if port == "" or port < 1024:
        port = 5000
    server_socket = socket.socket()  # create the socket
    server_socket.bind((host, port))  # bind host address and port together

    server_socket.listen(nb_players) # the server will be able to listen up to <nb_players> connections
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    while True:
        data = conn.recv(MAX_SIZE).decode()
        if not data:
            break
        print("from connected user: " + str(data))
        data = input(' -> ')
        conn.send(data.encode())  # send data to the client

    conn.close()  # close the connection


if __name__ == '__main__':
    server_socket()