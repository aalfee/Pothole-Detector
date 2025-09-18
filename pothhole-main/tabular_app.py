#!/usr/bin/env python3
"""
Simple tabular training script inspired by the original app.py.

It loads listing data (CSV or JSON lines) containing fields like:
  _id, name, accommodates, room_type, pricePerNight, host_name, host_email

The script trains a RandomForestRegressor to predict `pricePerNight` from the other
features, saves the trained model as `listing_model.joblib`, and writes a simple
plot `training_results.png` showing predicted vs actual prices and feature importances.

Usage examples:
  python tabular_app.py --data listings.csv --dry-run
  python tabular_app.py --data listings.jsonl
"""
import argparse
import logging
import os
import sys

import matplotlib.pyplot as plt
import pickle
import numpy as np
import pandas as pd

# We'll use a simple closed-form ridge regression (no sklearn) to avoid heavy deps
from typing import Tuple


def load_data(path: str) -> pd.DataFrame:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Data file {path} does not exist")

    # support csv and jsonl
    if path.endswith('.csv'):
        df = pd.read_csv(path)
    else:
        # try json lines or json
        try:
            df = pd.read_json(path, lines=True)
        except ValueError:
            df = pd.read_json(path)
    return df


def prepare_features(df: pd.DataFrame):
    # Keep a small set of useful columns and do minimal cleaning
    df = df.copy()

    # Standardize column names
    df.columns = [c.strip() for c in df.columns]

    # Ensure numeric target
    if 'pricePerNight' not in df.columns:
        raise KeyError('pricePerNight column is required')
    df = df.dropna(subset=['pricePerNight'])
    df['pricePerNight'] = pd.to_numeric(df['pricePerNight'], errors='coerce')
    df = df.dropna(subset=['pricePerNight'])

    # Basic numeric features
    numeric_cols = ['accommodates']
    for c in numeric_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)
        else:
            df[c] = 0

    # Text-derived features from `name`
    if 'name' in df.columns:
        df['name_len'] = df['name'].astype(str).apply(len)
        df['name_word_count'] = df['name'].astype(str).apply(lambda s: len(s.split()))
        # presence of some helpful keywords
        keywords = ['charm', 'cozy', 'lux', 'modern', 'spacious']
        for kw in keywords:
            df[f'name_kw_{kw}'] = df['name'].astype(str).str.lower().str.contains(kw).astype(int)
        numeric_cols += ['name_len', 'name_word_count'] + [f'name_kw_{kw}' for kw in keywords]

        # --- TF-IDF features (lightweight, no sklearn) ---
        # tokenize names and compute document frequency
        import re
        token_re = re.compile(r"\b[\w']{2,}\b")
        docs = df['name'].astype(str).str.lower().tolist()
        token_lists = [token_re.findall(d) for d in docs]
        # simple stoplist
        stopwords = set(['the', 'and', 'a', 'an', 'of', 'in', 'on', 'to', 'for'])
        token_lists = [[t for t in toks if t not in stopwords] for toks in token_lists]

        # compute document frequency
        from collections import Counter, defaultdict
        df_counts = Counter()
        for toks in token_lists:
            df_counts.update(set(toks))

        # choose top_k tokens by document frequency
        top_k = 20
        top_tokens = [t for t, _ in df_counts.most_common(top_k)]

        # compute idf
        N = max(1, len(token_lists))
        idf = {t: np.log((N + 1) / (1 + df_counts.get(t, 0))) + 1.0 for t in top_tokens}

        # compute tf-idf per document for top tokens
        tfidf_matrix = np.zeros((N, len(top_tokens)), dtype=float)
        for i, toks in enumerate(token_lists):
            if len(toks) == 0:
                continue
            counts = Counter(toks)
            L = sum(counts.values())
            for j, t in enumerate(top_tokens):
                tf = counts.get(t, 0) / L
                tfidf_matrix[i, j] = tf * idf.get(t, 0.0)

        # add TF-IDF columns to df and numeric_cols
        for j, t in enumerate(top_tokens):
            col = f'tfidf_name_{t}'
            df[col] = tfidf_matrix[:, j]
            numeric_cols.append(col)

    # Categorical features to one-hot (limit unique values to avoid explosion)
    cat_cols = []
    if 'room_type' in df.columns:
        cat_cols.append('room_type')
    if 'host_name' in df.columns:
        # host_name can be high-cardinality; keep top 10 hosts and mark the rest as OTHER
        top_hosts = df['host_name'].value_counts().nlargest(10).index.tolist()
        df['host_name_reduced'] = df['host_name'].where(df['host_name'].isin(top_hosts), 'OTHER')
        cat_cols.append('host_name_reduced')

    # Extract domain from host_email and reduce to top domains
    if 'host_email' in df.columns:
        def extract_domain(e):
            try:
                return str(e).split('@')[-1].lower()
            except Exception:
                return 'unknown'
        df['host_domain'] = df['host_email'].apply(extract_domain)
        top_domains = df['host_domain'].value_counts().nlargest(10).index.tolist()
        df['host_domain_reduced'] = df['host_domain'].where(df['host_domain'].isin(top_domains), 'other')
        cat_cols.append('host_domain_reduced')

    # Text fields like name, host_email are ignored for now

    X_num = df[numeric_cols].values

    if cat_cols:
        # use pandas get_dummies for one-hot encoding (keeps it simple)
        df_cat = pd.get_dummies(df[cat_cols].astype(str), prefix=cat_cols)
        feature_names = numeric_cols + df_cat.columns.tolist()
        X_cat = df_cat.values
        X = np.hstack([X_num, X_cat])
        return X, df['pricePerNight'].values, feature_names
    else:
        feature_names = numeric_cols
        return X_num, df['pricePerNight'].values, feature_names


def main():
    parser = argparse.ArgumentParser(description='Train a simple model on listing data')
    parser.add_argument('--data', required=True, help='Path to CSV or JSONL data file')
    parser.add_argument('--dry-run', action='store_true', help='Quick smoke test on a small slice')
    parser.add_argument('--no-save', action='store_true', help="Don't save model/plots")
    parser.add_argument('--quiet', action='store_true', help='Reduce logging')
    args = parser.parse_args()

    logging.basicConfig(level=(logging.ERROR if args.quiet else logging.INFO), format='%(asctime)s %(levelname)s: %(message)s')
    log = logging.getLogger(__name__)

    try:
        df = load_data(args.data)
    except Exception as e:
        log.error(f'Failed to load data: {e}')
        sys.exit(1)

    if df.shape[0] == 0:
        log.error('Loaded dataset is empty')
        sys.exit(1)

    X, y, feature_names = prepare_features(df)

    test_size = 0.2
    if args.dry_run:
        # use a very small sample for fast smoke test
        n = min(200, X.shape[0])
        X = X[:n]
        y = y[:n]
        test_size = 0.2

    # simple train/test split
    rng = np.random.default_rng(42)
    idx = np.arange(X.shape[0])
    rng.shuffle(idx)
    split = int((1 - test_size) * X.shape[0])
    train_idx, test_idx = idx[:split], idx[split:]
    X_train, X_test = X[train_idx], X[test_idx]
    y_train, y_test = y[train_idx], y[test_idx]

    # Ridge regression closed-form solution: w = (X^T X + alpha I)^-1 X^T y
    alpha = 1.0
    log.info('Training ridge regression model...')
    # add bias term
    X_train_aug = np.hstack([np.ones((X_train.shape[0], 1)), X_train])
    X_test_aug = np.hstack([np.ones((X_test.shape[0], 1)), X_test])
    D = X_train_aug.shape[1]
    A = X_train_aug.T @ X_train_aug + alpha * np.eye(D)
    w = np.linalg.solve(A, X_train_aug.T @ y_train)

    y_pred = X_test_aug @ w
    mse = float(np.mean((y_test - y_pred) ** 2))
    # R2 score
    ss_res = np.sum((y_test - y_pred) ** 2)
    ss_tot = np.sum((y_test - np.mean(y_test)) ** 2)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0.0
    log.info(f'Test MSE: {mse:.3f}, R2: {r2:.3f}')

    if not args.no_save:
        try:
            with open('listing_model.pkl', 'wb') as f:
                pickle.dump({'weights': w, 'feature_names': ['bias'] + feature_names}, f)
            log.info('Saved model to listing_model.pkl')
        except Exception as e:
            log.warning(f'Failed to save model: {e}')

    # Plot predicted vs actual and feature importances
    try:
        plt.figure(figsize=(12, 5))

        plt.subplot(1, 2, 1)
        plt.scatter(y_test, y_pred, alpha=0.6)
        plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=2)
        plt.xlabel('Actual pricePerNight')
        plt.ylabel('Predicted pricePerNight')
        plt.title('Predicted vs Actual')

        plt.subplot(1, 2, 2)
        # compute importances from weights (absolute value, ignore bias)
        weights = w[1:]
        importances = np.abs(weights)
        names = feature_names
        # pick top 10
        k = min(10, len(importances))
        inds = np.argsort(importances)[-k:][::-1]
        plt.barh(range(k), importances[inds][::-1], align='center')
        plt.yticks(range(k), [names[i] for i in inds][::-1])
        plt.title('Top feature importances')

        plt.tight_layout()
        if not args.no_save:
            plt.savefig('training_results.png')
            log.info('Saved training_results.png')
    except Exception as e:
        log.warning(f'Failed to create plots: {e}')


if __name__ == '__main__':
    main()
