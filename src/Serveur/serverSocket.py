import socket
nb_players = 2
MAX_SIZE = 2048

def server_function():
    #host = socket.gethostname() #get the name of host's machine
    host = "25.26.61.36"
    print("hostname = %s"%host)

    port = input("Choose a port number : ")

    ## TESTING PORT ##
    if port == '':
        port = 5000 # arbitrary number, was used during previous experiment
        print("Port initialized with 5000: can't be NULL")

    elif int(port) < 1024:
        port = 5000 # arbitrary number, was used during previous experiment
        print("Port initialized with 5000: port can't be >= 1024")

    
    port = int(port)
    ## END TESTING PORT ##

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
    server_function()