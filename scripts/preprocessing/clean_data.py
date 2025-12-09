import pandas as pd
import re
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def clean_text(text: str) -> str:
    """Clean text data"""
    if pd.isna(text):
        return ""
    
    # Convert to string
    text = str(text)
    
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    
    # Remove email addresses
    text = re.sub(r'\S+@\S+', '', text)
    
    # Remove HTML tags
    text = re.sub(r'<.*?>', '', text)
    
    # Remove special characters but keep basic punctuation
    text = re.sub(r'[^\w\s.,!?-]', '', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def process_corpus(input_path: str, output_path: str):
    """Process and clean the corpus"""
    logger.info(f"Loading data from {input_path}")
    
    # Load data
    df = pd.read_csv(input_path)
    logger.info(f"Loaded {len(df)} documents")
    
    # Clean text
    logger.info("Cleaning text...")
    df['text'] = df['text'].apply(clean_text)
    
    # Remove empty texts
    df = df[df['text'].str.len() > 0]
    logger.info(f"Remaining documents after cleaning: {len(df)}")
    
    # Add metadata if needed
    if 'doc_id' not in df.columns:
        df['doc_id'] = df.index.astype(str)
    
    # Save processed data
    output_dir = Path(output_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)
    
    df.to_csv(output_path, index=False)
    logger.info(f"✓ Processed data saved to {output_path}")

if __name__ == "__main__":
    input_path = "data/raw/corpus.csv"
    output_path = "data/processed/docs.csv"
    process_corpus(input_path, output_path)
