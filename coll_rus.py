from bs4 import BeautifulSoup
import requests

import os

import time, sys, threading
from datetime import timedelta, date
import datetime

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import pickle


from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

proc=int(sys.argv[1])
i=int(sys.argv[2])

time.sleep(10*i)



os.environ['MOZ_HEADLESS'] = '1'


firefox_profile = webdriver.FirefoxProfile()
firefox_profile.set_preference('permissions.default.stylesheet', 2)
firefox_profile.set_preference('permissions.default.image', 2)
firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
firefox_profile.set_preference('-headless', 1)
# create driver
driver = webdriver.Firefox(firefox_profile=firefox_profile)



now = datetime.datetime.now()

start_year = 2017
start_month = 10
start_day = 1
end_year = now.year
end_month = now.month
end_day = now.day

start_date = str(date(start_year, start_month, start_day))
end_date = str(date(end_year, end_month, end_day))

delta= ((date(end_year, end_month, end_day) - date(start_year, start_month, start_day)).days)/proc

#end_date = str(date(start_year, start_month, start_day)+timedelta(days=delta*(i+1)-1))
#start_date = str(date(start_year, start_month, start_day)+ timedelta(days=delta*i))

end_date = str(date(end_year, end_month, end_day)-timedelta(days=(delta+1)*i))
start_date = str(date(end_year, end_month, end_day)-timedelta(days=delta*(i+1)+i))

# twitter required params
#ini_url = lambda hashtag : 'https://twitter.com/search?q={}'.format(hashtag) + + since + start_date + until + end_date + src
#base_url = 'https://twitter.com/search?q='
since = '%20since%3A'
until = '%20until%3A'
src = '&src=hash'

#base_url = ini_url + since + start_date + until + end_date + src
base_url = lambda hashtag : ('https://twitter.com/search?q={}'+ since + start_date + until + end_date + src).format(hashtag)




def get_soup(url):
    return BeautifulSoup( requests.get(url).content, 'lxml')

def crawl_page(url, n):
    # open url
    driver.get(url)
    # wait for page to load
    driver.implicitly_wait(15)
    # scroll for n seconds
    for i in range(n):
        elem = driver.find_element_by_tag_name('a')
        elem.send_keys(Keys.END)
        time.sleep(2)
        sys.stderr.write('\r{0}/{1} complete...'.format(i+1,n))
    # gather list items
    list_items = driver.find_elements_by_tag_name('ol')
    # get soup
    soup = BeautifulSoup(list_items[0].get_attribute('innerHTML'),'lxml')
    return soup

#def extract_tweet_ids(soup):
#    return [ tag.get('data-item-id') for tag in soup.findAll('li') if 'data-item-type' in tag.attrs and tag.attrs['data-item-type'] == 'tweet']

def extract_tweet_ids(soup):
	tweets = soup.find_all('li','js-stream-item')
	tweet_user = []
	tweet_text = []
	tweet_id = []
	timestamp = []
	for tweet in tweets:
		if tweet.find('p','tweet-text'):
			tweet_user.append(tweet.find('span','username').text)
			tweet_text.append(tweet.find('p','tweet-text').text.encode('utf8'))
			tweet_id.append(tweet['data-item-id'])
			timestamp.append(tweet.find('a','tweet-timestamp')['title'])
			#tweet_timestamp = dt.datetime.strptime(timestamp, '%H:%M - %d %b %Y')
		else:
			continue
        tweet_data = zip(tweet_text, timestamp)
	return tweet_data

def save_tweets(hashtags, n, group):
    # hashtag -> list of hashtags
    #  construct urls and gather tweets
    for hashtag in hashtags:
        print('>> Crawling for #{}'.format(hashtag))
        # crawl page
        print base_url(hashtag)
        soup = crawl_page(base_url(hashtag), n)
        # get tweet tags
        tweet_ids = extract_tweet_ids(soup)
        print('>> Grabbed {0} tweets from {1}...'.format(len(tweet_ids),hashtag))
        # check if group folder exists
        if not os.path.exists('save/' + group):
            os.makedirs('save/' + group)
        # write to file
        with open('save_coll_russ'+str(i)+'.p'.format(group,hashtag), 'ab') as f:
            pickle.dump(tweet_ids,f)



if __name__ == '__main__':
    hashtags = ['collusion AND russia']
    save_tweets(hashtags, n=20, group='set3')
    driver.quit()

