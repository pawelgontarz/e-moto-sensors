import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 10001)
print('starting up on %s port %s' % server_address)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()

    try:
        print ('connection from', client_address)
        
        # Receive the data in small chunks and retransmit it
        while True:
            
            data = log_data()
            print(data)
            sleep(3)
            #data = connection.recv(16)
            if data:
                print('sending data back to the client')
                connection.sendall(data)
            else:
                print('no more data from', client_address)
                break
            
            #connection.sendall()
            #connection.sendall(message1)
            #connection.sendall(id2)
            #connection.sendall(message2)
            #connection.sendall(id3)
            #connection.sendall(message3)


            
    finally:
        # Clean up the connection
        connection.close()