import pandas as pd
from crawler import crawler
from modify_df import modify_df
import os
from argparse import ArgumentParser

# main

if __name__ == "__main__":
    
    parser = ArgumentParser()
    parser.add_argument("--load", required=True, help="original data path")
    parser.add_argument("--save", required=True, help="save path")
    args = parser.parse_args()

    df = pd.read_csv(args.load)
    data_list = df['ori데이터셋명'].values

    for i, d in enumerate(data_list):
    	crawl_list = crawler(d)
    	print('link : {}'.format(crawl_list[-1]))
    	df = modify_df(df, i, crawl_list)

    df.to_csv(args.save)