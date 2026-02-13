from typing import List
from sqlalchemy.orm import Session
from src.domain.condition_report import ConditionReport
from src.repositories.condition_report_repository_protocol import ConditionReportRepositoryProtocol

class ConditionReportRepository(ConditionReportRepositoryProtocol):
    def __init__(self, session: Session):
        self.session = session

    def get_all_reports(self) -> List[ConditionReport]:
        return self.session.query(ConditionReport).all()

    def add_report(self, report: ConditionReport) -> ConditionReport:
        self.session.add(report)
        self.session.commit()
        return str(report.report_id)

    def get_report_by_id(self, report_id: str) -> ConditionReport:
        return self.session.query(ConditionReport).filter(ConditionReport.report_id == report_id).first()

    def get_reports_by_artifact(self, artifact_id: str) -> List[ConditionReport]:
        return self.session.query(ConditionReport).filter(ConditionReport.artifact_id == artifact_id).all()

    def update_report(self, report_id: str, updated_fields_dict: dict) -> str:
        report = self.session.get(ConditionReport, report_id)
        
        if not report:
            return None

        
        allowed_fields = {col.name for col in ConditionReport.__table__.columns if not col.primary_key}

        for field, value in updated_fields_dict.items():
            if field not in allowed_fields:
                raise ValueError(f"Field not updatable: {field}")
            setattr(report, field, value)

        self.session.commit()
        self.session.refresh(report)
        return str(report.report_id)

    def remove_report(self, report_id: str) -> str:
        report = self.get_report_by_id(report_id)
        if not report:
            return None
        self.session.delete(report)
        self.session.commit()
        return str(report.report_id)
    
    
