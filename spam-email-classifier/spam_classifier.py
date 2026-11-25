"""
Spam Email Classifier
---------------------
Trains Naive Bayes and SVM models to detect spam messages.

Steps:
  1. Load the SMS Spam Collection dataset (downloaded automatically)
  2. Clean the text and split into train/test sets
  3. Convert text to numbers using TF-IDF
  4. Train Multinomial Naive Bayes and Linear SVM
  5. Compare accuracy, save the best model and a confusion matrix
  6. Let you type your own message to test it

Run:  python spam_classifier.py
"""

import os
import re
import urllib.request

import joblib
import matplotlib
import pandas as pd

matplotlib.use("Agg")  # saves plots to files, works on any machine
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import (ConfusionMatrixDisplay, accuracy_score,
                             classification_report)
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC

DATA_URL = ("https://raw.githubusercontent.com/justmarkham/"
            "pycon-2016-tutorial/master/data/sms.tsv")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "sms.tsv")
MODEL_PATH = os.path.join(BASE_DIR, "spam_model.joblib")
PLOT_PATH = os.path.join(BASE_DIR, "confusion_matrix.png")


def load_data():
    """Download the dataset once, then load it from disk."""
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    if not os.path.exists(DATA_PATH):
        print("Downloading dataset...")
        urllib.request.urlretrieve(DATA_URL, DATA_PATH)
    df = pd.read_csv(DATA_PATH, sep="\t", header=None, names=["label", "message"])
    df["target"] = (df["label"] == "spam").astype(int)  # spam=1, ham=0
    return df


def clean_text(text):
    """Lowercase, replace links/numbers with tokens, drop extra symbols."""
    text = text.lower()
    text = re.sub(r"http\S+|www\S+", " urltoken ", text)
    text = re.sub(r"\d+", " numtoken ", text)
    text = re.sub(r"[^a-z\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def build_pipeline(classifier):
    return Pipeline([
        ("tfidf", TfidfVectorizer(stop_words="english", ngram_range=(1, 2), min_df=2)),
        ("clf", classifier),
    ])


def main():
    df = load_data()
    print(f"Loaded {len(df)} messages")
    print(df["label"].value_counts().to_string(), "\n")

    df["clean"] = df["message"].apply(clean_text)
    X_train, X_test, y_train, y_test = train_test_split(
        df["clean"], df["target"], test_size=0.2, random_state=42, stratify=df["target"]
    )

    models = {
        "Naive Bayes": build_pipeline(MultinomialNB()),
        "Linear SVM": build_pipeline(LinearSVC()),
    }

    best_name, best_model, best_acc = None, None, 0
    for name, model in models.items():
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        acc = accuracy_score(y_test, preds)
        print(f"=== {name} === accuracy: {acc:.4f}")
        print(classification_report(y_test, preds, target_names=["ham", "spam"]))
        if acc > best_acc:
            best_name, best_model, best_acc = name, model, acc

    print(f"Best model: {best_name} ({best_acc:.2%})")
    joblib.dump(best_model, MODEL_PATH)
    print(f"Saved model to {MODEL_PATH}")

    ConfusionMatrixDisplay.from_estimator(
        best_model, X_test, y_test, display_labels=["ham", "spam"], cmap="Blues"
    )
    plt.title(f"Confusion Matrix - {best_name}")
    plt.savefig(PLOT_PATH, dpi=120, bbox_inches="tight")
    print(f"Saved confusion matrix to {PLOT_PATH}\n")

    # Interactive demo
    print("Type a message to check it (or press Enter to quit).")
    while True:
        try:
            msg = input("> ").strip()
        except EOFError:
            break
        if not msg:
            break
        label = best_model.predict([clean_text(msg)])[0]
        print("  -> SPAM" if label == 1 else "  -> Not spam (ham)")


if __name__ == "__main__":
    main()
