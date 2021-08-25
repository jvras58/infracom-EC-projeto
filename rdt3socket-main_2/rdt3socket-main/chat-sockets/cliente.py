import socket
import sys

HOST = 'localhost'  # Endereco IP do Servidor
PORT = 5000            # Porta que o Servidor esta
dest = (HOST, PORT)
ORIGEM = 3000
HEADER_SIZE = 65
BUFFER_SIZE = 102400

def checksum(byte_msg):
    total = 0
    length = len(byte_msg)
    i = 0
    while length > 1:
        total += ((byte_msg[i + 1] << 8) & 0xFF00) + ((byte_msg[i]) & 0xFF)
        i += 2
        length -= 2

    if length > 0:
        total += (byte_msg[i] & 0xFF)

    while (total >> 16) > 0:
        total = (total & 0xFFFF) + (total >> 16)

    total = ~total

    return total & 0xFFFF

def addHeader(porta_origem, porta_destino, size, checksum, seq, data):
    final_msg = str(porta_origem).ljust(16, "-") + str(porta_destino).ljust(16, "-") + str(size).ljust(16, "-") + str(checksum).ljust(16, "-") + str(seq) + str(data)
    return final_msg 



udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.bind(('localhost', ORIGEM))

print('Para sair use CTRL+X\n')

def ack_rcvr():
    udp.settimeout(5)
    while True:
        try: 
            data = udp.recv(BUFFER_SIZE)
            return data
        except socket.timeout:
            return False

while True:

        
    file_name = input('Enter file name: ')
    f = open(file_name, 'rb')
    data = f.read(256) #1024
    seq = 0 #'0'

    checksum_file_name = checksum(file_name) #checksum(str.encode(file_name))
    print('checksum do file name: ', checksum_file_name)
    final_file_name = addHeader(ORIGEM, PORT, HEADER_SIZE +  len(file_name), checksum_file_name, seq, file_name)
    print('final file name: ', final_file_name)

    try:
        udp.sendto(final_file_name, dest) #(final_file_name.encode(), dest)
    except socket.error:
        print('ERROR IN SENDING FILE NAME: ')
        sys.exit()

    checksum_data = checksum(data)
    final_data = addHeader(ORIGEM, PORT, HEADER_SIZE +  len(data), checksum_data, seq, data) #data.decode())
    printAux = udp.sendto(final_data, dest) #(final_data.encode(), dest)

    while(data):
        if (printAux):
            print('sending...')
            data = f.read(256) #data = f.read(1024)
           # seq = seq + 1
            final_data = addHeader(ORIGEM, PORT, HEADER_SIZE +  len(data), checksum_data, seq, data) #data.decode())
            printAux = udp.sendto(final_data, dest) #printAux = udp.sendto(final_data.encode(), dest)
    
    f.close()

    msg, clientAddr = udp.recvfrom(BUFFER_SIZE)
    file_name = msg.strip()
    print("Received File:", file_name)

    f2 = open('[CLIENTE] '.encode() + file_name,'wb')
    msg,clientAddr = udp.recvfrom(BUFFER_SIZE)
    while(msg):
        print(msg)
        f2.write(msg)
        print('msg1')
        msg, clientAddr = udp.recvfrom(BUFFER_SIZE)
        print('msg2')
    print(msg)
    f2.close()

    if(f == '\x18'):
        break

udp.close()