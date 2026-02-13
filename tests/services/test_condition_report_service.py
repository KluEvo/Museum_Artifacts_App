import pytest
import uuid
from datetime import datetime, timezone

from src.services.condition_report_service import ConditionReportService
from src.domain.condition_report import ConditionReport
from src.exceptions import ValidationException, NotFoundException
from tests.mocks.mock_condition_report_repository import MockConditionReportRepository

def make_condition_report() -> ConditionReport:
    return ConditionReport(
        report_id=uuid.uuid4(),
        artifact_id=uuid.uuid4(),
        report_date=datetime.now(timezone.utc),
        condition_rating=4.2,
        notes="Test report",
    )

def test_add_condition_report_positive():
    repo = MockConditionReportRepository()
    svc = ConditionReportService(repo)

    report = make_condition_report()
    new_id = svc.add_condition_report(report)

    assert new_id == "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"

def test_add_condition_report_negative():
    repo = MockConditionReportRepository()
    svc = ConditionReportService(repo)

    with pytest.raises(ValidationException):
        svc.add_condition_report("not a ConditionReport")

def test_get_condition_report_by_id_positive():
    repo = MockConditionReportRepository()
    svc = ConditionReportService(repo)

    report_id = "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
    report = svc.get_condition_report_by_id(report_id)

    assert report is not None
    assert str(report.report_id) == report_id

def test_get_condition_report_by_id_negative():
    repo = MockConditionReportRepository()
    svc = ConditionReportService(repo)

    with pytest.raises(ValidationException) as e:
        svc.get_condition_report_by_id(123)
    assert "ConditionReport ID must be a string." in str(e.value)