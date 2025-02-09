from flask import Flask, render_template, request
from tkinter_text_summarizer import summarize_text  # Import your summarization function

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    summary = ""
    if request.method == "POST":
        text = request.form["text"]
        summary = summarize_text(text)  # Your summarization logic
    return render_template("index.html", summary=summary)

if __name__ == "__main__":
    app.run(debug=True)
