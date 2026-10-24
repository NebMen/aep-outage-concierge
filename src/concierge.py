import ollama

def generate_customer_alert(premise_id, time_range, damaged_assets):
    """
    Calls the local Ollama model (Phi-3 Mini) to generate a plain-language customer alert.
    """
    prompt = f"""You are an AI utility concierge for a power company. A severe storm has hit.
    
    Customer Context:
    - Premise ID: {premise_id}
    - Damaged Equipment to Replace: {', '.join(damaged_assets)}
    - Calculated Restoration Time: {time_range}
    
    Task: Draft a concise, empathetic SMS alert to the customer. 
    1. State the estimated restoration range clearly. 
    2. Provide 2 practical safety or preparation tips based on the outage. 
    3. Explicitly disclose that this is an AI estimate based on current network conditions.
    
    Keep the message under 4 sentences. Do not use technical utility jargon."""

    try:
        response = ollama.chat(model='llama3.2:1b', messages=[
            {'role': 'user', 'content': prompt}
        ])
        return response['message']['content']
    except Exception as e:
        return f"System Alert: Unable to reach LLM backend. Please prepare for an outage lasting {time_range}."