# SERVEUR

!!! POUR LE MOMENT, CETTE METHODE NE SERT QUE POUR LES TESTS ET PEUT ETRE AMENEE A CHANGER VOIRE ENTIEREMENT DISPARAITRE !!!

To run the server:
  -
  - Install Hamachi : https://www.vpn.net/linux
  - Install Haguichi (allow to use Hamachi):  
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
  - Retrieve ipv4 adress from haguichi and pass it to the "host" variable in "serverSocket.py"
  - Run "serverPocket.py":
  ```sh
  python3 serverSocket.py
  ```
  - Choose a port number (all the clients need the same)
  - Wait for the clients to connect

To run the client:
   - Wait for the server to be ready
   - Retrieve the hostname (should be printed when the server is being runned) and pass it to the "host" variable in "clientSocket.py"
   - Retrieve the port number (should be printed when the server is being runned) and pass it to the "port" variable in "clientSocket.py"
   - Send the cutest message to the server you've got
   - Hope it works
