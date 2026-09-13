from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Literal

class Performance(BaseModel):
    topic: str
    score: float
    confidence: float
    attempts: int = 1

class Resource(BaseModel):
    title: str
    topic: str
    type: str
    minutes: int
    level: str
    url: str
    reason: str

class Session(BaseModel):
    id: str
    day: str
    date: str
    start: str
    end: str
    topic: str
    activity: str
    resource: str = ""
    status: Literal['upcoming','completed','missed','rescheduled'] = 'upcoming'
    score: Optional[float] = None

class StudentState(BaseModel):
    goal: str = 'Master Advanced Data Structures & Algorithms'
    deadline: str = '2026-10-31'
    weekly_hours_target: float = 10
    performance: List[Performance] = Field(default_factory=list)
    sessions: List[Session] = Field(default_factory=list)
    blocked_times: List[Dict[str,str]] = Field(default_factory=list)
    agent_events: List[Dict[str,str]] = Field(default_factory=list)
