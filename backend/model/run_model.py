import onnxruntime as ort
import torch
from transformers import MobileBertTokenizer
import json
import re

def load_labels(json_path='./model/edgeCare-de-id-labels.json'):
    with open(json_path, "r", encoding="utf-8") as f:
        ids_to_labels = json.load(f)
        ids_to_labels = {int(k): v for k, v in ids_to_labels.items()}
    return ids_to_labels

# Load Tokenizer
model_name = "google/mobilebert-uncased"
tokenizer = MobileBertTokenizer.from_pretrained(model_name)

# Label mappings
ids_to_labels = load_labels()

# Load ONNX Model
onnx_model_path = "./model/edgeCare-de-identifier.onnx"  # Ensure this path is correct
session = ort.InferenceSession(onnx_model_path)

def format_output(tokens, predicted_labels, text):

    # Removing special tokens
    token_label_pairs = []
    for token, label in zip(tokens, predicted_labels):
        if token not in ["[CLS]", "[SEP]"]:
            token_label_pairs.append((token, label))

    formatted_results = []
    current_entity = {"token": "", "tag": "O"}
    for i, (token, tag) in enumerate(token_label_pairs):
        word = token.replace("##", "")  # Merge subword tokens
        if i > 0 and token.startswith("##"):  
            current_entity["token"] += word
        elif tag == current_entity["tag"]:
            current_entity["token"] += " " + word
        else:
            if current_entity["token"]:
                formatted_results.append(current_entity)
            current_entity = {"token": word, "tag": tag}

        ## [TODO] - Handle new line characters
        #check if present in test and then add {"token": ''\n', "tag": 0}


    if current_entity["token"]:
        formatted_results.append(current_entity)

    # Adjust token spacing to match original text
    formatted_text = text
    for entity in formatted_results:
        match = re.search(re.escape(entity["token"]), formatted_text, re.IGNORECASE)
        if match:
            entity["token"] = formatted_text[match.start(): match.end()]
    

    return formatted_results

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

    # Format outpu
    formatted_results = format_output(tokens, predicted_labels, text)
    print("text",text)
    print("tokens",tokens)
    print("predicted_labels",predicted_labels)
    print("formatted_results",formatted_results)
    
    return formatted_results
