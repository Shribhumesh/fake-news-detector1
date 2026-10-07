import pandas as pd
import re
import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report


# -----------------------------
# FILE PATHS
# -----------------------------

DATASET_PATH = "dataset/news.csv"
MODEL_DIR = "model"

MODEL_PATH = os.path.join(
    MODEL_DIR,
    "fake_news_model.pkl"
)

VECTORIZER_PATH = os.path.join(
    MODEL_DIR,
    "tfidf_vectorizer.pkl"
)


# -----------------------------
# TEXT CLEANING
# -----------------------------

def clean_text(text):

    text = str(text)

    text = text.lower()

    text = re.sub(
        r"http\S+|www\S+",
        "",
        text
    )

    text = re.sub(
        r"<.*?>",
        "",
        text
    )

    text = re.sub(
        r"[^a-zA-Z0-9\s]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# -----------------------------
# LOAD DATASET
# -----------------------------

print("Loading dataset...")

if not os.path.exists(DATASET_PATH):

    print("ERROR: news.csv not found!")

    print(
        "Please put news.csv inside the dataset folder."
    )

    exit()


df = pd.read_csv(DATASET_PATH)

print("Dataset loaded successfully!")

print("Columns:", list(df.columns))

print("Number of rows:", len(df))


# -----------------------------
# CHECK REQUIRED COLUMNS
# -----------------------------

required_columns = [
    "title",
    "text",
    "label"
]

for column in required_columns:

    if column not in df.columns:

        print(
            f"ERROR: Missing column: {column}"
        )

        exit()


# -----------------------------
# REMOVE EMPTY VALUES
# -----------------------------

df = df.dropna(
    subset=[
        "title",
        "text",
        "label"
    ]
)


# -----------------------------
# COMBINE TITLE + TEXT
# -----------------------------

df["content"] = (
    df["title"].astype(str)
    + " "
    + df["text"].astype(str)
)


# -----------------------------
# CLEAN TEXT
# -----------------------------

print("Cleaning text...")

df["content"] = df["content"].apply(
    clean_text
)


# -----------------------------
# FEATURES AND LABEL
# -----------------------------

X = df["content"]

y = df["label"].astype(str).str.upper()


# -----------------------------
# CHECK LABELS
# -----------------------------

print("Labels found:", y.unique())

if len(y.unique()) < 2:

    print(
        "ERROR: Dataset must contain at least "
        "two different labels."
    )

    exit()


# -----------------------------
# TRAIN TEST SPLIT
# -----------------------------

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.2,

    random_state=42,

    stratify=y
)


print("Training samples:", len(X_train))
print("Testing samples:", len(X_test))


# -----------------------------
# TF-IDF
# -----------------------------

print("Creating TF-IDF vectorizer...")

vectorizer = TfidfVectorizer(

    stop_words="english",

    max_features=50000,

    ngram_range=(1, 2)
)


X_train_tfidf = vectorizer.fit_transform(
    X_train
)

X_test_tfidf = vectorizer.transform(
    X_test
)


# -----------------------------
# TRAIN MODEL
# -----------------------------

print("Training Logistic Regression model...")

model = LogisticRegression(
    max_iter=1000
)

model.fit(
    X_train_tfidf,
    y_train
)


# -----------------------------
# TEST MODEL
# -----------------------------

print("Testing model...")

predictions = model.predict(
    X_test_tfidf
)


accuracy = accuracy_score(
    y_test,
    predictions
)


print()
print("==============================")
print("MODEL TRAINING COMPLETE")
print("==============================")

print(
    f"Accuracy: {accuracy * 100:.2f}%"
)

print()
print("Classification Report:")

print(
    classification_report(
        y_test,
        predictions
    )
)


# -----------------------------
# CREATE MODEL FOLDER
# -----------------------------

os.makedirs(
    MODEL_DIR,
    exist_ok=True
)


# -----------------------------
# SAVE MODEL
# -----------------------------

joblib.dump(
    model,
    MODEL_PATH
)

joblib.dump(
    vectorizer,
    VECTORIZER_PATH
)


print()
print("==============================")
print("FILES SAVED SUCCESSFULLY")
print("==============================")

print(
    "Model:",
    MODEL_PATH
)

print(
    "Vectorizer:",
    VECTORIZER_PATH
)

print()
print("Training finished successfully!")