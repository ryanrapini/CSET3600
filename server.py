# Server protocol for battleship

# A quick note on technical limitations: for the sake of this project's simplicity and my own
# sanity, I make a pretty risky assumption about my sockets: that every single communication
# will successfully send all 1024 bytes in one go.

# Naturally, when you are in a networking environment there are hundreds of factors that may
# affect the fidelity of the connection and this represents a bit of a risk. However, in our
# case we appear to come well within the 1024 byte limit for a single transmit.

# our data array (the only significant thing we are sending) comes in at 192 bytes, empty:
# >>> sys.getsizeof([[0 for i in range(10)] for j in range(10)])
# 192

# of course, pickling it for serialization introduces significant size overhead:
# >>> import pickle
# >>> sys.getsizeof(pickle.dumps([[0 for i in range(10)] for j in range(10)]))
# 507

# but even with a fully populated array, we seem to be just fine:
# >>> sys.getsizeof(pickle.dumps([[256 for i in range(10)] for j in range(10)]))
# 707

# of course, staying under the size requirement isn't a guarantee, but it certainly makes me
# feel better. There is a possibility of transmission failures due to other network issues, but
# the code should mostly compensate for these by virtue of constantly updating - if the data array
# is transmitted mashed in one pass, it should be corrected on the next pass. this is further
# enforced by the fact that our server is authoritative and will contain the One True State of our
# game board, from which both clients will update.


import socket
import pickle
import sys
import threading
from threading import Thread

class Server(threading.Thread):
	def __init__(self):
		self.gameboard = [[0 for i in range(10)] for j in range(10)]
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
		for x in range (0,2):
			self.s.listen(2)
			print('Listening for connection...')	

			#wait to accept a connection - blocking call
			self.conn, addr = self.s.accept()
			print('Connected by', addr)
			
			t = Thread(target=clientthread, args=(self.conn,self.status,self.turn,self.gameboard))
			t.start()
		self.stop()

	def stop(self):
		self.s.close()


def clientthread(conn, status, turn, gameboard):
	ePreamble = "{0}.{1}".format(status, turn).encode()
	conn.send(ePreamble)
	ePreambleRecv = conn.recv(1024)

	if (ePreamble == ePreambleRecv):
		print ("Preamble OK")

	pData = pickle.dumps(gameboard)
	print("Sending data...")
	conn.send(pData)
	pDataRecv = conn.recv(1024)

	if (pDataRecv == pDataRecv):
		print ("Data OK")

	pMoveRecv = conn.recv(1024)

	print("|{0}|".format(pMoveRecv))

	try:
		lolcats = pickle.loads(pMoveRecv)
	except:
		if pMoveRecv.decode() == '':
			# No move to submit, just close connection and return
			print ("Client quit without submitting a move.")
			conn.close()
			return

	print("|{0}|".format(lolcats))
	conn.close()

serv = Server()
servthread = Thread(target=serv.listen, args=())
servthread.start()