import tweepy
import matplotlib.pyplot as plt 
import key
import random
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import os
import re

def authenticate():
    auth = tweepy.OAuthHandler(key.CONSUMER_KEY, key.CONSUMER_SECRET)
    auth.set_access_token(key.ACCESS_TOKEN, key.ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    return api

def clean_tweet(tweet):
    tweet = re.sub(r'https\S+', '', tweet)
    tweet = re.sub(r'\n+', '\n', tweet)
    return tweet

def show_tweets(pos_tweets, neg_tweets):
    print('\nPositive Tweets')
    for tweet in random.sample(pos_tweets, 3):
        print(f'>{tweet}')
    print('\nNegative Tweets')
    for tweet in random.sample(neg_tweets, 3):
        print(f'>{tweet}')

def visualise_pie_chart(positive, negative, neutral):
    data = [positive, negative, neutral]
    activites = ['positive', 'negative', 'neutral']
    colors = ['g', 'r', 'c']
    plt.pie(data, labels=activites, colors=colors, startangle=120, autopct='%.1f%%', shadow=True)
    plt.title('Percentage of Postive, Negative and Neutral Tweets', bbox={'facecolor':'0.8', 'pad':5})
    plt.show()

def calculate_sentiment_VADER(tweets):
    analyser = SentimentIntensityAnalyzer()
    analysed_tweets = []
    for tweet in tweets:
        c_tweet = clean_tweet(tweet.full_text)
        vs = analyser.polarity_scores(c_tweet)
        analysed_tweets.append((c_tweet, vs['compound'], vs['pos'], vs['neg'], vs['neu']))
    return analysed_tweets

def saveFile(tweets, filename, search_tag):
    try:
        with open(f'{filename}.txt', 'w', encoding='utf-8') as file:
            for i, tweet in enumerate(tweets):
                file.write(f'{i+1}. {tweet}\n\n')
        print(f'{filename} tweets saved succesfully!')
    except:
        print('Data is already saved')

os.system('cls')

api = authenticate()

search_tag = input('Enter Tag to Analyse: ')
no = int(input('Number of Tweets to Analyse: '))

tweets = tweepy.Cursor(api.search, q=f'{search_tag} -filter:retweets', tweet_mode='extended', lang='en').items(no)

print('\nANALYSING TWEETS...')

analysed_tweets = calculate_sentiment_VADER(tweets)

pos_tweets = [tweet[0] for tweet in analysed_tweets if tweet[1] >= 0.05]
neg_tweets = [tweet[0] for tweet in analysed_tweets if tweet[1] <= -0.05]
neu_tweets = [tweet[0] for tweet in analysed_tweets if tweet[1] < 0.05 and tweet[1] > -0.05]

print('\nTweets are analysed!')


while True:
    os.system('cls')

    print('Tag: ', search_tag)

    print('\nPositive Tweets: ', len(pos_tweets))
    print('Negative Tweets: ', len(neg_tweets))
    print('Neutral Tweets: ', len(neu_tweets))
    print('\n1.Save Tweets')
    print('2.Visualise Data in Pie Chart')
    print('3.Show some Positive and Negative Tweets')
    print('4.Exit')
    choice = int(input('\nOption: '))

    if choice == 1:
        os.chdir(os.getcwd())
        try:
            os.mkdir(search_tag)
        except:
            pass
        os.chdir(os.getcwd() + '\\' + search_tag)
        saveFile(pos_tweets, 'positive', search_tag)
        saveFile(neg_tweets, 'negative', search_tag)
        saveFile(neu_tweets, 'neutral', search_tag)
        input('Press Enter to continue...')

    elif choice == 2:
        positive = len(pos_tweets)
        negative = len(neg_tweets)
        neutral = len(neu_tweets)
        visualise_pie_chart(positive, negative, neutral)

    elif choice == 3:
        show_tweets(pos_tweets, neg_tweets)
        input('Press Enter to continue...')

    else:
        break

    os.system('cls')