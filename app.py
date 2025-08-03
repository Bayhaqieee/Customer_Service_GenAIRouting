from flask import Flask, render_template, request, jsonify
import uuid
from config import validate_config
from agents import agent_team, CustomerTicket
from router import IntelligentRouter

# Initialization
app = Flask(__name__)
validate_config()  # Check .env file on startup
intelligent_router = IntelligentRouter(agent_team)

# Routes
@app.route('/')
def index():
    """Renders the main chat page."""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handles the chat message from the user."""
    data = request.json
    user_name = data.get('name')
    user_role = data.get('role')
    user_message = data.get('message')

    if not all([user_name, user_role, user_message]):
        return jsonify({'error': 'Missing name, role, or message'}), 400

    # 1. Classify the user's message
    ticket_type = intelligent_router.classify_ticket(user_message)

    # 2. Route to the appropriate agent
    agent = intelligent_router.route_to_agent(ticket_type)

    # 3. Create a ticket object for context
    ticket = CustomerTicket(
        id=str(uuid.uuid4()),
        customer_name=user_name,
        issue=user_message,
        type=ticket_type
    )

    # 4. Get the response from the agent
    response_text = agent.handle_ticket(ticket, user_role)

    return jsonify({
        'agent_name': agent.name,
        'agent_specialization': agent.specialization.value,
        'response': response_text
    })

if __name__ == '__main__':
    app.run(debug=True, port=5001)