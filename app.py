from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import json
import os

app = FastAPI(
    title="Message API",
    description="API for receiving and storing messages in JSON files",
    version="1.0.0"
)

class Message(BaseModel):
    content: str
    sender: str

@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.post("/message", tags=["Messages"])
async def save_message(message: Message):
    """
    Save a message to a JSON file
    
    The message will be stored in a JSON file with timestamp as filename
    """
    try:
        # Create data directory if it doesn't exist
        os.makedirs("data", exist_ok=True)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"data/message_{timestamp}.json"
        
        # Prepare message data
        message_data = {
            "content": message.content,
            "sender": message.sender,
            "timestamp": datetime.now().isoformat()
        }
        
        # Save to JSON file
        with open(filename, "w") as f:
            json.dump(message_data, f, indent=4)
            
        return {"status": "success", "filename": filename}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
