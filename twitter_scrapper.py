import snscrape.modules.twitter as sntwitter
import pandas as pd
import datetime
import string
import re
# enchant library use to check the language word spelling
from enchant.checker import SpellChecker

max_error_count = 5
min_text_length = 3

#function use to clean the data
def dataCleaning(text):
    from nltk.corpus import stopwords
    punctuation = string.punctuation
    stopwords = stopwords.words('english')
    text = text.lower()
    text = re.sub('www.[^\s]+', '', text)
    text = re.sub('https:[^\s]+', '', text)
    text = re.sub(r'[0-9]', '',text)
    emoj = re.compile("["
                      u"\U0001F600-\U0001F64F"  # emoticons
                      u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                      u"\U0001F680-\U0001F6FF"  # transport & map symbols
                      u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                      u"\U00002500-\U00002BEF"  # chinese char
                      u"\U00002702-\U000027B0"
                      u"\U00002702-\U000027B0"
                      u"\U000024C2-\U0001F251"
                      u"\U0001f926-\U0001f937"
                      u"\U00010000-\U0010ffff"
                      u"\u2640-\u2642"
                      u"\u2600-\u2B55"
                      u"\u200d"
                      u"\u23cf"
                      u"\u23e9"
                      u"\u231a"
                      u"\ufe0f"  # dingbats
                      u"\u3030"
                      "]+", re.UNICODE)
    text = re.sub(emoj, '', text)
    text = "".join(x for x in text if x not in punctuation)
    words = text.split()
    words = [w for w in words if w not in stopwords]
    text = " ".join(words)

    return text

# return true if the text is english otherwise return false
def is_in_english(text):
  d = SpellChecker("en_US")
  d.set_text(text)
  errors = [err.word for err in d]
  return False if ((len(errors) > max_error_count) or len(text.split()) < min_text_length) else True

tweets_list2 = []

#function use to scrape the data between given date
def twitter_data_scrape(keyword,start_date,end_date):
    # Creating list to append tweet data to

    # Using TwitterSearchScraper to scrape data and append tweets to list
    query = str(keyword)+' since:'+str(start_date)+' until:'+str(end_date)
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()): #'ethereum since:2022-01-15 until:2022-02-01'
        print("posts scrapping count ", i, " date : ", tweet.date)
        try:
            clean_text = dataCleaning(tweet.content)
            if is_in_english(clean_text):
                tweets_list2.append([tweet.date, tweet.id, clean_text, tweet.user.username])
        except:
            continue

keyword = input("Enter keyword: ")
start_date = input("Enter start date in this format yyyy-mm-dd:  ")
start_date =datetime.datetime.strptime(start_date , "%Y-%m-%d")
end_date = input("Enter end date in this format yyyy-mm-dd:  ")
end_date =datetime.datetime.strptime(end_date , "%Y-%m-%d")

twitter_data_scrape(keyword,start_date,end_date)

# Creating a dataframe from the tweets list above
tweets_df2 = pd.DataFrame(tweets_list2, columns=['Datetime', 'Tweet Id', 'Text', 'Username'])
tweets_df2.to_csv('scrapped_date.csv',  index=False)
print("---------------All tweets store into the scrapped_data.csv file----------------------")
















