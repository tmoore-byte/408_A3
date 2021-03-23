# import statements
import sqlite3
import pandas as pd
from pandas import DataFrame

# importing the students.csv file into created Students table
conn = sqlite3.connect('./StudentDB.sqlite')  # establishing connection to database
print("opened database")
mycursor = conn.cursor()  # the connection cursor allows python to execute SQL statements


# reading in students.csv
def file():
    # selecting everything from Student table
    mycursor.execute("SELECT * FROM Students")
    data = mycursor.fetchall()
    if (data == []):
        with open("./students.csv") as f:
            records = 0
            for row in f:
                if records != 0:
                    mycursor.execute(
                        "INSERT INTO Students(FirstName, LastName, Address, City, State, ZipCode, MobileNumber, Major, GPA) VALUES (?,?,?,?,?,?,?,?,?)",
                        row.split(","))
                    conn.commit()
                records += 1


def options():
    while True:
        print("Welcome to the Student Database! ")
        print("Would you like to: ")
        print("1: Display all Students & attributes")
        print("2: Add a Student")
        print("3: Update a record")
        print("4: Delete a record")
        print("5: Search/Display a Students with attributes")
        print("Enter 6 if you would like to exit")

        # this is where the user selects what they want to do

        entry = int(input("enter the associated number: "))

        # this is where we check the user's entry
        if (entry == 1):
            display()
            continue
        elif (entry == 2):
            add()
            continue
        elif (entry == 3):
            update()
            continue
        elif (entry == 4):
            delete()
            continue
        elif (entry == 5):
            search()
            continue
        elif (entry == 6):
            exit()
        else:
            print("you have entered an invalid entry ")
            # return to to start of program code here


# defining all of our funtions that the user will call from entry
def display():
    mycursor.execute('SELECT * FROM Students;')
    all_records = mycursor.fetchall()
    # use pd.set_option to display full table with all attributes
    pd.set_option("display.max_rows", None, "display.max_columns", None, "display.width", None)
    # use DataFrame for cleaner display
    df = DataFrame(all_records,
                   columns=['StudentId', 'FirstName', 'LastName', 'GPA', 'Major', 'FacultyAdvisor', 'Address', 'City',
                            'State', 'ZipCode', 'MobileNumber', 'isDeleted'])
    print(df)


def add():
    # code to add a student to the database
    userFirstName = input("enter the first name: ")
    userLastName = input("enter the last name: ")
    while True:
        try:
            userGPA = float(input("Enter student's GPA: "))
            break
        except ValueError:
            print("invalid entry format: ")
    userMajor = input("Enter student's major: ")
    userFacultyAdvisor = input("enter student's advisor: ")
    userAddress = input("enter student's address: ")
    userCity = input("enter student's city: ")
    userState = input("enter the state the student lives: ")
    ii = True
    while (ii == True):
        try:
            userZipCode = int(input("enter the student's zipcode: "))
            count = 0
            while (userZipCode > 0):
                userZipCode = userZipCode // 10
                count += 1
            if (count == 5):
                ii = False
            else:
                print("enter 5 digit zipcode: ")
                continue
            break
        except ValueError:
            print("Please enter digits. Try again: ")
    while True:
        try:
            userMobileNumber = input("Enter the student's phone number: ")
            break
        except ValueError:
            print("Please enter all digits of phone number. Try again: ")
    mycursor.execute(
        "INSERT INTO Students (FirstName, LastName, GPA, Major, FacultyAdvisor, Address, City, State, ZipCode, MobileNumber) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",(userFirstName, userLastName, userGPA, userMajor, userFacultyAdvisor, userAddress, userCity, userState,
         userZipCode, userMobileNumber,))
    print("The student was successfully added.")
    conn.commit()


def update():
    # updating a record in student database
    test = True
    while (test == True):
        # Check to make sure the enter student id is in the Students table
        userUpdate = input("Please enter the student ID of the student you would like to update: ")
        mycursor.execute("SELECT DISTINCT StudentId FROM Students WHERE StudentId = ?", [userUpdate])
        records = mycursor.fetchall()
        if records == []:
            print("Please enter a valid student ID")
            continue
        else:
            option = True
            while (option == True):
                userChoice = input(
                    "Would you like to update major(1), advisor(2), mobile number(3). Please type in the corresponding number: ")
                if userChoice == "1":
                    majorUpdate = input("Please enter the new updated major: ")
                    mycursor.execute("UPDATE Students SET Major = ? WHERE StudentId = ?", (majorUpdate, userUpdate,))
                    print("Successfully updated!")
                    test = False
                    option = False
                elif userChoice == "2":
                    advisorUpdate = input("Please enter the new updated advisor: ")
                    mycursor.execute("UPDATE Students SET FacultyAdvisor = ? WHERE StudentId = ?",
                                     (advisorUpdate, userUpdate,))
                    print("Successfully updated!")
                    test = False
                    option = False
                elif userChoice == "3":
                    while True:
                        try:
                            phoneUpdate = input("Please enter the new updated phone number: ")
                            break
                        except ValueError:
                            print("Please enter all digits of phone number. Try again: ")
                    mycursor.execute("UPDATE Students SET MobileNumber = ? WHERE StudentId = ?",
                                     (phoneUpdate, userUpdate,))
                    print("Successfully updated!")
                    test = False
                    option = False
                else:
                    print("Please enter a valid option.")
                    continue
    conn.commit()


def delete():
    # deleting a record from student database
    i = 1
    while (i == 1):
        # Check to make sure the enter student id is in the Students table
        delete_id = input("Who would you like to delete (enter student ID): ")
        mycursor.execute("SELECT DISTINCT StudentId FROM Students WHERE StudentId = ?", [delete_id])
        records = mycursor.fetchall()
        # checking if its empty
        if records == []:
            print("Please enter a valid student ID")
            continue
        else:
            i != 1
            mycursor.execute("UPDATE Students SET isDeleted = 1 WHERE StudentId = ?", (delete_id,))
            print("Deleted, ", delete_id, "from the database")
            conn.commit()


def search():
    # searching and displaying a record from student database
    print("Enter the number you would like to search a student by: ")
    print("1 major")
    print("2 GPA")
    print("3 city")
    print("4 state")
    print("5 faculty advisor")
    i = True
    while (1 == 1):
        search_num = input("selected number: ")
        if search_num == "1":
            mycursor.execute("select DISTINCT Major from Students")  # only showing unique majors... no repeats
            print(mycursor.fetchall())
            ii = True
            # if they selected search by major... now we ask what major
            while (ii == 1):
                search_major = input("Select a major to search by: ")
                mycursor.execute("SELECT * FROM Students WHERE Major = ?", (search_major,))
                records = mycursor.fetchall()
                if records == []:
                    print("invalid entry")
                    continue
                else:
                    ii = False
                    pd.set_option("display.max_rows", None, "display.max_columns", None, "display.width", None)
                    df = DataFrame(records,
                                   columns=['StudentId', 'FirstName', 'LastName', 'GPA', 'Major', 'FacultyAdvisor',
                                            'Address', 'City', 'State', 'ZipCode', 'MobileNumber', 'isDeleted'])
                    print(df)
                    i = False
        elif search_num == "2":
            # show user their options to choose from
            mycursor.execute("SELECT DISTINCT GPA FROM Students")
            print(mycursor.fetchall())
            ii = True
            while (ii == True):
                search_gpa = input("Select a gpa to search by: ")
                mycursor.execute("SELECT * FROM Students WHERE GPA = ?", (search_gpa,))
                records = mycursor.fetchall()
                if records == []:
                    print("invalid entry")
                    continue
                else:
                    ii = False
                    pd.set_option("display.max_rows", None, "display.max_columns", None, "display.width", None)
                    df = DataFrame(records,
                                   columns=['StudentId', 'FirstName', 'LastName', 'GPA', 'Major', 'FacultyAdvisor',
                                            'Address', 'City', 'State', 'ZipCode', 'MobileNumber', 'isDeleted'])
                    print(df)
                    i = False
        # if user selects to search by city
        elif search_num == "3":
            mycursor.execute("SELECT DISTINCT City FROM Students")
            print(mycursor.fetchall())
            ii = True
            while (ii == True):
                search_city = input("What city would you like to search by: ")
                mycursor.execute("SELECT * FROM Students WHERE City = ?", (search_city,))
                records = mycursor.fetchall()
                if records == []:
                    print("invalid entry")
                    continue
                else:
                    ii = False
                    pd.set_option("display.max_rows", None, "display.max_columns", None, "display.width", None)
                    df = DataFrame(records,
                                   columns=['StudentId', 'FirstName', 'LastName', 'GPA', 'Major', 'FacultyAdvisor',
                                            'Address', 'City', 'State', 'ZipCode', 'MobileNumber', 'isDeleted'])
                    print(df)
                    i = False
        # if user selects to search by selected state
        elif search_num == "4":
            mycursor.execute("SELECT DISTINCT State FROM Students")
            print(mycursor.fetchall())
            ii = True
            while (ii == True):
                search_state = input("What state would you like to search by: ")
                mycursor.execute("SELECT * FROM Students WHERE State = ?", (search_state,))
                records = mycursor.fetchall()
                if records == []:
                    print("invalid entry")
                    continue
                else:
                    ii = False
                    pd.set_option("display.max_rows", None, "display.max_columns", None, "display.width", None)
                    df = DataFrame(records,
                                   columns=['StudentId', 'FirstName', 'LastName', 'GPA', 'Major', 'FacultyAdvisor',
                                            'Address', 'City', 'State', 'ZipCode', 'MobileNumber', 'isDeleted'])
                    print(df)
                    i = False
        # if user selects to search by Advisor
        elif search_num == "5":
            mycursor.execute("SELECT DISTINCT FacultyAdvisor FROM Students")
            print(mycursor.fetchall())
            ii = True
            while (ii == True):
                search_advisor = input("What advisor would you like to search by: ")
                mycursor.execute("SELECT * FROM Students WHERE FacultyAdvisor = ?", (search_advisor,))
                records = mycursor.fetchall()
                if records == []:
                    print("invalid entry")
                    continue
                else:
                    ii = False
                    pd.set_option("display.max_rows", None, "display.max_columns", None, "display.width", None)
                    df = DataFrame(records,
                                   columns=['StudentId', 'FirstName', 'LastName', 'GPA', 'Major', 'FacultyAdvisor',
                                            'Address', 'City', 'State', 'ZipCode', 'MobileNumber', 'isDeleted'])
                    print(df)
                    i = False
        else:
            print("invalid entry")
            continue
    conn.commit()


def exit():
    # exiting the program... maybe dont need this
    # just use and else
    print("this is the exit function")
