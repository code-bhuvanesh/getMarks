import pandas as pd
from bs4 import BeautifulSoup
import requests
import csv
import os
import datetime
import threading
from main import GetStudentMark

students = pd.read_csv("student_details.csv", index_col=None)



start = datetime.datetime.now()
print("start time ", start)



threads = []

print(len(students))
for ks in os.listdir("marks"):
    removeIndex = students.index[students['regno'] == int(ks.replace(".csv", ""))][0]
    students.drop(removeIndex, inplace=True)
print(len(students))

# for i in range(10):
#     student = GetStudentMark(students.regno[i],students.DOB[i])
#     thread = threading.Thread(target = student.getMarks)
#     thread.start()
#     threads.append(thread)

# for thread in threads:
#     thread.join()

end = datetime.datetime.now()
print("Time elapsed: ", end-start)    
