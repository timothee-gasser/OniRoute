import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1', 9000))
server_socket.listen(1)
print("Serveur en attente de connexion...")

conn, addr = server_socket.accept()
print(f"Connexion du relai : {addr}")

data = conn.recv(1024).decode()
print("Message reçu du relai :", data)

response = f"Message reçu : '{data}' - signé le Serveur"
conn.send(response.encode())

conn.close()
server_socket.close()
