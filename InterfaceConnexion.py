import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import json
import socket

host = 'localhost'
port = 9001

def handle_login():
    username = entry_username.get()
    password = entry_password.get()

    # Création de la demande de connexion
    request = {
        'type': 'login',
        'username': username,
        'password': password
    }
    request_json = json.dumps(request)

    # Connexion au serveur
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    # Envoi de la demande de connexion
    client_socket.send(request_json.encode())

    # Réception de la réponse du serveur
    response = client_socket.recv(1024).decode()
    response_data = json.loads(response)

    # Affichage de la réponse du serveur
    messagebox.showinfo('Status', response_data['message'])

    # Fermeture de la connexion
    client_socket.close()

# Création de la fenêtre
window = tk.Tk()
window.title('Connexion')
window.geometry('300x200')

# Création des styles
style = ttk.Style()
style.configure('Custom.TLabel', font=('Verdana', 10))
style.configure('Custom.TEntry', font=('Verdana', 10))
style.configure('Custom.TButton', font=('Verdana', 10), foreground='black', background='#0077cc')
style.map('Custom.TButton', foreground=[('active', '!disabled', 'white')], background=[('active', '#0099ff')])

label_username = ttk.Label(window, text='Nom d\'utilisateur', style='Custom.TLabel')
label_username.pack()

entry_username = ttk.Entry(window, style='Custom.TEntry')
entry_username.pack()

label_password = ttk.Label(window, text='Mot de passe', style='Custom.TLabel')
label_password.pack()

entry_password = ttk.Entry(window, show='*', style='Custom.TEntry')
entry_password.pack()

button_login = ttk.Button(window, text='Se connecter', command=handle_login, style='Custom.TButton')
button_login.pack()

# Boucle principale de la fenêtre
window.mainloop()