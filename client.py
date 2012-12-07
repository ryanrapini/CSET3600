# Client protocol for battleship
import socket
import pickle
import pprint


def try_connect(ip):
	HOST = ip    
	PORT = 58008
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		s.connect((HOST, PORT))
	except:
		return False
	s.close()
	return True

def get_preamble(s):
	print ('Getting preamble...')
	ePreamble = s.recv(1024)
	preamble = ePreamble.decode()
	s.send(ePreamble)
	print ('Recieved!')
	return preamble


def get_board(s):
	gameboards = []
	for x in range(0,4):
		print ('Getting board...')
		data = []
		pData = s.recv(1024)
		data += pickle.loads(pData)
		s.send(pData)
		print ('Recieved!')
		gameboards.append (data)
	return gameboards


def send_board(s):
	pBoard = pickle.dumps(gameboard)
	s.send(pBoard)
	pResponse = s.recv(1024)
	if (pResponse == pBoard):
		return True
	else:
		return False


def get_socket(ip):
	HOST = ip   
	PORT = 58008
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((HOST, PORT))
	return s



if __name__ == "__main__":
	HOST = socket.gethostname()    # The remote host
	PORT = 58008              # The same port as used by the server

	gameboard = [[0 for i in range(10)] for j in range(10)]

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((HOST, PORT))

	preamble = get_preamble(s)
	board = get_board(s)

	if send_board(s):
		print ("Move submitted!")

	pp = pprint.PrettyPrinter(indent=4)
	pp.pprint (board)

	s.close()