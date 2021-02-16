# scrape_tweets_to_csv
A python script to scrape tweets using [snscrape](https://github.com/JustAnotherArchivist/snscrape), and save them as a csv file.

## Usage
install [snscrape](https://github.com/JustAnotherArchivist/snscrape), and clone this repo.
```
pip install snscrape
git clone https://github.com/MarkOkd/scrape_tweets_to_csv.git
```
as python functions
```python
from scrape_tweets import scrape_tweets_by_keyword, scrape_tweets_by_username

#get tweets with a keyword
scrape_tweets_by_keyword(keyword='tweet', num_tweets=1000)

#get tweets from a user
scrape_tweets_by_username(username='Twitter', num_tweets=1000)

#get tweets with a keyword from a user
scrape_tweets_by_keyword(keyword='tweet', username='Twitter', num_tweets=1000)

#get tweets of specific dates and in a specific language
scrape_tweets_by_keyword(keyword='tweet', num_tweets=1000, since='2021-01-10', until='2021-01-12', lang='en')
```
from command line
```
python scrape_tweets.py\
    --keyword tweets\
    --num_tweets 1000\
    --lang en\
```
