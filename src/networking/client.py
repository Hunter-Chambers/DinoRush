#############################################################
### IMPORTS
#############################################################
from networking.connection import Connection

import pickle


class Client(Connection):
    def __init__(self, server_info):
        super().__init__()
        self.CLIENT = self.get_socket()
        self.CLIENT_ID = -1

        self.__SERVER_INFO = server_info
        self.get_connections()[server_info] = {
            "player": None,
            "recv_buffer_window": {
                "next_msg_num": 0,
                "buffer": {}
            },
            "sent_buffer_window": {
                "next_ack_num": 0,
                "buffer": {}
            }
        }
        self.CONNECTION_DATA = self.get_connections()[server_info]

        self.OTHER_PLAYERS = {}
    # end __init__

    def connect_to_server(self):
        message_data = {"INITIAL_CONNECTION": True}
        self.get_socket().sendto(
            pickle.dumps(message_data), self.__SERVER_INFO)
    # end connect_to_server

    def send_player_data_to_server(self, pressed_keys):
        player_data = {
            "msg_num": self.LAST_MSG_ID_SENT,
            "player_data": self.CONNECTION_DATA["player"]\
                .get_serializable_data(pressed_keys)
        }

        self.get_socket().sendto(pickle.dumps(player_data), self.__SERVER_INFO)

        self.CONNECTION_DATA["sent_buffer_window"]["buffer"]\
            [self.LAST_MSG_ID_SENT] = player_data["player_data"]

        self.LAST_MSG_ID_SENT += 1
    # end send_player_data_to_server
# end Client class