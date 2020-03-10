#Albert
import sqlite3 as sq
from datetime import datetime, date

con = sq.connect("novel.db")
c = con.cursor()

#Function gets author's data from the table
def get_author():
    res = c.execute("SELECT AuthorID, AuthorDOB, AuthorName from Author")
    data = c.fetchall() 
    return data

#Function gets novel's data from the table
def get_novel():
    res = c.execute("SELECT * from Novel")
    data = c.fetchall()
    return data

#Creates a data with only novel, author and publication date
def get_novel_report():
    res = c.execute("SELECT Title, AuthorName, NovelPD from author, novel where author.AuthorID = novel.AuthorID")
    data = c.fetchall()
    return data
#This function adds a new novel into the tables
def add_novel(dt, authorID, bookID, novel_name):
    ins_str = 'INSERT INTO Novel (BookID, Title, NovelPD, AuthorID) Values (' + str(bookID) + ', "' + str(novel_name) + '", "' + str(dt) + '", ' + str(authorID) + ');'
    res = c.execute(ins_str)
    con.commit()		




# This function gives the user 3 options, novel report, add novel, or exit
#main menu
def render_menu():
    print("1. All Novels & Authors")
    print("2. Enter New Novel")
    print("3. Exit")
    choice = int(input("Choose an option:\t"))

    if choice == 1:
        novel_report()
    elif choice == 2:
        enter_novel()
    elif choice == 3:
        end_program()
        return False;

    return True;


def end_program():
    con.close()

#This function prints out the novel report
def novel_report():
   
    report = get_novel_report()
    tbl = "|---------------------------\n|"
    for row in report:
        for field in row:
            tbl += str(field)
            tbl += ", "
        tbl += "\n|"
    tbl += "---------------------------"

    print("Report results\n\n" + tbl)

#This function gives the user a selection of authors where they can choose from. Then it asks for the novel name and publication date
def enter_novel():

    author = get_author()
    authorchoice = author_lb(author)
    
    novel_name = input("enter novel name: ")
    
    day = int(input("enter published day:\t"))
    month = int(input("enter published month:\t"))
    year = int(input("enter published year:\t"))

    c.execute("select count(BookID) from novel")

    bookid = c.fetchone()[0] + 1

    check_and_enter_selection(day, month, year, authorchoice, bookid, novel_name)

#This shows the author options 
def author_lb(author):
    print("\n\nAuthors\n")
    for row in author:
        print(row)
    author = input("\nChoose an author by ID num:\t")
    return author


# This function checks for error in the system and spits out an error message if there are.
def check_and_enter_selection(d, m, y, a, b, n):

    try: 
        dt = date(int(y), int(m) , int(d))
        add_novel(dt, a, b, n)
        print("Success", "Your Novel has been added")

    except:
        print("Error- Try again", "Possible errors:  \nthere is already a novel for that combination, you chose an invalid author\nthe date is in an invalid format, \nsomeone else is entering a novel at the same time")
        return


# repeats the menu after either option 1 or 2 is finished. Option 3 exits
while(render_menu()):
    print("\n\nWelcome to Albert's Library")

