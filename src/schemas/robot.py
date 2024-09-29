from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class Direction(str, Enum):
    NORTH = "north"
    EAST = "east"
    SOUTH = "south"
    WEST = "west"


class Command(BaseModel):
    direction: Direction
    steps: int


class Start(BaseModel):
    x: int
    y: int


class JobRequest(BaseModel):
    start: Start
    commands: list[Command]


class JobResult(BaseModel):
    id: int
    timestamp: datetime
    commands: int
    result: int
    duration: float
