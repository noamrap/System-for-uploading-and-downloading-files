import os
import socket

def upload_file():
    def get_file_path():
        return input('Enter a file path: ')

    def check_if_path_exists(file_path):
        if os.path.exists(file_path):
            print('The file exists')
            return True
        else:
            print('The specified file does NOT exist')
            return False

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("localhost", 19999))

    file_path = get_file_path()

    if check_if_path_exists(file_path):
        client.send(b"UPLOAD")
        file_name = os.path.basename(file_path)
        client.send(file_name.encode())
        file_size = os.path.getsize(file_path)
        client.send(str(file_size).encode())
        
        with open(file_path, 'rb') as file:
            while (data := file.read(1024)):
                client.sendall(data)
        
        client.send(b"<END>")
    client.close()

def receive_file():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("localhost", 19999))
    
    file_name = input("Enter the file name to retrieve from server: ")
    client.send(b"GET")
    client.send(file_name.encode())
    
    response = client.recv(1024).decode()
    if response == "NOT_FOUND":
        print("File not found on server.")
        client.close()
        return
    
    getback_directory = r"C:\Users\USER\Desktop\Projects-the programmers club\GETBACK"
    if not os.path.exists(getback_directory):
        os.makedirs(getback_directory)
    
    file_path = os.path.join(getback_directory, file_name)
    with open(file_path, "wb") as file:
        while True:
            data = client.recv(1024)
            if data == b"<END>":
                break
            file.write(data)
    
    print(f"File '{file_name}' received and saved to '{file_path}'.")
    client.close()

action = input("Enter 'upload' to upload a file or 'get' to retrieve a file: ").strip().lower()
if action == "upload":
    upload_file()
elif action == "get":
    receive_file()
else:
    print("Invalid action.")
