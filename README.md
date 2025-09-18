Below is a neat, ready-to-merge README section describing the tabular/listings workflow, how it works, how to run it, and examples for loading models and running predictions. Copy the whole markdown into your repo README where appropriate.

## Tabular (Listings) workflow

This section documents the tabular training and prediction tools added to the project. Two parallel approaches are provided:

- Lightweight baseline (fast, few deps): tabular_app.py — pure pandas + NumPy, internal TF‑IDF, closed‑form ridge regression. Good for smoke tests and small environments.
- Full scikit‑learn pipeline: `tabular_pipeline.py` + `predict_listing.py` — TF‑IDF using `TfidfVectorizer`, full preprocessing in a `Pipeline`, GridSearchCV, and RandomForestRegressor. Recommended for actual experiments; run in a separate venv to avoid dependency conflicts with TensorFlow.

---

## Files

- tabular_app.py  
  Lightweight pipeline: preprocessing (numeric, keyword indicators, internal TF‑IDF), closed‑form ridge regression, saves listing_model.pkl, saves training_results.png.

- `pothhole-main/tabular_pipeline.py`  
  scikit‑learn `Pipeline` with `TfidfVectorizer`, numeric preprocessing, `OneHotEncoder`, `RandomForestRegressor`, GridSearchCV; saves best pipeline to `listing_pipeline.joblib`.

- `pothhole-main/predict_listing.py`  
  Loads a trained scikit-learn pipeline (`.joblib`), applies the same preprocessing helper, and writes a CSV with `predicted_pricePerNight`.

- `pothhole-main/requirements-tabular.txt`  
  Requirements for scikit-learn pipeline (scikit-learn, joblib, pandas). Use in a separate venv.

- requirements.txt  
  Main project dependencies (TensorFlow etc.); keep separate from tabular requirements.

- `pothhole-main/README_tabular.md`  
  Short documentation and recommended setup for the tabular pipeline.

---

## What the code computes (features)

Both approaches compute a similar set of features (sklearn pipeline does it inside the pipeline; tabular_app.py does it in-place):

Numeric / derived
- `accommodates` — numeric
- `name_len` — length of `name` (characters)
- `name_word_count` — word count of `name`
- Keyword booleans for `name`: `name_kw_charm`, `name_kw_cozy`, `name_kw_lux`, `name_kw_modern`, `name_kw_spacious`
- TF‑IDF for `name`:
  - tabular_app.py: lightweight internal TF‑IDF limited to top-k tokens (top_k=20)
  - `tabular_pipeline.py`: scikit‑learn `TfidfVectorizer(max_features=200, ngram_range=(1,2))`

Categorical
- `room_type` — one-hot encoded
- `host_domain_reduced` — domain extracted from `host_email`, reduced to top domains and `'other'`, one-hot encoded

Target
- `pricePerNight` — numeric (required for training)

---

## Model persistence formats

- listing_model.pkl — (lightweight) pickle containing a dict with `weights` and `feature_names`. Predict by constructing feature vector + dot product with `weights`.
- `listing_pipeline.joblib` — (sklearn) complete `Pipeline` saved with `joblib.dump`. Includes preprocessing and estimator; call `pipeline.predict(df)` on the prepared DataFrame.

---

## Setup and recommended envs

Important: TensorFlow and scikit‑learn have different numpy version requirements. Use separate virtualenvs for image/TensorFlow work and for scikit‑learn tabular work.

1) Lightweight path (no new venv required; uses existing environment):
- Install minimal deps (if needed): your main requirements.txt already contains numpy and pandas.
- Train:
  ```bash
  python pothhole-main/tabular_app.py --data pothhole-main/listings.csv
  ```
  This creates listing_model.pkl and training_results.png.

2) scikit-learn pipeline (recommended for experiments — use separate venv)
- Create a separate venv and install `requirements-tabular.txt`:
  ```bash
  python3 -m venv .venv_tabular
  source .venv_tabular/bin/activate
  pip install -r pothhole-main/requirements-tabular.txt
  ```
- Train with cross-validation (example):
  ```bash
  python pothhole-main/tabular_pipeline.py \
    --data pothhole-main/listings.csv \
    --out pothhole-main/listing_pipeline.joblib \
    --cv 5
  ```
  This saves `listing_pipeline.joblib`.

- Predict:
  ```bash
  python pothhole-main/predict_listing.py \
    --model pothhole-main/listing_pipeline.joblib \
    --input pothhole-main/new_listings.csv \
    --out pothhole-main/preds.csv
  ```

---

## Quick examples: load and run predictions

A. Load lightweight pickle and predict a single row (pure Python)
```python
import pickle
import numpy as np
# load model
m = pickle.load(open('pothhole-main/listing_model.pkl','rb'))
weights = np.array(m['weights'])
feature_names = m['feature_names']

# construct feature vector in the same order as feature_names
# example: vector = [1 (bias), accommodates, name_len, name_word_count, name_kw_charm, ..., tfidf_name_x, ...]
# then compute:
pred = float(np.dot(vector, weights))
```
Note: You must build the feature vector exactly as training did (same order and same TF-IDF vocabulary if used).

B. Load sklearn joblib pipeline and predict on a DataFrame
```python
import joblib
import pandas as pd

pipeline = joblib.load('pothhole-main/listing_pipeline.joblib')
df = pd.read_csv('pothhole-main/new_listings.csv')   # raw rows with columns like name, host_email, etc.
preds = pipeline.predict(df)                        # pipeline performs preprocessing internally
df['predicted_pricePerNight'] = preds
df.to_csv('pothhole-main/preds.csv', index=False)
```

---

## Implementation notes & caveats

- Dependency conflicts:
  - TensorFlow requires newer numpy; scikit-learn (older versions) may require numpy < 2.0. That’s why the tabular sklearn pipeline uses a separate venv (.venv_tabular) with numpy compatible with scikit-learn.
- Small-sample behavior:
  - The sample CSV used for smoke tests is tiny — cross-validation and hyperparameter search are not meaningful with few rows. Use a larger dataset for reliable results.
- TF‑IDF:
  - tabular_app.py implements a small TF‑IDF (top-k tokens) to stay dependency-free.
  - `tabular_pipeline.py` uses `TfidfVectorizer` which is more robust and efficient for larger corpora.
- Persisted preprocessing:
  - For sklearn pipeline, preprocessing is persisted inside the joblib (no extra work required).
  - For the lightweight path, TF‑IDF vocabulary is baked into training; if you plan inference later, persist the vocabulary or prefer the sklearn pipeline.

---

## Suggested next improvements
- Add unit tests for `prepare_basic` and prediction helper.
- Expand TF‑IDF (increase `max_features`, add n‑grams) in `tabular_pipeline.py` and tune pipeline hyperparameters.
- Save preprocessing metadata for the lightweight pipeline (vocabulary, top domains). Or always use the sklearn pipeline for production.
- Add a small top-level README summary linking image-based training and tabular-based training sections.