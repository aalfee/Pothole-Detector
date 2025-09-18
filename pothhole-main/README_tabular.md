Tabular pipeline (listings)
===========================

This folder contains a scikit-learn based training pipeline for listing data.

Files
- `tabular_pipeline.py` — trains a pipeline (TF-IDF on `name`, one-hot on domains/room_type, numeric features) and performs cross-validation. Saves the pipeline as a joblib file (default `listing_pipeline.joblib`).
- `predict_listing.py` — helper script to load a trained pipeline and run predictions on new data.
- `requirements-tabular.txt` — minimal requirements for running the pipeline (separate environment recommended to avoid tensorflow/numpy conflicts).

How features are computed
- Numeric: `accommodates`, `name_len` (length of `name`), `name_word_count`.
- Keyword indicators from `name`: `name_kw_charm`, `name_kw_cozy`, `name_kw_lux`, `name_kw_modern`, `name_kw_spacious`.
- TF-IDF: applied to `name` with unigrams and bigrams, limited to `max_features=200`.
- Categorical: `room_type`, `host_domain_reduced` (top domains kept, others labeled `other`) — one-hot encoded.

Setup
1. Create a new virtualenv (recommended) or use your existing one.

   python3 -m venv .venv_tabular
   source .venv_tabular/bin/activate
   pip install -r requirements-tabular.txt

2. Train:

   python tabular_pipeline.py --data listings.csv --out listing_pipeline.joblib --cv 5

3. Predict using `predict_listing.py` (see script help):

   python predict_listing.py --model listing_pipeline.joblib --input new_listings.csv --out preds.csv

Notes
- This pipeline uses scikit-learn and may require a separate environment because your workspace already contains heavy TensorFlow dependencies.
