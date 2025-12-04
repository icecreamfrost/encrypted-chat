import socket
import threading
import sys

PORT = 9999

ask = input('To start a connection press[0]\nTo connect to a conncetion press[1]')

if ask == '0':
    ip_host = input('Enter your ipv4 address\n(To view your ipv4 address write \'ip\' in cd): ').strip()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server.bind((ip_host, PORT))
    except Exception as e:
        print('Failed to bind to', ip_host, PORT, '->', e)
        server.close()
        sys.exit(1)
    server.listen(1)  # start listening for incoming connections
    print('Listening on', ip_host, PORT)
    connector, addr = server.accept()
    print('Connected by', addr)

elif ask == '1':
    ip_connect = input('Enter the ipv4 address of the person you want to connect with:').strip()

    connector = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        connector.connect((ip_connect, PORT))
        print('Connected to', ip_connect, PORT)
    except Exception as e:
        print('Failed to connect to', ip_connect, PORT, '->', e)
        connector.close()
        sys.exit(1)

else:
    print('##########################INVALID RESPONSE, QUITTING#####################################')
    sys.exit(1)


def sending_messages(x):
    while True:
        try:
            message = input("")
            if message == '':
                continue
            x.send(message.encode())
            print('You: ' + message)
        except (BrokenPipeError, ConnectionResetError):
            print('Connection closed. Sender exiting.')
            break
        except Exception as e:
            print('Send error:', e)
            break


def receiving_message(x):
    while True:
        try:
            data = x.recv(1024)
            if not data:
                print('Connection closed by peer.')
                break
            print('Friend: ' + data.decode())
        except Exception as e:
            print('Receive error:', e)
            break


t1 = threading.Thread(target=sending_messages, args=(connector,), daemon=True)
t2 = threading.Thread(target=receiving_message, args=(connector,), daemon=True)
t1.start()
t2.start()

t1.join()
t2.join()