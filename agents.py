from enum import Enum
from dataclasses import dataclass
from typing import Optional, Tuple

# Import clients and config variables
from openai import AzureOpenAI, APIConnectionError
import ollama
from config import (
    AZURE_ENDPOINT, AZURE_KEY, AZURE_API_VERSION, AZURE_DEPLOYMENT_NAME,
    OLLAMA_BASE_URL, OLLAMA_MODEL
)

# Client Initialization
azure_client = AzureOpenAI(
    azure_endpoint=AZURE_ENDPOINT,
    api_key=AZURE_KEY,
    api_version=AZURE_API_VERSION,
)

if OLLAMA_BASE_URL:
    ollama.Client(host=OLLAMA_BASE_URL)

# Class Definitions
class TicketType(Enum):
    TECHNICAL = "technical"
    BILLING = "billing"
    GENERAL = "general"
    ESCALATION = "escalation"

@dataclass
class CustomerTicket:
    id: str
    customer_name: str
    issue: str
    type: TicketType
    priority: str = "medium"
    status: str = "open"
    resolution: Optional[str] = None

class CustomerServiceAgent:
    def __init__(self, name: str, specialization: TicketType, personality: str, model_preference: str):
        self.name = name
        self.specialization = specialization
        self.personality = personality
        self.model_preference = model_preference

        if self.model_preference == "pro":
            self.model_name = AZURE_DEPLOYMENT_NAME
        else: # Standard (Ollama)
            self.model_name = OLLAMA_MODEL

    def handle_ticket(self, ticket: CustomerTicket, user_role: str) -> str:
        system_prompt = (
            f"You are {self.name}, a {self.specialization.value} support specialist. "
            f"Your personality is: {self.personality}. "
            f"You are speaking to {ticket.customer_name}, who is a {user_role}. "
            "Address them by name and provide a helpful, professional, and concise response under 150 words."
        )
        user_prompt = f"Issue: {ticket.issue}"
        messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}]

        try:
            if self.model_preference == "pro":
                response = azure_client.chat.completions.create(
                    model=self.model_name, messages=messages, max_tokens=200, temperature=0.7
                )
                resolution = response.choices[0].message.content
            else: # Ollama
                response = ollama.chat(model=self.model_name, messages=messages)
                resolution = response['message']['content']
            return resolution
        except Exception as e:
            return f"Error connecting to the {self.model_preference} service. Please try again later."

# Agent Team Initialization
agent_team = {
    "alex_tech": CustomerServiceAgent(name="Alex", specialization=TicketType.TECHNICAL, personality="Analytical and detail-oriented.", model_preference="pro"),
    "sarah_billing": CustomerServiceAgent(name="Sarah", specialization=TicketType.BILLING, personality="Empathetic and patient.", model_preference="standard"),
    "mike_general": CustomerServiceAgent(name="Mike", specialization=TicketType.GENERAL, personality="Friendly and efficient.", model_preference="standard"),
    "emma_escalation": CustomerServiceAgent(name="Emma", specialization=TicketType.ESCALATION, personality="Calm and authoritative.", model_preference="pro")
}