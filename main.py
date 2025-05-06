import pandas as pd
import re
import nltk
from nltk.corpus import stopwords

# Load your data
train_data = pd.read_csv('data/train.csv')
validation_data = pd.read_csv('data/validation.csv')
test_data = pd.read_csv('data/test.csv')

# Handle missing values in content column
train_data['content'] = train_data['content'].fillna('')  # replace NaN with empty string

# Visualize text length distribution
train_data['text_length'] = train_data['content'].apply(len)  # create new column for length

print(train_data.head())

nltk.download('stopwords')
romanian_stopwords = set(stopwords.words('romanian'))

def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()

    # Remove special characters and numbers
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\d+', '', text)

    # Remove stopwords
    words = text.split()
    filtered_words = [word for word in words if word not in romanian_stopwords]

    return ' '.join(filtered_words)

# Apply preprocessing
train_data['processed_text'] = train_data['content'].apply(preprocess_text)

print(train_data['processed_text'].head())