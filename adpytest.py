import mysql.connector
import random
mycon=mysql.connector.connect(host="localhost",user="root",passwd="7603")
if mycon.is_connected():
    print("Succesfully connected")
cursor=mycon.cursor()
cursor.execute("Create database if not exists test;")
cursor.execute("Use test;")
cursor.execute("Drop table if exists Customer;")
cursor.execute("Drop table if exists Product;")
cursor.execute("Create table Product (Product_ID Varchar(6) PRIMARY KEY, P_name varchar(30) NOT NULL, Brand Varchar (20), Price_per_unit float (5,3) NOT NULL, Stock int NOT NULL);")
cursor.execute("Create table Customer (Customer_ID Varchar (9) PRIMARY KEY, C_name Varchar(30) NOT NULL,Points int, Loan float (4,2),phone_no bigint);")
LPN=['Almonds', 'Besan', 'Cashew', 'Cheese', 'Chips', 'Chocolate', 'Clock', 'Detergent', 'Dish washer', 'Eraser', 'Floor Cleaner', 'Gluestick', 'Gram Flour', 'Ice Cream', 'Incense', 'Milk', 'Mixture', 'Pen', 'Pencil', 'Perfume', 'Rahar Dal', 'Raisins', 'Rava', 'Rice Boiled', 'Rice Flour', 'Salt', 'Scissors', 'Softdrink', 'Sugar', 'Tape', 'Tea Leaves', 'Toor Dal', 'Toothbrush', 'Toothpaste', 'Wheat']
LPID=['A001', 'A002', 'A003', 'A004', 'A005', 'A006', 'A007', 'A008', 'A009', 'A0010', 'A0011', 'A0012', 'A0013', 'A0014', 'A0015', 'A0016', 'A0017', 'A0018', 'A0019', 'A0020', 'A0021', 'A0022', 'A0023', 'A0024', 'A0025', 'A0026', 'A0027', 'A0028', 'A0029', 'A0030', 'A0031', 'A0032', 'A0033', 'A0034', 'A0035']
Brand=["Null","Samrat","Null","Amul","Lays","Dairy Milk", "Null", "Surf","Rin","Apsara","Domex","Fevistick","Samrat","Amul","Grihasti","Amul","Haldiram","Trimax","Apsara","Yardley","Null","Null","Null","Null","Samrat","Tata","Null","Coco Cola","Perrys","Null","Tata","Null","Oral-B","Pepsodent","Null"]
Price=[20,50,30,20,90,60,99.99,90,10,90,50,10,50,90,50,20,70,10,5,90,50,90,50,30,50,60,30,35,60,20,70,50,20,30,30]
Stock=[7,1,13,11,5,20,24,31,13,28,22,12,15,8,4,2,9,10,23,29,12,34,32,21,32,20,19,16,18,2,8,3,14,21,22]
for i in range (0,35):
    cursor.execute("INSERT into Product VALUES ("+"'"+str(LPID[i])+"'"+","+"'"+str(LPN[i])+"'"+","+"'"+str(Brand[i])+"'"+","+str(Price[i])+","+str(Stock[i])+")"+";") 
    mycon.commit()
    print ("Row",i+1,"Succesfully inserted")
print ("Table Product succesfully created")
import random
CNO=[]
x=0
while True:
    x=random.randrange(9000000000,9999999999)
    CNO.append(x)
    if len(CNO)<16:
        continue
    else:
        break
print ("Customer Number List is,",CNO)
CID=[99987654, 99987655, 99987656, 99987657, 99987658, 99987659, 99987660, 99987661, 99987662, 99987663, 99987664, 99987665, 99987666, 99987667, 99987668]
Cname=["Sathvik Manoj","Ritesh Mukherjee","Adway Kumar","Sakshi Kambuj","Reeta Ambani","Ritu Kapadia","Anil Desai","Anuj Bharadwaj","Reshma Singhania","Ritwik Birla","Diksha Chaterjee","Hrishav Agarwal","M.Krishnamurthy","Sahil Bhose","Keshav Moray"]
Points=[20,35,26,17,90,57,39,19,27,38,76,56,43,28,95]
Loan=[0,20.10,90,50,78,0,23,67,0,50.50,20.30,70.56,29.40,0,0]
for i in range (0,15):
    cursor.execute("INSERT into Customer VALUES ("+"'"+str(CID[i])+"'"+","+"'"+str(Cname[i])+"'"+","+str(Points[i])+","+str(Loan[i])+","+str(CNO[i])+")"+";") 
    mycon.commit()
    print ("Row",i+1,"Succesfully inserted")
print ("Table Customer successfully created")


