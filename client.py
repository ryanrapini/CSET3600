# Echo client program
import socket
import pickle

HOST = socket.gethostname()    # The remote host
PORT = 58008              # The same port as used by the server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

def preamble(s):
	ePreamble = s.recv(1024)
	preamble = ePreamble.decode()
	s.send(ePreamble)
	return preamble

preamble(s)


# def recieve():
# 	while True:
# 		#Receiving from client
# 		pData = conn.recv(1024)
# 		if not pData: break
# 		data = pickle.loads(pData)
# 		conn.sendall(pData)



#conn.send("{0}.{1}".format(status, turn).encode()) #send only takes string

# print (preamble.decode())

# pData = s.recv(1024)
# print ("Data recieved!")
# data = pickle.loads(pData)
# print (repr(data))

# pData = pickle.dumps(array)
# print("Sending data...")
# s.sendall(pData)



s.close()