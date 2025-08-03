# Customer Service GenAI Routing

Welcome to my project! This project focuses on creating a smart customer service application that directs inquiries to different Large Language Models (LLMs) based on their importance. We use Azure's powerful models for high-priority tasks and a local Ollama instance for more general queries, creating an efficient and cost-effective solution.

## Project Status

🚧  **Status** : `Ongoing..`

## Project Target

The main goal of this project is to build an intelligent customer service system that can:

* **Classify incoming customer tickets** into categories like "technical," "billing," "general," and "escalation".
* **Route tickets to specialized AI agents** , each with a distinct personality and expertise.
* **Dynamically select an LLM provider** based on the ticket's type, using Azure for critical issues and Ollama for standard ones.
* Provide a **web-based chat interface** for users to interact with the AI agents.

---

## Technologies

This project is built with a combination of powerful and flexible technologies to handle everything from the user interface to the AI-powered responses.

### Core Framework

* **Flask** : A lightweight web framework used to build the application's backend and API.
* **Python** : The primary programming language for the application's logic.

### AI and Machine Learning

* **Azure OpenAI** : Used for handling high-priority and complex customer service tickets.
* **Ollama** : A local LLM provider for standard and general inquiries.
* **Google ADK** : The project utilizes the Google Agent Development Kit for its foundation.
* **LiteLLM** : A library for interfacing with multiple LLM providers.

### Frontend

* **HTML, CSS, and JavaScript** : Used to create a clean and user-friendly chat interface.

### Dependencies and Tooling

* **python-dotenv** : For managing environment variables and API keys.
* **requests, httpx, aiohttp** : For making HTTP requests to external services.
* **Jupyter & ipykernel** : Used for developing and testing the notebook version of the project.
* **pandas & numpy** : For data processing and analysis.
* **rich** : To enhance the visual output in the terminal.
* **tiktoken** : For token counting and cost management.
* **pytest & pytest-asyncio** : For testing the application.

---

## Setup

To get this project up and running on your local machine, follow these steps:

1. **Clone the repository:**
   **Bash**

   ```
   git clone https://github.com/bayhaqieee/customer_service_genairouting.git
   ```
2. **Install the required dependencies:**
   **Bash**

   ```
   pip install -r requirements.txt
   ```
3. **Configure your environment variables:**

   * Create a `.env` file in the project's root directory. You can use the `.env.example` file as a template.
   * Add your API keys and model configurations for Azure OpenAI and Ollama.
4. **Run the application:**
   **Bash**

   ```
   python app.py
   ```

The application will be accessible at `http://127.0.0.1:5001` in your web browser.
