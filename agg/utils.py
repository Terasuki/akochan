import json

def find_reach(log_file):
    reach_hands = []
    
    player_hands = [[] for _ in range(4)]
    
    current_kyoku_data = {}

    is_reach = False
    reach_actor = -1
    reach_kyoku_data_on_declare = {}

    with open(log_file, "r") as f:
        for line in f:
            event = json.loads(line)

            if event["type"] == "start_kyoku":
                for i in range(4):
                    player_hands[i] = list(event["tehais"][i])
                
                current_kyoku_data = {
                    "bakaze": event["bakaze"],
                    "dora_marker": event["dora_marker"],
                    "honba": event["honba"],
                    "kyoku": event["kyoku"],
                    "kyotaku": event["kyotaku"],
                    "oya": event["oya"],
                    "scores": event["scores"]
                }

            elif event["type"] == "tsumo":
                actor = event["actor"]
                pai = event["pai"]
                player_hands[actor].append(pai)

            elif event["type"] == "dahai":
                actor = event["actor"]
                pai = event["pai"]
                if pai in player_hands[actor]:
                    player_hands[actor].remove(pai)
                
                if is_reach and actor == reach_actor:
                    full_hand = tuple(sorted(player_hands[actor])) 
                    
                    output_data = {
                        "bakaze": reach_kyoku_data_on_declare["bakaze"],
                        "dora_marker": reach_kyoku_data_on_declare["dora_marker"],
                        "honba": reach_kyoku_data_on_declare["honba"],
                        "kyoku": reach_kyoku_data_on_declare["kyoku"],
                        "kyotaku": reach_kyoku_data_on_declare["kyotaku"],
                        "oya": reach_kyoku_data_on_declare["oya"],
                        "scores": reach_kyoku_data_on_declare["scores"],
                        "hand": full_hand,
                        "player": actor
                    }
                    reach_hands.append(output_data)
                    
                    is_reach = False
                    reach_actor = -1
                    reach_kyoku_data_on_declare = {}
                
            elif event["type"] == "chi":
                actor = event["actor"]
                consumed_tiles = event["consumed"]
                for tile in consumed_tiles:
                    if tile in player_hands[actor]:
                        player_hands[actor].remove(tile)
                
            elif event["type"] == "pon":
                actor = event["actor"]
                consumed_tiles = event["consumed"]
                for tile in consumed_tiles:
                    if tile in player_hands[actor]:
                        player_hands[actor].remove(tile)

            elif event["type"] == "ankan":
                actor = event["actor"]
                consumed_tiles = event["consumed"]
                
                for tile in consumed_tiles:
                    if tile in player_hands[actor]:
                        player_hands[actor].remove(tile)
                player_hands[actor].append(tile + "*")

            elif event["type"] == "reach":
                actor = event["actor"]
                is_reach = True
                reach_actor = actor
                reach_kyoku_data_on_declare = current_kyoku_data.copy()

    return reach_hands

def count_rounds(log_file):

    rounds = []
    current_kyoku_data = {}

    with open(log_file, "r") as f:
        for line in f:
            event = json.loads(line)
            if event["type"] == "start_kyoku":
                current_kyoku_data = {
                    "bakaze": event["bakaze"],
                    "dora_marker": event["dora_marker"],
                    "honba": event["honba"],
                    "kyoku": event["kyoku"],
                    "kyotaku": event["kyotaku"],
                    "oya": event["oya"],
                    "scores": event["scores"]
                }
                rounds.append(current_kyoku_data)
    
    return rounds