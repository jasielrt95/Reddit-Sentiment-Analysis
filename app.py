import reddit_sentiment as rs

def main():
    Reddit_Sentiment = rs.RedditSentiment("credentials.txt")
    Reddit_Sentiment.get_subreddit_sentiment("Trueoffmychest", 5)
    word_frq = Reddit_Sentiment.word_frequency("technews", 100)
    Reddit_Sentiment.word_cloud_generator(word_frq, "technews")

if __name__ == '__main__':
    main()