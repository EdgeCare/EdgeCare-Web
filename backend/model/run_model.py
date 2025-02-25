import onnxruntime as ort
import torch
from transformers import MobileBertTokenizer
import json

def load_labels(json_path='./model/edgeCare-de-id-labels.json'):
    with open(json_path, "r", encoding="utf-8") as f:
        ids_to_labels = json.load(f)
    return ids_to_labels

# Load Tokenizer
model_name = "google/mobilebert-uncased"
tokenizer = MobileBertTokenizer.from_pretrained(model_name)

# Label mappings
ids_to_labels = load_labels()

# Load ONNX Model
onnx_model_path = "./model/edgeCare-de-identifier.onnx"  # Ensure this path is correct
session = ort.InferenceSession(onnx_model_path)

def format_output(tokens, predicted_labels):
    # Merge subwords into complete words
    merged_tokens = []
    merged_labels = []
    current_word = ""
    current_label = None

    for token, label in zip(tokens, predicted_labels):
        if token in ["[SEP]", "[CLS]"]:  # Ignore special tokens
            continue

        if token.startswith("##"):
            current_word += token[2:]  # Merge subword
        else:
            if current_word:  # Save previous word before starting a new one
                merged_tokens.append(current_word)
                merged_labels.append(current_label)

            current_word = token  # Start new word
            current_label = label  # Assign label

    # Append last word
    if current_word:
        merged_tokens.append(current_word)
        merged_labels.append(current_label)

    # Merge consecutive tokens with the same label
    grouped_results = []
    current_phrase = merged_tokens[0]
    current_tag = merged_labels[0]

    for i in range(1, len(merged_tokens)):
        if merged_labels[i] == current_tag:  # If the same tag, merge words
            current_phrase += " " + merged_tokens[i]
        else:
            grouped_results.append({"token": current_phrase, "tag": current_tag})
            current_phrase = merged_tokens[i]  # Start new phrase
            current_tag = merged_labels[i]

    # Append last merged phrase
    if current_phrase:
        grouped_results.append({"token": current_phrase, "tag": current_tag})

    return grouped_results

async def predict_entities(text: str):
    """Runs ONNX model inference for NER"""
    
    # Tokenize input
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, is_split_into_words=False)

    # Ensure token_type_ids is included
    if "token_type_ids" not in inputs:
        inputs["token_type_ids"] = torch.zeros_like(inputs["input_ids"])  # Default to zeros

    # Convert input tensors to numpy for ONNX inference
    input_ids = inputs["input_ids"].numpy()
    attention_mask = inputs["attention_mask"].numpy()
    token_type_ids = inputs["token_type_ids"].numpy()  # Include token_type_ids

    # Run inference with ONNX model
    ort_inputs = {"input_ids": input_ids, "attention_mask": attention_mask, "token_type_ids": token_type_ids}
    ort_outputs = session.run(None, ort_inputs)

    # Extract predictions
    logits = ort_outputs[0]
    predictions = torch.argmax(torch.tensor(logits), dim=2)  # Get the highest probability class

    # Convert tokens and predictions to readable format
    tokens = tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])
    predicted_labels = [ids_to_labels[pred.item()] for pred in predictions[0]]

    # Format output
    formatted_results = format_output(tokens, predicted_labels)
    
    return formatted_results
