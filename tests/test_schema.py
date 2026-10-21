import pytest
from pydantic import ValidationError
from ingestion.schema import RaceResult

def test_valid_finished_result():
    result = RaceResult(race_id="score-2026", bib="101", status="FINISHED", finish_seconds=7200)
    assert result.finish_seconds == 7200

def test_finished_result_requires_time():
    with pytest.raises(ValidationError):
        RaceResult(race_id="score-2026", bib="101", status="FINISHED")

def test_blank_bib_is_rejected():
    with pytest.raises(ValidationError):
        RaceResult(race_id="score-2026", bib="  ", status="DNF")
