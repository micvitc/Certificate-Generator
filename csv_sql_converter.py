import csv
table_name=input("Enter table name:")
h=input("Enter csv file name:")
if h[-4:]!=".csv":
    h+=".csv"
try:
    f=open(h,'r')
    c=csv.reader(f)
    l=[]
    while True:
        s=''
        l=next(c)
        for i in l:
            try:
                a=float(i)
                s+=str(a)
                if l.index(i)!=len(l)-1:
                    s+=','
            except ValueError:
                if i=="NULL":
                    s+=i
                    if l.index(i)!=len(l)-1:
                        s+=","
                    continue
                s+="\'"
                s+=i
                s+="\'"
                if l.index(i)!=len(l)-1:
                    s+=","
        print("Insert into",table_name,"values (",s,");")
except StopIteration:
    print("Commands end here")
except FileNotFoundError:
    print("File Not Found")
