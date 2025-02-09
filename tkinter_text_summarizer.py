import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from summarizer import summarizer
import os
from PyPDF2 import PdfReader
from docx import Document


def extract_text_from_pdf(filepath):
    reader = PdfReader(filepath)
    text = "".join([page.extract_text() for page in reader.pages if page.extract_text()])
    return text


def extract_text_from_docx(filepath):
    doc = Document(filepath)
    return "\n".join([para.text for para in doc.paragraphs])


def summarize_text():
    input_text = text_input.get("1.0", tk.END).strip()
    if not input_text:
        messagebox.showwarning("Warning", "Please enter text or upload a file!")
        return
    
    summary, original_txt, len_orig_txt, len_summary = summarizer(input_text)
    summary_output.config(state=tk.NORMAL)
    summary_output.delete("1.0", tk.END)
    summary_output.insert(tk.END, summary)
    summary_output.config(state=tk.DISABLED)
    original_count.config(text=f"Words: {len_orig_txt}")
    summary_count.config(text=f"Words: {len_summary}")


def upload_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("PDF Files", "*.pdf"), ("Word Documents", "*.docx")])
    if not file_path:
        return
    
    extracted_text = ""
    if file_path.endswith(".pdf"):
        extracted_text = extract_text_from_pdf(file_path)
    elif file_path.endswith(".docx"):
        extracted_text = extract_text_from_docx(file_path)
    elif file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            extracted_text = f.read()
    
    text_input.delete("1.0", tk.END)
    text_input.insert(tk.END, extracted_text)


# GUI Setup
root = tk.Tk()
root.title("Text Summarizer")
root.geometry("600x500")

# Input Section
tk.Label(root, text="Enter Text or Upload File:", font=("Arial", 12, "bold")).pack(pady=5)
text_input = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=10)
text_input.pack(pady=5)

# Buttons
btn_frame = tk.Frame(root)
btn_frame.pack(pady=5)
tk.Button(btn_frame, text="Summarize", command=summarize_text, bg="#26A69A", fg="white", padx=10, pady=5).pack(side=tk.LEFT, padx=10)
tk.Button(btn_frame, text="Upload File", command=upload_file, bg="#92C7CF", fg="black", padx=10, pady=5).pack(side=tk.LEFT, padx=10)

# Summary Section
tk.Label(root, text="Summary:", font=("Arial", 12, "bold")).pack(pady=5)
summary_output = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=8, state=tk.DISABLED)
summary_output.pack(pady=5)

# Word Counts
count_frame = tk.Frame(root)
count_frame.pack(pady=5)
original_count = tk.Label(count_frame, text="Words: 0", font=("Arial", 10))
original_count.pack(side=tk.LEFT, padx=20)
summary_count = tk.Label(count_frame, text="Words: 0", font=("Arial", 10))
summary_count.pack(side=tk.LEFT, padx=20)

# Run the GUI
root.mainloop()
