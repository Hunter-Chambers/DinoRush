import socket
from threading import Thread
import json

import pygame


from src import constants


SERVER = "10.0.0.191"
PORT = 27016
BUFFER_SIZE = 4096


def connect_to_server():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(5)

    try:
        client_socket.connect((SERVER, PORT))

        client_socket.send('<RECEIVING>'.encode())
        msg = client_socket.recv(BUFFER_SIZE).decode()

        if ('Player' in msg):
            constants.recv_thread = Thread(target=recv_from_server, args=(client_socket,))
            constants.recv_thread.start()

            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.settimeout(5)

            client_socket.connect((SERVER, PORT))

            client_socket.send('<SENDING>'.encode())

            constants.send_thread = Thread(target=send_from_client, args=(client_socket,))
            constants.send_thread.start()

            return (False, msg)
        else:
            client_socket.shutdown(socket.SHUT_RDWR)
            client_socket.close()
            raise socket.error
        # end if
    except socket.error:
        return (True, 'Server is full or timed out')
    # end try/except
# end connect_to_server

def recv_from_server(client_socket):
    client_socket.settimeout(None)

    while(constants.loop[0]):
        try:
            msg = client_socket.recv(BUFFER_SIZE).decode()
            if (not msg):
                raise socket.error
            # end if

            client_socket.send(msg.encode())
        except socket.error:
            break
        # end try/except

        info = json.loads(msg)
        player_id = list(info.keys())[0]
        constants.players[player_id] = info[player_id]

        '''
        img = pygame.transform.scale(pygame.image.load('assets/animations/' + info['img']), info['size'])
        constants.SCREEN.blit(img, info['location'])
        '''
    # end while

    client_socket.shutdown(socket.SHUT_RDWR)
    client_socket.close()
# end recv_from_server

def send_from_client(client_socket):
    client_socket.settimeout(None)

    while(constants.loop[0]):
        if (constants.location):
            msg = json.dumps({constants.id:{'location':constants.location, 'img':constants.img, 'size':constants.size}})

            try:
                client_socket.send(msg.encode())
                client_socket.recv(BUFFER_SIZE)
            except socket.error:
                break
            # end try/except
        # end if
    # end while

    client_socket.shutdown(socket.SHUT_RDWR)
    client_socket.close()
# end send_from_client