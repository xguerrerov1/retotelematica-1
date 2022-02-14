 # Socket client example in python
import socket
import sys

valores = sys.argv[1:]

host = valores[0]
port = int(valores[1]) 

def robarSocket(host,port,url):
    print('# Creating socket')
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #ip version 4, socket en TCP
        s.settimeout(5)
    except socket.error:
        print('Failed to create socket')
        sys.exit()

    print('# Getting remote IP address') 
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print('Hostname could not be resolved. Exiting')
        sys.exit()

    print('# Connecting to server, ' + host + ' (' + remote_ip + ')')
    s.connect((remote_ip , port))

    request = f'GET /{url} HTTP/1.1\r\nHost: {host}\r\nConection: close\r\n\r\n'
    print('# Sending data to server')


    try:
        s.sendall(request.encode('utf-8'))
    except socket.error:
        print ('Send failed')
        sys.exit()

    print('# Receive data from server')

    a = b''
    while True:
        try:
            msg = s.recv(4096)
            if not msg:
                break
            a += msg[:]
        except socket.timeout:
            break
    s.close()
    header,file = a.split(b'\r\n\r\n',1)
    print(header.decode('latin-1'))
    return header,file

def guardar(file,contador):
    contentType = header.lower().split(b'content-type: ')[1].split(b'/')[1].replace(b';',b'\r\n').split(b'\r\n')
    with open(f"robado/file{contador}.{contentType[0].decode('latin-1')}", "wb") as f:
        f.write(file)

print('# Creating socket')
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
except socket.error:
    print('Failed to create socket')
    sys.exit()

print('# Getting remote IP address') 
try:
    remote_ip = socket.gethostbyname( host )
except socket.gaierror:
    print('Hostname could not be resolved. Exiting')
    sys.exit()

print('# Connecting to server, ' + host + ' (' + remote_ip + ')')
s.connect((remote_ip , port))

request = 'GET ' + input('Ingrese URL\n') + ' HTTP/1.1\r\nHost: ' + host + '\r\nConection: close\r\n\r\n'
print('# Sending data to server')


try:
    s.sendall(request.encode('utf-8'))
except socket.error:
    print ('Send failed')
    sys.exit()

print('# Receive data from server')

a = b''
while True:
    try:
        msg = s.recv(4096)
        if not msg:
            break
        a += msg[:]
    except socket.timeout:
        break
s.close()
header,file = a.split(b'\r\n\r\n',1)
print(header.decode('latin-1'))
guardar(file,0)

xd = file.decode('latin-1').lower().replace(' ','')
href = xd.split('href="')
src = xd.split('src="')
archivos = href + src
robado = []
for s in archivos:
    if s[0:s.find('"')].endswith(('.png','.jpg', '.gif' ,'.pdf','.svg','jepg','.mp3','.mp4','.webm')):
        robado.append(s[:s.find('"')].replace('//',''))
robado = robado[1:]
contador = 1
for archivo in robado:
    print(archivo)
    host = archivo.split('/',1)
    header,file = robarSocket(host = host[0],port = 80,url = host[1])
    guardar(file,contador)
    contador += 1
