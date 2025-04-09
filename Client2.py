import socket

relay1= '127.0.0.1',7002
relay2= '127.0.0.1',8001
serveur = '127.0.0.1',9000

data = "Bonjour, ici le client !"

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((relay1))

message = f"{relay2},{serveur},{data}"
client_socket.send(message.encode())

response = client_socket.recv(1024).decode()
print("Réponse finale reçue :", response)

client_socket.close()
