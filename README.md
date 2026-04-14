<h1 align="center">
  <img src="https://github.com/daemoncibsec/intruder/blob/main/intruder-header.png" alt="intruder" width="1000px">
  <br>
</h1>

Intruder is a tool for remote communication between computers. At the moment, **is just a concept of a C2 server**, that allows remote control over the clients, and **though it's functional, it doesn't implement yet the functionalities that characterize this type of sotfware**. In the future, I'll implement functionalities such as SSL encryption or DNS communication to bypass defensive software such as firewalls, but at the moment, **it's in development**.

## Installation

```bash
git clone https://github.com/daemoncibsec/intruder.git
cd intruder
pip install -r requirements.txt
```

Additionally, you can make it a binary in Linux systems using these "cython" library, so you don't have to move between folders, and have it implemented in your system as well as with other commands.

- For the client (Linux Malware):

```bash
./generate_intruder 192.168.0.1 6789
```

- For the client (Windows Malware):

```powershell
pyinstaller -F .\intruder.py
```

- For the server:

```bash
pip install cython
python3 -m cython server_intruder.py --embed
gcc -Os $(python3-config --includes) server_intruder.c -o marrow $(python3-config --ldflags --embed)
```

## Usage/Examples

- To start the server:

```bash
python3 server_intruder.py
```

- To start the client, you will need to specify the IP address of the server inside the script:

```bash
python3 intruder.py
```

In case you have the script compiled with cython and gcc:


- To start the server:


```bash
./server_intruder
```

- To start the client, you will need to specify the IP address of the server inside the script *before compilation*:


```bash
./intruder
```

## Known vulnerabilities and bugs

- When starting the server, the port 6789 doesn't check which software the client is using to connect to the server, which allows the client to manipulate the information being sent to the server. This can't harm the computer, but it causes poor reception of requests.
- The server doesn't check for duplicated conections from a client, which means that a client can spam the server with connections potentially crashing it (there is also no command implemented that allows the host to disconnect someone from the server, so, yeah, I'll have to fix that).
- The client's software data is fully unencrypted, which means that a competitive reverse engineer could discover the IP of the server it is connecting to really easily.

## Authors

- [@daemoncibsec](https://www.github.com/daemoncibsec)

## Testers

- [@javij27](https://mrtecno.jjimenezg.es/)
