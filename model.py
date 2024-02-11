import requests
import json
import openai
import time
import logging
from transformers import AutoModelForCausalLM, AutoTokenizer

# Replace with your actual API key and API endpoint
def openai():
    openai.api_key = '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'
    API_ENDPOINT = 'https://api.openai.com//v1/chat/completions'

    prompt = "You are a helpful assistant that translates programming instructions from Polish to JavaScript"
    model = "text-davinci-003"
    response = openai.Completion.create(engine=model, prompt=prompt, max_tokens=50)

    generated_text = response.choices[0].text
    print(generated_text)

#def huggingface_interface(data, model_id, api_token):

logging.basicConfig(filename='inference_log.txt', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def huggingface_inference(model_id, text, temperature=0.8, max_length=50, top_k=50, top_p=1.0):
    api_token = "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"
    
    # Update the data payload with additional parameters
    data = {
        "inputs": text,
        "temperature": temperature,
        "max_length": max_length,
        "top_k": top_k,
        "top_p": top_p
    }

    headers = {"Authorization": f"Bearer {api_token}"}
    API_URL = f"https://api-inference.huggingface.co/models/{model_id}"
    
    retries = 5
    for attempt in range(retries):
        logging.info(f"Attempt {attempt + 1} to access model {model_id}")
        response = requests.post(API_URL, headers=headers, json=data)
        response_data = response.json()
        if 'error' in response_data and 'estimated_time' in response_data:
            wait_time = response_data['estimated_time']
            logging.warning(f"Error encountered: {response_data['error']}. Retrying in {wait_time + 5} seconds.")
            time.sleep(wait_time + 5)  # Wait for the estimated time plus a buffer
        else:
            logging.info(f"Successfully accessed model {model_id} on attempt {attempt + 1}")
            return response_data
    logging.error(f"Model {model_id} could not be loaded after {retries} retries.")
    return {"error": "Model could not be loaded after several retries."}


#TODO podpiąć tu pycharm i potestować jak łączyć ze sobą modele
def hf():
    checkpoint = "Deci/DeciCoder-1b"
    device = 'cpu'
    #device = 'cuda'

    logging.info('Loading the tokenizer...')
    tokenizer = AutoTokenizer.from_pretrained(checkpoint)

    logging.info('Loading the model...')
    model = AutoModelForCausalLM.from_pretrained(checkpoint, trust_remote_code=True).to(device)

    logging.info('Encoding the input and generating the output...')
    inputs = tokenizer.encode("def print_hello_world():", return_tensors="pt").to(device)
    outputs = model.generate(inputs, max_new_tokens=100)
    
    decoded_output = tokenizer.decode(outputs[0])
    logging.info('Decoded output: %s', decoded_output)
    return decoded_output
   


if __name__ == '__main__':
    #model = "gpt2-medium"  # for example
    model = "meta-llama/Llama-2-7b"
    text = "Once upon a time"
    result = huggingface_inference(model, text, 0.8, 50, 20, 0.5)
    print(result)

    print("---")
    result = huggingface_inference(model, text, 0.8, 50, 20, 0.6)
    print(result)

    print("---")
    result = huggingface_inference(model, text, 0.8, 50, 20, 0.7)
    print(result)

"""
Modele do kodu:
https://huggingface.co/defog/sqlcoder
https://huggingface.co/Deci/DeciCoder-1b

https://huggingface.co/models?other=custom_code
https://huggingface.co/models?other=`code

"""