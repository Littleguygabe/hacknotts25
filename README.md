**Hi, this is the HackNotts '25 git repo for our team's submission**



## Initial Ideas

### Ai Sentiment Analysis
Phase 1: Setup & Data Collection (Hours 1-6)
Your goal is to get a steady stream of text data to analyze. Don't try to boil the ocean; pick one data source and get it working reliably.

Environment Setup:

Set up a Python virtual environment.

Install your key libraries:

Data Collection: requests, beautifulsoup4 (for scraping) OR tweepy (for X/Twitter) OR praw (for Reddit) OR newsapi-python (for a news API).

Data Handling: pandas.

AI/NLP: vaderSentiment OR textblob.

Visualization: streamlit.

Choose ONE Data Source:

Option 1: News Headlines (Recommended)

Use a free API like NewsAPI. Get a free developer key.

Write a script to fetch all headlines containing keywords like "stocks," "market," "NASDAQ," or specific tickers (e.g., "AAPL," "TSLA").

Option 2: Reddit

Use the praw library. Get API keys from your Reddit account.

Track new posts or comments in subreddits like r/wallstreetbets, r/investing, or r/stocks.

Option 3: X (Twitter) (Harder)

Getting API access can be slow. If you don't already have it, this might not be feasible for a hackathon.

Collect and Store Data:

Write a function that fetches the data (e.g., the top 100 news headlines from the last hour).

Extract the key information: the text (headline/post body) and the timestamp.

Store this data in a pandas DataFrame. At this stage, you can just save it to a CSV file (data.csv) that your app will read.

Phase 2: AI Sentiment Analysis (Hours 7-12)
This is the "AI" core of your project. Don't train a model from scratch. Use a powerful, pre-trained library.

Choose Your Analyzer (Pick One):

VADER (Recommended): vaderSentiment. It's lightweight, requires no API keys, and is specifically tuned for social media and short text, making it great for headlines.

TextBlob: textblob. Also very simple and lightweight. A great alternative to VADER.

Process Your Data:

Load your data.csv into a pandas DataFrame.

Initialize the VADER sentiment analyzer.

Create a new column in your DataFrame called sentiment_score.

Loop through each row (each headline) and run the analyzer on the text.

From the VADER results, grab the compound score. This is a single, normalized score from -1.0 (very negative) to +1.0 (very positive). Store this score in your sentiment_score column.

Phase 3: Quantification & Aggregation (Hours 13-16)
Now you turn thousands of individual scores into a single, trackable "market sentiment" metric.

Ensure Timestamps are Correct: Make sure your DataFrame's timestamp column is in the proper datetime format. This is crucial for plotting.

Aggregate the Data: You don't want to plot 10,000 individual dots. You want a time-series line.

Use the pandas.resample() function.

Resample your data by a time "bucket" (e.g., "H" for hourly or "D" for daily).

Calculate the mean (average) of the sentiment_score for each bucket.

This gives you a new, smaller DataFrame: timestamp | average_sentiment_score. This is your final metric!

Phase 4: Visualization (Hours 17-24)
This is what you'll present to the judges. Make it interactive and clear.

Use Streamlit: This is the fastest way to build a web app in Python. Don't mess with Flask/Django/HTML/CSS.

Create Your App (app.py):

Import streamlit as st and pandas as pd.

Add a title: st.title("Live Market Sentiment Analyzer").

Load your final aggregated data (the resampled DataFrame).

Add a line chart: st.line_chart(your_aggregated_dataframe). This one line creates a beautiful, interactive chart.

Bonus: Add a checkbox (st.checkbox) to "Show Raw Data" and display the original headlines DataFrame using st.dataframe(your_raw_data_df).

Bonus: Add a "word cloud" of the most common terms in your headlines.

To Run: In your terminal, just type streamlit run app.py and your interactive dashboard will open in your browser.

Hackathon Pro-Tips:
Version Control: Use Git from hour 1. Commit after every small victory. It will save you.

Work in Parallel: If you have a team:

Person 1: Works on Data Collection (Phase 1).

Person 2: Works on the Streamlit dashboard with dummy data (Phase 4).

Together: You meet in the middle to do Phase 2 & 3, plugging the real data into the finished dashboard.

Presentation: Focus your demo on the final dashboard. Show how the sentiment score line reacts to major news (e.g., a big drop after a "market crash" headline).

Good luck, this is a very achievable and impressive project!