import os
import socket


database_directory = r"C:\Users\USER\Desktop\Projects-the programmers club\DATABASE"
if not os.path.exists(database_directory):
    os.makedirs(database_directory)

def handle_file_upload(client):
    file_name = client.recv(1024).decode()
    file_path = os.path.join(database_directory, file_name)
    file_bytes = b""

    with open(file_path, "wb") as file:
        while True:
            data = client.recv(1024)
            file_bytes += data
            if file_bytes[-5:] == b"<END>":
                file_bytes = file_bytes[:-5] 
                break
        file.write(file_bytes)

def handle_file_download(client):
    file_name = client.recv(1024).decode()
    file_path = os.path.join(database_directory, file_name)
    if os.path.exists(file_path):
        client.send(b"FOUND")
        with open(file_path, "rb") as file:
            while (data := file.read(1024)):
                client.sendall(data)
        client.send(b"<END>")
    else:
        client.send(b"NOT_FOUND")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 19999))
server.listen()

while True:
    client, addr = server.accept()
    action = client.recv(1024).decode()
    
    if action == "UPLOAD":
        handle_file_upload(client)
    elif action == "GET":
        handle_file_download(client)
    
    client.close()
