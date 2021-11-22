from numpy import positive
import praw
import matplotlib.pyplot as plt
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from wordcloud import WordCloud

class RedditAnalysis:
    """
    This class have useful methods for analyzing data about subreddits.

    ...

    Attributes
    ----------
    client_id : str
        The client ID for the reddit API.
    client_secret : str
        The client secret for the reddit API.
    reddit : praw.Reddit
        The reddit API object.

    Methods
    -------
    reddit_sentiment(subreddit, num_posts=100, title_only=False)
        Returns a list of dictionaries containing the title, text, score, url, and sentiment of the top posts from the given subreddit.

    """

    def __init__(self, file_name="credentials.txt"):

        # Grab the reddit API credentials from the file
        with open(file_name, 'r') as file:
            self.client_id = file.readline().strip()
            self.client_secret = file.readline().strip()

        # Create the reddit API object
        self.reddit = praw.Reddit(client_id=self.client_id,
                                  client_secret=self.client_secret,
                                  user_agent='reddit_sentiment')

    def subreddit_info(self, subreddit, num_posts=100, title_only=False):

        # Create a sia object
        sia = SentimentIntensityAnalyzer()

        # Get the hot posts from the subreddit
        hot_posts = self.reddit.subreddit(subreddit).top(limit=num_posts)

        # Create a list to hold the posts
        post_info = []

        # tokenizer to remove punctuation
        tokenizer = RegexpTokenizer(r'\w+')

        for post in hot_posts:

            # Get the post text
            text = post.selftext
            text = text.lower()
            text = tokenizer.tokenize(text)
            text = [
                word for word in text if word not in stopwords.words('english')]
            text = ' '.join(text)

            # Get the post title
            title = post.title
            title = title.lower()
            title = tokenizer.tokenize(title)
            title = [
                word for word in title if word not in stopwords.words('english')]
            title = ' '.join(title)

            # Get the post score
            score = post.score

            # Get the post URL
            url = post.url

            # Get the post sentiment
            if title_only:
                sentiment = sia.polarity_scores(title)

            else:
                # Get the post sentiment
                post = title + " " + text
                sentiment = sia.polarity_scores(post)

            if sentiment['compound'] > 0:
                sentiment = "positive"

            elif sentiment['compound'] < 0:
                sentiment = "negative"

            else:
                sentiment = "neutral"

            # create a dictionary to store the post data
            post_dict = {
                'title': title,
                'text': text,
                'score': score,
                'url': url,
                'sentiment': sentiment
            }

            # add the post to the list
            post_info.append(post_dict)

        return post_info

    def subreddit_sentiment(self, post_info):
        positives = 0
        negatives = 0
        neutrals = 0

        for post in post_info:
            if post['sentiment'] == 'positive':
                positives += 1
            elif post['sentiment'] == 'negative':
                negatives += 1
            else:
                neutrals += 1

        dictionary = { 'positive': positives, 'negative': negatives, 'neutral': neutrals }

        return dictionary

    def subreddit_word_frequency(self, postinfo):
        exclude = ["r", "https", "com"]
        text = ""
        word_freq = {}
        for post in postinfo:
            text += post['text'] + " "
            text += post['title'] + " "

        text = text.split()
        for word in text:
            if word not in word_freq and word not in exclude:
                word_freq[word] = 1
            elif word not in exclude:
                word_freq[word] += 1
        
        return word_freq

    def top_words_graph(self, word_freq, num_words=10, title="Top Words"):

        # order the words by frequency
        if len(word_freq) > 0:
            word_freq = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)

            # Create the graph
            plt.title(title)
            plt.xlabel("Word")
            plt.ylabel("Frequency")
            plt.bar(range(num_words), [word_freq[i][1] for i in range(num_words)])
            plt.xticks(range(num_words), [word_freq[i][0] for i in range(num_words)])
            plt.show()
        else:
            print("No words to graph")

    def get_positive_posts(self, posts):
        positive_posts = []
        for post in posts:
            if post['sentiment'] == 'positive':
                positive_posts.append(post)
        return positive_posts

    def get_negative_posts(self, posts):
        negative_posts = []
        for post in posts:
            if post['sentiment'] == 'negative':
                negative_posts.append(post)
        return negative_posts

    def get_neutral_posts(self, posts):
        neutral_posts = []
        for post in posts:
            if post['sentiment'] == 'neutral':
                neutral_posts.append(post)
        return neutral_posts

    def get_top_posts(self, posts, num_posts):
        # order posts by score
        if len(posts) < num_posts:
            num_posts = len(posts)
        if len(posts) > 0:
            top_posts = []
            posts = sorted(posts, key=lambda x: x['score'], reverse=True)
            for i in range(num_posts):
                top_posts.append(posts[i]['url'])
            return top_posts
        else:
            return "No posts to return"


    def subreddit_wordcloud(self, word_freq):
            
            # Create a word cloud object
            wordcloud = WordCloud(
                width=800,
                height=400,
                background_color='#383a59',
                stopwords=stopwords.words('english'),
                colormap='tab20'
            ).generate_from_frequencies(word_freq)
            
            # Change the font color
            # wordcloud.recolor(color_func="#BD93F9")

            # Save the word cloud image
            wordcloud.to_file("wordcloud.png")

            # Display the word cloud image
            plt.imshow(wordcloud, interpolation='bilinear')

    
    def subreddit_sentiment_piechart(self, sentiment_dict, title="Sentiment"):
        """
        Plot a graph of the sentiment of the top posts from the given subreddit.

        Parameters
        ----------
        post_info : list
            A list of dictionaries containing the title, text, score, url, and sentiment of the top posts from the given subreddit.

        Returns
        -------
        None.

        """
        positives = sentiment_dict['positive']
        negatives = sentiment_dict['negative']
        neutrals = sentiment_dict['neutral']
        plt.title(title)

        if neutrals > 0:
            # Create the pie chart
            labels = 'Positive', 'Neutral', 'Negative'
            sizes = [positives, neutrals, negatives]
            colors = ['green', 'blue', 'red']
            plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%')
            plt.axis('equal')
            plt.show()
        else:
            labels = 'Positive', 'Negative'
            sizes = [positives, negatives]
            colors = ['green', 'red']
            plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%')
            plt.axis('equal')
            plt.show()





