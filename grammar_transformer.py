import os
import pandas as pd
import json
import openai
from dotenv import load_dotenv
import requests

# Explicitly load the .env file from the specified path
dotenv_path = '/Users/cclam/Desktop/CSS495 Capstone/GTP3Key/key.env'
load_dotenv(dotenv_path)

def load_data(file_path):
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        print(f"Error loading data file: {e}")
        return None

def prepare_training_file(data_file, output_file):
    try:
        data = pd.read_csv(data_file)
        
        training_data = []
        for _, row in data.iterrows():
            prompt = row['Ungrammatical Statement']
            completion = row['Standard English']
            training_data.append({"prompt": prompt, "completion": completion})
        
        with open(output_file, 'w') as f:
            for item in training_data:
                json.dump(item, f)
                f.write('\n')
        
        print(f"Training data prepared and saved to {output_file}")
    except Exception as e:
        print(f"Error preparing training file: {e}")

def upload_file(file_path):
    try:
        with open(file_path, 'rb') as f:
            response = openai.File.create(
                file=f,
                purpose='fine-tune'
            )
        file_id = response['id']
        print(f"File uploaded successfully. File ID: {file_id}")
        return file_id
    except Exception as e:
        print(f"Error uploading file: {e}")
        return None

def create_fine_tune_job(file_id, model="davinci-002", suffix=None):
    url = "https://api.openai.com/v1/fine_tuning/jobs"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"
    }
    data = {
        "model": model,
        "training_file": file_id,
        "suffix": suffix
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        job_response = response.json()
        print(f"Fine-tuning job created successfully. Job ID: {job_response['id']}")
        return job_response
    except requests.exceptions.RequestException as e:
        print(f"Error creating fine-tune job: {e}")
        return None

def generate_grammar_correction(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0125",
            messages=[
                {"role": "system", "content": "You are a helpful assistant who corrects grammar."},
                {"role": "user", "content": f"Correct the grammar: {prompt}"}
            ]
        )
        return response.choices[0].message['content']
    except Exception as e:
        print(f"Error generating grammar correction: {e}")
        return None

def main():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("API key not found. Please set the OPENAI_API_KEY environment variable.")
        return

    openai.api_key = api_key
    data_file = '/Users/cclam/Desktop/CSS495 Capstone/readyToGoGrammarTrainResources/GTP3TrainningResource/preprocessed_grammar_data.csv'
    output_file = '/Users/cclam/Desktop/CSS495 Capstone/readyToGoGrammarTrainResources/GTP3TrainningResource/gtp3_training_data.jsonl'
    output_txt = '/Users/cclam/Desktop/CSS495 Capstone/readyToGoGrammarTrainResources/GTP3TrainningResource/output.txt'

    prepare_training_file(data_file, output_file)
    
    file_id = upload_file(output_file)
    if not file_id:
        return
    
    response = create_fine_tune_job(file_id, model="davinci-002", suffix="grammar-correction")
    if response:
        print("Fine-tuning job response:", response)

    data = load_data(data_file)
    if data is None:
        return

    with open(output_txt, 'w') as f:
        for i, row in data.iterrows():
            ungrammatical_statement = row['Ungrammatical Statement']
            correction = generate_grammar_correction(ungrammatical_statement)
            output = (
                f"Ungrammatical: {ungrammatical_statement}\n"
                f"Generated correction: {correction}\n"
                f"Expected correction: {row['Standard English']}\n\n"
            )
            f.write(output)
            print(output)

if __name__ == '__main__':
    main()
