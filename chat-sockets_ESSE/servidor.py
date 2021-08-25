import socket
import time


HOST = 'localhost'              # Endereco IP do Servidor
PORT = 5000            # Porta que o Servidor esta
PORT_DEST = 3000
orig = (HOST, PORT)
dest = (HOST, PORT_DEST)
BUFFER_SIZE = 1024


def splitMsgFromHeader(data):
    print('data type: ', type(data))
    print('O QUE ENTROU:', data)
    origem = data[0:16].replace("-", "")
    destino = data[16:32].replace("-", "")
    size = data[32:48].replace("-", "")
    checksum = data[48:64].replace("-", "")
    seq = data[64].replace("-", "")
    msg = data[65:]
    return origem, destino, size, checksum, seq, msg


udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.bind(orig)

i = 0
while True:
    msg, clientAddr = udp.recvfrom(BUFFER_SIZE)
    file_name_with_header = msg.decode()
    print('FNWH: ', type(file_name_with_header), file_name_with_header)
    origem, destino, size, checksum_file_name, seq, file_name = splitMsgFromHeader(file_name_with_header)
    print('checksum file name: ', checksum_file_name)

    print("Received File:", file_name)
    
    f = open('[BACKUP SERVER] '.encode() + file_name.encode(),'wb')

    msg,clientAddr = udp.recvfrom(BUFFER_SIZE)
    while(msg):
        print('msg inicial:  ', msg)
        origem, destino, size, checksum_file_name, seq, final_msg = splitMsgFromHeader(msg.decode())
        print('vou escrever :', final_msg)
        f.write(final_msg.encode())
 
        tmp_msg, clientAddr = udp.recvfrom(BUFFER_SIZE)
        origem, destino, size, checksum_file_name, seq, aux_msg = splitMsgFromHeader(tmp_msg.decode())
        print('msg auxiliar', aux_msg)
        msg = aux_msg.encode()
        print('msg2: ', msg)
    if(not msg):
        print('end')
        f.close()
        # Envio do arquivo lido
        f2 = open('[BACKUP SERVER] '.encode() + file_name.encode(),'rb')
        data = f2.read(BUFFER_SIZE)
        
        udp.sendto(file_name.encode(), dest)
        printAux = udp.sendto(data, dest)

        while(data):
            if(printAux):
                print('sending to client...')
                print(data)
                data = f2.read(BUFFER_SIZE)
                print(data)
                printAux = udp.sendto(data, dest)
        
        print('fechou')
        f2.close()
        
    print('terminou', data)

    if(msg == '\x18'):
       break
udp.close()