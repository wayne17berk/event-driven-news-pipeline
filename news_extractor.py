import re
import time
from dataclasses import dataclass
from typing import List

@dataclass
class NewsEvent:
    text: str
    entities: List[str]
    sentiment: float
    timestamp: float

class NewsSignalExtractor:
    def __init__(self):
        self.entity_patterns = {
            'PERSON': r'\b[A-Z][a-z]+ [A-Z][a-z]+\b',
            'ORG': r'\b(?:Congress|Senate|House|Fed|Treasury)\b'
        }

    def extract_entities(self, text: str) -> List[str]:
        """Simple NER using regex patterns"""
        entities = []
        for entity_type, pattern in self.entity_patterns.items():
            matches = re.findall(pattern, text)
            entities.extend(matches)
        return entities

    def calculate_sentiment(self, text: str) -> float:
        """Basic sentiment scoring"""
        positive = ['approve', 'pass', 'win', 'gain', 'rise']
        negative = ['reject', 'fail', 'lose', 'drop', 'fall']

        score = 0
        words = text.lower().split()
        for word in words:
            if word in positive:
                score += 1
            elif word in negative:
                score -= 1

        return max(-1, min(1, score / max(len(words), 1) * 10))

    def process_news(self, text: str) -> NewsEvent:
        """Extract structured signals from news text"""
        start = time.time()
        entities = self.extract_entities(text)
        sentiment = self.calculate_sentiment(text)
        latency = time.time() - start

        return NewsEvent(text, entities, sentiment, latency)

    def generate_probability_update(self, event: NewsEvent, base_prob: float) -> float:
        """Update market probability based on news signal"""
        adjustment = event.sentiment * 0.05
        return max(0.01, min(0.99, base_prob + adjustment))

if __name__ == "__main__":
    extractor = NewsSignalExtractor()

    news = "Congress votes to approve new legislation"
    event = extractor.process_news(news)

    print(f"Entities: {event.entities}")
    print(f"Sentiment: {event.sentiment:.2f}")
    print(f"Processing time: {event.timestamp*1000:.1f}ms")

    new_prob = extractor.generate_probability_update(event, base_prob=0.50)
    print(f"Probability update: 0.50 -> {new_prob:.2f}")
