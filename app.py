import reddit_sentiment as rs

def main():
    Reddit_Sentiment = rs.RedditSentiment("credentials.txt")
    subredditPosNeg = Reddit_Sentiment.get_subreddit_sentiment("worldnews", 100)
    Reddit_Sentiment.graph_Barplot("graphPositiveNegative", subredditPosNeg, 'Positive and negative posts in r/worldnews', 'Quantity')
    
    word_frq = Reddit_Sentiment.word_frequency("technews", 100)
    Reddit_Sentiment.word_cloud_generator(word_frq, "technews")

    positiveFreq = Reddit_Sentiment.positiveWordFreq("worldnews", 100)
    Reddit_Sentiment.graph_Barplot("positiveFreq", positiveFreq, 'Positive frequenly used words in r/worldnews', 'Positive', 'Words')

    negativeFreq = Reddit_Sentiment.negativeWordFreq("worldnews", 100)
    Reddit_Sentiment.graph_Barplot("negativeFreq", negativeFreq, 'Negative frequenly used words in r/worldnews', 'Negative', 'Words')

    print("Finished")

if __name__ == '__main__':
    main()