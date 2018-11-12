import requests
from os import system, name, path
from getpass import *
import argparse
from BeautifulSoup import *
import re
global accountData
accountData = {}
#>([_A-Za-z]+),\x20([_A-Za-z]+)</option>
def submitHW(filename, teacherComment=""):
    f = open(filename, "rb")
    url = "http://bert.stuy.edu/pbrooks/fall2018/pages.py"
    data = {
        "students":accountData["ID"] + ";" + accountData["name"], 
        "classes":"p10", 
        "password":accountData["password"], 
        "Submit":"Submit", 
        "page":"submit_homework2"
    }
    r = requests.post(url, data=data, allow_redirects=True)    
    soup = BeautifulSoup(r.content)
    assignmentID = soup.find('option', selected=True)["value"]
    id4 = soup.find("input", {"name":"id4"})["value"]
    files = {
        "filecontents":f
    }
    data = {
        "students":accountData["ID"] + ";" + accountData["name"], 
        "classid":"p10", 
        "assignmentid":assignmentID,
        "teacher_comment":teacherComment,
        "password":accountData["password"], 
        "Submit":"Submit this assignment", 
        "page":"store_homework",
        "id4":id4}#,
        #"filecontents":f}
    r = requests.post(url, files=files, data=data, allow_redirects=True)    
    
def viewHWSoup(submit=False):
    url = "http://bert.stuy.edu/pbrooks/fall2018/pages.py"
    page = "homework_view2" if not submit else "submit_homework2"
    data = {
        "students":accountData["ID"] + ";" + accountData["name"], 
        "classes":"p10", 
        "password":accountData["password"], 
        "Submit":"Submit", 
        "page":page
    }
    r = requests.post(url, data=data, allow_redirects=True)
    #print r.content    
    soup = BeautifulSoup(r.content.decode("utf8"))
    return soup
def clear():
    """ Clears the screen. """
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')
      
def setupAccount():
    lines = open("classData.txt").readlines()
    count = 1
    fData = {}
    for line in lines:
        print "[" + str(count) + "] -> " + line.strip().split(";")[1]
        fData[count] = tuple(line.strip().split(";"))
        count += 1
        
    number = ""
    
    while not number.isdigit():
        number = raw_input("Please select your name (number) :")
    number = int(number)
    accountID, name = fData[number]
    password = ""
    password2 = "1"
    while password != password2:
        clear()
        password = getpass("Please enter password: ")
        password2 = getpass("Please enter confirmation password: ")
    account = open("account.txt", "w")
    account.write("name:" + name + "\n")
    account.write("ID:" + accountID + "\n")
    account.write("password:" + password )
    clear()
    
def viewData(verbose=False):

    soup = viewHWSoup()
    tables = soup.findAll("table")
    tables.pop(0)
    for table in tables:
        rows = table.findChildren("tr")
        data = [[td.findChildren(text=True) for td in tr.findAll("td")] for tr in rows]
    
        data = [["".join(d).strip().replace("&nbsp", "").replace(";", "") for d in l] for l in data]
        #print "\n"
        if verbose:
            for i in data:

                for x in xrange(0, len(i) - 1, 2):
                    print i[x], i[x + 1]#, "\n"
        else:
            print data[0][0], data[0][1]
        print "-" * 20
 #   x
def viewTests(opt="all"):
    soup = viewHWSoup()
    tables = soup.findAll("table")
    table = tables.pop(1)    
    links = table.findAll("a")
    HWFile, test, prevTests = tuple(links)
    HWFile = re.search('href=(.*)>t', str(HWFile)).group(1).replace('"',"")
    test = re.search('href=(.*)><img', str(test)).group(1).replace('"',"")
    prevTests = re.search('href=(.*)><img', str(prevTests)).group(1).replace('"',"")
    if opt == "hw":
        r = requests.get("http://bert.stuy.edu/pbrooks/fall2018/" + HWFile)
        print r.content
    else:
        if opt == "test":
            r = requests.get("http://bert.stuy.edu/pbrooks/fall2018/" + test)
        else:
            r = requests.get("http://bert.stuy.edu/pbrooks/fall2018/" + prevTests)
        soup = BeautifulSoup(r.content.decode("utf8"))
        tables = soup.findAll("table")
        tables.pop(0)
        rows = tables[0].findChildren("tr")
        data = [[td.findChildren(text=True) for td in tr.findAll("td")] for tr in rows]
    
        data = [["".join(d).strip().replace("&nbsp", "").replace(";", "") for d in l] for l in data]
        print data[0][0]
        print "-" * 17
        if opt== "all":
            for i in xrange(1, len(data) - 1, 2):
                for x in xrange(4):
                    print data[1][x], " : ", data[i][x]     
                print "-" * 17
        else:
            for i in xrange(4):
                print data[1][i], " : ", data[2][i]
    
def loadData():
    lines = open("account.txt").readlines()
    for line in lines:
        l = line.strip().split(":")
        accountData[l[0]] = l[1]
        
    

def main():
    if not path.exists("account.txt"):
        setupAccount()
    else:
        loadData()
        parser = argparse.ArgumentParser(
            description="A program to work with Mr Brooks' site.",
            epilog="""Usage:
    python ProgramTester.py -hw [-v -f] 
        Displays list of homework assignments.
        Extra Options:
            -v : Displays homework assignments and other information.
            -f : Displays the file you submitted for the homework.
        
    python ProgramTester.py -s <file name> [-c <Comment to the teacher>]
        Submits the file for the latest homework.
        Extra Options:
            -c <comment> : Submits the file with <comment> as the comment to the teacher   
    python ProgramTester.py -t [-v]
        Tests the program on the program tester and displays the result.
        Extra Options:
            -v : View previous tests without testing.    
            """,
            formatter_class=argparse.RawTextHelpFormatter
        )
        parser.add_argument("-hw", "--homework", help="Views the latest homework", action="store_true")
        parser.add_argument("-f", "--viewfile", help="Views the latest homework file. Used with -hw", action="store_true")        
        parser.add_argument("-v", "--verbose", help="Makes output verbose. Used with -hw or -t", action="store_true") 
        
        parser.add_argument("-r", "--reset", help="Reset saved account data on your machine.", action="store_true")
        
        parser.add_argument("-t", "--test", help="Tests the latest homework on the server.", action="store_true")
        
        parser.add_argument("-s", "--submit", help="Submits the homework file to the latest assignment.", dest="filename", action="store")
        parser.add_argument("-c", "--comment", help="Adds a comment while submitting the file. Used with -c", dest="comment", action="store")
        
        args = parser.parse_args()        
        if args.homework:
            if not args.viewfile:
                viewData(verbose=args.verbose)
            else:
                viewTests(opt="hw")
        elif args.reset:
            setupAccount()
        elif args.test:
            o = "all" if args.verbose else "test"
            viewTests(opt=o)
        elif args.filename:
            comment = args.comment if args.comment else ""
            submitHW(args.filename, teacherComment=comment)


if __name__ == "__main__":
    main()