from TikTokApi import TikTokApi
import string
import random
import pandas as pd


import sys
import logging
from logging import critical, error, info, warning, debug
import argparse

# logging
logging.basicConfig(format='%(message)s', level=logging.DEBUG, stream=sys.stdout)


def parse_arguments():
    """Read arguments from a command line."""
    parser = argparse.ArgumentParser(description='Arguments get parsed via --commands')
    parser.add_argument('-v', metavar='verbosity', type=int, default=2,
        help='Verbosity of logging: 0 -critical, 1- error, 2 -warning, 3 -info, 4 -debug')

    args = parser.parse_args()
    verbose = {0: logging.CRITICAL, 1: logging.ERROR, 2: logging.WARNING, 3: logging.INFO, 4: logging.DEBUG}
    logging.basicConfig(format='%(message)s', level=verbose[args.v], stream=sys.stdout)
    
    return args



#tiktok api

api = TikTokApi.get_instance()

# Since TikTok changed their API you need to use the custom_verifyFp option. 
# In your web browser you will need to go to TikTok, Log in and get the s_v_web_id value.
verifyFp = 'verify_kqgb2ddc_hlXcGbqj_zMOz_4qIi_8Pyk_SXz1ejZXzRHj'

results = 10

trending = api.trending(count=results, custom_verifyFp= verifyFp)



def simple_dict(tiktok_dict):
    to_return = {}
    to_return['user_name'] = tiktok_dict['author']['uniqueId']
    to_return['user_id'] = tiktok_dict['author']['id']
    to_return['video_id'] = tiktok_dict['id']
    to_return['video_desc'] = tiktok_dict['desc']
    to_return['video_time'] = tiktok_dict['createTime']
    to_return['video_length'] = tiktok_dict['video']['duration']
    to_return['video_link'] = 'https://www.tiktok.com/@{}/video/{}?lang=en'.format(
                to_return['user_name'], to_return['video_id'])
    to_return['n_likes'] = tiktok_dict['stats']['diggCount']
    to_return['n_shares'] = tiktok_dict['stats']['shareCount']
    to_return['n_comments'] = tiktok_dict['stats']['commentCount']
    to_return['n_plays'] = tiktok_dict['stats']['playCount']
    return to_return

def trending():
    n_trending = 20
    trending_videos = api.trending(count=n_trending)
    trending_videos = [simple_dict(v) for v in trending_videos]
    trending_videos_df = pd.DataFrame(trending_videos)
    trending_videos_df.to_csv('trending.csv',index=False)
    print('csv created')


if __name__ == '__main__':
    trending()