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

1. Activate the virtual environment

        . venv/bin/activate


2. Run the python script


        python main.py
    

3. Wait until the script asks for a prompt. Enter your prompt and you will get a response. You will be repeatedly asked for another prompt; to quit press Enter on an empty prompt.


## Notes

In case of problems with getting data from the API (for example: rate limits), the script will default to the files in this folder.



## Improvements

Finetuning with some parameters can be done to improve performance (ex: chunk size, temperature).