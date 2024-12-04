#############################################################
### IMPORTS
#############################################################
from networking.client import Client
from dino_rush_player import DinoRushPlayer


class DinoRushClient(Client):
    def __init__(self, world):
        super().__init__(world)
    # end __init__

    def create_entity(self, entity_data):
        sprite_id = entity_data["sprite_id"]
        scale_factor = entity_data["scale_factor"]
        position = entity_data["position"]
        entity_id = entity_data["entity_id"]
        entity = DinoRushPlayer(sprite_id, scale_factor, *position, entity_id)
        self.add_entity(entity)
        return entity
    # end create_entity

    def initialize_client(self, _, message):
        self.create_entity(message)
        super().initialize_client(_, message)
    # end initialize_client
# end DinoRushClient class