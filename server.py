# Echo server program
import socket
import pickle
import sys
from threading import Thread

HOST = socket.gethostname()
PORT = 58008
status = 1
turn = 1

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print ('Created Socket')

try:
	s.bind((HOST, PORT))
except Exception as ex:
	print ('Failed to bind to port. Selfdestructing.')
	sys.exit(1)
print ('Socket bound')

s.listen(2)
print('Listening for connection...')

def clientthread(conn):
	conn.send("{0}.{1}".format(status, turn).encode()) #send only takes string

	# keep thread alive with infinite loop
	while True:
		#Receiving from client
		pData = conn.recv(1024)
		if not pData: break
		data = pickle.loads(pData)
		conn.sendall(pData)

	conn.close()

#now keep talking with the client
while 1:
	#wait to accept a connection - blocking call
	conn, addr = s.accept()
	print('Connected by', addr)
	
	t = Thread(target=clientthread, args=(conn,))
	t.start()

s.close()

print(data)