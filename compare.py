
import torch
from pix2tex.cli import LatexOCR
import re
import difflib
from sympy import simplify, sympify
from Levenshtein import distance as levenshtein_distance
from PIL import Image

# Load Pix2Tex model
model = LatexOCR()

def extract_latex_from_image(image_path):
    image = Image.open(image_path).convert("RGB")
    latex = model(image)
    return latex

def clean_latex(text):
    text = text.replace(" ", "").replace("\n", "")
    text = re.sub(r"[^a-zA-Z0-9+\\=\\-\\*/(){}]", "", text)  # Remove unwanted characters
    return text

def compare_latex_levenshtein(latex1, latex2):
    dist = levenshtein_distance(latex1, latex2)
    max_len = max(len(latex1), len(latex2))
    similarity = (1 - dist / max_len) * 100  # Convert to percentage
    return similarity

def compare_latex_sympy(latex1, latex2):
    try:
        expr1 = simplify(sympify(latex1))
        expr2 = simplify(sympify(latex2))
        return expr1 == expr2
    except Exception:
        return False  # If parsing fails, assume they are different

def compare_structurally(latex1, latex2):
    return difflib.SequenceMatcher(None, latex1, latex2).ratio() * 100

if __name__ == "__main__":
    img1 = "./t.jpg"  # Change to your image paths
    img2 = "./t1.jpg"

    latex1 = extract_latex_from_image(img1)
    latex2 = extract_latex_from_image(img2)

    latex1 = clean_latex(latex1)
    latex2 = clean_latex(latex2)

    print(f"Extracted LaTeX 1: {latex1}")
    print(f"Extracted LaTeX 2: {latex2}")

    levenshtein_sim = compare_latex_levenshtein(latex1, latex2)
    structural_sim = compare_structurally(latex1, latex2)
    sympy_equiv = compare_latex_sympy(latex1, latex2)

    print(f"Levenshtein Similarity: {levenshtein_sim:.2f}%")
    print(f"Structural Similarity: {structural_sim:.2f}%")
    print(f"Mathematical Equivalence: {'Equivalent' if sympy_equiv else 'Different'}")
