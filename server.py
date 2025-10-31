import socket
import threading
from _thread import start_new_thread

"""
CSCI-321 Project 2
Austin McBride, Vincent Ziccardi, Trey Custodio
10/30/2025

Two Client Chat Application Server Code

Listen for incoming connections from exactly 2 clients,
Relay messages between clients,
Close connections when clients type “exit”
"""

class Client(object):
    """Represents a client that the server interacts with"""
    def __init__(self, socket, port, user_name = "client"):
        self.socket = socket
        self.port = port
        self.user_name = user_name

    def set_name(self, name=""):
        self.user_name = name

    def get_name(self):
        return self.user_name
    
    def get_socket(self):
        return self.socket
    
    def get_port(self):
        return self.port
    
    def send_data(self, data):
        """Encode and send data to the client"""
        self.socket.sendall(data.encode())
        return
    
    def receive_data(self):
        """Receive, decode, and return data"""
        data = self.socket.recv(1024)
        return data.decode()
    
    def close_connection(self):
        self.socket.close()


class Server(object):
    """Represents a server that sends data to 2 clients"""
    def __init__(self, server_ip, server_port):
        #   Store the server ip and port    #
        self.server_ip = server_ip
        self.server_port = server_port

        #   Dictionary containing the 2 clients and their socket/port information   #
        self.clients = {
            0: None,
            1: None
        }
    
    
    def main(self):
        #   Create a log file   #
        log = open('log.txt', 'w')
        log.write("-" * 20)
        log.write("\n")
        log.write("Server Log\n")
        log.write("-" * 20)
        log.write("\n")
        log.flush()

        #   Define an exit event; use this to close the connections once activated  #
        exit_event = threading.Event()

        #   Define the Threaded Function  #
        def get_data(client, client_id):
            """Receive data from and send data to clients.
            If 'exit' is typed, then close the connections."""
            while not exit_event.is_set():
                data = client.receive_data()

                if data:
                    #   Close the connections if 'exit' is typed
                    if data == "QUIT":
                        exit_event.set()
                        return

                    #   Send the message to the other client
                    else:
                        #   The other client has stopped chatting; close this connection
                        if exit_event.is_set():
                            client.send_data("QUIT")
                            return
                        
                        data = client.get_name() + ": " + data
                        
                        if client_id == 1:
                            client_2.send_data(data)
                            log.write(data + "\n")
                            log.flush()
                        
                        elif client_id == 2:
                            client_1.send_data(data)
                            log.write(data + "\n")
                            log.flush()


        #   Define a Socket with IPv4 address family and TCP Socket Type #
        host = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #   Bind the socket #
        host.bind((self.server_ip, self.server_port))

        #   Listen for connections  #
        host.listen()

        #   Accept connections from exactly 2 clients   #
        print("Waiting for Clients...")
        num_connections = 0
        while num_connections != 2:
            #   Accept the host
            self.clients[num_connections] = Client(*host.accept(), "Client" + str(num_connections + 1))
            sockname = self.clients[num_connections].get_socket().getsockname()
            print("Client at IP", str(sockname[0]), "on port",  str(sockname[1]), "connected")
            
            #   Start a thread for the client
            if num_connections == 0:
                thread_1 = threading.Thread(target=get_data, args=(self.clients[num_connections],1))

            elif num_connections == 1:
                thread_2 = threading.Thread(target=get_data, args=(self.clients[num_connections],2))

            #   Increment num_connections
            num_connections += 1

        #   Begin the chat #
        #   Store the clients in variables for ease of access
        client_1 = self.clients[0]
        client_2 = self.clients[1]

        #   Send over a confirmation code to both clients
        client_1.send_data("1")
        client_2.send_data("1")

        #   Get each username
        name_1 = client_1.receive_data()
        name_2 = client_2.receive_data()
        print(name_1)
        print(name_2)
        client_1.set_name(name_1)
        client_2.set_name(name_2)

        #   Send confirmation again
        client_1.send_data("1")
        client_2.send_data("1")

        thread_1.start()
        thread_2.start()

        #   Display a confirmation message
        print("Both clients connected. Now commencing chat.")
        
        #   Run the threaded functions until the exit event is triggered
        exit_event.wait()
        print("Closing connections...")

        thread_1.join()
        client_1.close_connection()
        print("Client 1's connection closed.")

        thread_2.join()
        client_2.close_connection()
        print("Client 2's connection closed.")

        host.close()
        log.close()
        print("Server closed.")
        return
    

#   Main Message Relay Routine   #
def main():
    #   Set Server IP and port  #
    # SERVER_IP = '127.0.0.1'
    SERVER_IP = "192.168.56.101"
    SERVER_PORT = 5000
    
    #   Initialize and run the server   #
    server = Server(SERVER_IP, SERVER_PORT)
    server.main()

main()