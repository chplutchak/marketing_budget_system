from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CostCenterBase(BaseModel):
    name: str
    code: str
    description: Optional[str] = None
    department: str = "Marketing"

class CostCenterCreate(CostCenterBase):
    pass

class CostCenterUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None
    department: Optional[str] = None
    is_active: Optional[bool] = None

class CostCenter(CostCenterBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True