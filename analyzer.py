import torch
import streamlit as st
from transformers import pipeline
import re
import spacy
import numpy as np
import nltk

from newspaper import Article, Config
from newspaper.article import ArticleException

# This must happen before any newspaper3k functions are called
try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab')
    nltk.download('punkt')


    



@st.cache_resource
def load_summarizer():
    """Loads the summarization model once and caches it."""
    # We explicitly provide the model name to ensure the task is recognized
    return pipeline(
        "summarization", 
        model="facebook/bart-large-cnn",
        framework="pt" # Forces it to use PyTorch
    )

@st.cache_resource
def load_sentiment_analyzer():
    """Loads the sentiment analysis model once and caches it."""
    print("--- Loading Sentiment Model (first time only) ---")
    return pipeline("sentiment-analysis", model="distilbert/distilbert-base-uncased-finetuned-sst-2-english")

@st.cache_resource
def load_spacy_model():
    """Loads the pre-installed spaCy model."""
    # Do NOT try to download here; it causes permission errors
    return spacy.load("en_core_web_md")

# --- ANALYSIS FUNCTIONS ---

def summarize_text(text_to_summarize):
    """
    Summarizes text using the pre-loaded, cached model.
    """
    summarizer = load_summarizer()
    max_chunk_length = 1500
    summary_list = summarizer(
        text_to_summarize[:max_chunk_length], 
        max_length=150, 
        min_length=50, 
        do_sample=False
    )
    return summary_list[0]['summary_text']

def analyze_sentiment(text_to_analyze):
    """
    Analyzes sentiment using the pre-loaded, cached model.
    """
    sentiment_analyzer = load_sentiment_analyzer()
    result = sentiment_analyzer(text_to_analyze[:512])
    return result[0]

def analyze_bias_advanced(text_to_analyze):
    """
    Analyzes political bias using word embeddings and cosine similarity.
    This is a more accurate and context-aware method.
    """
    print("Analyzing for bias with advanced embedding model...")
    nlp = load_spacy_model()

    # Define core "seed" concepts for each ideology.
    # We choose words that are central to each political philosophy.
    left_seed_words = ['equality', 'collective', 'social', 'welfare', 'regulation', 'justice']
    right_seed_words = ['liberty', 'individual', 'market', 'freedom', 'tradition', 'capitalism']

    # Get the vector representations for our seed words
    left_vectors = [nlp(word).vector for word in left_seed_words if nlp.vocab.has_vector(word)]
    right_vectors = [nlp(word).vector for word in right_seed_words if nlp.vocab.has_vector(word)]

    # Create an average "ideology vector" for each side
    left_ideology_vector = np.mean(left_vectors, axis=0)
    right_ideology_vector = np.mean(right_vectors, axis=0)

    # Process the article text
    doc = nlp(text_to_analyze)
    
    # We only consider relevant words (nouns, adjectives, verbs)
    relevant_words = [token for token in doc if token.pos_ in ['NOUN', 'ADJ', 'VERB'] and token.has_vector and not token.is_stop]
    
    if not relevant_words:
        return {'left_leaning_score': 0, 'right_leaning_score': 0}

    left_similarity_scores = []
    right_similarity_scores = []

    for token in relevant_words:
        # Cosine similarity function
        def cosine_similarity(vec1, vec2):
            return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

        # Calculate how similar each word is to the core ideologies
        left_sim = cosine_similarity(token.vector, left_ideology_vector)
        right_sim = cosine_similarity(token.vector, right_ideology_vector)
        
        # We check which ideology the word is more similar to
        if left_sim > right_sim:
            left_similarity_scores.append(left_sim)
        else:
            right_similarity_scores.append(right_sim)

    # The final score is the average similarity to each ideology
    # This gives a measure of how much the text "leans" one way or the other
    final_left_score = np.mean(left_similarity_scores) if left_similarity_scores else 0
    final_right_score = np.mean(right_similarity_scores) if right_similarity_scores else 0
    
    print("Bias analysis complete.")
    # We return these as percentages for easier interpretation
    return {'left_leaning_score': final_left_score * 100, 'right_leaning_score': final_right_score * 100}