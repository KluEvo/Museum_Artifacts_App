import os
import requests
from fastapi import Depends, FastAPI, Query

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

class main:
    def __init__(self):
        self.running = True

    def start(self):
        print("⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠴⠛⣽⠏⠉⠉⠛⠳⢤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣜⣥⣶⣞⣻⣶⣶⣄⡀⠀⠀⠙⢦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⡿⠉⠁⠀⠀⠀⠀⠉⠛⣶⡀⡀⢨⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⡇⡇⠀⠀⠀⠀⠀⠀⠀⠀⢸⣷⣸⣜⡾⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣷⠃⣷⣶⣷⡄⠠⣿⣿⣿⡆⡞⣟⢿⠘⡄⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣾⠄⡇⠀⠀⡧⠀⠀⠀⠀⠀⢿⠏⣿⡇⢳⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣻⢀⣇⠀⠸⣵⠴⠆⠀⠀⠀⣿⣾⣿⠁⣞⢿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣻⡜⡿⣄⠘⢿⠿⠞⠀⠀⠀⣼⣿⢏⡇⢸⡜⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣼⡅⣿⡷⣍⣙⣁⡤⠔⠛⡇⣻⣾⡀⢸⢡⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⣋⣏⣧⡇⣿⠀⠀⠀⠀⠀⣿⣟⢸⠃⡿⣜⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣟⣿⣧⣹⣿⠀⠀⠀⠀⠘⡇⣇⢸⠀⡇⠈⠱⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣿⡟⠋⠁⠀⠀⠀⠀⠀⠀⣽⢸⢾⢰⠃⠀⠀⠉⠳⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡴⠛⢉⣿⢿⡇⠀⠀⠀⠀⠀⠀⠀⠀⡇⣸⢸⣀⡧⠤⠔⠒⠛⠻⠳⢤⡀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡟⠀⢀⠞⣿⣌⠁⠀⠀⠀⠀⠀⠀⠀⠀⣱⣿⣟⣭⣦⡤⢶⣖⣒⣲⠶⢤⣈⣦⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠠⣴⠋⠀⠀⡼⠀⠈⣺⠵⣶⡤⣤⣤⣤⣤⡴⢛⣧⢿⣿⡟⢛⡟⠉⠀⠀⠈⠙⢦⣬⣹⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⠀⠀⢀⡇⠀⣸⡟⢰⡇⢈⣿⠙⣺⢋⣴⣿⠗⠁⣼⠁⢸⠀⠀⠀⠀⠀⠀⠈⡇⠹⡄⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⡼⠀⠀⠀⠈⡇⠀⣿⠁⣿⢁⣾⢏⡜⣡⣿⣿⠏⠀⢠⡇⠀⡇⠀⠀⠀⠀⠀⠀⣰⠁⠀⢻⡀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⡼⠁⣀⣀⣀⡀⢇⠀⡏⠀⡇⣸⣯⢏⣴⢟⡵⠋⠀⠀⡼⠀⢀⠇⠀⠀⠀⠀⠀⠀⢻⡀⠀⠈⢧⠀⠀⠀\n⠀⠀⠀⠀⠀⣴⠿⠒⠉⠁⠀⠀⠈⠹⡄⠃⠀⠇⢟⣾⡿⠛⠉⠀⠀⠀⢀⡇⠀⢸⠀⠀⠀⠀⠀⠀⠀⠀⢧⠀⠀⠘⡆⠀⠀\n⠀⠀⠀⣠⠏⠃⠀⠀⣀⡤⠤⠦⣄⠀⡇⠀⠀⢠⠟⠁⠀⠀⠀⠀⠀⠀⡼⠀⠀⡏⠀⠀⣀⣀⣀⣀⣀⣀⠼⡆⠀⠀⢹⡀⠀\n⠀⠀⢰⡇⠀⠀⣰⣟⠭⠚⣠⠄⠈⢻⡀⠀⢠⠋⠀⠀⠀⠀⠀⠀⠀⢰⠃⠀⡼⣀⡴⠟⠓⠒⠢⠤⠤⣤⡤⡇⠀⠀⠀⡇⠀\n⠀⢀⡟⠀⠀⠀⣿⡃⠀⡾⠁⢀⡾⡿⠋⠙⠓⠶⠤⣀⡀⠀⠀⠀⣰⠃⠀⣼⠟⣡⡤⠤⢤⣀⠀⠀⠀⠀⠀⣇⠀⠀⠀⢻⡀\n⠀⢸⠁⠀⠀⠀⢿⣆⠀⣷⠀⢼⣰⠁⠀⠀⠀⠀⠀⠀⠈⠳⣤⣼⡁⣠⡾⠷⠏⠀⠈⠉⠀⠈⠓⢤⣀⠀⠀⢻⡄⠀⠀⠘⡇\n⠀⠸⣄⠀⠀⠀⠀⢯⠉⠛⠒⠚⣮⡿⢦⣀⠀⠀⠀⢀⠐⢶⣦⡙⠫⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⣹⣿⠀⠀⠀⢱\n⠀⠀⠘⣷⠀⠀⠀⠈⢧⠀⠀⣾⣩⢥⠀⠈⢢⡀⢤⣈⠳⣄⠙⢿⠲⢬⣢⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⠏⣿⠀⠀⠀⡀\n⠀⠀⢠⠟⠀⠀⠀⠀⠘⡆⠰⣿⢁⣼⡇⠀⠀⠉⣳⣮⣳⣦⣝⣶⣵⣄⠀⠀⣄⡀⢀⣀⠀⣤⣀⡼⢶⠻⡇⠀⢹⡆⠀⠀⠁\n⠀⢠⢿⡀⠀⠀⠀⠀⠀⣷⠀⠙⣿⣞⣰⣻⣿⠛⠒⠛⠒⠛⠛⠚⠛⠋⠉⠉⠑⠒⠛⠛⠉⠉⢀⣤⠏⢀⠇⠀⣼⠇⠀⠀⢀\n⠀⡏⠈⠻⠄⠀⠀⠀⢀⣿⠔⠾⣉⠑⠛⠙⢳⠤⣀⠠⠤⠤⠤⠤⡴⢦⡦⠒⠒⠒⠒⣿⠹⡏⠉⠀⣠⠛⠀⢀⡟⠀⠀⠀⢸\n⢸⡇⠀⠀⠀⠀⢀⣔⡛⠓⢢⠀⠈⠀⠀⠀⣸⠀⡇⠀⠀⠀⠀⢀⡷⠀⢧⠀⠀⠀⢠⡟⠀⣧⠀⡰⠃⠀⠀⢸⠀⠀⠀⢠⡇\n⠈⠉⠀⠀⠀⠀⠁⠀⠈⠁⠀⠀⠀⠀⠀⠈⠁⠀⠁⠀⠀⠀⠀⠈⠀⠀⠈⠀⠀⠀⠈⠁⠀⠉⠈⠁⠀⠀⠀⠉⠀⠀⠀⠈⠀\n⠀⠀⢀⣤⣦⣤⣠⣤⣤⣠⣀⣤⣤⣤⣠⣀⣤⣦⡀⣠⣤⣤⣤⣤⡀⢀⠀⢴⣤⣦⣖⣤⣖⢒⣦⢶⣴⣦⣖⣴⣦⣶⡄⠀⠀\n⠀⠀⠘⠛⠃⠛⠛⠓⠛⠛⠛⠙⠛⠛⠛⠛⠓⠛⠒⠛⡚⠛⠛⠋⠃⠀⠀⢚⠋⠛⠚⠉⠛⠛⠁⠚⠚⠋⢚⢛⠛⠓⠃⠀⠀\n")
        print('Welcome to the museum app. Type \'help\' for a list of commands')
        while self.running:
            cmd = input('>>>').strip()
            self.handle_command(cmd)

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

    # TODO: Edit all cases for current project
    def handle_command(self, cmd):
        match cmd:
            case 'exit':
                self.running = False
                print("goodbye!")
            case 'getAllArtifacts':
                self.get_all_artifacts()
            case 'addArtifact':
                self.add_artifact()
            case 'findArtifactById':
                self.find_artifact_by_id()
            case 'removeArtifact':
                self.remove_artifact()
            case 'updateArtifact':
                self.update_artifact()
            case 'addLoan':
                self.add_loan()
            case 'getLoanById':
                self.get_loan_by_id()
            case 'updateLoan':
                self.update_loan()
            case 'removeLoan':
                self.remove_loan()
            case 'getAllMuseums':
                self.get_all_museums()
            case 'help':
                print("Commands:")
                print("addArtifact, removeArtifact, updateArtifact, getAllArtifacts, findArtifactById")
                print("addLoan, getLoanById, updateLoan, deleteLoan")
                print("getAllMuseums")
                print("help, exit")
            case _:
                print("No valid command detected")

    @app.post("/artifact/add", response_model=List[ArtifactCreate])
    def add_artifact(self):
        #Add implementation
        pass
        # try:
        #     print('====Enter Artifact Details====')
        #     name = input('Artifact Name: ')
        #     accession_number = input('Accession Number: ')
        #     museum_id = input('Museum ID: ')
        #     artifact = Artifact(name=name, accession_number=accession_number, museum_id=museum_id)
        #     new_artifact_id = self.artifact_svc.add_artifact(artifact)
        #     print(new_artifact_id)
        # except Exception as e:
        #     print(f'An unexpected error has occurred: {e}')

    @app.get("/artifacts", response_model=List[ArtifactRead])
    def get_all_artifacts(self):
        #Add implementation
        pass

    @app.get("/artifact/search", response_model=List[ArtifactRead])
    def find_artifact_by_id(self):
        #Add implementation
        pass

    @app.put("/artifact/update", response_model=List[ArtifactCreate])
    def update_artifact(self):
        #Add implementation
        pass

    @app.delete("/artifact", response_model=List[CheckoutHistoryRead])
    def remove_artifact(self):
        #Add implementation
        pass

    @app.post("/loan", response_model=List[CheckoutHistoryRead])
    def add_loan(self):
        #Add implementation
        pass

    @app.get("/loan", response_model=List[CheckoutHistoryRead])
    def get_loan_by_id(self):
        #Add implementation
        pass

    @app.patch("/loan", response_model=List[CheckoutHistoryRead])
    def update_loan(self):
        #Add implementation
        pass

    @app.delete("/loan", response_model=List[CheckoutHistoryRead])
    def remove_loan(self):
        #Add implementation
        pass

    @app.get("/museumsall", response_model=List[CheckoutHistoryRead])
    def get_all_museums(self):
        #Add implementation
        pass