import pandas as pd
import numpy as np
from textblob import TextBlob
import textblob
import nltk


# Assuming your CSV file is named 'sample_exam.csv' and located in the same directory as this script
csv_file_path = 'sample_exam.csv'

# Read the CSV file, assuming the first line provided is a header that's incorrectly placed
df = pd.read_csv(csv_file_path, skiprows=1, header=None)
df.columns = ['Student', 'Feedback', 'Positivity_Level']

# Basic cleaning with NumPy: Remove missing values
df.replace("", np.nan, inplace=True)
df.dropna(inplace=True)

# Ensure strings are uniform (example: stripping extra spaces, converting to lowercase)
df['Student'] = df['Student'].str.strip().str.lower()
df['Feedback'] = df['Feedback'].str.strip().str.lower()
df['Positivity_Level'] = df['Positivity_Level'].str.strip().str.lower()

# Function to get sentiment polarity
def get_sentiment_polarity(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity

# Applying TextBlob sentiment analysis to the 'Feedback' column
df['Sentiment_Polarity'] = df['Feedback'].apply(get_sentiment_polarity)
negative_words = [
    "disappointing",
    "struggled",
    "avoidable",
    "mistakes",
    "below",
    "expectations",
    "need",
    "improvement",
    "areas",
    "improve",
    "fell",
    "short",
    "crucial",
    "disappointing",
    "indicate",
    "satisfactory",
    "average",
    "decent",
    "satisfactory",
    "average",
    "below",
    "expectations"
]

positive_words = [
    "Great",
    "clearly",
    "understood",
    "excellent",
    "excelled",
    "thorough",
    "well-reasoned",
    "deep",
    "outstanding",
    "solid",
    "keep",
    "good",
    "work",
    "strive",
    "excellence",
    "excellent",
    "strong",
    "effectively",
    "well-structured",
    "clear",
    "comprehensive",
    "insightful",
    "exceptional",
    "analytical",
    "concise",
    "exemplary",
    "thorough",
    "detailed",
    "commendable",
    "impressive",
    "outstanding"
]
# You can still count positive and negative words if you want to compare or supplement the analysis
# Counting positive and negative sentiment words
df['Positive_Count'] = df['Feedback'].apply(lambda text: sum(text.count(word) for word in positive_words))
df['Negative_Count'] = df['Feedback'].apply(lambda text: sum(text.count(word) for word in negative_words))

# Print the DataFrame with sentiment polarity and word counts
print(df[['Student', 'Sentiment_Polarity', 'Positive_Count', 'Negative_Count']])
