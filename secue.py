import socket
import threading



ask = input('To start a connection press[0]\nTo connect to a conncetion press[1]')


if ask == '0':
    ip_host = input('Enter your ipv4 address\n(To view your ipv4 address write \'ip\' in cd)',)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #
    server.bind(('ip_host',9999))
    
    connector, _ = server.accept()




elif ask == '1':
    ip_connect = input('Enter the ipv4 address of the person you want to connect with:')

    connector = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connector.connect(('ip_connect', 9999))

else:
    print('##########################INVALID RESPONSE, QUITTING#####################################')
    exit()


def sending_messages(x):
    while True:
        message = input("")
        x.send(message.encode())
        print('You: ' + message)

def receiving_message(x):
    while True:
        print('Friend: '+ x.recv(1024).decode())

threading.Thread(target=sending_messages, args=(connector,)).start()
threading.Thread(target=receiving_message, args=(connector,)).start()