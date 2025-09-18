#!/usr/bin/env python3
"""
Load a trained pipeline (joblib) and run predictions on new listings.

Outputs a CSV with original columns plus `predicted_pricePerNight`.
"""
import argparse
import logging
import os
import sys

import joblib
import pandas as pd

# reuse preprocessing helper from the training script
from tabular_pipeline import prepare_basic


def load_data(path: str):
    if path.endswith('.csv'):
        return pd.read_csv(path)
    else:
        return pd.read_json(path, lines=True)


def main():
    parser = argparse.ArgumentParser(description='Predict listings from a trained pipeline')
    parser.add_argument('--model', required=True, help='Path to joblib pipeline (listing_pipeline.joblib)')
    parser.add_argument('--input', required=True, help='CSV or JSONL with listings')
    parser.add_argument('--out', default='preds.csv', help='Output CSV path')
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

    if not os.path.exists(args.model):
        logging.error('Model not found: %s', args.model)
        sys.exit(1)

    model = joblib.load(args.model)
    df = load_data(args.input)

    # Preprocess similarly to the training pipeline so expected columns exist
    df_prepared = prepare_basic(df)

    # The model pipeline was trained to accept the prepared dataframe
    preds = model.predict(df_prepared)
    df_out = df.copy()
    df_out['predicted_pricePerNight'] = preds
    df_out.to_csv(args.out, index=False)
    logging.info('Wrote predictions to %s', args.out)


if __name__ == '__main__':
    main()
