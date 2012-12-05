# Echo server program
import socket
import pickle
from datetime import datetime
from datetime import timedelta

class Timeout:
	def __init__(self, length):
		self.starttime = datetime.now()
		self.length = length
	def check(self):
		elapsed = datetime.now() - self.starttime
		if (elapsed > timedelta(seconds=self.length)):
			print ('timeout')
			return True
		return False

HOST = socket.gethostname()  # Symbolic name meaning all available interfaces
PORT = 58008              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)

print('Listening for connection...')

timeout = Timeout(5)

conn, addr = s.accept()
print('Connected by', addr)

while True:
	pData = conn.recv(1024)
	if not pData: break
	data = pickle.loads(pData)
	conn.sendall(pData)


print(data)

conn.close()
