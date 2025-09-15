# Bring in lightweight dependencies
from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import pandas as pd
import os


app = FastAPI()

class ScoringItem(BaseModel): 
    YearsAtCompany: float #/ 1, // Float value 
    EmployeeSatisfaction: float #0.01, // Float value 
    Position:str # "Non-Manager", # Manager or Non-Manager
    Salary: int #4.0 // Ordinal 1,2,3,4,5


# Get the directory where this script is located
current_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(current_dir, 'rfmodel.pkl')

with open(model_path, 'rb') as f: 
    model = pickle.load(f)

@app.post('/')
async def scoring_endpoint(item:ScoringItem): 
    df = pd.DataFrame([item.dict().values()], columns=item.dict().keys())
    yhat = model.predict(df)
    return {"prediction":int(yhat)}