# SERVEUR

!!! POUR LE MOMENT, CETTE METHODE NE SERT QUE POUR LES TESTS ET PEUT ETRE AMENEE A CHANGER VOIRE ENTIEREMENT DISPARAITRE !!!

In both cases:
-
- Install Hamachi : https://www.vpn.net/linux
  - Install Haguichi (allow to use Hamachi on Linux):  
  ```sh 
  sudo add-apt-repository -y ppa:ztefn/haguichi-stable
  sudo apt update
  sudo apt install -y haguichi
  ```
  - Run Haguichi :
  ```sh
  haguichi&
  ```
  - Configure haguichi by pressing "Configure" (doesn't need any humain input)
  - Retrieve ipv4 of the server from Haguichi or Hamachi
  
To run the server:
  -
  - Create a new network/join an already created one with Haguichi (Linux) or Hamachi (Windows)
  - Retrieve the ipv4 of the machine that'll serve as the server from Haguichi or Hamachi
  - Run "serverPocket.py":
  ```sh
  python3 serverSocket.py <server_ipv4>
  ```
  - Choose a port number (all the clients need the same)
  - Wait for the clients to connect

To run the client:
   -
   - Connect to the server with Hamachi
   - Wait for the server to be ready
   - Retrieve the hostname (should be printed when the server is being runned)
   - Run "clientSocket.py":
   ```sh
  python3 clientSocket.py <server_ipv4>
  ```
   - Retrieve the port number (should be printed when the server is being runned) and enter it
   - Send the cutest message to the server you've got
   - Hope it works
