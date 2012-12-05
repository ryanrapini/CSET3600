# Echo client program
import socket
import pickle

HOST = socket.gethostname()    # The remote host
PORT = 58008              # The same port as used by the server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

array = [[0 for i in range(10)] for j in range(10)]

preamble = s.recv(1024)

print (preamble.decode())

pData = pickle.dumps(array)
print("Sending data...")
s.sendall(pData)

pData = s.recv(1024)
print ("Data recieved!")
data = pickle.loads(pData)
print (repr(data))

s.close()