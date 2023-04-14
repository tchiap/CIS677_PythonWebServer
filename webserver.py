# Thomas Chiapete
# CIS 677
# Socket Programming Assignment 1: Web Server
# Tested with Python 3.10.8


#import socket module
from socket import *
import sys # In order to terminate the program


serverSocket = socket(AF_INET, SOCK_STREAM)


#Prepare a sever socket

# Assign IP and port so we can listen to incoming requests on this IP and port, then listen:
serverPort = 6789
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print ('The web server is running on port: ', serverPort)


while True:
	#Establish the connection

	print ('Ready to serve...')

	# Set up a new connection from the client
	# Accept a connection.  Learned about it here:  https://docs.python.org/3/library/socket.html#socket-objects
	
	connectionSocket, addr = serverSocket.accept() 

	try:

		# According to https://pythonprogramming.net/sockets-tutorial-python-3/ , they say the argument in recv is the buffer size.
		# They use 1024 bytes, so I will too.
		message = connectionSocket.recv(1024)

		filename = message.split()[1]
		
		f = open(filename[1:])

		outputdata = f.read() 

		# We need to send back 200 OK
		connectionSocket.send('\nHTTP/1.1 200 OK\n\n'.encode())
		print("Returning a document!")


		# Send the content of the requested file to the connection socket
		for i in range(0, len(outputdata)):
			connectionSocket.send(outputdata[i].encode())
		connectionSocket.send("\r\n".encode())
		connectionSocket.close()

	except IOError:
		# Send HTTP response message for file not found
		connectionSocket.send("\nHTTP/1.1 404 Not Found\n\n".encode())
		print("Returning 404 File Not Found")
		# Close the client connection socket
		connectionSocket.close()

	# I'm throwing in another couple of exception catches because I dislike like the fact that if you 
	# provide no filename(just the host and port), it crashes the server via uncaught IndexError from the split() above.   
	# In that event, I'm telling it to return HTTP 404, rather letting the server crash from an uncaught exception.
	except IndexError:
		connectionSocket.send("\nHTTP/1.1 404 Not Found\n\n".encode())
		connectionSocket.close()

	# Threw in a generic exception for any other errors.  I'm just returning HTTP 404.
	except Exception:
		connectionSocket.send("\nHTTP/1.1 404 Not Found\n\n".encode())
		connectionSocket.close()


serverSocket.close()
sys.exit() #Terminate the program after sending the corresponding data                                    