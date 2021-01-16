import socket
import select
import model
HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 1234
import ast
# create the socket
# AF_INET == ipv4
# SOCK_STREAM == TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Sets REUSEADDR (as a socket option) to 1 on socket to overcome "Address already in use"
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# we bind to IP and PORT
server_socket.bind((IP,PORT))
#listening for incoming connection
server_socket.listen()
# List of sockets for select.select()
socket_list = [server_socket]
#list to save clients headee and names
clients = {}
# the server call the model to get these values which will used every time the user enter the answers of the questions in UI
meanOfNumericalData,modeOfCategoricalData,classifier = model.Model().RandomForestModel()

def receive_message(client_socket):
    try:
        # get the header 
        message_header = client_socket.recv(HEADER_LENGTH)
        # if message doesn't contain header that means "there is no data" 
        if not len(message_header):
            return False
        # Convert header to int value
        message_length = int(message_header.decode("utf-8").strip())
        message = client_socket.recv(message_length)
        # Return an object of message header and message data
        return {"header": message_header, "data": message}
    except:
        return False

while True:
    #to check the sockets that we receive
    read_sockets, _, exception_sockets = select.select(socket_list, [], socket_list)
    for notified_socket in read_sockets:
       #to check the new connections
        if notified_socket == server_socket:
            # accept the connection and get client address and client data "Client_socket"
            client_socket, client_address = server_socket.accept()
            # call receive_message to decode the data
            user = receive_message(client_socket)
            if user is False:
                continue
            # Add accepted socket to select.select() list
            socket_list.append(client_socket)
            #for our application we receives two types of data 'strings'(chat),'dict'(machine model),so if it is dict we do another actions:
            if user['data'].decode('utf-8')[0] == "{":
                #we convert the data from bytes to string then to dict
                data = ast.literal_eval(user['data'].decode('utf-8'))
                #we take the first item of the dict(name) and save it as a user
                user = {'header':f"{len(data['name']):<{HEADER_LENGTH}}".encode('utf-8'), 'data':data['name'].encode('utf-8')}
                #we add the user to the clients list
                clients[client_socket] = user
                #we rewrite the dict without the name to send it to the model
                newdata=dict()
                for key,value in data.items():
                    if key != "name":
                        newdata[key] = value
                # class the model and enter the values to get the output 
                output = model.predict(newdata
                                       , meanOfNumericalData
                                       , modeOfCategoricalData
                                       , classifier).predict()
                # encode the output to be able to send it over socket into the client
                encodedOutput = output.encode('utf-8')
                print(bytes(f"{len(encodedOutput):<{HEADER_LENGTH}}", 'utf-8'))
                client_socket.send(bytes(f"{len(encodedOutput):<{HEADER_LENGTH}}", 'utf-8') + encodedOutput)

            else:
                # for string name from string we save it directly
                clients[client_socket] = user

        else:
            # if it's not a new connection then it's the chat talk and we want to resend it the other clients
            message = receive_message(notified_socket)
            #that means that the client closed the connection so we delete him from the lists
            if message is False:
                socket_list.remove(notified_socket)
                del clients[notified_socket]
                continue
            #if there is a message we get the client name from the list and save it as user
            user = clients[notified_socket]
            #then we loop over all the clients except the sender
            for client_socket in clients:
                if client_socket != notified_socket:
                #and we send the user name and the message
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])
        # for handling some socket exceptions
    for notified_socket in exception_sockets:
        # Remove from list for socket.socket()
        socket_list.remove(notified_socket)

        # Remove from our list of users
        del clients[notified_socket]
