import socket
import sys
import subprocess
from _thread import *

nb_players = 8
MAX_SIZE = 2048

def server_function(conn,numClient):
    global nbClientConnectes
    recv = ""
    data = "Connected to the server"
    conn.send(data.encode())  # send data to the client

    while True:
        recv = conn.recv(MAX_SIZE).decode()
        if not recv or recv == "quit": # if a client stopped the connection
            print("End of communication with the client %d"%numClient)
            break
        print("from client number",numClient,": " + str(recv))
        cmd = ['../Robot/ServerToRaspToBot.py',recv]
        #exec(open(cmd).read())
        subprocess.run(["python3"] + cmd)
        print("salut")
        #data = input("Response : ")
        #data = "OK"

        if (data.lower().strip() == "end"):
            conn.close()
            server_socket.close()

        conn.send(recv.encode())  # send data to the client

    nbClientConnectes -= 1
    conn.close()  # close the connection

if __name__ == '__main__':

    try:
        ## TESTING CORRECT USAGE ##
        if len(sys.argv) != 2:
            print("Usage : python3 %s <server_ipv4>"%sys.argv[0])
            sys.exit(1)
        ## END TESTING USAGE

        #host = socket.gethostname() #get the name of host's machine
        host = sys.argv[1]
        print("hostip = %s"%host)

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
        nbClientConnectes = 0
        try: 
            while True:
                conn, address = server_socket.accept()  # accept new connection
                print("Connection from: " + str(address))
                nbClientConnectes+=1
                start_new_thread(server_function,(conn,nbClientConnectes))
                print("A new client is connected, for a total of: %d"%nbClientConnectes)
            server_socket.close()

        except KeyboardInterrupt:
            print("\nProgram ended after the creation of the server, you need to also interrupt any left client")
            server_socket.close()
            sys.exit(3)
    except KeyboardInterrupt:
            print("\nProgram ended before the creation of the server")
            sys.exit(2)
