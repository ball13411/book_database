from django.shortcuts import render,redirect
from .forms import TestForm,login_userForm,login_passwordForm,SelecttableForm
from django.contrib import messages
import mysql.connector

# Create your views here.

#global variable
username,password,table,mydb,status,primary_key,level,mycursor = '','','','','login','',0,''
columns = []
#---------------------------------------------------------------------------------------------------------
def query(request):
    myresult,columns,count = [],[],0
    global username,mydb,status,level
    if username == "":
        return redirect('/login')
    if level == 0:
        return redirect('/home')
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
    return render(request, 'query.html',
                  {'myresult':myresult,'columns':columns,'name':username,'login':username,'logout':status,'count':count,'level':level})

#---------------------------------------------------------------------------------------------------------
def login(request):
    global username,password,status,level,mydb
    username,password,status = "","","login"
    if request.method == 'POST':
        username = request.POST['Username']
        password = request.POST['Password']
        mydb = mysql.connector.connect(
          host="localhost",
          user="user1",
          passwd="1234",
          database="book"
        )
        mycursor = mydb.cursor()
        sql = "SELECT * FROM Userdb"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        for testuser in myresult:
            if username in testuser and password in testuser:
                username = "user1"
                password = "1234"
        try:
            mydb = mysql.connector.connect(
                    host ="localhost",
                    user = username,
                    passwd = password,
                    database ="book"
                    )
            status = "logout"
            mycursor = mydb.cursor()
            username = request.POST['Username']
            try:
                mycursor.execute(("INSERT INTO cinsert (No, ID) VALUES (%s, %s)"),['10000000','71'])
                mydb.commit()
                level = 1

            except mysql.connector.errors.ProgrammingError:
                level = 0
            return redirect('/books')
        except mysql.connector.errors.ProgrammingError:
            username = ""
            messages.info(request, '!!! Login Error !!!')
    return render(request,'login.html', {'user':login_userForm,'pass':login_passwordForm,'login':username,'logout':status,'level':level})

#---------------------------------------------------------------------------------------------------------
def register(request):
    global status
    log = 0
    if request.method == "POST":
        values = []
        name = request.POST['aabb']
        email = request.POST['Email']
        passwd = request.POST['pass']
        con_passwd = request.POST["con_pass"]
        if passwd != con_passwd:
            messages.info(request, '!!! Password Error !!!')
            log = 1
            return render(request,'register.html',{'log':log,'logout':status})
        try:
            mydb = mysql.connector.connect(
                        host ="localhost",
                        user = "root1",
                        passwd = "1341",
                        database ="book"
                        )
            mycursor = mydb.cursor()
            values.append(name),values.append(email),values.append(passwd)
            insert_user = ("INSERT INTO Userdb "
                            "(Username, Email, Password) "
                            "VALUES (%s, %s, %s)")
            mycursor.execute(insert_user, values)
            mydb.commit()
            messages.info(request, '!!! Register Success !!!')
            log = 2
        except mysql.connector.errors.IntegrityError:
            messages.info(request, '!!! User Error !!!')
            log = 3
    return render(request,'register.html',{'log':log,'logout':status})
#---------------------------------------------------------------------------------------------------------
def database(request):
    global mysql,mydb,level
    myresult,columns,count = [],[],0
    if username == "":
        return redirect('/login')
    if request.method == 'POST':
        table = request.POST['Select_Table']
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
                  {'choice':SelecttableForm,'myresult':myresult,'columns':columns,'login':username,'logout':status,'count':count,'level':level})

#---------------------------------------------------------------------------------------------------------
def insert(request):
    global columns,table,username,password,level,mydb
    add_table,values,count = "",[],0
    if username == "":
        return redirect('/login')
    if level == 0:
        return redirect('/home')
    if request.method == 'POST' and 'table' in request.POST and level == 1:
        table = request.POST['Select_Table']
        sql = "SELECT * FROM "+str(table)+";"
        mycursor = mydb.cursor()
        mycursor.execute(sql)
        myresullt = mycursor.fetchall()
        columns = mycursor.column_names
        count = 1
    if request.method == 'POST' and 'insert' in request.POST:
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
        columns = []
        messages.info(request, 'Insert Success!!!')
    return render(request,'insert.html',
                  {'choice':SelecttableForm,'columns':columns,'login':username,'logout':status,'count':count,'level':level})

#---------------------------------------------------------------------------------------------------------
def home(request):
    global username,level
    return render(request,'home.html',({'login':username,'logout':status,'level':level}))
#----------------------------------------------------------------------------------------------------------
def update(request):
    global columns,table,username,password,primary_key,mydb,level
    add_table,values,count = "",[],0
    if username == "":
        return redirect('/login')
    if level == 0:
        return redirect('/home')
    if request.method == 'POST' and 'table' in request.POST and level:
        table = request.POST['Select_Table']
        mycursor = mydb.cursor()
        sql = "SELECT * FROM "+str(table)+";"
        mycursor.execute(sql)
        myresullt = mycursor.fetchall()
        columns = mycursor.column_names
        primary_key = str(columns[0])
        count = 1
    if request.method == 'POST' and 'update' in request.POST :
        for column in columns:
            value = request.POST[column]
            values.append(value)
        values.append(request.POST['primary_key'])
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
        print(values)
        mycursor.execute(update_table, values)
        mydb.commit()
        columns,primary_key = [],""
        messages.info(request, 'Insert Success!!!')
    return render(request,'update.html',
                  {'choice':SelecttableForm,'columns':columns,'login':username,'logout':status,'count':count,'primary_key':primary_key,'level':level})
#-----------------------------------------------------------------------------------------
def books(request):
    global username,status,mydb,level
    if username == "":
        return redirect('/login')
    sql = ("SELECT books.BookID,books.Title,books.Category,authors.Fname,books.PubDate "
           "FROM ((Books INNER JOIN Write_to ON Books.BookID = Write_to.Book_ID) "
           "INNER JOIN authors ON authors.No = Write_to.Author_ID);")
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    columns = mycursor.column_names
    myresult = mycursor.fetchall()
    return render(request, 'books.html',
                  {'myresult':myresult,'columns':columns,'name':username,'login':username,'logout':status,'level':level})
#-------------------------------------------------------------------------------------------
def delete(request):
    global columns,table,username,password,primary_key,mydb,level
    add_table,values,count = "",[],0
    if username == "":
        return redirect('/login')
    if level == 0:
        return redirect('/home')
    if request.method == 'POST' and 'table' in request.POST and level:
        table = request.POST['Select_Table']
        mycursor = mydb.cursor()
        sql = "SELECT * FROM "+str(table)+";"
        mycursor.execute(sql)
        myresullt = mycursor.fetchall()
        columns = mycursor.column_names
        primary_key = str(columns[0])
        count = 1
    if request.method == 'POST' and 'delete' in request.POST :
        value = (request.POST['primary_key'])
        print(value)
        if table == 'Books':
            delete_table = ("DELETE FROM Books WHERE BookID=%s;"%(value))
        elif table == 'Authors':
            delete_table = ("DELETE FROM Authors WHERE No=%s;"%(value))
        elif table == 'Locations':
            delete_table = ("DELETE FROM Locations WHERE No=%s;"%(value))
        elif table == 'Publishers':
            delete_table = ("DELETE FROM Publishers WHERE No=%s;"%(value))
        elif table == 'Sent_to':
            delete_table = ("DELETE FROM Sent_to WHERE Author_ID=%s;"%(value))
        elif table == 'Write_to':
            delete_table = ("DELETE FROM Write_to WHERE Book_ID=%s;"%(value))
        mydb = mysql.connector.connect(
            host ="localhost",
            user = username,
            passwd = password,
            database ="book"
            )
        mycursor = mydb.cursor()
        mycursor.execute(delete_table)
        mydb.commit()
        columns,primary_key = [],""
        messages.info(request, 'Insert Success!!!')
    return render(request,'delete.html',
                  {'choice':SelecttableForm,'columns':columns,'login':username,'logout':status,'count':count,'primary_key':primary_key,'level':level})
#-----------------------------------------------------------------------------------



