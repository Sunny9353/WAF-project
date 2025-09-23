import pandas as pd
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
import os
import pickle

def load_cleaned_logs(file_path):
    """
    Load cleaned log data from a tab-separated file.
    Columns: ip, method, url, status
    """
    df = pd.read_csv(file_path, sep='\t', header=None, names=['ip', 'method', 'url', 'status'])
    return df

def encode_categoricals(df):
    """
    Encode HTTP method and status code as integer labels.
    Returns encoded DataFrame and fitted encoders.
    """
    method_encoder = LabelEncoder()
    df['method_encoded'] = method_encoder.fit_transform(df['method'])

    df['status'] = df['status'].astype(str)
    status_encoder = LabelEncoder()
    df['status_encoded'] = status_encoder.fit_transform(df['status'])

    return df, method_encoder, status_encoder

def tokenize_urls(df, max_len=10):
    """
    Tokenize URL paths into sequences of integer tokens.
    Padding is added to reach fixed sequence length.
    Returns padded sequences and fitted tokenizer.
    """
    urls = df['url'].str.lstrip('/')  # Remove leading slash

    tokenizer = Tokenizer(oov_token='<OOV>')
    tokenizer.fit_on_texts(urls)

    sequences = tokenizer.texts_to_sequences(urls)
    padded_sequences = pad_sequences(sequences, maxlen=max_len, padding='post')

    return padded_sequences, tokenizer

def prepare_model_inputs(df, url_seq):
    """
    Combine encoded method, status with URL token sequences.
    Returns a tuple of (other_features, url_sequences).
    """
    method_arr = df['method_encoded'].values
    status_arr = df['status_encoded'].values

    other_features = np.stack([method_arr, status_arr], axis=1)

    return other_features, url_seq

def save_artifacts(url_seq, other_features, tokenizer, method_enc, status_enc, save_dir='data/processed'):
    """
    Save processed data arrays and fitted tokenizer and encoders to disk.
    """
    os.makedirs(save_dir, exist_ok=True)

    np.savez_compressed(os.path.join(save_dir, 'tokenized_data.npz'),
                        url_sequences=url_seq,
                        other_features=other_features)

    with open(os.path.join(save_dir, 'url_tokenizer.pkl'), 'wb') as f:
        pickle.dump(tokenizer, f)

    with open(os.path.join(save_dir, 'method_encoder.pkl'), 'wb') as f:
        pickle.dump(method_enc, f)

    with open(os.path.join(save_dir, 'status_encoder.pkl'), 'wb') as f:
        pickle.dump(status_enc, f)

    print("Saved tokenized data, tokenizer, and encoders to disk.")

def load_artifacts(save_dir='data/processed'):
    """
    Load processed data and tokenizer/encoders from disk.
    Returns loaded arrays and objects.
    """
    data = np.load(os.path.join(save_dir, 'tokenized_data.npz'))
    url_sequences = data['url_sequences']
    other_features = data['other_features']

    with open(os.path.join(save_dir, 'url_tokenizer.pkl'), 'rb') as f:
        url_tokenizer = pickle.load(f)

    with open(os.path.join(save_dir, 'method_encoder.pkl'), 'rb') as f:
        method_enc = pickle.load(f)

    with open(os.path.join(save_dir, 'status_encoder.pkl'), 'rb') as f:
        status_enc = pickle.load(f)

    print("Loaded tokenized data, tokenizer, and encoders from disk.")
    return url_sequences, other_features, url_tokenizer, method_enc, status_enc

if __name__ == "__main__":
    input_file = os.path.join('data', 'processed', 'cleaned_logs.txt')

    # Step 1: Load data
    logs_df = load_cleaned_logs(input_file)

    # Step 2: Encode categorical columns
    logs_df, method_enc, status_enc = encode_categoricals(logs_df)

    # Step 3: Tokenize URLs
    url_seq, url_tokenizer = tokenize_urls(logs_df, max_len=10)

    # Step 4: Prepare final inputs for model
    other_features, url_seq = prepare_model_inputs(logs_df, url_seq)

    # Step 5: Save all artifacts to disk
    save_artifacts(url_seq, other_features, url_tokenizer, method_enc, status_enc)

    # Sample output to verify
    print("Sample tokenized URL sequences:")
    print(url_seq[:5])
    print("\nSample encoded method and status features:")
    print(other_features[:5])
