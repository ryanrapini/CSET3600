# Client protocol for battleship
import socket
import pickle
import pprint


# def try_connect(ip):
# 	HOST = ip    
# 	PORT = 58008
# 	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 	try:
# 		s.connect((HOST, PORT))
# 		s.close()
# 	except:
# 		print ("oh noes")
# 		return False
	
# 	return True

def get_preamble(s):
	debug = False
	if debug:
		print ('Getting preamble...')
	ePreamble = s.recv(1024)
	preamble = ePreamble.decode()
	s.sendall(ePreamble)
	if debug:
		print ('Recieved!')
	return preamble


def get_boards(s):
	debug = False
	gameboards = []
	for x in range(0,4):
		if debug:
			print ('Getting board...')
		data = []
		pData = s.recv(1024)
		data += pickle.loads(pData)
		s.send(pData)
		if debug:
			print ('Recieved!')
		gameboards.append (data)
	return gameboards


def send_boards(s, gameboards):
	debug = False
	try:
		for board in gameboards:
			pData = pickle.dumps(board)
			if debug:
				print("Sending data...")
			s.send(pData)
			pDataRecv = s.recv(1024)

			if (pDataRecv == pDataRecv):
				if debug:
					print ("Board OK")
	except:
		return False
	return True


def get_socket(ip):
	HOST = ip    # The remote host
	PORT = 58008              # The same port as used by the server

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((HOST, PORT))
	return s



if __name__ == "__main__":
	ip = socket.gethostbyname(socket.gethostname())
	HOST = '192.168.1.107'   # The remote host
	PORT = 58008              # The same port as used by the server

	gameboards = [[[0 for i in range(10)] for j in range(10)] for k in range (4)]

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((HOST, PORT))
	# try_connect(ip)
	# s = get_socket(ip)
	preamble = get_preamble(s)
	print (preamble)
	board = get_boards(s)

	# if send_boards(s, gameboards):
	# 	print ("Move submitted!")

	# pp = pprint.PrettyPrinter(indent=4)
	# pp.pprint (board)

	s.close()