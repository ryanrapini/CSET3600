# Client protocol for battleship
import socket
import pickle
import pprint

HOST = 'ryanrapini.com'    # The remote host
PORT = 58008              # The same port as used by the server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))


def get_preamble(s):
	print ('Getting preamble...')
	ePreamble = s.recv(1024)
	preamble = ePreamble.decode()
	s.send(ePreamble)
	print ('Recieved!')
	return preamble


def get_board(s):
	print ('Getting board...')
	data = []
	pData = s.recv(1024)
	data += pickle.loads(pData)
	s.send(pData)
	print ('Recieved!')
	return data


def send_board(s):
	pass

preamble = get_preamble(s)
board = get_board(s)

pp = pprint.PrettyPrinter(indent=4)
pp.pprint (board)

#s.send("{0}.{1}".format(status, turn).encode()) #send only takes string

# print (preamble.decode())

# pData = s.recv(1024)
# print ("Data recieved!")
# data = pickle.loads(pData)
# print (repr(data))





s.close()