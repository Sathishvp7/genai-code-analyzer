# Code Analysis Chatbot

It is a Code Analysis Chatbot that scans any GitHub project and provides comprehensive summaries about its components. Built as a Retrieval-Augmented Generation (RAG) application, it utilizes the Gemini API for large language model capabilities and Chroma DB for knowledge storage, enabling users to interactively ask questions about the specified GitHub repository.

## Overview

Understanding a new codebase can be daunting. This chatbot application simplifies source code exploration by allowing users to input a GitHub project URL and engage in a dialogue about its structure and functionality. It combines retrieval and generation techniques to offer instant insights, helping developers quickly grasp essential aspects of the project.

## Key Features

- **GitHub Project Scanning**: Analyzes the provided GitHub project link to extract key information about its components.
- **Interactive Chatbot Interface**: Users can ask questions in natural language and receive accurate responses about the codebase.
- **Gemini API Integration**: Utilizes the Gemini API for powerful LLM capabilities, enhancing the chatbot's ability to understand and generate relevant answers.
- **Chroma DB Integration**: Uses Chroma DB for efficient knowledge storage, ensuring quick retrieval of information.
- **RAG Architecture**: Combines retrieval and generation processes to provide precise answers and contextual summaries of the project components.
- **Summary Generation**: Offers concise summaries and explanations of various parts of the project, enhancing user understanding.

## Technologies Used

- Python
- Gemini API
- Chroma DB
- Flask (or relevant framework for the web interface)
- GitHub API (for project data retrieval)
- Natural Language Processing (for chatbot functionality)
- Langchain

# How to run?

### STEP 01- Create a Virtual environment

```bash / CMD
python -m venv <envirnoment_name>
```

```bash / CMD
<envirnoment_name>\Scripts\activate 
```


### STEP 02- install the requirements
```bash / CMD
pip install -r requirements.txt
```


### Create a `.env` file in the root directory and add your GEMINI_API_KEY credentials as follows:

```ini
GEMINI_API_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

# Finally run the following command

```bash / CMD
python app.py
```

Now,
```bash / CMD
open up localhost: http://127.0.0.1:8080
 or  http://192.168.1.7:8080
```

### I have utilized the Google Gemini Open Source API for this project. However, you can choose to use any API that suits your needs, including the OpenAI API or Hugging Face models.
