from utils import find_reach, count_rounds

import pandas as pd

from glob import glob
from tqdm import tqdm

def create_df(func, name):
    logs_glob = glob("/Users/terasuki/Documents/Projects/akochan/match_result/haifu_*")
    all_data = []
    for log in tqdm(logs_glob):
        results = func(log)
        all_data = all_data + results
    
    df = pd.DataFrame(all_data)
    df.to_parquet(f"/Users/terasuki/Documents/Projects/akochan/agg/data/{name}.parquet")
    return df

if __name__ == "__main__":

    create_df(find_reach, "reach")
    create_df(count_rounds, "rounds")