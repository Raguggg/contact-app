import sqlite3
conn = sqlite3.connect('myContact.db')
cur = conn.cursor()
P=print
T = True
ip = """
*******************************************
\u001b[32m*       >view contact      ===> 1          *
\u001b[33m*       >Add contact       ===> 2          *
\u001b[34m*       >Search Contact    ===> 3          *
\u001b[35m*       >delete Contact    ===> 4          *
\u001b[36m*       >Edit contact      ===> 5          *
\u001b[31m*       >tab to back                       *
\u001b[38m*       >double tab to exit                *
        >You can search directly           *
\u001b[0m*******************************************
\u001b[31m===>\u001b[0m"""
try:
    cur.execute("""CREATE TABLE contact(
        Name text,
        phnoNumber text
    )
    """)
except:
    P()
    P("-------------Database connected successfully-----------------",flush=T)

PL1 = '\u001b[35m+'+'-'*6+'+'+'-'*31+'+'+'-'*27+'+\033[0m'
PL2 = "\u001b[35m|"+'-'*6+'|'+'-'*31+'|'+'-'*27+'|'
PL3 = '\u001b[35m|\033[0m  {:<4}\u001b[35m|\033[0m {:^30s}\u001b[35m|\033[0m {:^25s} \u001b[35m|'.format('Sno','Name', 'Phone_no')

#contact class
class contact:

    #for future update of oops
    def __init__(self):
        pass

    # Used to highlight text what user search
    def colored(value,text):
        l = len(text)
        C1=False
        for i in range(len(value)):
            if text.upper()==value[i:l].upper():
                j = value[i:l]
                C1 = T
                break
            l+=1
            pass
        if C1:return "\033[38;2;0;255;0m{}\033[38;2;255;255;255m".format(j).join(value.split(j))
        return value


    # checking weather db is empty
    def isempty(view=False):
        check = cur.execute("SELECT *FROM contact ORDER BY Name")
        IE1 = check.fetchall()
        if len(IE1)==0:
            P("Not yet single contact is saved.............",flush=T)
            return False
        if view:return IE1
        return T


    # view full contact
    def view():
        V = contact.isempty(T)
        if V==False:return 'continue'
        P(flush=T)
        P(PL1,PL3,PL2,sep='\n')
        j=1
        PL4 = len(V)
        for i in V:
            P("|\033[0m  {:<4d}\u001b[35m|\033[0m {:<30s}\u001b[35m|\033[0m {:<25s}".format(j, i[0], i[1]),end=" \u001b[35m|\n",flush=T)
            if j<PL4:P(PL2)
            j+=1
        P(PL1,flush=T)
        pass

    
    # It is used to view the contact in search
    def searchView(value,mainLoop=False):
        SV1,_ = contact.search(value)
        P(flush=T)
        if SV1==False:
            if mainLoop:return False
            P(f"-------------Oops '{value}' is not in your contact----------------'",flush=T)
        else:
            k=1
            SV4 = len(SV1)
            P(PL1,PL3,PL2,sep='\n')
            for i in SV1:
                P("|\033[0m  {:<4d}\u001b[35m|\033[0m {:<64s}\u001b[35m|\033[0m {:<25s}".format(k,contact.colored(i[0],value),contact.colored(i[1],value)),end=" \u001b[35m|\n",flush=T)
                if k<SV4:P(PL2)
                k+=1
                pass
            P(PL1)
            pass
        pass


    # search contact
    def search(value,ad=T):
        V6 = 'false'
        if ad:
            V1 = contact.isempty(T)
            if V1==False:return 'continue'
        V4 = []                             #V4 ===> store output list
        cmd = [ "Name='{}'",
                "Name LIKE '%{}%'",
                "phnoNumber='{}'",
                "phnoNumber LIKE '%{}%'"
               ]
        for V3 in range(2):
            V5 = cur.execute("SELECT *FROM contact WHERE "+ cmd[V3].format(value))
            V4+=V5.fetchall()
            pass
        VT = len(V4)
        if value.isnumeric():
            for V3 in range(2,4):
                V5 = cur.execute("SELECT *FROM contact WHERE "+ cmd[V3].format(value))
                V4+=V5.fetchall()
                pass
            pass
        if VT<len(V4):
            V6 = 'true'
        if len(V4)!=0:
            V4 = [*set(V4)]
            return V4,V6
        return False,V6


    # Used to check contact is present without case sensitive
    def check(value,add=T):
        C1,NUM = contact.search(value,add)
        if C1==False:return False,NUM
        for C2 in C1:
            if C2[0].upper()==value.upper():
                if not add:return False
                return C2,NUM
        if not add:return True
        return False,NUM


    # Adding new contact
    def addNewContact(data):
        A1 = contact.check(data[0],False)
        if A1:
            cur.execute("INSERT INTO contact VALUES (?,?)", data)
            P(flush=T)
            P(f"------------------'{data[0]}' is saved in your contact successfully----------------",flush=T)
            return T
        else:
            P(flush=T)
            P(f"----X-----X-----Oops '{data[0]}' is already exciting----X-------X----",flush=T)
            P(flush=T)
            A2 = input('Enter a new Name: ')
            if A2=='\t':return 'continue'
            A2 = A2.strip()
            A3 = list(data)
            A3[0]=A2
            return contact.addNewContact(tuple(A3))



    # Deleting contact
    def deleteContact(value):
        D1,NUM = contact.check(value)
        if  D1==False and NUM=='false':
            P(flush=T)
            P(f"----X-----------X---------'{value}' is not in your contact--------X----------X------",flush=T)
            return False
        elif NUM=='true':
            contact.searchView(value)
            P('Enter the Name to delete: ',end='')
            D2 = input()
            if D2=='\t':return 'continue'
            contact.deleteContact(D2.strip())
            pass
        else:
            cur.execute(f"DELETE FROM contact WHERE Name='{D1[0]}'")
            P(flush=T)
            P(f"-----'{value}' is deleted successfully-----",flush=T)
            return T


    # Edit contact 
    def editContact(value):
        E1,_=contact.check(value)
        P()
        if E1!=False:
            P()
            P(f"Name         : { E1[0]}\nPhone Number : {E1[1]}")
            P('If to edit name enter n or number enter num: ',flush=T)
            E2 = input()
            P()
            if E2=='\t':return 'continue'
            E2=E2.strip()
            if E2.upper()=='N':
                while True:
                    P("Enter the new Name : ",end='')
                    E3 = input()
                    if E3=='\t':break;return 'continue'
                    E3 = E3.strip()
                    E5,_=contact.check(E3)
                    if E5!=False:
                        P(f"oops the {E3} is already exciting ")
                        continue
                    else:
                        cur.execute(f"UPDATE contact SET Name='{E3}' WHERE Name='{E1[0]}'")
                        P("----------The contact is updated successfully--------------")
                        break
                pass
            if E2.upper()=='NUM':
                P("Enter the new Number: ",end='')
                E3 = input()
                if E3=='\t':return 'continue'
                E3 = E3.strip()
                cur.execute(f"UPDATE contact SET phnoNumber={E3} WHERE phnoNumber={E1[1]}")
                P("----------The contact is updated successfully--------------")
                pass
            pass
        else:
            P(f"oops! '{value}' is not in your contact!!")
        pass
    pass
pass


# It is used to Select function by user
while True:
    P()
    IP1 = input(ip)
    if IP1=='\t':continue
    if IP1=='\t\t':break
    IP1=IP1.strip()
    if IP1=='1':
        contact.view()
        pass
    elif IP1=='2':
        IP2 = input('Enter the Name: ')
        if IP2=='\t':continue
        if IP2=='\t\t':break
        IP3 = input('Enter the Phone Number: ')
        if IP3=='\t':continue
        if IP3=='\t\t':break
        contact.addNewContact((IP2.strip(),IP3.strip()))
        pass
    elif IP1=='3':
        IP2=input('Enter the Name or Number to search: ')
        if IP2=='\t':continue
        if IP2=='\t\t':break
        contact.searchView(IP2.strip())
        pass
    elif IP1=='4':
        IP2=input('Enter the Name to Delete: ')
        if IP2=='\t':continue
        if IP2=='\t\t':break
        contact.deleteContact(IP2.strip())
        pass
    elif IP1=='5':
        IP2=input('Enter the Name or Number to Edit: ')
        if IP2=='\t':continue
        if IP2=='\t\t':break
        contact.editContact(IP2.strip())
        pass
    else:
        IP2=contact.searchView(IP1,True)
        if IP2==False:continue
        pass
    conn.commit()
    pass
pass
conn.close()


                                                     # -----------------working flow --------------- #
'''                                 
                                                                User select
                                                                    |
                                                                    |
        ____________________________________________________________|____________________________________________________________________________
        |                          |                        |                           |                              |                        |
        |                          |                        |                           |                              |                        |
        |                          |                        |                           |                              |                        |
        |                          |                        |                           |                              |                        |
        V                          V                        V                           V                              V                        V
    view contact                Add contact             search contact              delete contact                  Edit contact            if not match
        |                           |                       |                             |                             |                     it search it 
        !-->is Empty                !-->check contact       |-->search the input          |-->check contact             |-->check contact     saved contacts
        !-->print in table          !-->save contact        |-->return to color text      |-->delete contact            |-->update contact    if contact is 
                                    in database           |      match with input                                                           it will print
                                                            |-->else return not found                                                         else continue
'''

# command of input
"""
*******************************************
*       >view contact      ===> 1          *
*       >Add contact       ===> 2          *
*       >Search Contact    ===> 3          *
*       >delete Contact    ===> 4          *
*       >Edit contact      ===> 5          *
*       >tab to back                       *
*       >double tab to exit                *
*******************************************
"""
    # debugging command and tested every function separately
# contact.addNewContact(('ragu','1234'))
# a = input('==>').strip()
# contact.searchView('1234')
# contact.deleteContact('123')
# contact.editContact(a)
# contact.view()


# view contact and add contact working fine
# del,edit,search need to verify
# search need to print result only
# stop at 11:35 pm in the day of 12.08.2022
# completed 10:07pm in the day of 16.08.2022
            #---------------completed jobs-------------------#
                #view-contact
                #add contact
                #delete contact
                #search
                #Edit contact