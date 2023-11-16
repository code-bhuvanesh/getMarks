import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import os

print("loaded pandas")

def checkCredentialsCorrent(content):
    return str(content).find("Invalid Register Number / Date of Birth!") == -1

url = "https://sist.sathyabama.ac.in/sist_ese_june_2023/login.php"

student_details = []

regno = "41110198"
dob = "26/11/2003"

student_details.append([regno,dob])

body = {
    "regno":"41110198",
    "dob" : "26/11/2003"
}
reponse = requests.post(url=url, data=body)

print(f"response : {reponse.status_code}")
print(f"{checkCredentialsCorrent(reponse.content)}")


table_col = ["Semester", "Course Code", "Course Title", "Course Type", "Internal Marks", "External Marks", "Total", "Max. Marks", "Result"]

bs = BeautifulSoup(reponse.content, "html.parser")
bs1 = BeautifulSoup(str(bs.find_all(name="table")[1]), "html.parser")


cont = [ c for c in bs1.find(name="tbody").contents if c!= "\n"]

cont = [ c.getText() for c in cont]

output = [[]]
count = 0
for c in cont:
    if(len(output) < (count//9 + 1)):
        output.append([])
    output[count//9].append(c)
    count += 1

# print(output)

df =  pd.DataFrame(columns=table_col, data=output)

print(df)

if "marks" not in os.listdir():
    os.makedirs("marks")

pd.DataFrame.to_csv(df, path_or_buf=f"marks/{regno}.csv", index=False)

# dfs = pd.read_html(str(bs1.find(name="tbody")))
# # df = dfs[2]  # pd.read_html reads in all tables and returns a list of DataFrames

# print(dfs)


