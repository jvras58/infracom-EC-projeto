import socket
import sys

HOST = 'localhost'  # Endereco IP do Servidor
PORT = 5000            # Porta que o Servidor esta
dest = (HOST, PORT)

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.bind(('localhost', 3000))

print('Para sair use CTRL+X\n')


while True:
    file_name = input('Enter file name:')
    f = open(file_name, 'rb')
    data = f.read(1024)

    udp.sendto(file_name.encode(), dest)
    printAux = udp.sendto(data, dest)

    while(data):
        if (printAux):
            print('sending...')
            data = f.read(1024)
            printAux = udp.sendto(data, dest)
    
    f.close()

    msg, clientAddr = udp.recvfrom(1024)
    file_name = msg.strip()
    print("Received File:", file_name)

    f2 = open('[CLIENTE] '.encode() + file_name,'wb')
    msg,clientAddr = udp.recvfrom(1024)
    while(msg):
        print(msg)
        f2.write(msg)
        print('msg1')
        msg, clientAddr = udp.recvfrom(1024)
        print('msg2')
    print(msg)
    f2.close()

    if(f == '\x18'):
        break

udp.close()