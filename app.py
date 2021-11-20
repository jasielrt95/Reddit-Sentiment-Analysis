import reddit_sentiment as rs

def main():
    Reddit_Sentiment = rs.RedditSentiment("credentials.txt")
    Reddit_Sentiment.get_subreddit_sentiment("worldnews", 5)

if __name__ == '__main__':
    main()