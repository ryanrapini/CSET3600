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
import queue
from threading import Thread

class Server(threading.Thread):
	def __init__(self):
		self.gameboards = [[[0 for i in range(10)] for j in range(10)] for k in range (4)]
		self.HOST = '192.168.1.107'
		self.PORT = 58008
		self.status = 1
		self.turn = 1
		self.client1_submit = False
		self.client2_submit = False
		self.preamble = (self.status, self.turn)

		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		print ('Created Socket')

		try:
			self.s.bind((self.HOST, self.PORT))
		except Exception as ex:
			print ('Failed to bind to port. Selfdestructing.')
			sys.exit(1)
		print ('Socket bound')

		# timeout after 60 seconds
		self.s.settimeout(60)


	def listen(self):
		q = queue.Queue()
		for x in range (0,500):
			self.preamble = (self.status, self.turn)
			self.s.listen(2)
			print('Listening for connection...')	

			#wait to accept a connection - blocking call
			self.conn, addr = self.s.accept()
			print('Connected by', addr)
			
			t = Thread(target=clientthread, args=(self.conn,self.preamble,self.gameboards, q))
			t.start()
			print("lol")
			sent_move = q.get()
			if not self.client1_submit:
				gameboards = sent_move

		self.stop()

	def stop(self):
		self.s.close()


def clientthread(conn, preamble, gameboards,q):
	status, turn = preamble
	ePreamble = "{0}.{1}".format(status, turn).encode()
	print (ePreamble)
	pPreamble = pickle.dumps(preamble)
	print("Sending preamble...")
	conn.send(ePreamble)
	print ("Recieving preamble.")
	pPreambleRecv = conn.recv(1024)
	print("done")
	if (pPreamble == pPreambleRecv):
		print ("Preamble OK")

	for board in gameboards:
		pData = pickle.dumps(board)
		print("Sending data...")
		conn.send(pData)
		pDataRecv = conn.recv(1024)

		if (pDataRecv == pDataRecv):
			print ("Board OK")

	# if still in initial setup

	try:
		submitted = []
		for x in range(0,4):
			print ('Getting board...')
			pData = conn.recv(1024)
			data = pickle.loads(pData)
			conn.send(pData)
			print ('Recieved!')
			submitted.append(data)
	except:
		if (submitted == []):
			# No move to submit, just close connection and return
			print ("Client quit without submitting a move.")
		else:
			print("Invalid submit?")

	conn.close()
	q.put(submitted)
	sys.exit()

if __name__ == "__main__":
	serv = Server()
	servthread = Thread(target=serv.listen, args=())
	servthread.start()