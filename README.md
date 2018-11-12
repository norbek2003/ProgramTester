# ProgramTester
A script for using Mr Brooks' site through the command line
#Usage:
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