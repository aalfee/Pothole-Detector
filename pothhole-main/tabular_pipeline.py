#!/usr/bin/env python3
"""
Train a tabular pipeline using scikit-learn: TF-IDF on `name`, one-hot on domains/room_type,
and a RandomForestRegressor. Performs cross-validation and saves the best estimator.

This script requires scikit-learn and joblib. See `requirements-tabular.txt`.
"""
import argparse
import logging
import os
import sys

import joblib
import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import GridSearchCV, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def prepare_basic(df: pd.DataFrame) -> pd.DataFrame:
    # minimal cleaning and derived columns used by the pipeline
    df = df.copy()
    df.columns = [c.strip() for c in df.columns]
    df['pricePerNight'] = pd.to_numeric(df['pricePerNight'], errors='coerce')
    df = df.dropna(subset=['pricePerNight'])

    # numeric
    df['accommodates'] = pd.to_numeric(df.get('accommodates', 0), errors='coerce').fillna(0)

    # name-derived
    df['name'] = df.get('name', '').astype(str)
    df['name_len'] = df['name'].str.len()
    df['name_word_count'] = df['name'].str.split().apply(len)
    keywords = ['charm', 'cozy', 'lux', 'modern', 'spacious']
    for kw in keywords:
        df[f'name_kw_{kw}'] = df['name'].str.lower().str.contains(kw).astype(int)

    # host domain
    if 'host_email' in df.columns:
        df['host_domain'] = df['host_email'].astype(str).str.split('@').str[-1].str.lower().fillna('')
        top = df['host_domain'].value_counts().nlargest(20).index.tolist()
        df['host_domain_reduced'] = df['host_domain'].where(df['host_domain'].isin(top), 'other')
    else:
        df['host_domain_reduced'] = 'unknown'

    # room_type
    df['room_type'] = df.get('room_type', '').astype(str)

    return df


def build_and_train(df: pd.DataFrame, out_path: str, cv: int = 5):
    df = prepare_basic(df)
    y = df['pricePerNight'].values

    # Column groups
    text_col = 'name'
    numeric_cols = ['accommodates', 'name_len', 'name_word_count'] + [c for c in df.columns if c.startswith('name_kw_')]
    cat_cols = ['room_type', 'host_domain_reduced']

    # Preprocessing
    text_transform = Pipeline([
        ('tfidf', TfidfVectorizer(max_features=200, ngram_range=(1,2)))
    ])

    num_transform = Pipeline([
        ('imputer', SimpleImputer(strategy='constant', fill_value=0)),
        ('scaler', StandardScaler())
    ])

    cat_transform = Pipeline([
        ('imputer', SimpleImputer(strategy='constant', fill_value='')), 
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse=False))
    ])

    preprocessor = ColumnTransformer([
        ('text', text_transform, text_col),
        ('num', num_transform, numeric_cols),
        ('cat', cat_transform, cat_cols),
    ], remainder='drop')

    pipeline = Pipeline([
        ('pre', preprocessor),
        ('model', RandomForestRegressor(random_state=42))
    ])

    # Quick grid for n_estimators
    param_grid = {
        'model__n_estimators': [50, 100],
        'model__max_depth': [None, 10]
    }

    logging.info('Starting GridSearchCV...')
    gs = GridSearchCV(pipeline, param_grid, cv=cv, n_jobs=-1, scoring='neg_mean_squared_error')
    gs.fit(df, y)

    logging.info(f'Best params: {gs.best_params_}')
    logging.info(f'Best CV score (neg MSE): {gs.best_score_}')

    # Save model
    joblib.dump(gs.best_estimator_, out_path)
    logging.info(f'Saved trained pipeline to {out_path}')


def main():
    parser = argparse.ArgumentParser(description='Train tabular pipeline with sklearn')
    parser.add_argument('--data', required=True, help='CSV or JSONL data file')
    parser.add_argument('--out', default='listing_pipeline.joblib', help='Output model path')
    parser.add_argument('--cv', type=int, default=5, help='Cross-validation folds')
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

    if not os.path.exists(args.data):
        logging.error('Data file does not exist: %s', args.data)
        sys.exit(1)

    # load
    if args.data.endswith('.csv'):
        df = pd.read_csv(args.data)
    else:
        df = pd.read_json(args.data, lines=True)

    build_and_train(df, args.out, cv=args.cv)


if __name__ == '__main__':
    main()
