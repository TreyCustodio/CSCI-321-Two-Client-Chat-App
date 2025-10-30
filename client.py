import socket
import threading

"""
CSCI-321 Project 2
Austin McBride, Vincent Ziccardi, Trey Custodio
10/30/2025

Two Client Chat Application Client Code

Connect to the server IP/port,
Send and receive messages,
Exit on typing “exit”
Stop receiving and disconnect when the other client disconnects.
"""

#   Server IP and Port  #
# SERVER_IP = '127.0.0.1'
SERVER_IP = '192.168.56.101'
SERVER_PORT = 5000


#   Receive Function -- could be used with threading   #
def receive(client):
    #   Receive Data    #
    data = client.recv(1024)
    if data.decode() == "QUIT":
        client.close()
    else:
        print("Them:", data.decode(), end="\n\n")


#   Routine for connecting to server and chatting with other client #
def main():
    #   Create an IPv4/TCP Socket   #
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #   Connect to the server   #
    print("Connecting to server at " + str(SERVER_IP) + " on port " + str(SERVER_PORT) + "...")
    client.connect((SERVER_IP, SERVER_PORT))

    print('Successfully connected to server.\n')
    data = client.recv(1024)
    
    #   Print the instructions  #
    instructions = "Beginning of chat. Enter your message or enter \'exit\' to QUIT.\n"
    print("-" * (len(instructions) - 1))
    print(instructions)

    #   Chat with the other client  #
    while True:
        #   Get the message from the user -- this blocks the console from receiving messages until an input is entered.   #
        message = input("You: ")
        
        #   Break the loop if the client types exit #
        if message == "exit":
            client.send(b"QUIT")
            client.close()
            break

        elif message == "":
            while message == "":
                message = input()

        #   Send the message    #
        client.send(message.encode())

        #   Receive messages    #
        receive(client)

    #   Close the connection   #
    client.close()


main()