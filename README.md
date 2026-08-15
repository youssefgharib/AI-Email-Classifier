# AI Email Classification & Automation

An LLM-powered customer email classification system built with Python. The system analyzes unstructured customer emails and converts them into structured, machine-readable information that can support customer service workflows.

## Overview

Customer service teams receive emails containing different problems, requests, and contextual information. Manually identifying the customer's main issue, urgency, and appropriate next action can be repetitive and time-consuming.

This project uses an LLM API to analyze customer emails and return structured classification results.

The system identifies:

* Primary customer issue
* Secondary actionable issues
* Urgency
* Summary
* Suggested action

## Key Features

* LLM-powered customer email classification
* Primary and secondary issue detection
* Urgency classification
* Automatic email summarization
* Suggested next action
* Structured JSON output
* Schema-based output structure
* Classification rules for distinguishing actionable issues from contextual information
* API error handling
* Environment-based API credential management

## Architecture

```text
Customer Email
      │
      ▼
Python Application
      │
      ▼
Groq LLM API
      │
      ▼
Classification & Analysis
      │
      ▼
Structured JSON Output
      │
      ▼
Customer Service Workflow
```

## Example

### Input

```text
Hi, I received my package today, but the item inside was damaged.
I would like a refund because I cannot use the product.
```

### Output

```json
{
  "primary_category": "shipping",
  "secondary_categories": [],
  "summary": "Customer received a damaged package and requests a full refund.",
  "suggested_action": "Verify the damaged shipment and check refund eligibility under the company's refund policy.",
  "urgency": "medium"
}
```

## Classification Logic

The system is designed to distinguish between:

### Primary Issue

The main problem or request that requires attention.

### Secondary Issue

A second distinct and actionable problem or request.

### Context

Information that provides background but does not represent a separate actionable issue.

A secondary category should not be assigned simply because a category is mentioned in the email.

For example, a customer requesting a refund because their package was damaged should not automatically receive `refund` as a separate category if the refund represents the requested resolution rather than a distinct underlying problem.

## Output Structure

The system produces structured output containing:

```text
primary_category
secondary_categories
urgency
summary
suggested_action
```

This structured approach makes the result easier for downstream software or automation workflows to consume.

## Error Handling

The application includes specific handling for API-related failures, including:

* Authentication errors
* Rate limits
* Invalid requests
* Provider-side errors

## Technologies

* Python
* Groq LLM API
* OpenAI Python SDK
* JSON
* JSON Schema / structured output
* API Integration
* Prompt Engineering
* Environment Variables

## Project Structure

```text
AI-Email-Classifier/
│
├── main.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
└── tests/
    └── test_cases.md
```

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/youssefgharib/AI-Email-Classifier.git
cd AI-Email-Classifier
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate the environment:

**Windows**

```bash
.venv\Scripts\activate
```

**macOS / Linux**

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the API key

Create a `.env` file in the project root:

```text
GROQ_API_KEY=your_groq_api_key_here
```

Never commit the `.env` file to GitHub.

### 5. Run the application

```bash
python main.py
```

## Testing

The classifier was tested against multiple customer email scenarios covering different categories, urgency levels, and multi-issue requests.

Testing focused on:

* Primary category selection
* Secondary category selection
* Urgency classification
* Summary generation
* Suggested action generation
* Distinguishing actionable requests from contextual information
* Structured JSON output consistency

## Future Improvements

Potential future improvements include:

* Connecting the system to a real email inbox
* Processing emails automatically
* Storing classification results
* Adding confidence scoring
* Building a dashboard for reviewing classifications
* Integrating the classifier into a larger customer service automation workflow

## Purpose

This project demonstrates how LLM APIs can be integrated into practical business workflows to transform unstructured customer communication into structured and actionable information.