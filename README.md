# 📡 Radar | AI News Analysis

Media today is noisy and often polarized. **Radar** is an AI-powered analytical tool designed to cut through that noise. By simply pasting the URL of a news article, this application fetches the text, generates a concise summary, evaluates the emotional sentiment, and measures underlying political bias using advanced Natural Language Processing (NLP). 

Built as a mainstream Python application, this project explores how machine learning can be practically implemented to make information consumption more transparent.

## ✨ Key Features

* **📰 Smart Article Extraction:** Uses `newspaper3k` to bypass basic blockers and cleanly scrape article text, titles, and authors directly from the web.
* **🧠 Advanced Summarization:** Condenses lengthy articles into easily digestible summaries using the Hugging Face `facebook/bart-large-cnn` transformer model.
* **🎭 Sentiment Analysis:** Evaluates the emotional tone (Positive, Negative, Neutral) of the news piece using a fine-tuned DistilBERT model.
* **⚖️ Context-Aware Bias Detection:** Goes beyond simple keyword matching. The app calculates semantic similarity using SpaCy word embeddings (`en_core_web_md`), mapping the article's language against core ideological concepts (Left vs. Right) to detect subtle political leanings.
* **📊 Interactive Dashboard:** A sleek, dark-themed UI built with Streamlit, featuring custom Plotly visualizations (gauge charts and stacked bars) for intuitive data interpretation.

## 🛠️ Tech Stack & Architecture

* **Frontend:** Streamlit (Custom CSS for a polished UI)
* **NLP & ML Pipelines:** Hugging Face `transformers`, PyTorch (`torch`)
* **Embeddings & Vector Math:** SpaCy, NumPy
* **Data Visualization:** Plotly Graph Objects, Pandas
* **Web Scraping:** Newspaper3k, lxml

## 🔬 Under the Hood: How the Bias Engine Works

Instead of relying on a fragile list of "biased words," the analyzer uses a vector-based approach:
1. It establishes "seed words" for distinct political philosophies (e.g., *equality, collective, welfare* vs. *liberty, individual, market*).
2. It generates average "ideology vectors" using pre-trained word embeddings.
3. It parses the target article, filters out stop-words, and isolates contextually relevant nouns, adjectives, and verbs.
4. Using **Cosine Similarity**, it measures how closely the article's vocabulary aligns with the spatial vectors of those core ideologies, returning a percentage-based lean score.

## 🚀 Installation & Setup

To run this project locally, follow these steps:

**1. Clone the repository**
```bash
git clone [https://github.com/yourusername/news_bias_radar.git](https://github.com/yourusername/news_bias_radar.git)
cd news_bias_radar
