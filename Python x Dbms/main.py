from tkinter import *
import tkinter
from tkinter import messagebox
import mysql.connector
from tkinter import ttk
import PIL
from PIL import Image,ImageTk

mydb = mysql.connector.connect(
    host="localhost",
    username="root",
    password="root",
    database="EventManagement"
)
mycur = mydb.cursor()

# ======= Login GUI =======
root = tkinter.Tk()
root.title("Login")
root.geometry("1550x800+0+0")

bg=ImageTk.PhotoImage(file=r"image1.jpg")
lbl_bg=Label(root,image=bg)
lbl_bg.place(x=0,y=0,relwidth=1,relheight=1)

frame=Frame(root,bg="black")
frame.place(x=610,y=170,width=340,height=450)

img1=Image.open(r"loginlogo.png")
img1=img1.resize((70,70),Image.LANCZOS)
photoimage1=ImageTk.PhotoImage(img1)
lblimg1=Label(image=photoimage1,bg="black",borderwidth=0)
lblimg1.place(x=745,y=190,width=70,height=70)

get_str=Label(frame,text="Get Started",font=("arial",20,"bold"),fg="white",bg="black")
get_str.place(x=95,y=100)

username=lbl=Label(frame,text="UserID",font=("arial",14,"bold"),fg="white",bg="black")
username.place(x=50,y=145)

txtuser=ttk.Entry(frame,font=("arial",15,"bold"))
txtuser.place(x=50,y=170,width=240)

password=lbl=Label(frame,text="Password",font=("arial",14,"bold"),fg="white",bg="black")
password.place(x=50,y=215)

txtpass=ttk.Entry(frame,font=("arial",15,"bold"))
txtpass.place(x=50,y=240,width=240)

v = IntVar()

#radiobuttons
emp_rdiobtn1=Radiobutton(frame, text="Employee", variable=v, value=1,font=("arial",10,"bold"),fg="white",bg="black",activeforeground="white",activebackground="black")
emp_rdiobtn1.place(x=45,y=340)

emp_rdiobtn2=Radiobutton(frame, text="Customer", variable=v, value=2,font=("arial",10,"bold"),fg="white",bg="black",activeforeground="white",activebackground="black")
emp_rdiobtn2.place(x=205,y=340)

#loginbutton
loginbtn=Button(frame,text="Login",command=lambda: loginuser(v.get()),font=("arial",12,"bold"),relief=RIDGE,fg="white",bg="blue")
loginbtn.place(x=120,y=290,width=100,height=35)

#registerbutton
registerbtn=Button(frame,text="New User Register",font=("arial",10,"bold"),borderwidth=0,fg="white",bg="black",
                   activeforeground="white",activebackground="black")
registerbtn.place(x=25,y=370,width=120,height=35)

#forgetbutton
forgetbtn=Button(frame,text="Forget password",font=("arial",10,"bold"),borderwidth=0,fg="white",bg="black",
                 activeforeground="white",activebackground="black")
forgetbtn.place(x=20,y=400,width=120,height=35)

# =======LOGIN FUNCTION======
def loginuser(value):

    if value == 1:
        mycur = mydb.cursor()
        uid = txtuser.get()
        password = txtpass.get()

        sql = "select * from Emplogin where empId=%s and empPass=%s"
        mycur.execute(sql, [uid, password])
        res = mycur.fetchall()
        if res:
            messagebox.showinfo("login alert", "Employee login successful")
            openemp(uid)

        else:
            messagebox.showinfo("login alert", "Incorrect credentials")

    elif value == 2:
        mycur1 = mydb.cursor()
        uid = txtuser.get()
        password = txtpass.get()

        sql = "select * from custlogin where custId=%s and custPass=%s"
        mycur1.execute(sql, [uid, password])
        res = mycur1.fetchall()
        if res:
            messagebox.showinfo("login alert", "Customer login successful")
            opencust(uid)

        else:
            messagebox.showinfo("login alert", "Incorrect credentials")
    else:
        messagebox.showwarning("", "Something is missing\nTry Again")

# ======= LANDING PAGE EMPLOYEE WINDOW ========
def openemp(val):
    #Employee window
    root.destroy()
    emp = tkinter.Tk()
    emp.title("Employee")
    emp.geometry("1550x800+0+0")

    frame2=Frame(emp, bd=4,bg="black", relief=RIDGE) 
    frame2.place(x=0,y=0,width=1550,height=140)

    main_title=Label(emp, text="EVENT MANAGEMENT SYSTEM", font=("arial", 40, "bold"), bg="blue", fg="white",bd=4,relief=RIDGE)
    main_title.place(x=0,y=140, width=1550,height=70)

    mycur1 = mydb.cursor()
    sql1 = "select empName,empId,empDno from Employee where empId=%s"
    mycur1.execute(sql1, [val])
    res1 = mycur1.fetchall()
    dres = ''
    for rec in res1[0]:
        dres += str(rec)

    login_text=Label(emp, text="Login Id: "+dres,fg="lightblue", bg="blue",font=("arial",14,"bold"),bd=4,relief=RIDGE)
    login_text.place(x=0,y=209,width=1550,height=30)

    lbl_menu=Label(emp, text="MENU", font=("arial",18,"bold"), bg="blue", fg="white",bd=4,relief=RIDGE) 
    lbl_menu.place(x=0,y=238,width=275)

    btn_frame=Frame(emp,bg="lightblue",bd=4,relief=RIDGE)
    btn_frame.place(x=0,y=275,width=275,height=520)

    cust_btn=Button(btn_frame, text="MANAGE CUSTOMER",command=newCust, width=22, font=("arial", 14, "bold"), bg="blue", fg="white",bd=0) 
    cust_btn.grid(row=0,column=0,pady=1)

    update_btn=Button(btn_frame, text="UPDATE PROFILE",command=lambda: (upProfile(1,val)), width=22, font=("arial", 14, "bold"), bg="blue", fg="white",bd=0)
    update_btn.grid(row=1,column=0,pady=1)

    frame3=Frame(emp,bd=4,relief=RIDGE,bg="lightblue")
    frame3.place(x=275,y=238,width=1265,height=562)

    # ttk.Separator(emp, orient='horizontal').place(y=70, relwidth=1)
    tree = ttk.Treeview(emp, columns=('custId','custName','custEmail'), show='headings')
    tree.heading('custId', text='Id')
    tree.heading('custName', text='Name')
    tree.heading('custEmail', text='Contact')
    sql= "select custId,custName,custEmail from Customer"
    mycur.execute(sql)
    record=mycur.fetchall()
    count=0
    for i in record:
        if(count%2==0):
            tree.insert(parent='', index='end', values=(i[0], i[1] ,i[2]),tags='even')
            count+=1
        else:
            tree.insert(parent='', index='end', values=(i[0], i[1], i[2]),tags='odd')
            count+=1
    tree.tag_configure('odd', background='lightblue')
    tree.place(x=907,y=288,width=582,height=442)

    scrollbar = ttk.Scrollbar(emp, orient=VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.place()

# ====== MANAGE CUSTOMER WINDOW =======
def newCust():
    #Customer window
    mycur = mydb.cursor()
    newcust = tkinter.Tk()
    newcust.title('Manage Customer')
    newcust.geometry("532x442+325+308")

    frame1=Frame(newcust,bg="blue")
    frame1.place(x=0,y=0,width=532,height=442)

    Label(frame1, text="Name",font=("arial",14,"bold"),fg="white",bg="blue").place(x=50,y=50)
    Label(frame1, text="Id",font=("arial",14,"bold"),fg="white",bg="blue").place(x=50,y=90)
    Label(frame1, text="Email",font=("arial",14,"bold"),fg="white",bg="blue").place(x=50,y=130)
    Label(frame1, text="Set Password",font=("arial",14,"bold"),fg="white",bg="blue").place(x=50,y=170)
    custname = ttk.Entry(frame1,font=("arial",15,"bold"))
    custname.place(x=250,y=50)
    #Cid not generating
    cid = (frame1,custname, id(custname))
    custid = Entry(frame1, textvariable=cid ,font=("arial",15,"bold"))
    custid.place(x=250,y=90)
    custmail = ttk.Entry(frame1,font=("arial",15,"bold"))
    custmail.place(x=250,y=130)
    custpass=ttk.Entry(frame1,font=("arial",15,"bold"))
    custpass.place(x=250,y=170)


    def subcust():
        mycur.execute("insert into Customer(custName, custId, custEmail) values(%s,%s,%s)",
                      (custname.get(), custid.get(), custmail.get())
                      )
        mycur.execute("insert into custlogin(custId, custPass) values(%s,%s)", (custid.get(), custpass.get()))
        mydb.commit()
        messagebox.showinfo("Customer", "Customer Added successfully")
        newcust.destroy()

    def delcust():
        mycur.execute("drop from eventManage where custId=%s", [custid.get()])
        mycur.execute("delete from customer where custID = %s", [custid.get()])
        mycur.execute("delete from custlogin where custID = %s", [custid.get()])
        mydb.commit()
        messagebox.showinfo("Customer", "Customer Removed")
        newcust.destroy()

    Button(frame1, text="Delete", command=delcust,font=("arial",12,"bold"),relief=RIDGE,fg="white",bg="red").place(x=50,y=220)
    Button(frame1, text="Add", command=subcust,font=("arial",12,"bold"),relief=RIDGE,fg="white",bg="red").place(x=250,y=220)

# ===== UPDATE WINDOW =====
def upProfile(num,value):
    if(num== 1):
        upemp = tkinter.Tk()
        upemp.title("Update Employee")
        upemp.geometry("532x442+325+308")

        frame3 = Frame(upemp, bg="blue")
        frame3.place(x=0,y=0,width=532,height=442)

        Label(frame3, text="Fill the box with Updated value if none keep empty", font=("arial", 14, "bold"), fg="white", bg="blue").place(x=50, y=50)
        Label(frame3, text="Name", font=("arial", 14, "bold"), fg="white", bg="blue").place(x=50, y=90)
        Label(frame3, text="Password", font=("arial", 14, "bold"), fg="white", bg="blue").place(x=50, y=130)
        upName=ttk.Entry(frame3, font=("arial", 15, "bold"))
        upName.place(x=250, y=90)
        upPass=ttk.Entry(frame3, font=("arial", 15, "bold"))
        upPass.place(x=250, y=130)

        def update():
            if upName.get() != "":
                sql = "update Employee set empName = %s where empId= %s"
                mycur.execute(sql, [upName.get(), value])
                mydb.commit()

            if upPass.get() != "":
                sql = "update EmpLogin set empPass = %s where empId= %s"
                mycur.execute(sql, [upPass.get(), value])
                mydb.commit()

            upemp.destroy()
            messagebox.showinfo("Update", "Yippee\nUpdation successfully")

        Button(frame3, text="Update",command=update,font=("arial",12,"bold"),relief=RIDGE,fg="white",bg="red").place(x=50,y=220)


    elif (num == 2):

        upcust = tkinter.Tk()
        upcust.title("Update Customer")
        upcust.geometry("532x442+325+308")

        frame3 = Frame(upcust, bg="blue")
        frame3.place(x=0,y=0,width=532,height=442)

        Label(frame3, text="Fill the box with Updated value if none keep empty", font=("arial", 14, "bold"), fg="white", bg="blue").place(x=50, y=50)
        Label(frame3, text="Name", font=("arial", 14, "bold"), fg="white", bg="blue").place(x=50, y=90)
        Label(frame3, text="Password", font=("arial", 14, "bold"), fg="white", bg="blue").place(x=50, y=130)
        upName=ttk.Entry(frame3, font=("arial", 15, "bold"))
        upName.place(x=250, y=90)
        upPass=ttk.Entry(frame3, font=("arial", 15, "bold"))
        upPass.place(x=250, y=130)


        def update():
            if upName.get() != "":
                sql = "update Customer set custName = %s where custId= %s"
                mycur.execute(sql, [upName.get(), value])
                mydb.commit()

            if upPass.get() != "":
                sql = "update custLogin set custPass = %s where custId= %s"
                mycur.execute(sql, [upPass.get(), value])
                mydb.commit()

            if upEmail.get() != "":
                sql = "update Customer set custEmail = %s where custId= %s"
                mycur.execute(sql, [upEmail.get(), value])
                mydb.commit()

            upcust.destroy()
            messagebox.showinfo("Update", "Yippee\nUpdation successfully")

        Button(frame3, text="Update",command=update,font=("arial",12,"bold"),relief=RIDGE,fg="white",bg="red").place(x=50,y=220)

    else:
        messagebox.showerror("Error", "Something unusual Occurred")

# ======= MANAGE EVENT =======
def manageEvent(val):

    mycur = mydb.cursor()
    newevent = tkinter.Tk()
    newevent.geometry("532x442+325+308")
    newevent.title("Managing Event")

    frame1=Frame(newevent,bg="blue")
    frame1.place(x=0,y=0,width=532,height=442)

    Label(frame1, text="Event Name",font=("arial",14,"bold"),fg="white",bg="blue").place(x=50,y=50)
    Label(frame1, text="Event Id",font=("arial",14,"bold"),fg="white",bg="blue").place(x=50,y=90)
    Label(frame1, text="City",font=("arial",14,"bold"),fg="white",bg="blue").place(x=50,y=130)
    Label(frame1, text="Date",font=("arial",14,"bold"),fg="white",bg="blue").place(x=50,y=170)
    eventname = ttk.Entry(frame1,font=("arial",15,"bold"))
    eventname.place(x=250,y=50)
    #Cid not generating
    eid = (frame1,eventname, id(eventname))
    eventid = Entry(frame1, textvariable=eid ,font=("arial",15,"bold"))
    eventid.place(x=250,y=90)
    city = ttk.Entry(frame1,font=("arial",15,"bold"))
    city.place(x=250,y=130)
    date=ttk.Entry(frame1,font=("arial",15,"bold"))
    date.place(x=250,y=170)

    def subevent():
        mycur.execute("select empId from Employee where empDno = 2 order by rand() Limit 1")
        res = mycur.fetchone()
        res = str(''.join(map(str, res)))
        sql = "select venueId from Venue where venueCity = %s order by rand() Limit 1"
        mycur.execute(sql, [city.get()])
        #ERROR HERE
        res1 = mycur.fetchone()
        res1 = int(''.join(map(str, res1)))

        mycur.execute("insert into eventManage(eventName, eventId, empId, custId, venueId, eventDate)"
                      "values(%s,%s,%s,%s,%s,%s)",
                      (eventname.get(), eventid.get(), res, val, res1, date.get())
                      )
        mydb.commit()
        messagebox.showinfo("Event", "Event Added successfully")
        newevent.destroy()

    eid=eventid.get()
    def canEvent():
        if(eventid.get()==i):
            mycur.execute("delete from eventManage where eventid=%s",[eventid.get()])
            mydb.commit()
            messagebox.showinfo("Event", "Event Cancelation successfully")


        else:
            messagebox.showinfo("Event", "Event Does not exist")
        newevent.destroy()


    Button(frame1, text="SUBMIT", command=subevent,font=("arial",12,"bold"),relief=RIDGE,fg="white",bg="red").place(x=50,y=220)
    Button(frame1, text="CANCEL", command=canEvent,font=("arial",12,"bold"),relief=RIDGE,fg="white",bg="red").place(x=250,y=220)

# ===== CUSTOMER PAGE =====
def opencust(val):

    root.destroy()
    cust = tkinter.Tk()
    cust.geometry("1550x800+0+0")
    cust.title("Customer")

    frame2=Frame(cust, bd=4,bg="black", relief=RIDGE) 
    frame2.place(x=0,y=0,width=1550,height=140)

    main_title=Label(cust, text="EVENT MANAGEMENT SYSTEM", font=("arial", 40, "bold"), bg="blue", fg="white",bd=4,relief=RIDGE)
    main_title.place(x=0,y=140, width=1550,height=70)

    mycur1 = mydb.cursor()
    sql1 = "select custName,custId from Customer where custId=%s"
    mycur1.execute(sql1, [val])
    res1 = mycur1.fetchall()
    dres = ''
    for rec in res1[0]:
        dres += str(rec)

    login_text=Label(cust, text="Login Id: "+dres,fg="lightblue", bg="blue",font=("arial",14,"bold"),bd=4,relief=RIDGE)
    login_text.place(x=0,y=209,width=1550,height=30)


    lbl_menu=Label(cust, text="MENU", font=("arial",18,"bold"), bg="blue", fg="white",bd=4,relief=RIDGE) 
    lbl_menu.place(x=0,y=238,width=275)

    btn_frame=Frame(cust,bg="lightblue",bd=4,relief=RIDGE)
    btn_frame.place(x=0,y=275,width=275,height=520)

    cust_btn=Button(btn_frame, text="MANAGE EVENT",command=lambda: manageEvent(val), width=22, font=("arial", 14, "bold"), bg="blue", fg="white",bd=0) 
    cust_btn.grid(row=0,column=0,pady=1)

    update_btn=Button(btn_frame, text="UPDATE PROFILE",command=lambda: upProfile(2, val), width=22, font=("arial", 14, "bold"), bg="blue", fg="white",bd=0)
    update_btn.grid(row=1,column=0,pady=1)

    frame3=Frame(cust,bd=4,relief=RIDGE,bg="lightblue")
    frame3.place(x=275,y=238,width=1265,height=562)

    tree = ttk.Treeview(cust, columns=('eventDate','eventName'), show='headings')
    tree.heading('eventDate', text='Date')
    tree.heading('eventName', text='Name')
    
    sql= "select eventDate,eventName from EventManage where custId=%s"
    mycur.execute(sql,[val])
    record=mycur.fetchall()
    count = 0
    for i in record:
        if (count % 2 == 0):
            tree.insert(parent='', index='end', values=(i[0], i[1]), tags='even')
            count += 1
        else:
            tree.insert(parent='', index='end', values=(i[0], i[1]), tags='odd')
            count += 1
    tree.tag_configure('odd', background='lightblue')
    tree.place(x=907,y=288,width=582,height=442)

    scrollbar = ttk.Scrollbar(frame2, orient=VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.place()

root.mainloop()
