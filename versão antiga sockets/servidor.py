import socket
import time

HOST = 'localhost'              # Endereco IP do Servidor
PORT = 5000            # Porta que o Servidor esta
PORT_DEST = 3000
orig = (HOST, PORT)
dest = (HOST, PORT_DEST)

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.bind(orig)

i = 0
while True:
    msg, clientAddr = udp.recvfrom(1024)
    file_name = msg.strip()
    print("Received File:", file_name)
    
    f = open('[BACKUP SERVER] '.encode() + file_name,'wb')

    msg,clientAddr = udp.recvfrom(1024)
    while(msg):
        print(msg)
        f.write(msg)
        print('msg1')
        msg, clientAddr = udp.recvfrom(1024)
        print('msg2')

    print(msg)
    if(not msg):
        print('end')
        f.close()
        # Envio do arquivo lido
        f2 = open('[BACKUP SERVER] '.encode() + file_name,'rb')
        data = f2.read(1024)
        
        udp.sendto(file_name, dest)
        printAux = udp.sendto(data, dest)

        while(data):
            if(printAux):
                print('sending to client...')
                print(data)
                data = f2.read(1024)
                print(data)
                printAux = udp.sendto(data, dest)
        
        print('fechou')
        f2.close()
        
    print('terminou', data)

    if(msg == '\x18'):
       break
udp.close()