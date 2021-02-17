import os
import time
import argparse
import pandas as pd
from tqdm.auto import tqdm
import snscrape.modules.twitter as sntwitter

def scrape_tweets_by_keyword(keyword, output_dir=None, num_tweets=10000,
                             username=None, exclude_replies=False, 
                             since=None, until=None, lang=None,
                             get_all=False, interval=1):
    #make query
    search_query = make_search_query(keyword, username, since, until, lang)
    if not search_query:
        print('at least one of keyword and username must be given')
        return
    #start scraping tweets
    tweets_list = []
    num_scraped = 0
    if not get_all:
        total = num_tweets
    else:
        total = len(list(sntwitter.TwitterSearchScraper(search_query).get_items()))
    with tqdm(total=total) as pbar:
        for tweet in sntwitter.TwitterSearchScraper(search_query).get_items():
            if num_tweets and num_scraped == total:
                break
            #whether or not include replies
            if exclude_replies and '@' in tweet.content:
                continue
            tweets_list.append([tweet.date, tweet.username, tweet.content])
            num_scraped += 1
            pbar.update(1)
            time.sleep(interval)
    #save scraped tweets as a csv file
    tweets_df = pd.DataFrame(tweets_list, columns=['Date', 'Username', 'Tweet'])
    if not output_dir:
        output_dir = os.getcwd()
    output_path = f'{output_dir}/tweets_about_{search_query}.csv'
    print(len(tweets_df), 'tweets obtained')
    tweets_df.to_csv(output_path, index=False)

def scrape_tweets_by_username(username, output_dir=None, num_tweets=10000,
                              exclude_replies=False, since=None, until=None,
                              lang=None, get_all=False, interval=1):
    #make query
    keyword = None
    search_query = make_search_query(keyword, username, since, until, lang)
    if not search_query:
        print('username must be given')
        return
    #start scraping tweets
    tweets_list = []
    num_scraped = 0
    if not get_all:
        total = num_tweets
    else:
        total = len(list(sntwitter.TwitterSearchScraper(search_query).get_items()))
    with tqdm(total=total) as pbar:
        for tweet in sntwitter.TwitterSearchScraper(search_query).get_items():
            if num_tweets and num_scraped == total:
                break
            #whether or not include replies
            if exclude_replies and '@' in tweet.content:
                continue
            tweets_list.append([tweet.date, tweet.username, tweet.content])
            num_scraped += 1
            pbar.update(1)
            time.sleep(interval)
    #save scraped tweets as a csv file
    tweets_df = pd.DataFrame(tweets_list, columns=['Date', 'Username', 'Tweet'])
    if not output_dir:
        output_dir = os.getcwd()
    output_path = f'{output_dir}/tweets_{search_query}.csv'
    print(len(tweets_df), 'tweets obtained')
    tweets_df.to_csv(output_path, index=False)

def make_search_query(keyword, username=None, since=None, until=None, lang=None):
    #add keyword and username to query
    if keyword and username:
        query = f'{keyword} from:{username}'
    elif keyword and not username:
        query = f'{keyword}'
    elif not keyword and username:
        query = f'from:{username}'
    else:
        return
    #add dates to query
    if not since and not until:
        pass
    elif since and not until:
        query = f'{query} since:{since}'
    elif not since and until:
        query = f'{query} until:{until}'
    else:
        query = f'{query} since:{since} until:{until}'
    #add language to query
    if lang:
        query = f'{query} lang:{lang}'
    else:
        pass
    return query

#get command line arguments
def get_arguments():
    parser = argparse.ArgumentParser(description='Scraping Tweets To CSV')
    parser.add_argument('--keyword', '-kw', type=str, default=None,
                         help='search for tweets with this keyword')
    parser.add_argument('--username', '-user',  type=str, default=None,
                         help='search for tweets from this username')
    parser.add_argument('--output_dir', '-dir', type=str, default=None,
                         help='save the output file in this directory')
    parser.add_argument('--num_tweets', '-num', type=int, default=10000,
                         help='get this number of tweets')
    parser.add_argument('--get_all', '-all', action='store_true',
                         help='whether or not get as many tweets as possible')
    parser.add_argument('--exclude_replies', '-ex_rep', action='store_true',
                         help='whether or not exclude replies')
    parser.add_argument('--since', type=str, default=None,
                         help='search for tweets since this date')
    parser.add_argument('--until', type=str, default=None,
                         help='search for tweets until this date')
    parser.add_argument('--lang', type=str, default=None,
                         help='search for tweets in this language')
    parser.add_argument('--interval', '-t', type=float, default=1,
                         help='wait for this interval before scraping next tweet. unit : second')
    return parser.parse_args()

if __name__ == '__main__':
    args = get_arguments()
    keyword = args.keyword
    username = args.username
    if not keyword and not username:
        print('at least one of keyword and username must be given')
    elif not keyword and username:
        print('scraping tweets')
        scrape_tweets_by_username(username=username, 
                                  output_dir=args.output_dir,
                                  num_tweets=args.num_tweets, 
                                  exclude_replies=args.exclude_replies,
                                  since=args.since, 
                                  until=args.until, 
                                  lang=args.lang,
                                  get_all=args.get_all,
                                  interval=args.interval)
    else:
        print('scraping tweets')
        scrape_tweets_by_keyword(keyword=keyword,
                                 output_dir=args.output_dir,
                                 num_tweets=args.num_tweets,
                                 username=username,
                                 exclude_replies=args.exclude_replies,
                                 since=args.since,
                                 until=args.until,
                                 lang=args.lang,
                                 get_all=args.get_all,
                                 interval=args.interval)
