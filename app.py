from flask import Flask, render_template, request
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest

app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")

def summarizer(rawdocs):
    stopwords = list(STOP_WORDS)
    doc = nlp(rawdocs)
    
    word_freq = {}
    for word in doc:
        if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
            word_freq[word.text] = word_freq.get(word.text, 0) + 1

    max_freq = max(word_freq.values())
    for word in word_freq.keys():
        word_freq[word] /= max_freq

    sent_tokens = [sent for sent in doc.sents]
    sent_scores = {}
    
    for sent in sent_tokens:
        for word in sent:
            if word.text in word_freq:
                sent_scores[sent] = sent_scores.get(sent, 0) + word_freq[word.text]

    select_len = int(len(sent_tokens) * 0.3)
    summary = nlargest(select_len, sent_scores, key=sent_scores.get)
    final_summary = " ".join([sent.text for sent in summary])

    return final_summary

@app.route("/", methods=["GET", "POST"])
def home():
    summary = ""
    if request.method == "POST":
        text = request.form["text"]
        summary = summarizer(text)
    return render_template("index.html", summary=summary)

if __name__ == "__main__":
    app.run(debug=True)
