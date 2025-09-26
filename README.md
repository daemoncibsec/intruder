<h1 align="center">
  <img src="https://github.com/daemoncibsec/intruder/blob/main/intruder-logo.png" alt="intruder" width="1000px">
  <br>
</h1>

Intruder is a tool for remote communication between computers. At the moment, **is just a concept of a C2 server**, that allows remote control over the clients, and **though it's functional, it doesn't implement yet the functionalities that characterize this type of sotfware**. In the future, I'll implement functionalities such as SSL encryptation or DNS communication to bypass defensive software such as firewalls, but at the moment, **it's in development**.

## Installation

```bash
git clone https://github.com/daemoncibsec/intruder.git
cd intruder
```

Additionally, you can make it a binary in Linux systems using these "cython" library, so you don't have to move between folders, and have it implemented in your system as well as with other commands.

- For the client:

```bash
pip install cython
python3 -m cython intruder.py --embed
gcc -Os $(python3-config --includes) intruder.c -o intruder $(python3-config --ldflags --embed)
```

- For the server:

```bash
pip install cython
python3 -m cython server_intruder.py --embed
gcc -Os $(python3-config --includes) server_intruder.c -o server_intruder $(python3-config --ldflags --embed)
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

## Authors

- [@daemoncibsec](https://www.github.com/daemoncibsec)
