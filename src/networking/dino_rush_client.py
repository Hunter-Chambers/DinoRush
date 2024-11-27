import engine
from networking.client import Client
from player.dino_rush_player import DinoRushPlayer


class DinoRushClient(Client):


    def __init__(self, server_info, world):
        super().__init__(server_info)
        self.WORLD = world
    # end __init__

    def create_player(self, _, current_time, player_data):
        character_id = player_data["character_id"]
        scale_factor = player_data["scale_factor"]
        position = player_data["position"]
        multiplayer_id = player_data["multiplayer_id"]
        timestamp = current_time

        player = DinoRushPlayer(
            character_id, scale_factor, *position,
            multiplayer_id,timestamp)

        self.CONNECTION_DATA["player"] = player
        self.CLIENT_ID = multiplayer_id

        self.CONNECTION_DATA["recv_buffer_window"]["next_msg_num"]\
            = player_data["next_msg_num"]
    # end create_player

    def process_player_data(self, _, all_player_data, current_time):
        for player_data in all_player_data["all_player_data"]:
            player_id = player_data["multiplayer_id"]

            if (player_id == self.CLIENT_ID):
                self.__handle_own_player_data(player_data, current_time)
            elif (player_id in self.OTHER_PLAYERS):
                self.__update_other_player(
                    player_id, player_data, current_time)
            else:
                self.__add_new_player(player_id, player_data, current_time)
            # end if
        # end for
    # end process_player_data

    def __add_new_player(self, player_id, player_data, current_time):
        self.OTHER_PLAYERS[player_id] = DinoRushPlayer(
            player_data["character_id"], player_data["scale_factor"],
            *player_data["position"], player_id, current_time)
    # end __add_new_player

    def __handle_own_player_data(self, player_data, current_time):
        player = self.CONNECTION_DATA["player"]
        player.set_from_unserialized_data(player_data, current_time)

        buffer = self.CONNECTION_DATA["sent_buffer_window"]["buffer"]

        for msg_num in sorted(buffer):
            plyr_data = buffer[msg_num]
            player.update(plyr_data["pressed_keys"], current_time)
            engine.handle_collisions(player, self.WORLD)
        # end for
    # end __handle_own_player_data

    def __update_other_player(self, player_id, player_data, current_time):
        player = self.OTHER_PLAYERS[player_id]
        player.set_from_unserialized_data(player_data, current_time)
    # end __update_other_player
# end DinoRushClient class