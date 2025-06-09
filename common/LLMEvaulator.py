from transformers import MT5Tokenizer, MT5ForConditionalGeneration, AutoModelForCausalLM, AutoTokenizer, LlamaTokenizer, AutoModelForSeq2SeqLM, BartTokenizer
import torch
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np


def evaluate_with_rag(question, content_dict, model_name):
    if len(question) > 0 and len(content_dict) > 0 \
            and len(model_name) > 0:
        tokenizer = MT5Tokenizer.from_pretrained(model_name)
        model = MT5ForConditionalGeneration.from_pretrained(model_name)
        input_text = f"Soru: {question} \n\nWeb'den alınan bilgiler: \n{str(content_dict)} \nYukarıdaki bilgilere dayanarak kısa ve güvenilir bir yanıt üret."
        print("\n\n" + input_text)
        input_ids = tokenizer(input_text, return_tensors="pt").input_ids
        output_ids = model.generate(input_ids, max_length=64, num_beams=4)
        answer = tokenizer.decode(output_ids[0], skip_special_tokens=True)
        return answer
    else:
        raise ValueError("question ,content_dict and model_name is mandotary")


def evaluate_with_rag_v2(question, content_dict, model_name):
    if len(question) > 0 and len(content_dict) > 0 \
            and len(model_name) > 0:
        tokenizer = AutoTokenizer.from_pretrained(
            model_name, trust_remote_code=True, use_fast=False)
        model = AutoModelForCausalLM.from_pretrained(
            model_name, torch_dtype=torch.float16, device_map="auto", trust_remote_code=True)
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model.to(device)
        prompt = f"Soru: {question} \n\nWeb'den alınan bilgiler: \n{str(content_dict)} \nYukarıdaki bilgilere dayanarak kısa ve güvenilir bir yanıt üret."
        print("\n\n" + prompt)
        inputs = tokenizer(prompt, return_tensors="pt").to(device)
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=100,
                temperature=0.7,
                top_p=0.9,
                do_sample=True,
                eos_token_id=tokenizer.eos_token_id
            )
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response
    else:
        raise ValueError("question ,content_dict and model_name is mandotary")


def evaluate_with_rag_v3(question, content_dict, model_name):
    if len(question) > 0 and len(content_dict) > 0 \
            and len(model_name) > 0:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(device)
        model.to(device)
        model.resize_token_embeddings(len(tokenizer))
        # Tokenize without returning `token_type_ids`
        prompt = f"Soru: {question} \n\nWeb'den alınan bilgiler: \n{str(content_dict)} \nYukarıdaki bilgilere dayanarak kısa ve güvenilir bir yanıt üret."
        inputs = tokenizer(prompt, return_tensors="pt",
                           return_token_type_ids=False, truncation=True)
        inputs = {k: v.to(device) for k, v in inputs.items()}

        # Or manually filter out token_type_ids if they exist
        inputs.pop("token_type_ids", None)

        # Generate text
        outputs = model.generate(
            input_ids=inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            max_new_tokens=100,  # <-- limits only the *output* tokens
            temperature=0.7,
            top_p=0.9,
            do_sample=True,
            eos_token_id=tokenizer.eos_token_id
        )
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return generated_text
    else:
        raise ValueError("question ,content_dict and model_name is mandotary")


def evaluate_with_rag_faiss(question, content_dict):
    model_name = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    if len(question) > 0 and len(content_dict) > 0 \
            and len(model_name) > 0:
        print("Faiss is working")
        model = SentenceTransformer(model_name)
        doc_embeddings = model.encode(content_dict)
        index = faiss.IndexFlatL2(doc_embeddings.shape[1])
        index.add(np.array(doc_embeddings))
        query_vec = model.encode([question])
        _, indices = index.search(np.array(query_vec), k=5) #QA için 3 - 10 arası öneriliyor
        new_content_dict = []
        if len(indices) > 0 and len(indices[0]) > 0:
            for i in range(len(indices[0])):
                new_content_dict.append(content_dict[indices[0][i]])
        #new_content_dict = content_dict[indices[0][0]]
        print(f"new_content_dict : {new_content_dict}")
        return new_content_dict
    else:
        raise ValueError("question ,content_dict and model_name is mandotary")


def evaluate_with_rag_faiss_and_return_only_description(question, content_dict):
    new_content_dict = evaluate_with_rag_faiss(question, content_dict)
    arr_to_return = []
    for item in new_content_dict:
        if "description" in item:
            arr_to_return.append(item["description"])
    print(f"arr_to_return:{arr_to_return}")
    return arr_to_return

