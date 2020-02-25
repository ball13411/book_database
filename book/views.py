from django.shortcuts import render,redirect
from .forms import TestForm,login_userForm,login_passwordForm,SelecttableForm
from django.contrib import messages
import mysql.connector

# Create your views here.

#global variable
username,password,table,mydb,status,primary_key = '','','','','login',''
columns = []
#---------------------------------------------------------------------------------------------------------
def index(request):
    myresult,columns,count = [],[],0
    global username,mydb
    if username == "":
        return redirect('/login')
    if request.method == 'POST' and 'query1' in request.POST:
        mycursor = mydb.cursor()
        try:
            sql = request.POST['query1']
            mycursor.execute(sql)
            columns = mycursor.column_names
            myresult = mycursor.fetchall()
            count = 1
        except:
            myresult,columns = [],[]
    return render(request, 'index.html',
                  {'myresult':myresult,'columns':columns,'name':username,'login':username,'logout':status,'count':count})


#---------------------------------------------------------------------------------------------------------
def login(request):
    global mydb,username,password,status
    username = ""
    password = ""
    status = "login"
    if request.method == 'POST':
        username = request.POST['Username']
        password = request.POST['Password']
        try:
            mydb = mysql.connector.connect(
            host ="localhost",
            user = username,
            passwd = password,
            database ="book"
            )
            status = "logout"
            return redirect('/index')
        except:
            username = ""
            messages.info(request, '!!! Login Error !!!')
    return render(request,'login.html', {'user':login_userForm,'pass':login_passwordForm,'login':username,'logout':status})

#---------------------------------------------------------------------------------------------------------
def database(request):
    myresult,columns,count = [],[],0
    if username == "":
        return redirect('/login')
    if request.method == 'POST':
        table = request.POST['Select_Table']
        mydb = mysql.connector.connect(
        host ="localhost",
        user = 'user1',
        passwd = '1234',
        database ="book"
        )
        mycursor = mydb.cursor()
        try:
            sql = "SELECT * FROM "+str(table)
            mycursor.execute(sql)
            columns = mycursor.column_names
            myresult = mycursor.fetchall()
            count = 1
        except:
            myresult,columns = [],[]

    return render(request, 'database.html',
                  {'choice':SelecttableForm,'myresult':myresult,'columns':columns,'login':username,'logout':status,'count':count})

#---------------------------------------------------------------------------------------------------------
def insert(request):
    global columns,table,username,password
    add_table,values,check,count = "",[],False,0
    if username == "":
        return redirect('/login')
    try:
        mydb = mysql.connector.connect(
        host ="localhost",
        user = username,
        passwd = password,
        database ="book"
        )
        mycursor = mydb.cursor()
        mycursor.execute(("INSERT INTO cinsert (No, ID) VALUES (%s, %s)"),['1','1'])
        mydb.commit()
        mycursor.close()
        mydb.close()
        check = True
    except mysql.connector.errors.ProgrammingError:
        messages.info(request, '!!! User Error !!!')
    if request.method == 'POST' and 'table' in request.POST and check:
        table = request.POST['Select_Table']
        mydb = mysql.connector.connect(
        host ="localhost",
        user = username,
        passwd = password,
        database ="book"
        )
        mycursor = mydb.cursor()
        sql = "SELECT * FROM "+str(table)+";"
        mycursor.execute(sql)
        columns = mycursor.column_names
        count = 1
    if request.method == 'POST' and 'insert' in request.POST :
        for column in columns:
            value = request.POST[column]
            values.append(value)
        if table == 'Books':
            add_table = ("INSERT INTO Books "
                        "(BookID, Title, No_of_Pages, Publish_No, Category,PubDate) "
                        "VALUES (%s, %s, %s, %s, %s, %s)")
        elif table == 'Authors':
            add_table = ("INSERT INTO Authors "
                        "(No, Fname, Lname) "
                        "VALUES (%s, %s, %s)")
        elif table == 'Locations':
            add_table = ("INSERT INTO Locations "
                        "(No, Location) "
                        "VALUES (%s, %s)")
        elif table == 'Publishers':
            add_table = ("INSERT INTO Publishers "
                        "(No, Publisher_Name, PhoneNo) "
                        "VALUES (%s, %s, %s)")
        elif table == 'Sent_to':
            add_table = ("INSERT INTO Sent_to "
                        "(Author_ID, Publisher_No) "
                        "VALUES (%s, %s)")
        elif table == 'Write_to':
            add_table = ("INSERT INTO Write_to "
                        "(Book_ID, Author_ID) "
                        "VALUES (%s, %s)")
        mydb = mysql.connector.connect(
        host ="localhost",
        user = username,
        passwd = password,
        database ="book"
        )
        mycursor = mydb.cursor()
        mycursor.execute(add_table, values)
        mydb.commit()
        mycursor.close()
        mydb.close()
        columns = []

    return render(request,'insert.html',{'choice':SelecttableForm,'columns':columns,'login':username,'logout':status,'count':count})

#---------------------------------------------------------------------------------------------------------
def home(request):
    global username
    return render(request,'home.html',({'login':username,'logout':status}))
#----------------------------------------------------------------------------------------------------------
def manage(request):
    global columns,table,username,password
    add_table,values,check,columns,myresult = "",[],False,[],[]
    if username == "":
        return redirect('/login')
    try:
        mydb = mysql.connector.connect(
        host ="localhost",
        user = username,
        passwd = password,
        database ="book"
        )
        mycursor = mydb.cursor()
        mycursor.execute(("INSERT INTO cinsert (No, ID) VALUES (%s, %s)"),['1','1'])
        mydb.commit()
        mycursor.close()
        mydb.close()
        check = True
    except mysql.connector.errors.ProgrammingError:
        messages.info(request, '!!! User Error !!!')
    if request.method == 'POST' and check:
        table = request.POST['Select_Table']
        mydb = mysql.connector.connect(
        host ="localhost",
        user = username,
        passwd = password,
        database ="book"
        )
        mycursor = mydb.cursor()
        try:
            sql = "SELECT * FROM "+str(table)
            mycursor.execute(sql)
            columns = mycursor.column_names
            # columns = list(columns) + ['Edit','Delete']
            myresult = mycursor.fetchall()
        except:
            myresult,columns = [],[]
    return render(request,'manage.html',{'choice':SelecttableForm,'myresult':myresult,'columns':columns,'login':username,'logout':status})

#-----------------------------------------------------------------------------------------
def update(request):
    global columns,table,username,password,primary_key
    add_table,values,check,count = "",[],False,0
    if username == "":
        return redirect('/login')
    try:
        mydb = mysql.connector.connect(
        host ="localhost",
        user = username,
        passwd = password,
        database ="book"
        )
        mycursor = mydb.cursor()
        mycursor.execute(("INSERT INTO cinsert (No, ID) VALUES (%s, %s)"),['1','1'])
        mydb.commit()
        mycursor.close()
        mydb.close()
        check = True
    except mysql.connector.errors.ProgrammingError:
        messages.info(request, '!!! User Error !!!')
    if request.method == 'POST' and 'table' in request.POST and check:
        table = request.POST['Select_Table']
        mydb = mysql.connector.connect(
        host ="localhost",
        user = username,
        passwd = password,
        database ="book"
        )
        mycursor = mydb.cursor()
        sql = "SELECT * FROM "+str(table)+";"
        mycursor.execute(sql)
        columns = mycursor.column_names
        primary_key = str(columns[0])
        count = 1
    if request.method == 'POST' and 'update' in request.POST :
        for column in columns:
            value = request.POST[column]
            values.append(value)
        values.append(request.POST[primary_key])
        if table == 'Books':
            update_table = ("UPDATE Books "
                            "SET BookID = %s,Title = %s,No_of_Pages  = %s,Publish_No = %s, Category  = %s,PubDate  = %s "
                            "WHERE BookID = %s")
        elif table == 'Authors':
            update_table = ("UPDATE Authors "
                            "SET No=%s, Fname=%s,Lname=%s "
                            "WHERE No=%s")
        elif table == 'Locations':
            update_table = ("UPDATE Locations "
                            "SET No=%s, Location=%s "
                            "WHERE No=%s")
        elif table == 'Publishers':
            update_table = ("UPDATE Publishers "
                            "SET No=%s, Publisher_Name=%s,PhoneNo=%s "
                            "WHERE No=%s")
        elif table == 'Sent_to':
            update_table = ("UPDATE Sent_to "
                            "SET Author_ID=%s, Publisher_No=%s "
                            "WHERE Author_ID=%s")
        elif table == 'Write_to':
            update_table = ("UPDATE Write_to "
                            "SET Book_ID=%s, Author_ID=%s "
                            "WHERE Book_ID=%s")
        mydb = mysql.connector.connect(
        host ="localhost",
        user = username,
        passwd = password,
        database ="book"
        )
        mycursor = mydb.cursor()
        mycursor.execute(update_table, values)
        mydb.commit()
        mycursor.close()
        mydb.close()
        columns,primary_key = [],""
    return render(request,'update.html',
                  {'choice':SelecttableForm,'columns':columns,'login':username,'logout':status,'count':count,'primary_key':primary_key})




