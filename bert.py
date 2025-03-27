# Load model directly
from transformers import AutoTokenizer, AutoModelForMaskedLM

tokenizer = AutoTokenizer.from_pretrained("tbs17/MathBERT")
model = AutoModelForMaskedLM.from_pretrained("tbs17/MathBERT")
