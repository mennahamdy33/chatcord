import socket
import select
import model
HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 1234
import ast
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((IP,PORT))

server_socket.listen()

socket_list = [server_socket]
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

        message_length = int(message_header.decode("utf-8").strip())
        message = client_socket.recv(message_length)
    
        return {"header": message_header, "data": message}
    except:
        return False

while True:
    read_sockets, _, exception_sockets = select.select(socket_list, [], socket_list)
    for notified_socket in read_sockets:
        if notified_socket == server_socket:
            # accept the connection and get client address and client data "Client_socket"
            client_socket, client_address = server_socket.accept()
            # call receive_message to decode the data
            user = receive_message(client_socket)
            print(user['data'].decode('utf-8')[0])
            if user is False:
                continue

            socket_list.append(client_socket)

            if user['data'].decode('utf-8')[0] == "{":
                data = ast.literal_eval(user['data'].decode('utf-8'))
            
                user = {'header':f"{len(data['name']):<{HEADER_LENGTH}}".encode('utf-8'), 'data':data['name'].encode('utf-8')}
                clients[client_socket] = user
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
                continue
            else:
                clients[client_socket] = user
                print(user)
            # print(f"Accepted new connection from {client_address[0]}:{client_address[1]} username:{user['data'].decode('utf-8')}")

        else:
            message = receive_message(notified_socket)
            if message is False:
                # print(f"Closed connection from {clients[notified_socket]['data'].decode('utf-8')}")
                socket_list.remove(notified_socket)
                del clients[notified_socket]
                continue
            user = clients[notified_socket]
            # print(f"Received message from {user['data'].decode('utf-8')}: {message['data'].decode('utf-8')}")
            for client_socket in clients:
                if client_socket != notified_socket:

                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])
        # for handling some socket exceptions
    for notified_socket in exception_sockets:
        # Remove from list for socket.socket()
        socket_list.remove(notified_socket)

        # Remove from our list of users
        del clients[notified_socket]
