import socket
import os

# Client Configuration
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5000
BUFFER_SIZE = 1024

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_HOST, SERVER_PORT))

    # Initial welcome message from the server
    print(client_socket.recv(BUFFER_SIZE).decode())

    # Authentication
    username = input("\nUsername : ")
    client_socket.send(username.encode())
    print(client_socket.recv(BUFFER_SIZE).decode())  # Prompt for password

    password = input("Password : ")
    client_socket.send(password.encode())
    
    auth_response = client_socket.recv(BUFFER_SIZE).decode()
    print(auth_response)
    if "Authentication Successful" not in auth_response:
        client_socket.close()
        return

    # Main command loop
    while True:
        command = input("\nEnter command (UPLOAD, DOWNLOAD, LIST, DELETE, QUIT) : ").strip().upper()
        
        if command == "UPLOAD":
            client_socket.send(command.encode())
            filename = input("Enter the file path to upload : ").strip()
            if not os.path.isfile(filename):
                print("File does not exist.")
                continue

            # Send filename to server
            client_socket.send(os.path.basename(filename).encode())
            with open(filename, "rb") as f:
                bytes_read = f.read(1024)
                client_socket.send(bytes_read)
            print(client_socket.recv(BUFFER_SIZE).decode())  # Acknowledge upload completion

        elif command == "DOWNLOAD":
            client_socket.send(command.encode())
            filename = input("Enter the filename to download : ").strip()
            client_socket.send(filename.encode())

            # Check if file exists on the server
            response = client_socket.recv(BUFFER_SIZE).decode()
            if response == "FILE FOUND":
                with open(f"downloaded_{filename}", "wb") as f:
                    bytes_read = client_socket.recv(1024)
                    f.write(bytes_read)
                print(f"{filename} downloaded successfully as downloaded_{filename}.")
            else:
                print("File Not Found on the server.")

        elif command == "LIST":
            client_socket.send(command.encode())
            response = client_socket.recv(BUFFER_SIZE).decode()
            if response == "Empty":
                print("No files available in your storage.")
            else:
                print("Files on server:", response)

        elif command == "DELETE":
            client_socket.send(command.encode())
            filename = input("Enter the filename to delete: ").strip()
            client_socket.send(filename.encode())
            print(client_socket.recv(BUFFER_SIZE).decode())

        elif command == "QUIT":
            client_socket.send(command.encode())
            print("Goodbye!")
            break

        else:
            print("Invalid command. Please enter UPLOAD, DOWNLOAD, LIST, DELETE, or QUIT.")

    client_socket.close()

if __name__ == "__main__":
    main()
