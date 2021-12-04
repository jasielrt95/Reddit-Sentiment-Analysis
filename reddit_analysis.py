##############################################################################################################
# This program was devoloped by Jasiel Rivera , Michael H. Terrefortes and Eliam Ruiz as the final proyect for
# Data Science class CCOM3031 first semester school year 2021-2022, professor P.Ordoñez UPRRP.
#
# Purpose: This program uses data collected through the Reddit API on a given/specified subreddit. Then the 
# information will be used to determine the given subreddit's sentiment. This is achieved by performing 
# analysis on its data such as word frequency, top posts, and these words are used to determine is a post is 
# 'positive, 'negative' or neutral. Then the results will be presented as charts, graphs and even a png 
# containig the word cloud (most frequent words) of the given subreddit
############################################################################################################## 
# imports necesary for the program to work
from numpy import positive
import praw
import matplotlib.pyplot as plt
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
nltk.download('vader_lexicon')
nltk.download('stopwords')
from wordcloud import WordCloud
import csv

# definition of a class that will contain functions/methods that will allow/facilitate teh analisis of the subreddits
class RedditAnalysis:
    """
    This class has useful methods for analyzing data about subreddits.

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
    subreddit_info(self, subreddit, num_posts=100, title_only=False)
        Returns a list in which each element is a dictionary that contains the all the information obtained from the respective post and post analisis.
    subreddit_sentiment(self, post_info)
        Returns a dictionary that contains the final count of each sentiment present in the post inofrmation 
    subreddit_word_frequency(self, postinfo)
        Returns a dictionary that contains what is essentially a map/histogram that contains the amount of times that each word is repeated in the post 
    top_words_graph(self, word_freq, num_words=10, title="Top Words")
        Displays a graph that shows the top (most repeated) words in the subreddit
    get_positive_posts(self, posts)
        Retuns a list that contains all positive posts in the given/analyzed subreddit (geter function)
    get_negative_posts(self, posts)
        Retuns a list that contains all negative posts in the given/analyzed subreddit (geter function)
    get_neutral_posts(self, posts)
        Retuns a list that contains all neutral posts in the given/analyzed subreddit (geter function)
    get_top_posts(self, posts, num_posts)
        Retuns a list that contains the top posts in the given/analyzed subreddit (geter function)
    subreddit_wordcloud(self, word_freq)
        Displays a workcloud using the most frequent words in the given/analyzed subreddit in which the size of every word corresponds to its level of frequency (bigger:mopre frequent, smaller:less frequent)
    subreddit_sentiment_piechart(self, sentiment_dict, title="Sentiment")
        Displays a piechart that represents how the subreddit sentiment is shared. Fraction of positiveness, negativeness and neutralness that add up to the whole 
    
    

    """

    def __init__(self, file_name="credentials.txt"):
        """
        Constructor funtion for redditanalysis class

        Parameters
        ----------
        file_name : string
            String variable that holds the credentials to the reddit API. Allows the program to retrieve information from reddit

        Returns
        -------
            None.
            """

        # Grab the reddit API credentials from the file
        with open(file_name, 'r') as file:
            self.client_id = file.readline().strip()
            self.client_secret = file.readline().strip()

        # Create the reddit API object
        self.reddit = praw.Reddit(client_id=self.client_id,
                                  client_secret=self.client_secret,
                                  user_agent='reddit_sentiment')

    def subreddit_info(self, subreddit, num_posts=100, title_only=False):
        """
        Funtion that retrieves and organize all the information to be analyzed fromthe given/analyzed subreddit

        Parameters
        ----------
        subreddit : object
            Access to the subrredit info on Reddit
        num_posts : integer
            Variable to set a hard limit/maximum value fo rthe amount of posts to retrieve from the subreddit
        title_only : bool
            Bool variable that does ??
        Returns
        -------
        post_info : list
            A list, organiazed/modularized that contains dictionaries with all the information for every post in the subreddit 

            """

        # Create a sia object
        sia = SentimentIntensityAnalyzer()

        # Get the hot posts from the subreddit
        hot_posts = self.reddit.subreddit(subreddit).top(limit=num_posts)

        # Create a list to hold the posts
        post_info = []

        # tokenizer to remove punctuation
        tokenizer = RegexpTokenizer(r'\w+')

        # saving the sentiment data for CSV file creation
        dictForCSV = []

        for post in hot_posts:

            # Get the post text
            text = post.selftext
            text = text.lower()
            # save the tokenized text 
            text = tokenizer.tokenize(text)
            # remove designated stop words that dont flag semntiment to avoid analizing them (stopwords for english language)
            text = [
                word for word in text if word not in stopwords.words('english')]
            # create full string divided by spaces
            text = ' '.join(text)

            # Get the post title
            title = post.title
            # 
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
                # Adds sentiment data
                dictForCSV.append(sentiment)

            else:
                # Get the post sentiment
                post = title + " " + text
                sentiment = sia.polarity_scores(post)
                # Adds sentiment data
                dictForCSV.append(sentiment)

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

       
        return post_info, dictForCSV

    def subreddit_sentiment(self, post_info):
        """
        Funtion that clasifies the sentiment of each post and stores the information in a dictionary

        Parameters
        ----------
        post_info : list
            A list that contains the posts gatherd information from the subreddit
        Returns
        -------
        dictionary : dictionary
            A dictionary that contains each sentiment and the amount/score earned throughout the post_info

            """
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
        """
        Funtion that counts the amount of times each word is repeated and stores the information in a dictionary

        Parameters
        ----------
        postinfo : list
            A list that contains the posts gatherd information from the subreddit
        Returns
        -------
        word_freq : dictionary
            A dictionary that contaions all the words mapped to the amount of times each respective word was repeated

            """
        exclude = ["r", "https", "com", "www"]
        text = ""
        word_freq = {}
        for post in postinfo:
            text += post['text'] + " "
            text += post['title'] + " "

        text = text.split()
        for word in text:
            if word not in word_freq and word not in exclude and not word.isdigit():
                word_freq[word] = 1
            elif word not in exclude and not word.isdigit():
                word_freq[word] += 1
        
        return word_freq

    def top_words_graph(self, word_freq, num_words=10, title="Top Words"):
        """
        Plot a graph of the top words from the given subreddit.

        Parameters
        ----------
        word_freq : dictionary
            A dictionary that contians each word and the amount of times it appears in the subreddit
        num_words : integer
            A variable to denote the limit/ maximum amount of words to be used in the graph
        title : string
            A string that contains the default graph title 

        Returns
        -------
        None.

        """

        # order the words by frequency
        if len(word_freq) > 0:
            word_freq = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)

            # Create the graph
            plt.title(title)
            plt.xlabel("Word")
            plt.ylabel("Frequency")
            plt.bar(range(num_words), [word_freq[i][1] for i in range(num_words)], color = ("yellow","cyan","red","black","purple","grey","green","orange","maroon","blue"))
            plt.xticks(range(num_words), [word_freq[i][0] for i in range(num_words)])
            plt.show()
        else:
            print("No words to graph")

    def get_positive_posts(self, posts):
        """
        Geter function that retrieves/determines the positive posts in the subreddit and stores them in a list

        Parameters
        ----------
        posts : list
            A list that contains the posts that where a part of the given/analyzed subreddit

        Returns
        -------
        positive_posts : list
            A list all the posts that where classified as positive posts in the subreddit

            """
        positive_posts = []
        for post in posts:
            if post['sentiment'] == 'positive':
                positive_posts.append(post)
        return positive_posts

    def get_negative_posts(self, posts):
        """
        Geter function that retrieves/determines the negative posts in the subreddit and stores them in a list

        Parameters
        ----------
        posts : list
            A list that contains the posts that where a part of the given/analyzed subreddit

        Returns
        -------
        negative_posts : list
            A list all the posts that where classified as negative posts in the subreddit

            """
        negative_posts = []
        for post in posts:
            if post['sentiment'] == 'negative':
                negative_posts.append(post)
        return negative_posts

    def get_neutral_posts(self, posts):
        """
        Geter function that retrieves/determines the neautral posts in the subreddit and stores them in a list

        Parameters
        ----------
        posts : list
            A list that contains the posts that where a part of the given/analyzed subreddit

        Returns
        -------
        neutral_posts : list
            A list all the posts that where classified as neutral posts in the subreddit

            """
        neutral_posts = []
        for post in posts:
            if post['sentiment'] == 'neutral':
                neutral_posts.append(post)
        return neutral_posts

    def get_top_posts(self, posts, num_posts):
        """
        Geter function that retrieves/determines the top posts in the subreddit and stores them in a sorted list

        Parameters
        ----------
        posts : list
            A list that contains the posts that where a part of the given/analyzed subreddit
        num_posts : integer
            Variable to store the amount of posts contained in the posts list

        Returns
        -------
        top_posts : list
            A list all the posts that where classified as top posts in the subreddit

            """
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
            """
            Create and display a workCloud .png for the user to visualize the word frequency in the subreddit.

            Parameters
            ----------
            word_freq : dictionary
                A dictionary that maps each word analyzed in the subreddit to the amount of times it was posted.

            Returns
            -------
            None.

            """
            
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

    def makeCSVFile(self, dictCSV, name = "data"):

        """
        Creates a CSV file with the reddit sentiment analysis.

        Parameters
        ----------
        dictCSV : dictionary
            A list of dictionaries containing the sentimental data from each reddit post: neg, neu, pos, compound.
        name: string
            A string to name the CSV file with default name as "data"

        Returns
        -------
        None.

        """

        # For the title of each column
        title = ["neg", "neu", "pos", "compound"]

        # Creates CSV file with specific name
        with open(name + '.csv', 'w') as csvfile:
            # Writes the header of each column
            writer = csv.DictWriter(csvfile, fieldnames = title)
            writer.writeheader()
            # Writes in each row the sentimental data of post
            writer.writerows(dictCSV)




