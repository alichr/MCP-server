# ML API Server

A FastAPI-based machine learning API that provides employee scoring predictions using a Random Forest model.

## Features

- Employee scoring endpoint that predicts based on:
  - Years at Company
  - Employee Satisfaction
  - Position (Manager/Non-Manager)
  - Salary (Ordinal scale 1-5)

## API Usage

### Endpoint
```
POST /
```

### Request Body
```json
{
  "YearsAtCompany": 3.5,
  "EmployeeSatisfaction": 0.85,
  "Position": "Manager",
  "Salary": 4
}
```

### Response
```json
{
  "prediction": 1
}
```

## Setup

1. Install dependencies:
```bash
pip install -r mlapi/requirements.txt
```

2. Run the server:
```bash
cd mlapi
uvicorn mlapi:app --reload
```

The API will be available at `http://localhost:8000`

## Files

- `mlapi/mlapi.py` - FastAPI application with scoring endpoint
- `mlapi/requirements.txt` - Python dependencies
- `mlapi/rfmodel.pkl` - Trained Random Forest model

## Technologies Used

- FastAPI
- Pandas
- Scikit-learn
- Pydantic
- Pickle (for model serialization)
