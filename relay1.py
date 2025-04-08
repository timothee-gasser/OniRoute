import socket

relay_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
relay_socket.bind(('127.0.0.1', 8001))
relay_socket.listen(1)
print("Relai1 en attente de connexion client...")

client_conn, client_addr = relay_socket.accept()
print(f"Client connecté depuis {client_addr}")


client_msg = client_conn.recv(1024).decode()
print("Message du client :", client_msg)


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.connect(('127.0.0.1', 8002))
server_socket.send(client_msg.encode())


server_response = server_socket.recv(1024).decode()
print("Réponse du serveur :", server_response)


client_conn.send(server_response.encode())


server_socket.close()
client_conn.close()
relay_socket.close()
