# Import the base class for data models
from pydantic import BaseModel
from datetime import datetime

# Define what a Vulnerability record looks like when returned from the API
class Vulnerability(BaseModel):
    id: int
    source: str
    severity: str
    description: str
    detected_on: datetime
    remediation_status: str
