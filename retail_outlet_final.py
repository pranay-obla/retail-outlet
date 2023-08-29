import sys
import math
import datetime
import mysql.connector as sqltor
from tkinter import *
import tkinter.font as font
import tkinter.messagebox
from PIL import Image,ImageTk
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import cv2
import qrcode

sys.setrecursionlimit(10**6)

mycon=sqltor.connect(host="localhost",user="root",passwd="7603",database="test")
if mycon.is_connected()==False:
    print("Error connecting to database")
cursor=mycon.cursor()
root=Tk()
myFont=font.Font(size=15)

cap = cv2.VideoCapture(0)
detector = cv2.QRCodeDetector()

a=True
i=0
total=0
SLNO=1
emaillist=[]

def window():
    global root
    root.destroy()
    root=Tk()
    
    root.geometry('800x800')
    root.title('Band')
    root.configure(bg='white')
    root.resizable(False, False)
    
    logo=Image.open('Band_logo.jpeg')
    ren=ImageTk.PhotoImage(logo)
    image=Label(root,image=ren,borderwidth=0)
    image.image=ren
    image.pack(side="top",anchor=CENTER)
    
def home():
    global root
    window()
    biling=Button(root,text="Billing",bg="white",fg="black",
                  padx=10,pady=20,borderwidth=0,font=myFont,
                  command=billingwindow).pack(side="top",pady=10,anchor=CENTER)
    newms=Button(root,text="New Membership",bg="white",fg="black",
                 padx=10,pady=20,borderwidth=0,font=myFont,
                 command=new_member).pack(side="top",pady=10,anchor=CENTER)
    msstat=Button(root,text="Membership Status",bg="white",fg="black",
                  padx=10,pady=20,borderwidth=0,font=myFont,
                  command=membership).pack(side="top",pady=10,anchor=CENTER)
    admin=Button(root,text="Admin Functions",bg="white",fg="black",
                 padx=10,pady=20,borderwidth=0,font=myFont,
                 command= Admin).pack(side="top",pady=10,anchor=CENTER)
    exitwindow=Button(root,text="EXIT",bg="white",fg="black",
                      padx=10,pady=20,borderwidth=0,font=myFont,
                      command= finish).pack(side="top",pady=10,anchor=CENTER)

def billingwindow():
    global a
    global listbox
    global root
    root.destroy()
    root=Tk()
    
    root.geometry('800x800')
    root.title('Band')
    root.configure(bg='white')
    logo=Image.open('Band_logo.jpeg')
    ren=ImageTk.PhotoImage(logo)
    image=Label(root,image=ren,borderwidth=0)
    image.image=ren
    image.pack(side="top",anchor=CENTER)
    Label(root,text="SCAN THE QR CODE OF THE PRODUCT",bg="white",fg="black",font=('arial',10,'bold')).pack(side="top",anchor=CENTER,pady=10)
    Button(root,text="Add Product",bg="white",fg="black",font=myFont,command=billing).pack(side="top",anchor=CENTER)
    Label(root,text="Sl No."+"\t \t"+"Product Name"+" \t \t \t \t \t \t"+"Price",bg="white",fg="black",font=myFont,padx=10).pack(side="top",anchor=W)
    b=Button(root,text="Print Bill",bg="white",fg="black",font=myFont,borderwidth=0,command=checkout).pack(side="bottom",pady=10,anchor=CENTER)
    listbox=Listbox(root,width=110,height=75,fg="black",bg="white",font=myFont)
    listbox.pack(side='left')
    scroll=Scrollbar(root,command=listbox.yview)
    listbox.configure(yscrollcommand=scroll.set)
    scroll.pack(side="left",fill=Y)

def billingbuffer():
    root.after(500,billing)

def billing():
    global i
    global SLNO
    global items
    global message
    global total
    global itemName
    global emaillist
    _,image = cap.read()
    
    try:
        data,_,_ = detector.detectAndDecode(image)
        if data:
            pid=data
            cursor.execute("select P_name from product where Product_ID='%s'"%(pid,))
            name=cursor.fetchall()
            cursor.execute("select Price_per_unit from product where Product_ID='%s'"%(pid,))
            price=cursor.fetchall()
            total+=price[0][0]
            strprice=str(price[0][0])
            name_space=44
            emaillist.append([str(SLNO),name[0][0],price[0][0]])
            price_space=118
            delspacename=name_space-(len(name[0][0]))
            delspaceprice=price_space-(len(name[0][0]))
            items="  "+str(SLNO)
            for i in range(delspacename):
                items+=" "
            items+=name[0][0]
            for i in range(delspaceprice):
                items+=" "
            items+=str(price[0][0])
            listbox.insert(END,items)
            i+=50
            SLNO+=1
            delspaceprice=0
            root.after(500,billingbuffer)
        else:
            billingbuffer()
            
    except:
        billingbuffer()
            
def checkout():
    global root
    global total
    global e
    window()
    cap.release()
    Label(root,text="Your total bill is : %s"%(total,),fg="black",bg="white",pady=20,font=font.Font(size=20)).pack(side="top",anchor=CENTER)
    Label(root,text="Enter your gmail id for your receipt",fg="black",bg="white",pady=20,font=myFont).pack(side="top",anchor=CENTER)
    e=Entry(root)
    e.pack(side="top",anchor=CENTER,pady=20,padx=40)
    email=Button(root,text="Submit",fg="black",bg="white",borderwidth=0,font=myFont,command=gmail).pack(side="top",anchor=CENTER,pady=15)
    pay_bill=Button(root,text="PAY BILL >>>",fg="black",bg="white",borderwidth=0,font=myFont,command=paybill).pack(side="top",anchor=CENTER,pady=15)

def gmail():
    x=datetime.datetime.now()
    sender_email = "cocthegrreat@gmail.com"
    receiver_email = e.get()
    password = "devjopran"
    message = MIMEMultipart("alternative")
    message["Subject"] = "Receipt from BAND Mart published at {} on {}".format(x.strftime("%X"),x.strftime("%d")+' '+x.strftime("%B")+' '+x.strftime("%Y"))
    message["From"] = sender_email
    message["To"] = receiver_email
    html = """
    <html>
        <body>
            <h1 style ="text-align:center">Thank you for shopping with BAND Mart</h1>
            <table style="font-family: arial, sans-serif; border-collapse: collapse; width: 100%;">
              <tr>
                <th style="border: 1px solid #dddddd; text-align: center; padding: 8px;" align="left">Serial No</th>
                <th style="border: 1px solid #dddddd; text-align: center; padding: 8px;" align="left">Items</th>
                <th style="border: 1px solid #dddddd; text-align: center; padding: 8px;" align="left">Price</th>
              </tr>"""
    for x in range(0,len(emaillist)):
        if x%2==0:
            html=html+'''
      <tr style="background-color: #dddddd;" bgcolor="#dddddd">
        <td style="border: 1px solid #dddddd; text-align: center; padding: 8px;" align="left">{}</td>
        <td style="border: 1px solid #dddddd; text-align: left; padding: 8px;" align="left">{}</td>
        <td style="border: 1px solid #dddddd; text-align: center; padding: 8px;" align="left">{}</td>
      </tr> '''.format(emaillist[x][0],emaillist[x][1],emaillist[x][2])
        else:
            html=html+'''
      <tr>
        <td style="border: 1px solid #dddddd; text-align: center; padding: 8px;" align="left">{}</td>
        <td style="border: 1px solid #dddddd; text-align: left; padding: 8px;" align="left">{}</td>
        <td style="border: 1px solid #dddddd; text-align: center; padding: 8px;" align="left">{}</td>
      </tr> '''.format(emaillist[x][0],emaillist[x][1],emaillist[x][2])
    html = html+'''</table>
                   <h2 style ="text-align:center">Total Price: Rs.{}</h2>

                   </body></html>'''.format(str(total))
    htmltext = MIMEText(html, "html")
    message.attach(htmltext)
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        try:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            tkinter.messagebox.showinfo("Email Sent", "Email successfully sent")
        
        except:
            tkinter.messagebox.showinfo("Error", "There was an error while sending email")

def paybill():
    window()
    Label(root,text="SELECT YOUR METHOD OF PAYEMENT",fg="black",bg="white",font=('arial',25,'bold')).pack(side="top",anchor=CENTER,pady=20)
    cash=Radiobutton(root,text="PAY BY CASH",fg="black",bg="white",font=('arial',15,'bold'),command=finish)
    cash.pack(side="top",anchor=W,pady=20,padx=150)
    point=Radiobutton(root,text="PAY USING MEMBERSHIP POINTS",fg="black",bg="white",font=('arial',15,'bold'),command=points)
    point.pack(side="top",anchor=W,pady=20,padx=150)
   
def finish():
    window()
    Label(root,text="THANK YOU FOR VISITING ",fg="black",bg="white",font=('arial',40,'bold')).pack(side="top",anchor=CENTER,pady=100)
    Exit=Button(root,text="EXIT",fg="black",bg="white",font=('arial',15,'bold'),command=exit).pack(side="bottom",anchor=CENTER,pady=15)
    back = Button(root,text="RETURN TO HOME",fg="black",bg="white",font=('arial',15,'bold'),command=home).pack(side="bottom",anchor=CENTER,pady=15)
     
def exit():
    root.destroy()

def customerid():
    idlist = []
    cursor.execute("Select Customer_id from Customer")
    ids = cursor.fetchall()
    for x in ids:
        idlist.append(x[0])
    return max(idlist)

def new_member():
    global root
    global nc_name
    global nc_phone_no
    window()
    Label(root,text="Please fill the form given below",fg="black",bg="white",pady=20,font=myFont).pack(side="top",anchor=CENTER)
    Label(root,text="Enter name",fg="black",bg="white",pady=20,font=myFont).pack(side="top",anchor=CENTER)
    nc_name=Entry(root)
    nc_name.pack(side="top",anchor=CENTER,pady=20,padx=40)
    
    Label(root,text="Enter Phone number",fg="black",bg="white",pady=20,font=myFont).pack(side="top",anchor=CENTER)
    nc_phone_no=Entry(root)
    nc_phone_no.pack(side="top",anchor=CENTER,pady=20,padx=40)
    def action():
        try:
            points=0
            
            newid = int(customerid())
            
            newid += 1
            
            val = (newid, nc_name.get(), points, 0, nc_phone_no.get()) 
            sql = "Insert into customer (Customer_id, C_name, points, loan, phone_no) Values (%s, %s, %s, %s,%s)"
            cursor.execute(sql, val)
            mycon.commit()
            tkinter.messagebox.showinfo("Success", "Successfully added an new member")
            finish()
        except:
            tkinter.messagebox.showinfo("Error", "Enter appropriate values")
            new_member()
    submit=Button(root,text="SUBMIT FORM",fg="black",bg="white",borderwidth=0,font=myFont,command=action).pack(side="top",anchor=CENTER,pady=15)
    Back=Button(root,text="BACK",bg="white",fg="black",padx=10,pady=20,borderwidth=0,font=myFont,command=home).pack(side="top",pady=5,anchor=CENTER)
    
def points():
    window()
    global myFont
    global mobile_no
    Label(root,text="Enter mobile number:",fg="black",bg="white",font=myFont).pack(side="top",anchor=CENTER,pady=15)
    mobile_no=Entry(root)
    mobile_no.pack(side="top",anchor=CENTER,pady=15)
    submit=Button(root,text="submit",borderwidth=0,fg="black",bg="white",font=myFont,command=member)
    submit.pack(side="top",anchor=CENTER,pady=15)

def member():
    try:
        global root
        global mobile_no
        global total
        
        m_n=mobile_no.get()
        window()
        cursor.execute("select C_name from Customer where phone_no =%s"%(m_n,))
        C_name=cursor.fetchall()
        cursor.execute("select Customer_ID from Customer where phone_no=%s"%(m_n,))
        C_id=cursor.fetchall()
        cursor.execute("select points from Customer where phone_no=%s"%(m_n,))
        C_points=cursor.fetchall()
        Label(root,text="Name : "+C_name[0][0],fg="black",bg="white",font=('arial',10,'bold')).place(x=150,y=300)
        Label(root,text="Customer ID : "+str(C_id[0][0]),fg="black",bg="white",font=('arial',10,'bold')).place(x=300,y=300)
        Label(root,text="Points : "+str(C_points[0][0]),fg="black",bg="white",font=('arial',10,'bold')).place(x=150,y=350)
        Label(root,text="Mobile Number : "+str(m_n),fg="black",bg="white",font=('arial',10,'bold')).place(x=300,y=350)

        if C_points[0][0]>=1000 and total>=40:
            Label(root,text=" ================================== DISCOUNT ====================================",fg="green",bg="white",font=myFont).place(x=50,y=400)
            Label(root,text="DISCOUNT : 100 ",fg="green",bg="white",font=('arial',13,'bold')).place(x=200,y=450)
            Label(root,text=" ================================== TOTAL BILL =====================================",fg="green",bg="white",font=myFont).place(x=50,y=500)
            total-=100
            Label(root,text="TOTAL  :  "+str(total),fg="black",bg="white",font=('arial',13,'bold')).place(x=200,y=550)
            payrest=Button(root,text="PAY THE REST ",fg="black",bg="white",font=myFont,command=finish).place(x=350,y=600)
            pointred=C_points[0][0]-1000
            cursor.execute("update Customer set points =%s where phone_no =%s"%(pointred,m_n))
            mycon.commit()
            cursor.execute("update Customer set points =%s where phone_no =%s"%(pointred+100,m_n))
            mycon.commit()

        else:
            Label(root,text="=================================NOT ELIGIBLE ======================================",fg="green",bg="white",font=myFont).pack(side="top",anchor=CENTER,pady=15)
            s = "Amount payable is : " + str(total)
            Label(root,text=s,fg="green",bg="white",font=myFont).pack(side="top",anchor=CENTER,pady=15)
            payrest=Button(root,text="PAY BY CASH ",fg="black",bg="white",font=myFont,command=finish)
            payrest.place(x=350,y=600)

        if total>=100:
            cursor.execute("update Customer  set points =%s where phone_no =%s"%((C_points[0][0])+100,m_n))
            mycon.commit()
            
    except:
            tkinter.messagebox.showinfo("Error", "Enter an existing phone no. or create an new member")
            paybill()

def Prod_id():
    sql = "Select Product_id from Product"
    cursor.execute(sql)
    res = cursor.fetchall()
    new = 0
    
    for i in res:
        i = i[0]
        i = int(i[1:])
        if i > new:
            new = i
    return new + 1

def change_price():
    window()
    
    Label(root,text="Enter Product id ",fg="black",bg="white",font=('arial',20,'bold')).pack(side="top",anchor=CENTER,pady=10)
    P_id = Entry(root)
    P_id.pack(side="top",anchor=CENTER,pady=20,padx=40)
    
    Label(root,text="Enter new Price",fg="black",bg="white",font=('arial',20,'bold')).pack(side="top",anchor=CENTER,pady=10)
    price = Entry(root)
    price.pack(side="top",anchor=CENTER,pady=20,padx=40)

    def action():
        try:
            sql = "Update Product set price_per_unit = %s where Product_id = %s;"
            val = (price.get(), P_id.get())
            cursor.execute(sql, val)
            mycon.commit()
            tkinter.messagebox.showinfo("Successfull", "Changed price successfully")
            
        except:
            tkinter.messagebox.showinfo("Error", "Enter existing product_id and price below 100")
            change_price()
       
    
    action = Button(root,text="Change Price",bg="white",fg="black",
                    padx=10,pady=20,borderwidth=0,font=myFont,
                    command=action).pack(side="top",pady=10,anchor=CENTER)
    back = Button(root,text="Back",bg="white",fg="black",
                  padx=10,pady=20,borderwidth=0,font=myFont,
                  command=Admin).pack(side="top",pady=10,anchor=CENTER)

    

def Add_Product():
    window()

    Label(root,text="Enter Product Name ",fg="black",bg="white",font=('arial',10,'bold')).pack(side="top",anchor=CENTER,pady=10)
    name = Entry(root)
    name.pack(side="top",anchor=CENTER,pady=10,padx=40)

    Label(root,text="Enter Price",fg="black",bg="white",font=('arial',10,'bold')).pack(side="top",anchor=CENTER,pady=10)
    price = Entry(root)
    price.pack(side="top",anchor=CENTER,pady=10,padx=40)

    Label(root,text="Enter stock",fg="black",bg="white",font=('arial',10,'bold')).pack(side="top",anchor=CENTER,pady=10)
    stock = Entry(root)
    stock.pack(side="top",anchor=CENTER,pady=10,padx=40)

    Label(root,text="Enter brand",fg="black",bg="white",font=('arial',10,'bold')).pack(side="top",anchor=CENTER,pady=10)
    brand = Entry(root)
    brand.pack(side="top",anchor=CENTER,pady=10,padx=40)

    def action():
        try:
            P_id = "A00"+str(Prod_id())
            sql = "Insert into Product (Product_id, P_Name, Brand, Price_per_unit, Stock) values(%s, %s, %s, %s, %s)"
            val = (P_id, name.get(), brand.get(), price.get(), stock.get())
            cursor.execute(sql, val)
            mycon.commit()
            tkinter.messagebox.showinfo("Successfull", "Added Product successfully")
            
        except:
            tkinter.messagebox.showinfo("Error", "Enter appropriate values (Price should be below 100)")
            Add_Product()

    action = Button(root,text="Add Product",bg="white",fg="black",padx=10,pady=20,borderwidth=0,font=myFont,command=action).pack(side="top",pady=10,anchor=CENTER)
    back = Button(root,text="Back",bg="white",fg="black",padx=10,pady=20,borderwidth=0,font=myFont,command=Admin).pack(side="top",pady=10,anchor=CENTER)


def Remove_Product():
    window()

    Label(root,text="Enter Product ID ",fg="black",bg="white",font=('arial',10,'bold')).pack(side="top",anchor=CENTER,pady=10)
    P_id = Entry(root)
    P_id.pack(side="top",anchor=CENTER,pady=10,padx=40)

    def action():
        try:
            sql = "delete from Product where Product_id = %s"
            val = (P_id.get(),)
            cursor.execute(sql, val)
            mycon.commit()
            tkinter.messagebox.showinfo("Successfull", "Removed Product successfully")
            
        except:
            tkinter.messagebox.showinfo("Error", "Enter a existing product id")
            Remove_Product()

    action = Button(root,text="Remove Product",bg="white",fg="black",padx=10,pady=20,borderwidth=0,font=myFont,command=action).pack(side="top",pady=10,anchor=CENTER)
    back = Button(root,text="Back",bg="white",fg="black",padx=10,pady=20,borderwidth=0,font=myFont,command=Admin).pack(side="top",pady=10,anchor=CENTER)


def CheckStock():
    window()
    
    Label(root,text="Enter Product ID ",fg="black",bg="white",font=('arial',10,'bold')).pack(side="top",anchor=CENTER,pady=10)
    P_id = Entry(root)
    P_id.pack(side="top",anchor=CENTER,pady=10,padx=40)

    Label(root,text="Enter Stock to be added ",fg="black",bg="white",font=('arial',10,'bold')).pack(side="top",anchor=CENTER,pady=10)
    stck = Entry(root)
    stck.pack(side="top",anchor=CENTER,pady=10,padx=40)
    
    def action1():
        try:
            sql = "Select stock from Product where Product_id = %s"
            val = (P_id.get(),)
            cursor.execute(sql, val)
            res = cursor.fetchall()
            Label(root, text = res[0], fg="black",bg="white",font=('arial',15,'bold'), width = 20).place(x = 275, y = 435)
            
        except:
            tkinter.messagebox.showinfo("Error", "Enter an existing Product id")
            CheckStock()

    def action2():
        try:
            sql = "Update Product set Stock = Stock + %s where Product_id = %s;"
            val = (stck.get(), P_id.get())
            tkinter.messagebox.showinfo("Success", "Stock has been updated")
            #Label(root, text = "Stock has been updated", fg="black",bg="white",font=('arial',10,'bold'), width = 20).place(x = 300, y = 220)
            cursor.execute(sql, val)
            mycon.commit()

        except:
            tkinter.messagebox.showinfo("Error", "Enter an existing Product id")
            CheckStock()    
    
    action1 = Button(root,text="Check Stock",bg="white",fg="black",padx=10,pady=20,borderwidth=0,font=myFont,command=action1).pack(side="top",pady=10,anchor=CENTER)
    action2 = Button(root,text="Add Stock",bg="white",fg="black",padx=10,pady=20,borderwidth=0,font=myFont,command=action2).pack(side="top",pady=10,anchor=CENTER)
    back = Button(root,text="Back",bg="white",fg="black",padx=10,pady=20,borderwidth=0,font=myFont,command=Admin).pack(side="top",pady=10,anchor=CENTER)
  

def membership():
    window()
    
    Label(root,text="Enter Customer ID ",fg="black",bg="white",font=('arial',10,'bold')).pack(side="top",anchor=CENTER,pady=10)
    C_id = Entry(root)
    C_id.pack(side="top",anchor=CENTER,pady=10,padx=40)

    Label(root, fg="black",bg="white",font=('arial',10,'bold'), width = 20).place(x = 300, y = 300)
    Label(root, fg="black",bg="white",font=('arial',10,'bold'), width = 20).place(x = 300, y = 325)
    Label(root, fg="black",bg="white",font=('arial',10,'bold'), width = 20).place(x = 300, y = 350)
    Label(root, fg="black",bg="white",font=('arial',10,'bold'), width = 20, height = 50).place(x = 300, y = 375)
        
    def action():
        try:
            res =[]
            sql = "Select * from Customer where Customer_id = %s"
            val = (C_id.get(),)
            cursor.execute(sql, val)
            res = cursor.fetchall()
            stext1 = "Customer id: " + str(res[0][0])
            stext2 = "Customer Name: " + str(res[0][1])
            stext3 = "Points: " + str(res[0][2])
            stext4 = "Mobile number: " + str(res[0][4])
                                             
            Label(root, text = stext1, fg="black",bg="white",font=('arial',10,'bold'), width = 30).place(x = 275, y = 345)
            Label(root, text = stext2, fg="black",bg="white",font=('arial',10,'bold'), width = 30).place(x = 275, y = 370)
            Label(root, text = stext3, fg="black",bg="white",font=('arial',10,'bold'), width = 30).place(x = 275, y = 395)
            Label(root, text = stext4, fg="black",bg="white",font=('arial',10,'bold'), width = 30).place(x = 275, y = 420)

        except:
            tkinter.messagebox.showinfo("Error", "Enter an existing Customer id")
            membership()
            
    action = Button(root,text="Check Membership details",bg="white",fg="black",padx=10,pady=10,borderwidth=0,font=myFont,command=action).pack(side="top",pady=10,anchor=CENTER)
    back = Button(root,text="Back",bg="white",fg="black",padx=10,pady=100,borderwidth=0,font=myFont,command=home).pack(side="top",pady=10,anchor=CENTER)


def Admin():
    window()
    price_change = Button(root,text="Change Price",bg="white",fg="black",padx=10,pady=20,borderwidth=0,font=myFont,command=change_price).pack(side="top",pady=5,anchor=CENTER)
    product_add = Button(root,text="Add a Product",bg="white",fg="black",padx=10,pady=20,borderwidth=0,font=myFont,command=Add_Product).pack(side="top",pady=5,anchor=CENTER)
    product_remove = Button(root,text="Remove a Product",bg="white",fg="black",padx=10,pady=20,borderwidth=0,font=myFont,command=Remove_Product).pack(side="top",pady=5,anchor=CENTER)
    stock_check = Button(root,text="Check stock",bg="white",fg="black",padx=10,pady=20,borderwidth=0,font=myFont,command=CheckStock).pack(side="top",pady=5,anchor=CENTER)
    membership_check = Button(root,text="Check Membership",bg="white",fg="black",padx=10,pady=20,borderwidth=0,font=myFont,command=membership).pack(side="top",pady=5,anchor=CENTER)
    Back=Button(root,text="BACK",bg="white",fg="black",padx=10,pady=20,borderwidth=0,font=myFont,command=home).pack(side="top",pady=5,anchor=CENTER)
    
home()
