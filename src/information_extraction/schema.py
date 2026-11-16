from pydantic import BaseModel
from typing import Optional


class MaintenanceReport(BaseModel):
    equipment: Optional[str] = None
    equipment_type: Optional[str] = None
    problem: Optional[str] = None
    symptoms: list[str] = []
    observations: list[str] = []
    actions_performed: list[str] = []
    priority: Optional[str] = None
    missing_information: list[str] = []