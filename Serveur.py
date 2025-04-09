import socket
import threading

def handle_client(conn, addr):
    print(f"[Serveur] Connexion depuis {addr}")

    try:
        data = conn.recv(1024).decode()
        print(f"[Serveur] Message reçu : {data}")

        response = f"[Serveur] Reçu : '{data}'"
        conn.send(response.encode())

    except Exception as e:
        print(f"[Serveur] Erreur avec {addr} : {e}")
    finally:
        conn.close()
        print(f"[Serveur] Connexion fermée avec {addr}")

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 9000))
    server_socket.listen()
    print("[Serveur] En attente de connexions...")

    while True:
        conn, addr = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[Serveur] Clients actifs : {threading.active_count() - 1}")

if __name__ == "__main__":
    start_server()
