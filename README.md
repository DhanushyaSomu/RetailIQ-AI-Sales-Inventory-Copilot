TRACK_ID=PS03
# RetailIQ – AI Sales & Inventory Copilot

## Problem

Retail store managers need to continuously monitor sales,
inventory levels, product performance and store performance.

Manually analyzing these datasets can make it difficult to
quickly identify low-stock products, overstock situations,
sales changes and top-performing products.

RetailIQ provides an AI-powered sales and inventory copilot
that allows managers to ask questions using natural language.

## Solution

RetailIQ combines deterministic Python analytics with the
Gemini API.

Python and Pandas calculate the actual business metrics from
the supplied retail datasets.

Gemini 3.5 Flash-Lite then explains those results in natural
language and provides practical recommendations.

The AI is grounded only in the calculated business context.

## Key Features

- Sales dashboard
- Top-selling product analysis
- Low-stock detection
- Overstock detection
- Store performance analysis
- Sales trend/change analysis
- Natural-language AI copilot
- Grounded Gemini responses
- Business recommendations

## Technology Stack

- Python
- Streamlit
- Pandas
- NumPy
- Gemini API
- Gemini 3.5 Flash-Lite
- CSV
- GitHub

## Architecture

CSV Dataset
↓
Python + Pandas
↓
Business Analytics
↓
Relevant Business Context
↓
Gemini 3.5 Flash-Lite
↓
AI Explanation
↓
Retail Manager

## Project Structure

RetailIQ/

├── app.py
├── create_data.py
├── test_analytics.py
├── test_gemini.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/
│   ├── products.csv
│   ├── stores.csv
│   ├── sales.csv
│   └── inventory.csv
│
└── src/
    ├── analytics.py
    └── gemini.py

## Running the Application

Install dependencies:

pip install -r requirements.txt

Run the complete application:

python app.py

The application will be available at:

http://localhost:8000

## Example Questions

The manager can ask:

- Which products are selling the most?
- Which products are low in stock?
- Which store has the highest sales?
- Which products have declining sales?
- What products need immediate attention?
- Where should inventory be replenished?
- Which products are overstocked?

## AI Grounding

RetailIQ does not allow the language model to independently
invent business values.

Sales and inventory calculations are performed using Python
and Pandas.

The resulting structured information is supplied to Gemini
as context.

If the available business data is insufficient to answer a
question, the AI is instructed to state that the available
data is insufficient.

## Data

The project uses locally generated retail datasets containing:

- Products
- Stores
- Sales transactions
- Inventory levels

## Security

The Gemini API key is stored in a `.env` file and excluded
from Git using `.gitignore`.

API keys must never be committed to the repository.
