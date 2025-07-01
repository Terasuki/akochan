from utils import process_mahjong_log

import json
import pandas as pd

from glob import glob

if __name__ == "__main__":

    logs_glob = glob("/Users/terasuki/Documents/Projects/akochan/match_result/haifu_*")
    reach_hands = []
    for log in logs_glob:
        results = process_mahjong_log(log)
        reach_hands = reach_hands + results
    
    df = pd.DataFrame(reach_hands)
    df.to_parquet("/Users/terasuki/Documents/Projects/akochan/agg/data/reach.parquet")