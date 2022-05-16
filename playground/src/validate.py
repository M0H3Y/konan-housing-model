import joblib
import pandas as pd

from file_handling import (
    read_metadata,
    read_data,
)
from utils.encoding import one_hot_encode, ordinal_encode
from utils.pipeline import run_testing


# ------------------------------------------------------------------- #
# Read the files
_, val = read_data()
metadata = read_metadata()
# print("Validation set size:", val.shape)


# ------------------------------------------------------------------- #
# Load model artifacts
regressor = joblib.load(
    'app/artifacts/model.pkl',
)
one_hot_encoder = joblib.load(
    'app/artifacts/one_hot_encoder.pkl',
)
ordinal_encoder = joblib.load(
    'app/artifacts/ordinal_encoder.pkl',
)


# ------------------------------------------------------------------- #
# Get log of target
# We use the numpy function log1p which  applies log(1+x) to all elements of the column
y_val: pd.Series = val.SalePrice


# ------------------------------------------------------------------- #
# Process features
X_val = val.copy().drop(
    ['SalePrice'],
    axis=1,
)


# ------------------------------------------------------------------- #
# One-Hot-Encode Categorial Features
X_val, _ = one_hot_encode(
    df=X_val,
    columns=metadata['oneHotEncoding'],
    encoder=one_hot_encoder,
)
# print("Validation Features after OneHotEncoding set size:", X_val.shape)


# ------------------------------------------------------------------- #
# Label-Encode Ordinal Features
X_val, _ = ordinal_encode(
    df=X_val,
    columns=list(metadata['ordinalEncoding'].keys()),
    categories=list(metadata['ordinalEncoding'].values()),
    encoder=ordinal_encoder,
)
# print("Validation Features after OrindalEncoding set size:", X_val.shape)

X_val = X_val.fillna(0)


# ------------------------------------------------------------------- #
# Validate the model
val_mape = run_testing(
    regressor=regressor,
    X_test=X_val,
    y_test=y_val,
)

print(f"Model validation Mean Absolute Percentage Error: {val_mape}")