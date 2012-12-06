# Echo server program
import socket
import pickle
import sys
import threading
from threading import Thread

class Server(threading.Thread):
	def __init__(self):
		self.array = self.gameboard = [[0 for i in range(10)] for j in range(10)]
		self.HOST = socket.gethostname()
		self.PORT = 58008
		self.status = 1
		self.turn = 1

		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		print ('Created Socket')

		try:
			self.s.bind((self.HOST, self.PORT))
		except Exception as ex:
			print ('Failed to bind to port. Selfdestructing.')
			sys.exit(1)
		print ('Socket bound')


	def listen(self):
		for x in range (0,10):
			self.s.listen(2)
			print('Listening for connection...')	

			#wait to accept a connection - blocking call
			self.conn, addr = self.s.accept()
			print('Connected by', addr)
			
			t = Thread(target=clientthread, args=(self.conn,self.status,self.turn))
			t.start()
		self.stop()

	def stop(self):
		self.s.close()


def clientthread(conn, status, turn):
	conn.send("{0}.{1}".format(status, turn).encode()) #send only takes string

	# keep thread alive with infinite loop
	while True:
		#Receiving from client
		pData = conn.recv(1024)
		if not pData: break
		data = pickle.loads(pData)
		conn.sendall(pData)
	conn.close()

serv = Server()
serv.listen()
print ("lol")