import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 7001))

message = "Bonjour, ici le client2 !"
client_socket.send(message.encode())

response = client_socket.recv(1024).decode()
print("Réponse finale reçue :", response)

client_socket.close()