import os
import pandas as pd
# print(os.listdir("marks"))

# output =    

fail = 0

for file in os.listdir("marks"):
    df = pd.read_csv("marks/" + file)
    print( file.replace(".csv", "") + " : " + str((df["Total"].sum()/df["Max. Marks"].sum()) * 100 ) + f", {len(df)}" )
    # break

for file in os.listdir("marks"):
    df = pd.read_csv("marks/st-03/" + file)
    avg = True
    fs = 0
    for r in (df["Result"] == "Pass"):
        avg = avg and r
        if not r:
            fs += 1
    if avg: 
        # print("PASS")
        pass
    else:
        print(f"FAIL {fs}   " + file.replace(".csv", ""))
    if not avg: 
        fail += 1 
    

print(f"fail no {fail}")