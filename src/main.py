import os
import requests
from fastapi import Depends, FastAPI, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text


from typing import List
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

app = FastAPI(title="Museum API")

running = True

def start():
    print("⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠴⠛⣽⠏⠉⠉⠛⠳⢤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣜⣥⣶⣞⣻⣶⣶⣄⡀⠀⠀⠙⢦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⡿⠉⠁⠀⠀⠀⠀⠉⠛⣶⡀⡀⢨⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⡇⡇⠀⠀⠀⠀⠀⠀⠀⠀⢸⣷⣸⣜⡾⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣷⠃⣷⣶⣷⡄⠠⣿⣿⣿⡆⡞⣟⢿⠘⡄⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣾⠄⡇⠀⠀⡧⠀⠀⠀⠀⠀⢿⠏⣿⡇⢳⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣻⢀⣇⠀⠸⣵⠴⠆⠀⠀⠀⣿⣾⣿⠁⣞⢿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣻⡜⡿⣄⠘⢿⠿⠞⠀⠀⠀⣼⣿⢏⡇⢸⡜⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣼⡅⣿⡷⣍⣙⣁⡤⠔⠛⡇⣻⣾⡀⢸⢡⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⣋⣏⣧⡇⣿⠀⠀⠀⠀⠀⣿⣟⢸⠃⡿⣜⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣟⣿⣧⣹⣿⠀⠀⠀⠀⠘⡇⣇⢸⠀⡇⠈⠱⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣿⡟⠋⠁⠀⠀⠀⠀⠀⠀⣽⢸⢾⢰⠃⠀⠀⠉⠳⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡴⠛⢉⣿⢿⡇⠀⠀⠀⠀⠀⠀⠀⠀⡇⣸⢸⣀⡧⠤⠔⠒⠛⠻⠳⢤⡀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡟⠀⢀⠞⣿⣌⠁⠀⠀⠀⠀⠀⠀⠀⠀⣱⣿⣟⣭⣦⡤⢶⣖⣒⣲⠶⢤⣈⣦⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠠⣴⠋⠀⠀⡼⠀⠈⣺⠵⣶⡤⣤⣤⣤⣤⡴⢛⣧⢿⣿⡟⢛⡟⠉⠀⠀⠈⠙⢦⣬⣹⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⠀⠀⢀⡇⠀⣸⡟⢰⡇⢈⣿⠙⣺⢋⣴⣿⠗⠁⣼⠁⢸⠀⠀⠀⠀⠀⠀⠈⡇⠹⡄⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⡼⠀⠀⠀⠈⡇⠀⣿⠁⣿⢁⣾⢏⡜⣡⣿⣿⠏⠀⢠⡇⠀⡇⠀⠀⠀⠀⠀⠀⣰⠁⠀⢻⡀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⡼⠁⣀⣀⣀⡀⢇⠀⡏⠀⡇⣸⣯⢏⣴⢟⡵⠋⠀⠀⡼⠀⢀⠇⠀⠀⠀⠀⠀⠀⢻⡀⠀⠈⢧⠀⠀⠀\n⠀⠀⠀⠀⠀⣴⠿⠒⠉⠁⠀⠀⠈⠹⡄⠃⠀⠇⢟⣾⡿⠛⠉⠀⠀⠀⢀⡇⠀⢸⠀⠀⠀⠀⠀⠀⠀⠀⢧⠀⠀⠘⡆⠀⠀\n⠀⠀⠀⣠⠏⠃⠀⠀⣀⡤⠤⠦⣄⠀⡇⠀⠀⢠⠟⠁⠀⠀⠀⠀⠀⠀⡼⠀⠀⡏⠀⠀⣀⣀⣀⣀⣀⣀⠼⡆⠀⠀⢹⡀⠀\n⠀⠀⢰⡇⠀⠀⣰⣟⠭⠚⣠⠄⠈⢻⡀⠀⢠⠋⠀⠀⠀⠀⠀⠀⠀⢰⠃⠀⡼⣀⡴⠟⠓⠒⠢⠤⠤⣤⡤⡇⠀⠀⠀⡇⠀\n⠀⢀⡟⠀⠀⠀⣿⡃⠀⡾⠁⢀⡾⡿⠋⠙⠓⠶⠤⣀⡀⠀⠀⠀⣰⠃⠀⣼⠟⣡⡤⠤⢤⣀⠀⠀⠀⠀⠀⣇⠀⠀⠀⢻⡀\n⠀⢸⠁⠀⠀⠀⢿⣆⠀⣷⠀⢼⣰⠁⠀⠀⠀⠀⠀⠀⠈⠳⣤⣼⡁⣠⡾⠷⠏⠀⠈⠉⠀⠈⠓⢤⣀⠀⠀⢻⡄⠀⠀⠘⡇\n⠀⠸⣄⠀⠀⠀⠀⢯⠉⠛⠒⠚⣮⡿⢦⣀⠀⠀⠀⢀⠐⢶⣦⡙⠫⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⣹⣿⠀⠀⠀⢱\n⠀⠀⠘⣷⠀⠀⠀⠈⢧⠀⠀⣾⣩⢥⠀⠈⢢⡀⢤⣈⠳⣄⠙⢿⠲⢬⣢⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⠏⣿⠀⠀⠀⡀\n⠀⠀⢠⠟⠀⠀⠀⠀⠘⡆⠰⣿⢁⣼⡇⠀⠀⠉⣳⣮⣳⣦⣝⣶⣵⣄⠀⠀⣄⡀⢀⣀⠀⣤⣀⡼⢶⠻⡇⠀⢹⡆⠀⠀⠁\n⠀⢠⢿⡀⠀⠀⠀⠀⠀⣷⠀⠙⣿⣞⣰⣻⣿⠛⠒⠛⠒⠛⠛⠚⠛⠋⠉⠉⠑⠒⠛⠛⠉⠉⢀⣤⠏⢀⠇⠀⣼⠇⠀⠀⢀\n⠀⡏⠈⠻⠄⠀⠀⠀⢀⣿⠔⠾⣉⠑⠛⠙⢳⠤⣀⠠⠤⠤⠤⠤⡴⢦⡦⠒⠒⠒⠒⣿⠹⡏⠉⠀⣠⠛⠀⢀⡟⠀⠀⠀⢸\n⢸⡇⠀⠀⠀⠀⢀⣔⡛⠓⢢⠀⠈⠀⠀⠀⣸⠀⡇⠀⠀⠀⠀⢀⡷⠀⢧⠀⠀⠀⢠⡟⠀⣧⠀⡰⠃⠀⠀⢸⠀⠀⠀⢠⡇\n⠈⠉⠀⠀⠀⠀⠁⠀⠈⠁⠀⠀⠀⠀⠀⠈⠁⠀⠁⠀⠀⠀⠀⠈⠀⠀⠈⠀⠀⠀⠈⠁⠀⠉⠈⠁⠀⠀⠀⠉⠀⠀⠀⠈⠀\n⠀⠀⢀⣤⣦⣤⣠⣤⣤⣠⣀⣤⣤⣤⣠⣀⣤⣦⡀⣠⣤⣤⣤⣤⡀⢀⠀⢴⣤⣦⣖⣤⣖⢒⣦⢶⣴⣦⣖⣴⣦⣶⡄⠀⠀\n⠀⠀⠘⠛⠃⠛⠛⠓⠛⠛⠛⠙⠛⠛⠛⠛⠓⠛⠒⠛⡚⠛⠛⠋⠃⠀⠀⢚⠋⠛⠚⠉⠛⠛⠁⠚⠚⠋⢚⢛⠛⠓⠃⠀⠀\n")
    print('Welcome to the museum app. Type \'help\' for a list of commands')
    while running:
        cmd = input('>>>').strip()
        handle_command(cmd)

#TODO: implement get functions
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
    with open('file.sql''r') as file:
        sql_commands = file.read()
        
    try:
        db.execute(text(sql_commands))
        db.commit()
        
        print("SQL file executed successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")


# TODO: Edit all cases for current project
def handle_command(cmd):
    match cmd:
        case 'exit':
            running = False
            print("goodbye!")
        case 'getAllArtifacts':
            get_all_artifacts()
        case 'addArtifact':
            add_artifact()
        case 'findArtifactById':
            find_artifact_by_id()
        case 'findArtifactByName':
            find_artifact_by_name()
        # case 'findArtifactByAccessionNumber':
        #     find_artifact_by_accession_number()
        # case 'findArtifactsByMuseum':
        #     find_artifacts_by_museum()
        # case 'findParentArtifact':
        #     find_parent_artifact()
        case 'removeArtifact':
            remove_artifact()
        case 'updateArtifact':
            update_artifact()
        case 'addLoan':
            add_loan()
        case 'getLoanById':
            get_loan_by_id()
        case 'updateLoan':
            update_loan()
        case 'removeLoan':
            remove_loan()
        case 'getAllMuseums':
            get_all_museums()
        case 'help':
            print("Commands:")
            print("addArtifactremoveArtifactupdateArtifactgetAllArtifactsfindArtifactById")
            print("addLoangetLoanByIdupdateLoandeleteLoan")
            print("getAllMuseums")
            print("helpexit")
        case _:
            print("No valid command detected")

@app.post("/artifact/add", response_model=str)
def add_artifact(
    payload: ArtifactCreate, 
    artifact_svc: ArtifactService = Depends(get_artifact_service)
):
    #Working
    try:
        artifact = Artifact(**payload.model_dump())
        new_artifact_id = artifact_svc.add_artifact(artifact)
        return new_artifact_id
        # return "asd"
    except Exception as e:
        print(f'An unexpected error has occurred: {e}')

@app.get("/artifacts", response_model=List[ArtifactRead])
def get_all_artifacts(
    svc: ArtifactService = Depends(get_artifact_service)
):
    #Working
    artifacts = svc.get_all_artifacts()
    return artifacts

@app.get("/artifact/id", response_model=ArtifactRead)
def find_artifact_by_id(
    id: str = Query(..., min_length=1), 
    svc: ArtifactService = Depends(get_artifact_service)
):
    #Working
    try:
        artifact = svc.find_artifact_by_id(id)
        return artifact
    except Exception as e:
        print(f'An unexpected error has occurred: {e}')
    
@app.get("/artifact/accession", response_model=List[ArtifactRead])
def find_artifact_by_accession_number(
    accession: str = Query(..., min_length=1), 
    svc: ArtifactService = Depends(get_artifact_service)
):
    #Working
    try:
        artifact = svc.find_artifacts_by_accession_number(accession)
        return artifact
    except Exception as e:
        print(f'An unexpected error has occurred: {e}')

@app.get("/artifact/name", response_model=List[ArtifactRead])
def find_artifact_by_name(
    #Working
    name: str = Query(..., min_length=1), 
    svc: ArtifactService = Depends(get_artifact_service)
):
    try:
        artifact = svc.find_artifacts_by_name(name)
        return artifact
    except Exception as e:
        print(f'An unexpected error has occurred: {e}')


@app.put("/artifact/{artifact_id}", response_model=str)
def update_artifact(
    #Working
    artifact_id: str,
    payload: ArtifactUpdate,
    svc: ArtifactService = Depends(get_artifact_service)
):
    try:
        updated_fields = payload.model_dump(exclude_unset=True, exclude_none=True)
        return svc.update_artifact(artifact_id, updated_fields)
    except Exception as e:
        return (f'An unexpected error has occurred: {e}')

@app.delete("/artifact", response_model=str)
def remove_artifact(
    id: str = Query(..., min_length=1), 
    svc: ArtifactService = Depends(get_artifact_service)
):
    #Working
    try: 
        a_id = svc.remove_artifact(id)
        return a_id
    except Exception as e:
        print(f'An unexpected error has occurred: {e}')

@app.delete("/artifact/name", response_model=List[str])
def remove_artifact_name(
    name: str = Query(..., min_length=1), 
    svc: ArtifactService = Depends(get_artifact_service)
):
    #Working
    try: 
        all_named_artifacts = svc.find_artifacts_by_name(name)
        removed_list = []
        for artifact in all_named_artifacts:
            removed = svc.remove_artifact(artifact.artifact_id)
            removed_list.append(removed)

        return removed_list
    except Exception as e:
        print(f'An unexpected error has occurred: {e}')

@app.post("/loan", response_model=str)
def add_loan(
    payload: LoanCreate, 
    loan_svc: LoanService = Depends(get_loan_service)
):
    #Working
    try:
        loan = Loan(**payload.model_dump())
        new_loan_id = loan_svc.add_loan(loan)
        return new_loan_id
    except Exception as e:
        print(f'An unexpected error has occurred: {e}')
        
@app.get("/loan/id", response_model=LoanRead)
def get_loan_by_id(
    id: str = Query(..., min_length=1), 
    svc: LoanService = Depends(get_loan_service)
):
    #Working
    try:
        loan = svc.get_loan_by_id(id)
        return loan
    except Exception as e:
        print(f'An unexpected error has occurred: {e}')

@app.patch("/loan/{loan_id}", response_model=str)
def update_loan(
    loan_id: str, 
    payload: LoanUpdate, 
    svc: LoanService = Depends(get_loan_service)
):
    #Working
    try:
        updated_fields = payload.model_dump(exclude_unset=True, exclude_none=True)
        return svc.update_loan(loan_id, updated_fields)
    except Exception as e:
        print(f'An unexpected error has occurred: {e}')

@app.delete("/loan", response_model=None)
def remove_loan(
    id: str = Query(..., min_length=1),
    svc: LoanService = Depends(get_loan_service)
):
    #Working
    try:
        return svc.remove_loan(id)
    except Exception as e:
        print(f'An unexpected error has occurred: {e}')

@app.get("/museumsall", response_model=List[MuseumRead])
def get_all_museums(
    svc: MuseumService = Depends(get_museum_service)
):
    #Working
    museums = svc.get_all_museums()
    return museums

#Get conditon report on artifact id
@app.get("/condtion", response_model=ConditionReportRead)
def get_condition_report(
    id: str = Query(..., min_length=1), 
    svc: ConditionReportService = Depends(get_condition_report_service)
):
    #Working
    try:
        report = svc.get_condition_report_by_id(id)
        return report
    except Exception as e:
        print(f'An unexpected error has occurred: {e}')

#Get artifact loan by artifact id
@app.get('/loan_contents' , response_model=List[ArtifactRead])
def get_artifacts_in_loan(
    id: str = Query(..., min_length=1), 
    al_svc: ArtifactLoanService = Depends(get_artifact_loan_service),
    artifact_svc: ArtifactService = Depends(get_artifact_service)
):
    #Working
    try:
        artifact_loans = al_svc.get_artifact_loans_by_loan(id)
        artifacts = []
        for artifact_loan in artifact_loans:

            artifacts.append(artifact_svc.find_artifact_by_id(str(artifact_loan.artifact_id)))
        return artifacts
    except Exception as e:
        # dummy test version
        raise HTTPException(status_code=500, detail = f'An unexpected error has occured: {e}')

@app.get('/loan_history' , response_model=List[LoanRead])
def get_loan_history_of_artifact(
    id: str = Query(..., min_length=1), 
    al_svc: ArtifactLoanService = Depends(get_artifact_loan_service),
    loan_svc: LoanService = Depends(get_loan_service)
):
    #Working
    try:
        artifact_loans = al_svc.get_artifact_loans_by_artifact(id)
        loans = []
        for artifact_loan in artifact_loans:
            loans.append(loan_svc.get_loan_by_id(str(artifact_loan.loan_id)))
        return loans
    except Exception as e:
        # dummy test version 
        raise HTTPException(status_code=500, detail = f'An unexpected error has occured: {e}')


@app.get("/artifacts/from_museum", response_model=List[ArtifactRead])
def get_all_artifacts_of_a_museum(
    id: str = Query(..., min_length=1), 
    svc: ArtifactService = Depends(get_artifact_service)
):
    #Working
    try:
        artifacts = svc.find_artifacts_by_museum(id)
        return artifacts
    except Exception as e:
        print(f'An unexpected error has occured: {e}')

@app.get("/artifact/count", response_model=int)
def get_num_artifacts( 
    svc: ArtifactService = Depends(get_artifact_service)
):
    #Working
    try:
        count = svc.get_artifact_count()
        return count
    except Exception as e:
        print(f'An unexpected error has occured: {e}')

