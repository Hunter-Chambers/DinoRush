import pickle
import time

import constants
from networking.connection import Connection


class Server(Connection):
    def __init__(self):
        super().__init__()
        self.SERVER = self.get_socket()
        self.SERVER.bind(constants.SERVER_CONNECTION_INFO)

        self.RUNNING = True
        self.UPDATE_INTERVAL = 0.1
        self.LAST_UPDATE_TIME = time.time()

        self.CLIENTS = self.get_connections()
        # this looks like:
        # {
        #     (<client_ip>, <port>): {
        #         # <player> will be the state of the player on this machine.
        #         # i.e. it references the client-side player when on the client
        #         # and the server-side player when on the server
        #
        #         "player": <player>,
        #         "recv_buffer_window": {
        #             "next_msg_num": <next expected message sequence number>,
        #             "buffer": {
        #                 <received buffered message sequence number>: <message>,
        #                 ...
        #             }
        #         },
        #         "sent_buffer_window": {
        #             "next_ack_num": <next expected acknowlegdement number>,
        #             "buffer": {
        #                 <sent buffered message sequence number>: <message>,
        #                 ...
        #             }
        #         }
        #     },
        #     ...
        # }
    # end __init__

    def start(self):
        raise NotImplementedError(
            "This method must be implemented in a subclass!")
    # end start

    def send_all_player_data_to_all_clients(self):
        if (len(self.CLIENTS)):
            all_player_data = {
                "msg_num": self.LAST_MSG_ID_SENT,
                "all_player_data": [
                    client_data["player"].get_serializable_data()
                    for client_data in self.CLIENTS.values()
                ]
            }

            for client in self.CLIENTS:
                self.get_socket().sendto(pickle.dumps(all_player_data), client)
                self.CLIENTS[client]["sent_buffer_window"]\
                    ["buffer"][self.LAST_MSG_ID_SENT] = all_player_data
            # end for

            self.LAST_MSG_ID_SENT += 1
        # end if
    # end send_all_player_data_to_all_clients
# end Server class