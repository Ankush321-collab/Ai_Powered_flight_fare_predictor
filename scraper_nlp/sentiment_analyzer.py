from textblob import TextBlob

# Simple sentiment: polarity -> [negative, neutral, positive]

def analyze_sentiment(text):
    tb = TextBlob(text)
    polarity = tb.sentiment.polarity  # -1..1
    if polarity > 0.1:
        sentiment = 'positive'
    elif polarity < -0.1:
        sentiment = 'negative'
    else:
        sentiment = 'neutral'
    score = (polarity + 1) / 2  # convert to 0..1
    return { 'sentiment': sentiment, 'score': round(score, 3) }

if __name__ == '__main__':
    print(analyze_sentiment('Crew was polite but seats uncomfortable.'))
