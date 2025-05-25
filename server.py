import socket
import threading
import os

# Server Configuration
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5000
BUFFER_SIZE = 1024
STORAGE_DIR = "server_storage"

# Authentication Function
def authenticate(username, password):
    with open("id_passwd.txt", "r") as f:
        for line in f:
            stored_username, stored_password = line.strip().split(',')
            if username == stored_username and password == stored_password:
                return True
    return False

# Client Handler Function
def handle_client(client_socket, address):
    print(f"\t\t\t\t\t\t\t\t\t      --------------------------")
    print(f"\t\t\t\t\t\t\t\t\t      | {address} |")
    print(f"\t\t\t\t\t\t\t\t\t      --------------------------")
    try:
        client_socket.send("\nHello my habibi, enter your username (in lower case only)".encode())
        username = client_socket.recv(BUFFER_SIZE).decode()
        client_socket.send("\nEnter your password".encode())
        password = client_socket.recv(BUFFER_SIZE).decode()

        if not authenticate(username, password):
            client_socket.send("\nDAI, who are you?! Disconnecting.".encode())
            client_socket.close()
            return

        client_socket.send("\nAuthentication Successful".encode())
        user_dir = os.path.join(STORAGE_DIR, username)
        os.makedirs(user_dir, exist_ok=True)

        while True:
            command = client_socket.recv(BUFFER_SIZE).decode()
            if command == "UPLOAD":
                filename = client_socket.recv(BUFFER_SIZE).decode()
                file_path = os.path.join(user_dir, filename)
                with open(file_path, "wb") as f:
                    bytes_read = client_socket.recv(1024)
                    f.write(bytes_read)
                client_socket.send("Upload Complete".encode())

            elif command == "DOWNLOAD":
                filename = client_socket.recv(BUFFER_SIZE).decode()
                file_path = os.path.join(user_dir, filename)
                if os.path.exists(file_path):
                    client_socket.send("FILE FOUND".encode())
                    with open(file_path, "rb") as f:
                        bytes_read = f.read(1024)
                        client_socket.send(bytes_read)
                else:
                    client_socket.send("File Not Found".encode())

            elif command == "LIST":
                files = os.listdir(user_dir)
                if not files:
                    client_socket.send("Empty".encode())
                else:
                    client_socket.send(", ".join(files).encode())

            elif command == "DELETE":
                filename = client_socket.recv(BUFFER_SIZE).decode()
                file_path = os.path.join(user_dir, filename)
                if os.path.exists(file_path):
                    os.remove(file_path)
                    client_socket.send(f"File {filename} deleted successfully.".encode())
                else:
                    client_socket.send("File Not Found.".encode())

            elif command == "QUIT":
                client_socket.send("Goodbye!".encode())
                break

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

# Server Setup
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen()
    print(f"\n\t\t\t\t\t\tThis BD project was made with <3 by Harish K, Greeshma S Harish, Keerthana and Bhuvan :D")
    print(f"\n\t\t\t\t\t\t\t\t\tServer listening on {SERVER_HOST} : {SERVER_PORT}\n")

    while True:
        client_socket, address = server_socket.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket, address))
        client_handler.start()

if __name__ == "__main__":
    start_server()
