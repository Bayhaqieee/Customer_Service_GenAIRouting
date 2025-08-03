from typing import Dict
from agents import CustomerServiceAgent, TicketType

class IntelligentRouter:
    def __init__(self, agent_team: Dict[str, CustomerServiceAgent]):
        self.agent_team = agent_team
        self.classification_keywords = {
            TicketType.TECHNICAL: ['bug', 'error', 'crash', 'login', 'password', 'setup', 'install', 'technical', 'not working'],
            TicketType.BILLING: ['bill', 'charge', 'payment', 'refund', 'invoice', 'subscription', 'pricing', 'cost'],
            TicketType.GENERAL: ['question', 'how to', 'information', 'help', 'support', 'general'],
            TicketType.ESCALATION: ['manager', 'complaint', 'urgent', 'escalate', 'supervisor', 'legal', 'dispute']
        }

    def classify_ticket(self, issue_text: str) -> TicketType:
        issue_lower = issue_text.lower()
        # Escalation has the highest priority
        if any(keyword in issue_lower for keyword in self.classification_keywords[TicketType.ESCALATION]):
            return TicketType.ESCALATION
        
        scores = {
            ttype: sum(1 for kw in kws if kw in issue_lower)
            for ttype, kws in self.classification_keywords.items()
        }
        
        # Find the type with the highest score, default to GENERAL if no keywords match
        if max(scores.values()) > 0:
            return max(scores, key=scores.get)
        return TicketType.GENERAL

    def route_to_agent(self, ticket_type: TicketType) -> CustomerServiceAgent:
        # Find an agent that specializes in this ticket type
        for agent in self.agent_team.values():
            if agent.specialization == ticket_type:
                return agent
        # Fallback to a general agent if no specialist is found
        return self.agent_team["mike_general"]