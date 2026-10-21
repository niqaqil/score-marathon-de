"""Validated models for normalized marathon timing records."""
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, model_validator

RaceStatus = Literal["FINISHED", "DNF", "DNS", "DSQ", "UNKNOWN"]

class CheckpointSplit(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    checkpoint: str = Field(min_length=1)
    elapsed_seconds: int = Field(ge=0)

class RaceResult(BaseModel):
    """Provider-neutral race result; map source fields before validation."""
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    race_id: str = Field(min_length=1)
    bib: str = Field(min_length=1)
    status: RaceStatus = "UNKNOWN"
    finish_seconds: int | None = Field(default=None, ge=0)
    category: str | None = None
    splits: list[CheckpointSplit] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_finished_time(self):
        if self.status == "FINISHED" and self.finish_seconds is None:
            raise ValueError("finish_seconds is required for FINISHED results")
        return self
