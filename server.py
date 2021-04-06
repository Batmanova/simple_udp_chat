import socket

addresses = {}
passwords = {}
connections = []
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
port = 9090
try:
    sock.bind(('', port))
    sock.listen(1)
except BaseException:
    for i in range(1024, 65536):
        try:
            sock.bind(('', i))
            sock.listen(1)
            port = i
        except BaseException:
            with open("log.txt", "w") as file:
                file.write("connecting error")

print('connected: ', port)

while True:
    received, addr = sock.recvfrom(8192)
    print(addr)
    if addr in addresses.values() and addr not in connections:
        sock.sendto('Enter the password'.encode('utf-8'), addr)
        data, addr = sock.recvfrom(8192)
        if not data:
            break
        if data == passwords[addresses.get(addr)]:
            sock.sendto('Welcome'.encode('utf-8'), addr)
            connections.append(addr)
        else:
            sock.sendto('Wrong password'.encode('utf-8'), addr)
            continue
    elif addr not in addresses.values():
        sock.sendto('Hi! Write your nickname'.encode('utf-8'), addr)
        data_name, addr = sock.recvfrom(8192)
        addresses[data_name] = addr
        sock.sendto('Write your password'.encode('utf-8'), addr)
        data_pass, addr = sock.recvfrom(8192)
        passwords[data_name] = data_pass
        sock.sendto('Welcome! Write your first message'.encode('utf-8'), addr)
        connections.append(addr)
    else:
        print('here')
        if not received:
            break
        if received == b'EXIT' or received == b'Exit' or received == b'exit':
            print('Exit ', addr)
            connections.remove(addr)
            sock.sendto('exit'.encode('utf-8'), addr)
        else:
            print(connections)
            print('ready')
            for conn in connections:
                #if conn != addr:
                    sock.sendto(received, conn)

sock.close()