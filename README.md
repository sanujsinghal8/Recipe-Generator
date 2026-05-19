 Recipe Generator – Transformer-Based Text Generation
 Overview

Recipe Generator is a Transformer-based text generation system that generates structured cooking recipes from user-provided prompts.

The system leverages sequence modeling and attention mechanisms to produce coherent, context-aware recipe instructions and ingredient lists.

A Streamlit-based UI allows real-time interaction with the model.

 Problem Statement

Creating structured recipes requires:

Understanding ingredient relationships

Maintaining step-wise cooking logic

Generating coherent instructions

Preserving culinary context

Traditional rule-based systems fail to generalize across cuisines.

This project uses a Transformer architecture to model long-range dependencies in cooking instructions.

 Model Architecture

The model is built using a Transformer-based language modeling approach:

Input Prompt → Tokenization → Embedding Layer → Multi-Head Attention → Feed Forward Network → Decoder → Generated Recipe

Key Concepts Used:

Self-Attention Mechanism

Positional Encoding

Autoregressive Text Generation

Sequence-to-Sequence Modeling

 Tech Stack

Python

HuggingFace Transformers (if used)

PyTorch / TensorFlow (whichever applies)

Streamlit (for web interface)

NumPy

 Project Structure
Recipe-Generator/
│
├── app.py
├── examples.py
├── dummy.py
├── meta.py
├── requirements.txt
├── .streamlit/
├── utils/
└── README.md
 Installation

Clone the repository:

git clone https://github.com/AdityaNautiyal927/Recipe-Generator.git
cd Recipe-Generator

Install dependencies:

pip install -r requirements.txt
▶ Run the Application
streamlit run app.py

The application will open in your browser.

 Features

Prompt-based recipe generation

Structured output (Ingredients + Instructions)

Interactive UI via Streamlit

Customizable generation parameters

Example prompts included

 Sample Output

Input Prompt:

Spicy paneer curry

Generated Output:

Ingredients:
- Paneer cubes
- Tomatoes
- Onions
- Spices

Instructions:
1. Heat oil in a pan...
2. Add chopped onions...

Future Improvements

Fine-tuning on domain-specific culinary datasets

Add nutritional analysis

Multi-language support

Deploy on HuggingFace Spaces

Add temperature/top-k controls in UI