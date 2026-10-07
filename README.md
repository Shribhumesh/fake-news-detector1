# 🛡️ TruthLens AI — Fake News Detector

<p align="center">

![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python\&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Web%20App-FF4B4B?logo=streamlit\&logoColor=white)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-Machine%20Learning-F7931E?logo=scikit-learn\&logoColor=white)
![Joblib](https://img.shields.io/badge/Joblib-Model%20Persistence-3776AB)
![Plotly](https://img.shields.io/badge/Plotly-Visualization-3F4F75?logo=plotly\&logoColor=white)
![Regex](https://img.shields.io/badge/Regex-Text%20Cleaning-4285F4)
![Machine Learning](https://img.shields.io/badge/Machine%20Learning-Classification-16A34A)
![GitHub](https://img.shields.io/badge/GitHub-Repository-181717?logo=github\&logoColor=white)

</p>

## 📌 Project Overview

**TruthLens AI** is a Machine Learning based **Fake News Detection** web application built using **Python and Streamlit**.

The application analyzes a news headline or article and predicts whether the content is:

* 🚨 **Likely Fake News**
* ✅ **Likely Real News**

It also provides a **prediction confidence score** and visual analysis of the model's probability.

> ⚠️ This project provides a machine-learning prediction and should not be treated as a guaranteed fact-checking system.

---

## ✨ Features

### 📰 News Analysis

Users can paste a news headline or article into the application and analyze it using the trained ML model.

### 🤖 Machine Learning Prediction

The trained classification model analyzes the text and predicts whether it is **FAKE** or **REAL**.

### 📊 Prediction Probability

The application calculates the probability for both:

* FAKE
* REAL

and displays the model's confidence.

### 🧹 Text Cleaning

Before prediction, the news text is cleaned using regular expressions.

The preprocessing includes:

* Converting text to lowercase
* Removing URLs
* Removing HTML tags
* Removing special characters
* Removing extra spaces

### 🔤 TF-IDF Text Vectorization

The cleaned news text is converted into numerical features using a **TF-IDF Vectorizer** before being passed to the machine-learning model.

### 📈 Interactive Visualization

The application uses **Plotly** to display prediction and probability information interactively.

### 🎨 Modern Streamlit UI

The application includes a custom interface with:

* Sky-blue background
* Purple and green theme
* Responsive layout
* Custom CSS
* News input section
* Prediction result section
* Confidence information
* Source-style information cards

---

## 🛠️ Technologies Used

| Technology             | Purpose                             |
| ---------------------- | ----------------------------------- |
| 🐍 **Python**          | Main programming language           |
| 🎈 **Streamlit**       | Interactive web application         |
| 🤖 **Scikit-learn**    | Machine Learning                    |
| 🔤 **TF-IDF**          | Text feature extraction             |
| 💾 **Joblib**          | Saving and loading ML models        |
| 📊 **Plotly**          | Interactive data visualization      |
| 🧹 **Regex (`re`)**    | Text preprocessing                  |
| 📁 **Pickle (`.pkl`)** | Stored trained model/vectorizer     |
| 🔀 **Git & GitHub**    | Version control and project hosting |

---

## 🧠 How It Works

```text
                📰 News Article
                       │
                       ▼
                🧹 Text Cleaning
                       │
                       ▼
              🔤 TF-IDF Vectorizer
                       │
                       ▼
             🤖 ML Classification Model
                       │
              ┌────────┴────────┐
              ▼                 ▼
          🚨 FAKE            ✅ REAL
              │                 │
              └────────┬────────┘
                       ▼
              📊 Probability
                       │
                       ▼
              🎯 Final Prediction
```

---

## 🔍 Text Processing

The application first cleans the input text.

```python
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
    ).strip()

    return text
```

This preprocessing helps convert the input into a consistent format before prediction.

---

## 🔤 TF-IDF Vectorization

After cleaning the text, the application uses a trained **TF-IDF vectorizer** to convert the news article into numerical features.

```python
vectorized_text = vectorizer.transform(
    [cleaned_text]
)
```

The resulting features are then passed to the trained machine-learning model.

---

## 🤖 Prediction

The trained model generates the final prediction:

```python
prediction = model.predict(
    vectorized_text
)[0]
```

The application also calculates prediction probabilities:

```python
probabilities = model.predict_proba(
    vectorized_text
)[0]
```

The highest probability is used as the model's confidence score.

---

## 📊 Example Output

### Real News

```text
✅ LIKELY REAL NEWS

Confidence: 69.31%
```

### Fake News

```text
🚨 LIKELY FAKE NEWS

Confidence: 85.42%
```

> The confidence score represents the model's prediction probability, not the factual truth of the article.

---

## 📂 Project Structure

```text
fake-news-detector1/
│
├── app.py
├── train_model.py
├── predict.py
├── requirements.txt
│
├── fake_news_model.pkl
├── tfidf_vectorizer.pkl
│
└── README.md
```

The GitHub repository currently contains the application, training/prediction scripts, requirements file, and serialized model/vectorizer files.

---

## 📄 File Description

### `app.py`

Main Streamlit web application.

It handles:

* User input
* Text cleaning
* TF-IDF transformation
* Model prediction
* Probability calculation
* Confidence score
* Visualization
* User interface

### `train_model.py`

Used for training the machine-learning model and creating the saved model/vectorizer files.

### `predict.py`

Provides a command-line prediction interface.

It accepts a news article from the user and returns the prediction and model confidence.

### `fake_news_model.pkl`

Saved trained machine-learning model.

### `tfidf_vectorizer.pkl`

Saved TF-IDF vectorizer used to transform text before prediction.

### `requirements.txt`

Contains the Python packages required to run the project.

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Shribhumesh/fake-news-detector1.git
```

### 2. Open the Project

```bash
cd fake-news-detector1
```

### 3. Create Virtual Environment

```bash
python -m venv .venv
```

### 4. Activate Virtual Environment

For Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

If required packages are missing, you can install the main dependencies manually:

```bash
pip install streamlit scikit-learn joblib plotly
```

### 6. Run the Streamlit Application

```bash
streamlit run app.py
```

---

## 🖥️ Command-Line Prediction

You can also test the model without Streamlit:

```bash
python predict.py
```

Then enter a news article:

```text
Enter News: The government announced a new education scheme for students.
```

The program returns the prediction and confidence score.

---

## 🎯 Project Objectives

The main objectives of this project are:

* Detect potentially fake news using Machine Learning
* Understand Natural Language Processing basics
* Perform text preprocessing
* Convert text into numerical features using TF-IDF
* Train and use a classification model
* Build an interactive ML web application
* Display prediction probabilities visually

---

## 📚 Learning Outcomes

Through this project, I learned:

* Python programming
* Natural Language Processing fundamentals
* Text preprocessing
* TF-IDF vectorization
* Machine Learning classification
* Model serialization using Joblib
* Prediction probability
* Streamlit application development
* Plotly visualization
* Git and GitHub

---

## 🔮 Future Improvements

Possible future improvements include:

* 🌐 Real-time news verification
* 🔎 Integration with trusted news sources
* 📰 News source credibility checking
* 🧠 More advanced NLP models
* 🤖 Transformer-based models such as BERT
* 📚 Larger and more diverse datasets
* 📈 Improved model evaluation
* 🌍 Multi-language fake news detection
* 🔗 URL-based news analysis
* ☁️ Online deployment

---

## ⚠️ Disclaimer

This project is created for **educational and demonstration purposes**.

The prediction is generated by a machine-learning model and does **not guarantee that a news article is factually true or false**.

Always verify important information using reliable and trusted sources.

---

## 👨‍💻 Author

### Shribhumesh Bandiwadekar

BCA Student | Machine Learning | Python | Web Development

---

## ⭐ Support

If you like this project, consider giving it a ⭐ on GitHub.

**Repository:** `Shribhumesh/fake-news-detector1`
