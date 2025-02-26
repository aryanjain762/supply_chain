import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

def query_llm(prompt, system_prompt="You are a supply chain optimization assistant"):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 600
    }
    
    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"Error querying Groq API: {e}")
        return {"error": str(e)}

@app.route("/api/optimize-transportation", methods=["POST"])
def optimize_transportation():
    data = request.json
    
    origins = data.get("origins", [])
    destinations = data.get("destinations", [])
    volumes = data.get("volumes", [])
    constraints = data.get("constraints", "")
    
    prompt = f"""
    Based on the following transportation data, suggest an optimized logistics plan that minimizes costs:
    
    Origin locations: {origins}
    Destination locations: {destinations}
    Shipment volumes: {volumes}
    Additional constraints: {constraints}
    
    Please provide:
    1. Recommended routing plan
    2. Estimated cost savings compared to standard routing
    3. Key optimization strategies applied
    """
    
    system_prompt = "You are a logistics optimization expert. Provide practical, actionable recommendations."
    response = query_llm(prompt, system_prompt)
    
    return jsonify({"recommendations": response})

@app.route("/api/production-planning", methods=["POST"])
def production_planning():
    data = request.json
    
    products = data.get("products", [])
    demand = data.get("demand", [])
    capacity = data.get("capacity", {})
    lead_times = data.get("lead_times", {})
    
    prompt = f"""
    Based on the following production data, suggest an optimized production schedule:
    
    Products: {products}
    Demand forecast: {demand}
    Production capacity: {capacity}
    Lead times: {lead_times}
    
    Please provide:
    1. Recommended production schedule for the next 4 weeks
    2. Suggested buffer inventory levels
    3. Potential bottlenecks and mitigation strategies
    """
    
    system_prompt = "You are a production planning expert. Provide practical, actionable production schedules."
    response = query_llm(prompt, system_prompt)
    
    return jsonify({"plan": response})

@app.route("/api/decision-support", methods=["POST"])
def decision_support():
    data = request.json
    
    question = data.get("question", "")
    context = data.get("context", {})
    
    prompt = f"""
    Supply Chain Decision Support Question:
    {question}
    
    Context:
    {context}
    
    Please provide a clear, actionable recommendation based on this information.
    Include rationale and any potential risks to consider.
    """
    
    response = query_llm(prompt)
    
    return jsonify({"recommendation": response})

@app.route("/api/chart-data", methods=["POST"])
def get_chart_data():
    data = request.json
    
    weeks = data.get("weeks", ["Week 1", "Week 2", "Week 3", "Week 4"])
    production_volumes = data.get("production_volumes", [1000, 1500, 1200, 1800])
    
    chart_data = {
        "labels": weeks,
        "datasets": [
            {
                "label": "Production Volume",
                "data": production_volumes,
                "backgroundColor": "rgba(75, 192, 192, 0.2)",
                "borderColor": "rgba(75, 192, 192, 1)",
                "borderWidth": 1
            }
        ]
    }
    
    return jsonify(chart_data)

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy"})

if __name__ == "__main__":
    app.run(debug=True, port=5000)