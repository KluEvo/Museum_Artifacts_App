import pandas as pd
import matplotlib.pyplot as plt
from src.db.database import SessionLocal

# Code Block 1
# Create a sample DataFrame
data = {    'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
    'Age': [25, 30, 35, 40, 45],                        
    'City': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix']
}
df = pd.DataFrame(data)
# Display the DataFrame
print(df)   
with SessionLocal() as db:
    artifacts = db.query(Artifact).all()
    
print('later')# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 



# Code Block 1: Imports
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy.orm import Session

from src.exceptions import *    
from src.db.database import SessionLocal
from src.domain.artifact import Artifact
from src.domain.loan import Loan
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


# Code Block 2: Initializing session, repos, and services
session: Session = SessionLocal()

artifact_repo = ArtifactRepository(session)
loan_repo = LoanRepository(session)
museum_repo = MuseumRepository(session)
artifact_loan_repo = ArtifactLoanRepository(session)
condition_report_repo = ConditionReportRepository(session)
artifact_service = ArtifactService(artifact_repo, museum_repo)
loan_service = LoanService(loan_repo)
museum_service = MuseumService(museum_repo)
artifact_loan_service = ArtifactLoanService(museum_repo)
condition_report_service = ConditionReportService(condition_report_repo)

###########
# Code Block 3
# Number of artifacts per museum

museums = museum_service.get_all_museums()
museum_ids = []

for museum in museums:
    museum_ids.append(museum.museum_id)

artifact_counts = {}

for museum_id in museum_ids:
    artifacts = artifact_service.find_artifacts_by_museum(str(museum_id))
    artifact_counts[museum_id] = len(artifacts)

df = pd.DataFrame(
    list(artifact_counts.items()),
    columns=["Museum ID", "Artifact Count"]
)

plt.figure()
plt.bar(df["Museum ID"], df["Artifact Count"])

plt.xlabel("Museum ID")
plt.ylabel("Number of Artifacts")
plt.title("Number of Artifacts per Museum")

plt.show()


print('later')

# Code Block 4
# pie chart: on loan vs not loaned
loans = loan_service.get_all_loans()
status = []
for loan in loans:
    status.append(loan.loan_status)

df = pd.DataFrame(status)
status = df.groupby(0)[0].count()
mylables = ['Completed' , 'Active', 'Scheduled']

plt.pie(status, labels=mylables, shadow=True, startangle=90, colors=['green', 'red', 'yellow'])
plt.title("Loan Status'")
plt.legend(title='Loan Status', loc = 'center left', bbox_to_anchor= (-.2,-.2))
plt.savefig('LByStatus.png')
plt.show()



# Code Block 5
# Average condition by museum
museums = museum_service.get_all_museums()
museum_ids = []

for museum in museums:
    museum_ids.append(museum.museum_id)

artifact_counts = {}
artifacts = []

for museum_id in museum_ids:
    artifacts += artifact_service.find_artifacts_by_museum(str(museum_id))
    artifact_counts[museum_id] = len(artifacts)

current_reports = {}
for artifact in artifacts:
    try:
        reports = condition_report_service.get_condition_report_by_artifact(str(artifact.artifact_id))
        

    except NotFoundException as e:
        continue    
    
    
    reports.sort(key=lambda r: r.report_date, reverse=True)
    current_reports[artifact.artifact_id] = [reports[0].condition_rating, artifact.museum_id]

df = pd.DataFrame.from_dict(current_reports, orient = 'index')
df = df.reset_index()
df.columns = ["Artifact ID", "Condition", "Museum ID"]

avg_condition = df.groupby("Museum ID")["Condition"].mean().reset_index()

plt.figure(figsize=(8, 5))
plt.bar(avg_condition["Museum ID"], avg_condition["Condition"], color='skyblue')
plt.xlabel("Museum ID")
plt.ylabel("Average Condition")
plt.title("Average Condition of Artifacts for Each Museum")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('AvgCondByM.png')
plt.show()



#distribution of artifact values
all_artifacts = artifact_service.get_all_artifacts()
values = []
for a in all_artifacts:
    if a.estimated_value:
        values.append(int(a.estimated_value))

plt.figure()
plt.hist(values, bins=20)
plt.xlabel("Estimated Value")
plt.ylabel("Frequency")
plt.title("Distribution of Artifact Estimated Values")
plt.savefig('EstValHist.png')
plt.show()

#  keep this at bottom of file
session.close()
