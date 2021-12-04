##############################################################################################################
# This program was devoloped by Jasiel Rivera , Michael H, Terrefortes and Eliam Ruiz as the final proyect for
# Data Science class CCOM3031 first semester school year 2021-2022, professor P.Ordoñez UPRRP.
#
# Purpose: This program uses data collected through the Reddit API on a given/specified subreddit. Then the 
# information will be used to determine the given subreddit's sentiment. This is achieved by performing 
# analysis on its data such as word frequency, top posts, and these words are used to determine is a post is 
# 'positive, 'negative' or neutral. Then the results will be presented as charts, graphs and even a png 
# containig the word cloud (most frequent words) of the given subreddit
############################################################################################################## 
import reddit_analysis as ra
import uuid

def main():
    reddit = ra.RedditAnalysis()

    # gather post data
    posts, dictForCSV = reddit.subreddit_info("politics", num_posts=500, title_only=True)

    # creates a CSV file with data
    reddit.makeCSVFile(dictForCSV, "politics")

    # get the sentiment of the subreddit
    sentiment = reddit.subreddit_sentiment(posts)

    # get positive posts
    positive_posts = reddit.get_positive_posts(posts)

    # get negative posts
    negative_posts = reddit.get_negative_posts(posts)

    # get neutral posts
    neutral_posts = reddit.get_neutral_posts(posts)

    # get the word frequency of the subreddit divided by sentiment
    positive_word_freq = reddit.subreddit_word_frequency(positive_posts)
    negative_word_freq = reddit.subreddit_word_frequency(negative_posts)
    neutral_word_freq = reddit.subreddit_word_frequency(neutral_posts)


    # create sentiment pie chart
    reddit.subreddit_sentiment_piechart(sentiment)

    # gather word frequency data
    word_freq = reddit.subreddit_word_frequency(posts)

    # create word frequency graph
    reddit.top_words_graph(word_freq)
    reddit.top_words_graph(positive_word_freq, num_words=10, title="Common words in positive posts")
    reddit.top_words_graph(negative_word_freq, num_words=10, title="Common words in negative posts")
    reddit.top_words_graph(neutral_word_freq, num_words=10, title="Common words in neutral posts")

    # create wordcloud png
    reddit.subreddit_wordcloud(word_freq)
    
    for post in posts:
        print(post)
        print("\n")
    print(word_freq)
    print(reddit.get_top_posts(positive_posts, 5,))
    print(reddit.get_top_posts(negative_posts, 5))
    print(reddit.get_top_posts(neutral_posts, 5))

    random_uuid = uuid.uuid4()
    print(random_uuid)

if __name__ == '__main__':
    main()