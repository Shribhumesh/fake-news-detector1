import joblib
import re
import os


# -----------------------------
# FILE PATHS
# -----------------------------

MODEL_PATH = "model/fake_news_model.pkl"
VECTORIZER_PATH = "model/tfidf_vectorizer.pkl"


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
# CHECK FILES
# -----------------------------

if not os.path.exists(MODEL_PATH):

    print("ERROR: Model file not found!")

    exit()


if not os.path.exists(VECTORIZER_PATH):

    print("ERROR: Vectorizer file not found!")

    exit()


# -----------------------------
# LOAD MODEL
# -----------------------------

model = joblib.load(
    MODEL_PATH
)

vectorizer = joblib.load(
    VECTORIZER_PATH
)


# -----------------------------
# USER INPUT
# -----------------------------

print()
print("==============================")
print("AI FAKE NEWS DETECTOR")
print("==============================")

print()
print("Enter a news headline/article.")
print("Type 'exit' to close the program.")
print()


news_text = input(
    "Enter News: "
)


# -----------------------------
# EXIT
# -----------------------------

if news_text.lower() == "exit":

    print("Program closed.")

    exit()


# -----------------------------
# CHECK INPUT
# -----------------------------

if not news_text.strip():

    print("Please enter some news.")

    exit()


# -----------------------------
# CLEAN TEXT
# -----------------------------

cleaned_text = clean_text(
    news_text
)


# -----------------------------
# TF-IDF
# -----------------------------

vectorized_text = vectorizer.transform(
    [cleaned_text]
)


# -----------------------------
# PREDICTION
# -----------------------------

prediction = model.predict(
    vectorized_text
)[0]


# -----------------------------
# CONFIDENCE
# -----------------------------

probabilities = model.predict_proba(
    vectorized_text
)[0]

confidence = max(
    probabilities
) * 100


# -----------------------------
# RESULT
# -----------------------------

print()
print("==============================")
print("RESULT")
print("==============================")


if prediction == "FAKE":

    print("Prediction: ⚠️ LIKELY FAKE NEWS")

else:

    print("Prediction: ✅ LIKELY REAL NEWS")


print(
    f"Model Confidence: {confidence:.2f}%"
)

print()
print(
    "Note: This is a machine-learning prediction, "
    "not a guaranteed fact check."
)

print()