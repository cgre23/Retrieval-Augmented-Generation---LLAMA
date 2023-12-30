# Retrieval Augmented Generation - LLAMA
### by Christian Grech


## Introduction

The aim is to gain a quick overview of the diverse possible uses of Llama-2. For this purpose, a question-answering system is to be developed that is based on scientific publications. The scientific papers on the subject of “Llama” available on [Arxiv.org]( http://arxiv.org/ ) serve as the primary source of information. This approach is intended to enable us to gain in-depth insights into the functionality and application areas of Llama-2, thereby supporting our decision-making processes regarding the integration of this technology into our projects.

## Solution

1. Data is collected from the Arxiv API and stored in a json/txt file
2. Langchain is used to split the text and create embeddings.
3. GPT-3.5-Turbo is used and is finetuned to allow the data as context.
4. The model is then queried with the user's input.


## Instructions

1. Make sure that you place the OPENAI_API_KEY in the .env file in this folder. Use this format: OPENAI_API_KEY=xxx. Access the file as follows:
        
        nano .env


2. Activate the virtual environment

        . venv/bin/activate


3. Run the python script


        python main.py
    

4. Wait until the script asks for a prompt. Enter your prompt and you will get a response. You will be repeatedly asked for another prompt; to quit press Enter on an empty prompt.


## Examples

    Enter your prompt: What can you find out about the model structure of Llama-2?
    Llama-2 is a collection of pretrained and fine-tuned large language models ranging from 7 billion to 70 billion parameters. The fine-tuned Llama-2 models, called Llama 2-Chat, are optimized for dialogue use cases and outperform open-source chat models on most benchmarks. The model structure of Llama-2 is described in detail in the provided context.

    Enter your prompt: For which tasks has Llama-2 already been used successfully? What are promising areas of application for Llama-2?
    Llama-2 has been successfully used for dialogue use cases, as the fine-tuned Llama 2-Chat models outperform open-source chat models on most benchmarks. Llama-2 has also been successfully used for multitask analysis of financial news, including tasks such as analyzing a text from financial market perspectives, highlighting main points, summarizing a text, and extracting named entities with sentiments. Promising areas of application for Llama-2 include language modeling in underrepresented languages like Tamil, where it has shown significant performance improvements in text generation.

    Enter your prompt: Name at least 5 domain-specific LLMs that have been created by fine-tuning Llama-2.
    Lawyer LLaMA, Llama 2-Chat, fine-tuned Llama 2 GPT model for financial news analysis, LLaMAntino family of Italian LLMs.

## Notes

In case of problems with getting data from the API (for example: rate limits), the script will default to the files in this folder.



## Improvements

Finetuning with some parameters can be done to improve performance (ex: chunk size, temperature).