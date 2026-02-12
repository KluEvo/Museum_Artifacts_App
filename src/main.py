import os
import requests
from fastapi import Depends, FastAPI, Query
from sqlalchemy.orm import Session
from sqlalchemy import text


from typing import List
from src.db.deps import get_db
from src.domain.artifact import Artifact
from src.dto.artifact import ArtifactCreate, ArtifactRead
from src.dto.loan import LoanCreate, LoanRead
from src.dto.condition_report import ConditionReportCreate, ConditionReportRead
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

def get_artifact_service(repo: ArtifactRepository = Depends(get_artifact_repository)) -> ArtifactService:
    return ArtifactService(repo)

def get_loan_repository(db: Session = Depends(get_db)) -> LoanRepository:
    return LoanRepository(db)

def get_loan_service(repo: LoanRepository = Depends(get_loan_repository)) -> LoanService:
    return LoanService(repo)

def get_museum_repository(db: Session = Depends(get_db)) -> MuseumRepository:
    return MuseumRepository(db)

def get_museum_service(repo: MuseumRepository = Depends(get_museum_repository)) -> MuseumService:
    return MuseumService(repo)

def get_artifact_loan_repository(db: Session = Depends(get_db)) -> ArtifactLoanRepository:
    return ArtifactLoanRepository(db)

def get_artifact_loan_service(repo: ArtifactLoanRepository = Depends(get_artifact_loan_repository)) -> ArtifactLoanService:
    return ArtifactLoanService(repo)

def get_condition_report_repository(db: Session = Depends(get_db)) -> ConditionReportRepository:
    return ConditionReportRepository(db)

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
    artifacts = svc.get_all_artifacts()
    return artifacts

@app.get("/artifact/search", response_model=List[ArtifactRead])
def find_artifact_by_id(
    id: str = Query(..., min_length=1), 
    svc: ArtifactService = Depends(get_artifact_service)
):
    #See if query works as intended
    artifact = svc.find_artifact_by_id(id)
    print(artifact)

@app.put("/artifact/{artifact_id}", response_model=str)
def update_artifact(
    artifact_id: str, 
    payload: ArtifactCreate, 
    svc: ArtifactService = Depends(get_artifact_service)
):
    try:
        updated_fields = payload.model_dump(exclude_unset=True, exclude_none=True)
        svc.update_artifact(artifact_id, updated_fields)
    except Exception as e:
        print(f'An unexpected error has occurred: {e}')



#TODO: figure out how to return what was deleted or some sort of confirmation message
@app.delete("/artifact", response_model=str)
def remove_artifact(
    id: str = Query(..., min_length=1), 
    svc: ArtifactService = Depends(get_artifact_service)
):
    try: 
        a_id = svc.remove_artifact(id)
        return a_id
    except Exception as e:
        print(f'An unexpected error has occurred: {e}')

@app.delete("/artifact/name", response_model=List[str])
def remove_artifact(
    name: str = Query(..., min_length=1), 
    svc: ArtifactService = Depends(get_artifact_service)
):
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
def add_loan():
    #Add implementation
    pass

@app.get("/loan", response_model=List[LoanRead])
def get_loan_by_id():
    #Add implementation
    pass

@app.patch("/loan", response_model=str)
def update_loan():
    #Add implementation
    pass

@app.delete("/loan", response_model=None)
def remove_loan(id: str = Query(..., min_length=1), svc: LoanService = Depends(get_loan_service)):
    #Add implementation
    try:
        return svc.remove_loan(id)
    except Exception as e:
        print(f'An unexpected error has occurred: {e}')
    pass

@app.get("/museumsall", response_model=List[MuseumRead])
def get_all_museums(svc: MuseumService = Depends(get_museum_service)):
    museums = svc.get_all_museums()
    return museums
