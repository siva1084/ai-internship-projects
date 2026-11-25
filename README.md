# Spam Email Classifier

A machine learning model that detects spam messages using **Naive Bayes** and **Support Vector Machine (SVM)**, built with Python and scikit-learn.

## How it works
1. **Data** - SMS Spam Collection (5,572 labelled messages: 4,825 ham, 747 spam), downloaded automatically.
2. **Cleaning** - lowercase text; replace links and numbers with tokens; remove symbols.
3. **Features** - TF-IDF converts text into numbers (single words and word pairs).
4. **Models** - Multinomial Naive Bayes and Linear SVM are trained and compared.
5. **Result** - the better model is saved, and a confusion matrix is generated.

## Results
| Model | Accuracy |
|---|---|
| Naive Bayes | 97.67% |
| Linear SVM | **98.83%** |

## Run in VS Code
```bash
# 1. Open this folder in VS Code, then open the terminal (Ctrl + `)
python -m venv .venv
.venv\Scripts\activate          # Windows   (Mac/Linux: source .venv/bin/activate)
pip install -r requirements.txt

# 2. Run
python spam_classifier.py
```
After training, type your own message at the `>` prompt to test it. Press Enter on an empty line to quit.

## Files
- `spam_classifier.py` - the full project
- `requirements.txt` - libraries needed
- `confusion_matrix.png` - generated after running

## Tech
Python, pandas, scikit-learn, matplotlib, joblib
