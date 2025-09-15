# Employee Churn Prediction System

A comprehensive AI-powered system that predicts employee churn using machine learning models and intelligent agents. The system combines a FastAPI-based ML service, MCP (Model Context Protocol) tools, and a BeeAI framework agent to provide intelligent churn predictions with natural language explanations.

## 🏗️ Architecture

The system consists of three main components:

1. **ML API Server** (`mlapi/`) - FastAPI service with trained Random Forest model
2. **MCP Server** (`employee/`) - Model Context Protocol server that exposes ML predictions as tools
3. **AI Agent** (`singleflowagent.py`) - BeeAI framework agent that orchestrates predictions and provides explanations

## 📁 Project Structure

```
MCP-server/
├── mlapi/                          # ML API Server
│   ├── mlapi.py                   # FastAPI application with churn prediction endpoint
│   ├── requirements.txt           # Python dependencies for ML service
│   └── rfmodel.pkl               # Trained Random Forest model
├── employee/                       # MCP Server & Agent Environment
│   ├── server.py                 # MCP server exposing PredictChurn tool
│   ├── singleflowagent.py        # BeeAI agent implementation
│   ├── pyproject.toml            # Project dependencies (BeeAI, MCP, etc.)
│   ├── uv.lock                   # Dependency lock file
│   └── README.md                 # Employee module documentation
├── singleflowagent.py            # Main agent script (root level)
└── README.md                     # This file
```

## 🚀 Features

- **Machine Learning Predictions**: Random Forest model trained for employee churn prediction
- **MCP Integration**: Exposes ML functionality as tools via Model Context Protocol
- **AI Agent**: Intelligent agent that uses ML predictions and provides natural language explanations
- **RESTful API**: FastAPI-based ML service with JSON endpoints
- **Async Processing**: Fully asynchronous agent workflow
- **Error Handling**: Robust error handling and graceful fallbacks

## 🛠️ Setup & Installation

### Prerequisites

- Python 3.13+
- Ollama (for LLM functionality)
- UV package manager

### 1. ML API Server Setup

```bash
# Install ML dependencies
cd mlapi
pip install -r requirements.txt

# Start the ML API server
uvicorn mlapi:app --reload
```

The ML API will be available at `http://localhost:8000`

### 2. MCP Server & Agent Setup

```bash
# Navigate to employee directory
cd employee

# Install dependencies using UV
uv sync

# Activate virtual environment
source .venv/bin/activate
```

### 3. Ollama Setup

```bash
# Install and start Ollama
ollama serve

# Pull the required model
ollama pull granite3.1-dense:8b
```

## 🎯 Usage

### Running the Complete System

1. **Start the ML API Server** (Terminal 1):
```bash
cd mlapi
uvicorn mlapi:app --reload
```

2. **Start the MCP Server** (Terminal 2):
```bash
cd employee
source .venv/bin/activate
uv run mcp run server.py
```

3. **Run the AI Agent** (Terminal 3):
```bash
source employee/.venv/bin/activate
python singleflowagent.py
```

### API Endpoints

#### ML API - Churn Prediction
```http
POST http://localhost:8000
Content-Type: application/json

{
  "YearsAtCompany": 3.5,
  "EmployeeSatisfaction": 0.85,
  "Position": "Manager",
  "Salary": 4
}
```

**Response:**
```json
{
  "prediction": 1
}
```

#### MCP Tools

The MCP server exposes the following tool:
- **PredictChurn**: Predicts employee churn based on employee attributes

## 🤖 AI Agent Capabilities

The BeeAI agent provides:

- **Intelligent Analysis**: Uses ML predictions combined with domain knowledge
- **Natural Language Explanations**: Provides detailed reasoning for predictions
- **Tool Integration**: Seamlessly uses MCP tools for ML predictions
- **Error Handling**: Graceful fallback when services are unavailable
- **Streaming Responses**: Real-time processing and response generation

### Example Agent Interaction

**Input:**
```python
employee_sample = {
    "YearsAtCompany": 1,
    "EmployeeSatisfaction": 0.01,
    "Position": "Non-Manager",
    "Salary": 2.0
}
```

**Agent Response:**
> "Based on the provided data, there is a low likelihood of this employee churning. The employee has been with the company for only one year, which is typically when turnover rates are higher. However, their Employee Satisfaction score is very high at 0.01, indicating a strong level of contentment. Additionally, they hold a non-managerial position and have a salary that is above average (2.0). These factors suggest that the employee may be satisfied with their current role and compensation, reducing the risk of churn."

## 🔧 Configuration

### Model Parameters

The system uses the following employee attributes for prediction:

- **YearsAtCompany**: Float - Years of employment
- **EmployeeSatisfaction**: Float (0.0-1.0) - Satisfaction score
- **Position**: String - "Manager" or "Non-Manager"
- **Salary**: Integer (1-5) - Ordinal salary scale

### Agent Configuration

The agent is configured with:
- **Model**: `ollama:granite3.1-dense:8b`
- **Max Iterations**: 3
- **Streaming**: Enabled
- **Tools**: MCP PredictChurn tool

## 🛡️ Error Handling

The system includes comprehensive error handling:

- **ML API Unavailable**: Agent falls back to LLM knowledge
- **MCP Tool Failures**: Graceful error handling and retry logic
- **LLM Errors**: Proper error propagation and logging
- **Network Issues**: Timeout handling and connection retries

## 📊 Technologies Used

### ML API
- **FastAPI**: Web framework
- **Pandas**: Data manipulation
- **Scikit-learn**: Machine learning
- **Pydantic**: Data validation
- **Pickle**: Model serialization

### MCP Server
- **FastMCP**: MCP server framework
- **Requests**: HTTP client
- **JSON**: Data serialization

### AI Agent
- **BeeAI Framework**: Agent orchestration
- **Ollama**: Local LLM
- **MCP Client**: Tool integration
- **Asyncio**: Async processing

## 🚦 System Status

To check if all services are running:

```bash
# Check ML API
curl http://localhost:8000/docs

# Check MCP Server
ps aux | grep "mcp.*server.py"

# Check Ollama
ollama ps
```

## 🔄 Development

### Adding New Features

1. **New ML Models**: Add to `mlapi/mlapi.py`
2. **New MCP Tools**: Add to `employee/server.py`
3. **Agent Behavior**: Modify `singleflowagent.py`

### Debugging

Enable debug logging by adding print statements in the agent code or using the built-in BeeAI logging system.

## 📝 License

This project is part of the MCP (Model Context Protocol) ecosystem and follows the Apache 2.0 license.