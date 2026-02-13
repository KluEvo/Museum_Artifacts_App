import os
import requests
from fastapi import Depends, FastAPI, Query, HTTPException, Request
from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi.responses import JSONResponse
from src.exceptions import AppErrorException
from typing import List
import logging


from src.db.deps import get_db
from src.domain.artifact import Artifact
from src.domain.loan import Loan
from src.dto.artifact import ArtifactCreate, ArtifactRead, ArtifactUpdate
from src.dto.loan import LoanCreate, LoanRead, LoanUpdate
from src.dto.condition_report import ConditionReportCreate, ConditionReportRead
from src.dto.artifact_loan import ArtifactLoanCreate, ArtifactLoanRead
from src.dto.museum import MuseumCreate, MuseumRead
from src.repositories.artifact_repository import ArtifactRepository
from src.repositories.loan_repository import LoanRepository
from src.repositories.museum_repository import MuseumRepository
from src.repositories.artifact_loan_repository import ArtifactLoanRepository
from src.repositories.condition_report_repository import ConditionReportRepository
from src.services.artifact_service import ArtifactService
from src.services.loan_service import LoanService
from src.services.museum_service import MuseumService
from src.services.artifact_loan_service import ArtifactLoanService
from src.services.condition_report_service import ConditionReportService

# Initialize FastAPI app
app = FastAPI(title="Museum API")
running = True

# Set up logging and exception handlers
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
@app.exception_handler(AppErrorException)
async def app_exception_handler(request: Request, exc: AppErrorException):
    logger.warning(f"Application error: {exc}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": str(exc)}
    )
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled Exception occurred")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error occurred."}
    )

def start():
    print("⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠴⠛⣽⠏⠉⠉⠛⠳⢤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣜⣥⣶⣞⣻⣶⣶⣄⡀⠀⠀⠙⢦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⡿⠉⠁⠀⠀⠀⠀⠉⠛⣶⡀⡀⢨⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⡇⡇⠀⠀⠀⠀⠀⠀⠀⠀⢸⣷⣸⣜⡾⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣷⠃⣷⣶⣷⡄⠠⣿⣿⣿⡆⡞⣟⢿⠘⡄⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣾⠄⡇⠀⠀⡧⠀⠀⠀⠀⠀⢿⠏⣿⡇⢳⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣻⢀⣇⠀⠸⣵⠴⠆⠀⠀⠀⣿⣾⣿⠁⣞⢿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣻⡜⡿⣄⠘⢿⠿⠞⠀⠀⠀⣼⣿⢏⡇⢸⡜⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣼⡅⣿⡷⣍⣙⣁⡤⠔⠛⡇⣻⣾⡀⢸⢡⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⣋⣏⣧⡇⣿⠀⠀⠀⠀⠀⣿⣟⢸⠃⡿⣜⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣟⣿⣧⣹⣿⠀⠀⠀⠀⠘⡇⣇⢸⠀⡇⠈⠱⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣿⡟⠋⠁⠀⠀⠀⠀⠀⠀⣽⢸⢾⢰⠃⠀⠀⠉⠳⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡴⠛⢉⣿⢿⡇⠀⠀⠀⠀⠀⠀⠀⠀⡇⣸⢸⣀⡧⠤⠔⠒⠛⠻⠳⢤⡀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡟⠀⢀⠞⣿⣌⠁⠀⠀⠀⠀⠀⠀⠀⠀⣱⣿⣟⣭⣦⡤⢶⣖⣒⣲⠶⢤⣈⣦⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠠⣴⠋⠀⠀⡼⠀⠈⣺⠵⣶⡤⣤⣤⣤⣤⡴⢛⣧⢿⣿⡟⢛⡟⠉⠀⠀⠈⠙⢦⣬⣹⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⠀⠀⢀⡇⠀⣸⡟⢰⡇⢈⣿⠙⣺⢋⣴⣿⠗⠁⣼⠁⢸⠀⠀⠀⠀⠀⠀⠈⡇⠹⡄⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⡼⠀⠀⠀⠈⡇⠀⣿⠁⣿⢁⣾⢏⡜⣡⣿⣿⠏⠀⢠⡇⠀⡇⠀⠀⠀⠀⠀⠀⣰⠁⠀⢻⡀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⡼⠁⣀⣀⣀⡀⢇⠀⡏⠀⡇⣸⣯⢏⣴⢟⡵⠋⠀⠀⡼⠀⢀⠇⠀⠀⠀⠀⠀⠀⢻⡀⠀⠈⢧⠀⠀⠀\n⠀⠀⠀⠀⠀⣴⠿⠒⠉⠁⠀⠀⠈⠹⡄⠃⠀⠇⢟⣾⡿⠛⠉⠀⠀⠀⢀⡇⠀⢸⠀⠀⠀⠀⠀⠀⠀⠀⢧⠀⠀⠘⡆⠀⠀\n⠀⠀⠀⣠⠏⠃⠀⠀⣀⡤⠤⠦⣄⠀⡇⠀⠀⢠⠟⠁⠀⠀⠀⠀⠀⠀⡼⠀⠀⡏⠀⠀⣀⣀⣀⣀⣀⣀⠼⡆⠀⠀⢹⡀⠀\n⠀⠀⢰⡇⠀⠀⣰⣟⠭⠚⣠⠄⠈⢻⡀⠀⢠⠋⠀⠀⠀⠀⠀⠀⠀⢰⠃⠀⡼⣀⡴⠟⠓⠒⠢⠤⠤⣤⡤⡇⠀⠀⠀⡇⠀\n⠀⢀⡟⠀⠀⠀⣿⡃⠀⡾⠁⢀⡾⡿⠋⠙⠓⠶⠤⣀⡀⠀⠀⠀⣰⠃⠀⣼⠟⣡⡤⠤⢤⣀⠀⠀⠀⠀⠀⣇⠀⠀⠀⢻⡀\n⠀⢸⠁⠀⠀⠀⢿⣆⠀⣷⠀⢼⣰⠁⠀⠀⠀⠀⠀⠀⠈⠳⣤⣼⡁⣠⡾⠷⠏⠀⠈⠉⠀⠈⠓⢤⣀⠀⠀⢻⡄⠀⠀⠘⡇\n⠀⠸⣄⠀⠀⠀⠀⢯⠉⠛⠒⠚⣮⡿⢦⣀⠀⠀⠀⢀⠐⢶⣦⡙⠫⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⣹⣿⠀⠀⠀⢱\n⠀⠀⠘⣷⠀⠀⠀⠈⢧⠀⠀⣾⣩⢥⠀⠈⢢⡀⢤⣈⠳⣄⠙⢿⠲⢬⣢⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⠏⣿⠀⠀⠀⡀\n⠀⠀⢠⠟⠀⠀⠀⠀⠘⡆⠰⣿⢁⣼⡇⠀⠀⠉⣳⣮⣳⣦⣝⣶⣵⣄⠀⠀⣄⡀⢀⣀⠀⣤⣀⡼⢶⠻⡇⠀⢹⡆⠀⠀⠁\n⠀⢠⢿⡀⠀⠀⠀⠀⠀⣷⠀⠙⣿⣞⣰⣻⣿⠛⠒⠛⠒⠛⠛⠚⠛⠋⠉⠉⠑⠒⠛⠛⠉⠉⢀⣤⠏⢀⠇⠀⣼⠇⠀⠀⢀\n⠀⡏⠈⠻⠄⠀⠀⠀⢀⣿⠔⠾⣉⠑⠛⠙⢳⠤⣀⠠⠤⠤⠤⠤⡴⢦⡦⠒⠒⠒⠒⣿⠹⡏⠉⠀⣠⠛⠀⢀⡟⠀⠀⠀⢸\n⢸⡇⠀⠀⠀⠀⢀⣔⡛⠓⢢⠀⠈⠀⠀⠀⣸⠀⡇⠀⠀⠀⠀⢀⡷⠀⢧⠀⠀⠀⢠⡟⠀⣧⠀⡰⠃⠀⠀⢸⠀⠀⠀⢠⡇\n⠈⠉⠀⠀⠀⠀⠁⠀⠈⠁⠀⠀⠀⠀⠀⠈⠁⠀⠁⠀⠀⠀⠀⠈⠀⠀⠈⠀⠀⠀⠈⠁⠀⠉⠈⠁⠀⠀⠀⠉⠀⠀⠀⠈⠀\n⠀⠀⢀⣤⣦⣤⣠⣤⣤⣠⣀⣤⣤⣤⣠⣀⣤⣦⡀⣠⣤⣤⣤⣤⡀⢀⠀⢴⣤⣦⣖⣤⣖⢒⣦⢶⣴⣦⣖⣴⣦⣶⡄⠀⠀\n⠀⠀⠘⠛⠃⠛⠛⠓⠛⠛⠛⠙⠛⠛⠛⠛⠓⠛⠒⠛⡚⠛⠛⠋⠃⠀⠀⢚⠋⠛⠚⠉⠛⠛⠁⠚⠚⠋⢚⢛⠛⠓⠃⠀⠀\n")
    print('Welcome to the museum app. Type \'help\' for a list of commands')


def get_artifact_repository(db: Session = Depends(get_db)) -> ArtifactRepository:
    return ArtifactRepository(db)

def get_loan_repository(db: Session = Depends(get_db)) -> LoanRepository:
    return LoanRepository(db)

def get_museum_repository(db: Session = Depends(get_db)) -> MuseumRepository:
    return MuseumRepository(db)

def get_artifact_loan_repository(db: Session = Depends(get_db)) -> ArtifactLoanRepository:
    return ArtifactLoanRepository(db)

def get_condition_report_repository(db: Session = Depends(get_db)) -> ConditionReportRepository:
    return ConditionReportRepository(db)

def get_artifact_service(
        artifact_repo: ArtifactRepository = Depends(get_artifact_repository), 
        museum_repo: MuseumRepository = Depends(get_museum_repository)) -> ArtifactService:
    return ArtifactService(artifact_repo, museum_repo)

def get_loan_service(repo: LoanRepository = Depends(get_loan_repository)) -> LoanService:
    return LoanService(repo)

def get_museum_service(repo: MuseumRepository = Depends(get_museum_repository)) -> MuseumService:
    return MuseumService(repo)

def get_artifact_loan_service(repo: ArtifactLoanRepository = Depends(get_artifact_loan_repository)) -> ArtifactLoanService:
    return ArtifactLoanService(repo)

def get_condition_report_service(repo: ConditionReportRepository = Depends(get_condition_report_repository)) -> ConditionReportService:
    return ConditionReportService(repo)

# function to run a sql file "file.sql":
def run_sql(db: Session = Depends(get_db)):
    with open('file.sql', 'r') as file:
        sql_commands = file.read()
    db.execute(text(sql_commands))
    db.commit()


@app.post("/artifact/add", response_model=str)
def add_artifact(payload: ArtifactCreate, artifact_svc: ArtifactService = Depends(get_artifact_service)):
    artifact = Artifact(**payload.model_dump())
    return artifact_svc.add_artifact(artifact)

@app.get("/artifacts", response_model=List[ArtifactRead])
def get_all_artifacts(
    svc: ArtifactService = Depends(get_artifact_service)
):
    return svc.get_all_artifacts()

@app.get("/artifact/id", response_model=ArtifactRead)
def find_artifact_by_id(id: str = Query(..., min_length=1),
     svc: ArtifactService = Depends(get_artifact_service)
):
    return svc.find_artifact_by_id(id)
    
@app.get("/artifact/accession", response_model=List[ArtifactRead])
def find_artifact_by_accession_number(
    accession: str = Query(..., min_length=1), 
    svc: ArtifactService = Depends(get_artifact_service)
):
    return svc.find_artifacts_by_accession_number(accession)

@app.get("/artifact/name", response_model=List[ArtifactRead])
def find_artifact_by_name(
    name: str = Query(..., min_length=1), 
    svc: ArtifactService = Depends(get_artifact_service)
):
    return svc.find_artifacts_by_name(name)


@app.put("/artifact/{artifact_id}", response_model=str)
def update_artifact(
    artifact_id: str,
    payload: ArtifactUpdate,
    svc: ArtifactService = Depends(get_artifact_service)
):
    updated_fields = payload.model_dump(exclude_unset=True, exclude_none=True)
    return svc.update_artifact(artifact_id, updated_fields)

@app.delete("/artifact", response_model=str)
def remove_artifact(
    id: str = Query(..., min_length=1), 
    svc: ArtifactService = Depends(get_artifact_service)
):
    return svc.remove_artifact(id)

@app.delete("/artifact/name", response_model=List[str])
def remove_artifact_name(
    name: str = Query(..., min_length=1), 
    svc: ArtifactService = Depends(get_artifact_service)
):
    all_named_artifacts = svc.find_artifacts_by_name(name)
    removed_list = []
    for artifact in all_named_artifacts:
        removed = svc.remove_artifact(artifact.artifact_id)
        removed_list.append(removed)
    return removed_list

@app.post("/loan", response_model=str)
def add_loan(
    payload: LoanCreate, 
    loan_svc: LoanService = Depends(get_loan_service)
):
    loan = Loan(**payload.model_dump())
    return loan_svc.add_loan(loan)
        
@app.get("/loan/id", response_model=LoanRead)
def get_loan_by_id(
    id: str = Query(..., min_length=1), 
    svc: LoanService = Depends(get_loan_service)
):
    return svc.get_loan_by_id(id)

@app.patch("/loan/{loan_id}", response_model=str)
def update_loan(
    loan_id: str, 
    payload: LoanUpdate, 
    svc: LoanService = Depends(get_loan_service)
):
    updated_fields = payload.model_dump(exclude_unset=True, exclude_none=True)
    return svc.update_loan(loan_id, updated_fields)

@app.delete("/loan", response_model=None)
def remove_loan(
    id: str = Query(..., min_length=1),
    svc: LoanService = Depends(get_loan_service)
):
    return svc.remove_loan(id)

@app.get("/museumsall", response_model=List[MuseumRead])
def get_all_museums(
    svc: MuseumService = Depends(get_museum_service)
):
    #Working
    return svc.get_all_museums()

#Get conditon report on artifact id
@app.get("/condition", response_model=ConditionReportRead)
def get_condition_report(
    id: str = Query(..., min_length=1), 
    svc: ConditionReportService = Depends(get_condition_report_service)
):
    #Working
    report = svc.get_condition_report_by_id(id)
    return report

#Get artifact's loan history by artifact id
@app.get('/loan_contents' , response_model=List[ArtifactRead])
def get_artifacts_in_loan(
    id: str = Query(..., min_length=1), 
    al_svc: ArtifactLoanService = Depends(get_artifact_loan_service),
    artifact_svc: ArtifactService = Depends(get_artifact_service)
):
    artifact_loans = al_svc.get_artifact_loans_by_loan(id)
    artifacts = []
    for artifact_loan in artifact_loans:

        artifacts.append(artifact_svc.find_artifact_by_id(str(artifact_loan.artifact_id)))
    return artifacts

@app.get('/loan_history' , response_model=List[LoanRead])
def get_loan_history_of_artifact(
    id: str = Query(..., min_length=1), 
    al_svc: ArtifactLoanService = Depends(get_artifact_loan_service),
    loan_svc: LoanService = Depends(get_loan_service)
):
    artifact_loans = al_svc.get_artifact_loans_by_artifact(id)
    loans = []
    for artifact_loan in artifact_loans:
        loans.append(loan_svc.get_loan_by_id(str(artifact_loan.loan_id)))
    return loans
    
#Get artifact loan details for specific artifact and loan
@app.get('/artifact_loan' , response_model=ArtifactLoanRead)
def get_artifacts_loan(
    artifact_id: str = Query(..., min_length=1),
    loan_id: str = Query(..., min_length=1), 
    al_svc: ArtifactLoanService = Depends(get_artifact_loan_service)
):
    artifact_loans = al_svc.get_artifact_loan_by_ids(artifact_id, loan_id)
    return artifact_loans
    
@app.get("/artifacts/from_museum", response_model=List[ArtifactRead])
def get_all_artifacts_of_a_museum(
    id: str = Query(..., min_length=1), 
    svc: ArtifactService = Depends(get_artifact_service)
):
    artifacts = svc.find_artifacts_by_museum(id)
    return artifacts

@app.get("/artifact/count", response_model=int)
def get_num_artifacts( 
    svc: ArtifactService = Depends(get_artifact_service)
):
    count = svc.get_artifact_count()
    return count


if __name__ == "__main__":
    start()