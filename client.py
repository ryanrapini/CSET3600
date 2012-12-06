# Client protocol for battleship
import socket
import pickle
import pprint

HOST = socket.gethostname()    # The remote host
PORT = 58008              # The same port as used by the server

gameboard = [[0 for i in range(10)] for j in range(10)]

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
	pBoard = pickle.dumps(gameboard)
	s.send(pBoard)
	pResponse = s.recv(1024)
	if (pResponse == pBoard):
		return True
	else:
		return False

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

preamble = get_preamble(s)
board = get_board(s)

if send_board(s):
	print ("Move submitted!")

pp = pprint.PrettyPrinter(indent=4)
pp.pprint (board)

s.close()