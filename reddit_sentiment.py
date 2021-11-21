# This program will scrape the top posts from a subreddit and save them to a file.
# It will also save the title and the url of each post.

# Import the necessary modules
import operator
import praw
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, RegexpTokenizer
import nltk
# nltk.download('vader_lexicon')
# nltk.download('stopwords')
from nltk.sentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import operator

class RedditSentiment:
    """
    This class will scrape the top posts from a subreddit and analyze the sentiment of each post.

    ...

    Attributes:
        reddit: reddit object
            The reddit object
        sia: sentiment analyzer object
            The sentiment analyzer object
        client_id: str
            The client id for the reddit API
        client_secret: str
            The client secret for the reddit API

    Methods:
        get_subreddit_sentiment(self, subreddit="amitheasshole", num_posts=10): 
            This method will scrape the top posts from a subreddit and analyze the sentiment of each post(num_posts).
    """

    def __init__(self, file_name="credentials.txt"):
        """
        This method will initialize the RedditSentiment class.

        ...

        Parameters:
            file_name: str, by default "credentials.txt"
                name of the file containing the credentials for the reddit API

        Attributes:
            reddit: reddit object
                The reddit object
            sia: sentiment analyzer object
                The sentiment analyzer object
            client_id: str
                The client id for the reddit API
            client_secret: str
                The client secret for the reddit API
        """
        # Grab the reddit API credentials from the file
        with open(file_name, 'r') as file:
            self.client_id = file.readline().strip()
            self.client_secret = file.readline().strip()

        # Create a sentiment analyzer object
        self.sia = SentimentIntensityAnalyzer()

        # Create an instance of the Reddit API
        self.reddit = praw.Reddit(
            client_id=self.client_id, client_secret=self.client_secret, user_agent='Reddit_Scrapper')

    def get_subreddit_sentiment(self, subreddit="amitheasshole", num_posts=10):
        """
        This method will scrape the top posts from a subreddit and analyze the sentiment of each post(num_posts).

        ...

        Parameters:
            subreddit: str, by default "amitheasshole"
                The subreddit to scrape
            num_posts: int, by default 10
                The number of posts to scrape
        """

        # Get the top posts from the subreddit
        subreddit = self.reddit.subreddit(subreddit)
        top_posts = subreddit.hot(limit=num_posts)

        # Print the title, content and url of each post if its not stickied
        tuple = {}

        positiveNegativePosts = {}
        
        for post in top_posts:
            # print("Title: ", post.title, "\n")

            if self.sia.polarity_scores(post.title)['compound'] > 0:
                # print("Sentiment: Positive")
                if "Positive" in positiveNegativePosts:
                    positiveNegativePosts["Positive"] = positiveNegativePosts["Positive"] + 1
                else:
                    positiveNegativePosts["Positive"] = 1

            elif self.sia.polarity_scores(post.title)['compound'] < 0:
                # print("Sentiment: Negative")
                if "Negative" in positiveNegativePosts:
                    positiveNegativePosts["Negative"] = positiveNegativePosts["Negative"] + 1
                else:
                    positiveNegativePosts["Negative"] = 1

            else:
                # print("Sentiment: Neutral")
                if "Neutral" in positiveNegativePosts:
                    positiveNegativePosts["Neutral"] = positiveNegativePosts["Neutral"] + 1
                else:
                    positiveNegativePosts["Neutral"] = 1

            print("URL: ", post.url, "\n")
            print("\n")
            print("="*50)

        print(tuple)
        fig, ax1 = plt.subplots()
        ax1.bar(tuple.keys(), tuple.values())
        fig.autofmt_xdate()
        plt.savefig('graph.png')
        plt.show()
        

            # print("URL: ", post.url, "\n")
            # print("\n")
            # print("="*50)
            
        return positiveNegativePosts

    def word_frequency(self, subreddit="amitheasshole", num_posts=10):
        """
        This method will scrape the top posts from a subreddit and check the frequency of each word in the posts.

        ...

        Parameters:
            subreddit: str, by default "amitheasshole"
                The subreddit to scrape
            num_posts: int, by default 10
                The number of posts to scrape
        """

        # Get the top posts from the subreddit
        subreddit = self.reddit.subreddit(subreddit)
        top_posts = subreddit.hot(limit=num_posts)
        stop_words = set(stopwords.words('english'))
        word_freq = {}

        # Remove punctuation and convert to lowercase
        tokenizer = RegexpTokenizer(r'\w+')
        for post in top_posts:
            content = post.title.lower()
            content = tokenizer.tokenize(content)
            content = [word for word in content if word not in stop_words]
            for word in content:
                if word in word_freq:
                    word_freq[word] += 1
                else:
                    word_freq[word] = 1
        
      
        return word_freq

    def word_cloud_generator(self, word_freq, name):
        mask = np.array(Image.open("./world.png"))
        wordcloud = WordCloud(background_color="white", mask=mask, max_words=100, max_font_size=40, random_state=42, width=mask.shape[1], height=mask.shape[0]).generate_from_frequencies(word_freq)
        wc = plt.imshow(wordcloud, interpolation='bilinear')
        # save the image of the word cloud
        plt.axis("off")
        plt.savefig(name)
        plt.show()
        
        wordcloud.to_file(name + ".png")

    def positiveWordFreq(self, subreddit="amitheasshole", num_posts=10):

        # Get the top posts from the subreddit
        subreddit = self.reddit.subreddit(subreddit)
        top_posts = subreddit.hot(limit=num_posts)
        stop_words = set(stopwords.words('english'))

        # Remove punctuation and convert to lowercase
        tokenizer = RegexpTokenizer(r'\w+')
        # Print the title, content and url of each post if its not stickied
        positiveWordsFreq = {}
        
        for post in top_posts:

            if self.sia.polarity_scores(post.title)['compound'] > 0:

                content = post.title.lower()
                content = tokenizer.tokenize(content)
                content = [word for word in content if word not in stop_words]
                
                for word in content:
                        if word in positiveWordsFreq:
                            positiveWordsFreq[word] += 1
                        else:
                            positiveWordsFreq[word] = 1

        
        sorted_d = dict( sorted(positiveWordsFreq.items(), key=operator.itemgetter(1),reverse=True))
        
        return sorted_d

    def negativeWordFreq(self, subreddit="amitheasshole", num_posts=10):

        # Get the top posts from the subreddit
        subreddit = self.reddit.subreddit(subreddit)
        top_posts = subreddit.hot(limit=num_posts)
        stop_words = set(stopwords.words('english'))

        # Remove punctuation and convert to lowercase
        tokenizer = RegexpTokenizer(r'\w+')
        # Print the title, content and url of each post if its not stickied
        negativeWordsFreq = {}
        
        for post in top_posts:

            if self.sia.polarity_scores(post.title)['compound'] < 0:

                content = post.title.lower()
                content = tokenizer.tokenize(content)
                content = [word for word in content if word not in stop_words]
                
                for word in content:
                        if word in negativeWordsFreq:
                            negativeWordsFreq[word] += 1
                        else:
                            negativeWordsFreq[word] = 1

        
        sorted_d = dict( sorted(negativeWordsFreq.items(), key=operator.itemgetter(1),reverse=True))
        
        return sorted_d

    def graph_Barplot(self, name, listgraph, titleGraph, yAxis="", xAxis=""):
        
            plt.title(titleGraph)
            plt.xlabel(xAxis)
            plt.ylabel(yAxis)
          
            plt.bar(list(listgraph.keys())[:10], list(listgraph.values())[:10])
           
            plt.savefig(name + '.png')
            
            # plt.show()
        