import os
import requests
from fastapi import Depends, FastAPI, Query

app = FastAPI(title="Museum API")

class main:
    def __init__(self):
        self.running = True

    def start(self):
        print('Welcome to the museum app. Type \'help\' for a list of commands')
        while self.running:
            cmd = input('>>>').strip()
            self.handle_command(cmd)
    
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
            case 'deleteLoan':
                self.delete_Loan()
            case 'help':
                print("Commands:")
                print("addBook, removeBook, updateBook, getAllRecords, findByName, getJoke, help, exit")
                print("getAveragePrice, getTopBooks, getValueScores, medianPriceByGenre, genrePop2026")
                print("priceSD, pricePercent, priceCorr, ratingHist")
                print("checkIn, checkOut, checkoutHist")
            case _:
                print("No valid command detected")

    def add_artifact(self):
        #Add implementation
        pass

    def get_all_artifacts(self):
        #Add implementation
        pass

    def find_artifact_by_id(self):
        #Add implementation
        pass

    def update_artifact(self):
        #Add implementation
        pass

    def remove_artifact(self):
        #Add implementation
        pass

    def add_artifact(self):
        #Add implementation
        pass

    def add_artifact(self):
        #Add implementation
        pass

    def add_artifact(self):
        #Add implementation
        pass

    def add_artifact(self):
        #Add implementation
        pass