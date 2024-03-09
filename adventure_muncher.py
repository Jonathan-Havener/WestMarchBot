from basic_thread import Basic_Thread
from player_information import Player
from player_information import Character


class AdventureMuncher:

    def update_players_from_adventure(self, adventure: Basic_Thread, player_list=None) -> list:
        if player_list is None:
            player_list = []
        for gamer_tag in adventure.players:

            # find the existing player or create a new one
            matching_players = [existing_player for existing_player in player_list if existing_player.discord_tag == gamer_tag]
            if matching_players:
                player = matching_players[0]
            else:
                player = Player()
                player.discord_tag = gamer_tag
                player_list.append(player)

            character = player.get_character(gamer_tag)
            if not character:
                # We don't know the characters name yet, so just give it the discord tag for now.
                character = Character(name=gamer_tag)
                player.add_character(character=character)

            character.go_on_adventure(quest_name=adventure.name,
                               adventure_date=adventure.created_at,
                               adventurer_messages=adventure.player_messages(gamer_tag))

            player.backup()

        return player_list


if __name__ == "__main__":
    import pickle

    with open("data.pkl", "rb") as f:
        data = pickle.load(f)

    for thread in data:
        data[thread].build_logger()

    players = []
    for adventure_name in data:
        players = AdventureMuncher().update_players_from_adventure(data[adventure_name], players)

    print(players[0].show_history())
    print("done")