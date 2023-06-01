import socket
import json
import sqlite3
import random
import string
import threading

host = 'localhost'
port = 9001


connected_players = []
victim_positions = []
loaded_victims = []


def read_configuration_file(file_path):
    terrain_info = {}

    try:
        with open(file_path, 'r') as file:
            for line in file:
                # Ignorer les lignes vides et les lignes de commentaire commençant par #
                if line.strip() == '' or line.strip().startswith('#'):
                    continue

                # Séparer la clé et la valeur en utilisant le signe égal (=) comme séparateur
                key, value = line.strip().split('=')

                # Ajouter la paire clé-valeur au dictionnaire des informations du terrain
                terrain_info[key.strip()] = value.strip()

    except FileNotFoundError:
        print(f"Le fichier {file_path} n'a pas été trouvé.")
    except Exception as e:
        print(f"Une erreur s'est produite lors de la lecture du fichier : {str(e)}")

    return terrain_info

    

# Vérifier si la position donnée correspond à l'hôpital
def is_hospital_position(x, y):
    hospital_x = 50  # Coordonnée X de l'hôpital (exemple)
    hospital_y = 50  # Coordonnée Y de l'hôpital (exemple)
    return x == hospital_x and y == hospital_y



# Générer les positions aléatoires des victimes sur la carte
def generate_victim_positions():
    global victim_positions
    victim_positions = []  # Réinitialiser les positions des victimes

    num_victims = random.randint(5, 10)  # Nombre aléatoire de victimes entre 5 et 10
    for _ in range(num_victims):
        x = random.randint(0, 100)  # Coordonnée X aléatoire entre 0 et 100
        y = random.randint(0, 100)  # Coordonnée Y aléatoire entre 0 et 100
        victim_positions.append((x, y))  # Ajouter la position à la liste



# Vérifier si la position donnée correspond à une victime
def is_victim_position(x, y):
    return (x, y) in victim_positions

def is_valid_credentials(username, password):
    #if username == "admin" and password == "admin":
     #   return True
    #else:
     #   return False
    
    conn = sqlite3.connect('C:\\Users\\PC\\database.db')
    cursor = conn.cursor()

    # Requête pour récupérer les informations de l'utilisateur en fonction du nom d'utilisateur
    query = "SELECT username, password FROM users WHERE username = admin"
    cursor.execute(query, (username,))
    result = cursor.fetchone()

    # Vérification du mot de passe
    if result is not None and password == result[1]:
        return True
    else:
        return False

    # Fermer la connexion à la base de données après utilisation
    conn.close()

def create_session(username):
    # Générer un identifiant de session unique
    session_id = generate_session_id()

    # Enregistrer la session dans une base de données ou une structure de données appropriée
    save_session(session_id, username)

    # Renvoyer l'identifiant de session généré
    return session_id

def generate_session_id():
    # Générer un identifiant de session aléatoire
    letters = string.ascii_letters + string.digits
    session_id = ''.join(random.choice(letters) for _ in range(10))
    return session_id



def save_session(session_id, username):
    # Enregistrer la session dans une base de données en utilisant SQLite

    # Se connecter à la base de données
    connection = sqlite3.connect('C:\\Users\\PC\\database.db')
    cursor = connection.cursor()

    # Insérer la session dans la table des sessions
    cursor.execute("INSERT INTO sessions (session_id, username) VALUES (?, ?)", (session_id, username))

    # Valider les changements et fermer la connexion
    connection.commit()
    connection.close()


def start_server():
    # Créer une socket TCP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Lier la socket à l'adresse et au port spécifiés
        server_socket.bind((host, port))
    except socket.error as e:
        print("Erreur lors de la liaison de la socket :", str(e))
        exit()

    # Écouter les connexions entrantes
    server_socket.listen(10)
    print("Le serveur est en marche")

    # Accepter les connexions et gérer les clients
    while True:
        # Accepter une nouvelle connexion
        conn, addr = server_socket.accept()
        print("Un joueur est connecté :", addr)

        # Gérer la connexion du client dans un thread séparé
        # Ca permet au serveur de gérer plusieurs clients en parallèle
        client_thread = threading.Thread(target=handle_client_connection, args=(conn,))
        client_thread.start()

if __name__ == '__main__':
    start_server()


# Fonction pour récupérer la victime à partir de la position
def get_victim_at_position(x, y):
    for victim in victim_positions:
        if victim['x'] == x and victim['y'] == y:
            return victim
    return None

# Fonction pour récupérer le véhicule du joueur
def get_player_vehicle(username):
    for player in connected_players:
        if player['username'] == username:
            return player['vehicle']
    return None

def increase_player_score(username, score_increase):
    # Recherche du joueur dans la liste des joueurs connectés
    for player in connected_players:
        if player['username'] == username:
            # Augmentation du score du joueur
            player['score'] += score_increase
            break

# Si les victimes avaient des types (c'est un exemple pour voir si ça marche)
def calculate_score_increase(victim):
    score_increase = 0
    if victim == 'victim_type1':
        score_increase = 10
    elif victim == 'victim_type2':
        score_increase = 20
    elif victim == 'victim_type3':
        score_increase = 30
    else:
        score_increase = 5

    return score_increase


def handle_client_connection(conn):
    # Attendre les données du client
    data = conn.recv(1024).decode()
    if not data:
        return

    # Analyser les données JSON envoyées par le client
    try:
        request = json.loads(data)
    except json.JSONDecodeError:
        return

    if 'type' not in request:
        return

    # Gérer la demande en fonction du type
    if request['type'] == 'login':
        if 'username' not in request or 'password' not in request:
            return

        username = request['username']
        password = request['password']

        # Vérification de l'authentification du joueur
        if is_valid_credentials(username, password):
            session_id = create_session(username)
            connected_players.append({'username': username, 'session_id': session_id})

            response = {'status': 'success', 'message': 'Connexion réussie', 'session_id': session_id}
        else:
            response = {'status': 'failure', 'message': 'Échec de la connexion'}
        
        # Envoyer la réponse au client
        conn.send(json.dumps(response).encode())


                     ######## Logique de jeu à revoir avec Valentin #########

    elif request['type'] == 'move':
        if 'direction' not in request:
            return

        direction = request['direction']
        current_x = 0  # Coordonnée X actuelle du joueur (à remplacer par la valeur réelle)
        current_y = 0  # Coordonnée Y actuelle du joueur (à remplacer par la valeur réelle)

        # Calculer les nouvelles coordonnées en fct de la direction
        if direction == 'left':
            new_x = current_x - 1
            new_y = current_y
        elif direction == 'right':
            new_x = current_x + 1
            new_y = current_y
        elif direction == 'up':
            new_x = current_x
            new_y = current_y - 1
        elif direction == 'down':
            new_x = current_x
            new_y = current_y + 1
        else:
            return

        response = {'status': 'success'}

        # Vérifier si le joueur a atteint une victime
        if is_victim_position(new_x, new_y):
            response['message'] = 'Victime trouvée !'
            # Récupérer la victime à partir de la position actuelle du joueur
            victim = get_victim_at_position(new_x, new_y)
            if victim is not None:
                # Charger la victime dans le véhicule du joueur
                player_vehicle = get_player_vehicle(username)
                player_vehicle['victims'].append(victim)

                # Supprimer la victime de la liste des positions des victimes
                victim_positions.remove((new_x, new_y))

                # Répondre avec un message indiquant que la victime a été chargée avec succès
                response['message'] = 'Victime chargée avec succès !'
            else:
                # La position correspond à une victime inexistante ou déjà chargée
                response['message'] = 'Aucune victime trouvée à cette position.'

        # Vérifier si le joueur est arrivé à l'hôpital
        elif is_hospital_position(new_x, new_y):
            response['message'] = 'Victime déposée à l\'hôpital !'
            # Récupérer le véhicule du joueur
            player_vehicle = get_player_vehicle(username)

            # Vérifier si le joueur a des victimes dans son véhicule
            if len(player_vehicle['victims']) > 0:
                # Déposer la victime à l'hôpital
                deposited_victim = player_vehicle['victims'].pop(0)  # Supprimer la première victime du véhicule

                # Enregistrer la victime déposée à l'hôpital

                # Ma structure de données pour stocker les informations des victimes déposées à l'hôpital (à revoir avecc Valentin)
                hospital_records = []

                # Je suppose que la variable 'deposited_victim' contienne les informations de la victime déposée à l'hôpital

                # Ajouter la victime déposée à la liste des enregistrements de l'hôpital
                hospital_records.append(deposited_victim)

                # Augmenter le score du joueur en fonction de la victime déposée (ou alors le score peut être unique)
                score_increase = calculate_score_increase(deposited_victim)
                increase_player_score(username, score_increase)

                # Affichage des informations de la victime déposée à l'hôpital (à revoir)
                print("Victime déposée à l'hôpital :")
                print("Nom : ", deposited_victim['name'])
                print("Score ajouté au joueur :", score_increase)

                # Répondre avec un message indiquant que la victime a été déposée avec succès à l'hôpital
                response['message'] = 'Victime déposée à l\'hôpital avec succès !'
            else:
                # Le joueur n'a pas de victimes dans son véhicule
                response['message'] = 'Aucune victime à déposer à l\'hôpital.'


        else:
            response['message'] = 'Déplacement effectué.'

        # Envoyer la réponse au client
        conn.send(json.dumps(response).encode())


    # Fermer la connexion du client
    conn.close()
