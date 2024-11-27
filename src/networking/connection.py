import pickle
import socket

import constants


class Connection:
    __MAX_MSG_ID = 10000

    def __init__(self):
        self.LAST_MSG_ID_SENT = 0
        self.__SOCKET = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__SOCKET.setblocking(False)
        self.__CONNECTIONS = {}
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

    def close(self):
        self.__SOCKET.close()
    # end close

    def create_player(self, addr, current_time, message_data):
        raise NotImplementedError(
            "This method must be implemented in a subclass!")
    # end create_player

    def get_connections(self):
        return self.__CONNECTIONS
    # end get_connections

    def get_msg_buffer(self, addr):
        return self.__CONNECTIONS[addr]["recv_buffer_window"]
    # end get_msg_buffer

    def get_socket(self):
        return self.__SOCKET
    # end get_socket

    def process_ack_message(self, addr, message_data):
        buffer_window = self.__CONNECTIONS[addr]["sent_buffer_window"]
        buffer = buffer_window["buffer"]

        ack_msg_num = message_data["ack_msg_num"]

        buffer_window["next_ack_num"] = ack_msg_num + 1
        buffer_window["buffer"] = {
            msg_num: msg_data
            for msg_num, msg_data in buffer.items()
            if msg_num > ack_msg_num}
    # end process_ack_message

    def process_player_data(self, addr, player_data, current_time):
        raise NotImplementedError(
            "This method must be implemented in a subclass!")
    # end process_player_data

    def send_ack_message(self, ack_num, addr):
        message = {"ack_msg_num": ack_num}
        self.__SOCKET.sendto(pickle.dumps(message), addr)
    # end send_ack_message

    def start(self):
        raise NotImplementedError(
            "This method must be implemented in a subclass!")
    # end start

    @classmethod
    def handle_message(cls, connection, current_time):
        reading = True
        while (reading):
            try:
                message, addr = connection.get_socket()\
                    .recvfrom(constants.BUFFER_SIZE)
            except BlockingIOError:
                reading = False
                continue
            # end try/except

            message_data = pickle.loads(message)

            if ("INITIAL_CONNECTION" in message_data):
                connection.create_player(addr, current_time, message_data)
            elif ("CLOSING_CONNECTION" in message_data):
                # TODO: handle client disconnecting
                raise NotImplementedError("NEED TO HANDLE DISCONNECTING")
            elif ("msg_num" in message_data):
                Connection.process_data_message(
                    connection, addr, message_data, current_time)
            else:
                connection.process_ack_message(addr, message_data)
            # end if
        # end if
    # end __handle_message

    @classmethod
    def process_data_message(
        cls, connection, addr, message_data, current_time):

        buffer_window = connection.get_msg_buffer(addr)
        next_msg_num = buffer_window["next_msg_num"]
        buffer = buffer_window["buffer"]

        recv_msg_num = message_data["msg_num"]

        if (recv_msg_num == next_msg_num):
            connection.process_player_data(addr, message_data, current_time)

            next_msg_num += 1

            while (next_msg_num in buffer):
                msg_data = buffer.pop(next_msg_num)
                connection.process_player_data(addr, msg_data, current_time)

                next_msg_num += 1
            # end while

            buffer_window["next_msg_num"] = next_msg_num

            connection.send_ack_message(next_msg_num - 1, addr)
        elif (recv_msg_num > next_msg_num):
            buffer[recv_msg_num] = message_data
        else:
            # TODO: check for wrap around
            raise NotImplementedError("NEED TO CHECK FOR WRAP-AROUND ON MESSAGE IDS")
        # end if
    # end process_data_message
# end Server class