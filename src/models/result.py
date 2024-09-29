from sqlalchemy import Column, Integer, Float, DateTime
from src.core.database import Base


class Result(Base):
    # TODO(oe): The naming of this table is a bit off, I originally
    # named it results, since I believe it is fitting,
    # therefore the object name Result. 
    #
    # Before submitting I saw it should be named executions.
    __tablename__ = "executions"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, nullable=False)
    commands = Column(Integer, nullable=False)
    result = Column(Integer, nullable=False)
    duration = Column(Float, nullable=False)
