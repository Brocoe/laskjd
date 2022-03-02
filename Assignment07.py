# ---------------------------------------------------------------------------- #
# Title: Assignment 07
# Description: Working with pickling and binary files and well as error handling
#              Creates an employee database that stores data in binary file
#              allows the user to add, edit and delete data
#              Error handling should be able to handle and variety of possible errors
# Brooke Biscoe,February 27, 2022,Started code to complete assignment 07
# Brooke Biscoe, February 28, 2022, Made more adjustments, added a number of customer error handling
# ---------------------------------------------------------------------------- #
import pickle

#Data--------------------------------------------------------------------------#

keys = ['Id','Name','Department','Salary']
employeeList = [{keys[0]:'Employee ID',keys[1]:'Employee Name',keys[2]:'Company Department',keys[3]:'Employee Salary'}]
fileName = 'Employee_Data.dat'
options = ['View Data','Add Data','Delete Data','Edit Data','Save Data','Exit']
departmentNames = ['Accounting','Research','Sales','Finance']

# Processing-------------------------------------------------------------------#

class InvalidOptionError(Exception):
    def __str__(self):
        global options
        return 'This is an invalid option. The available options are {}.'.format(options)
class NotUniqueEmployeeIDError(Exception):
    def __str__(self):
        return 'This employee ID is already in use. You must create a unique ID'
class MustNotBeNumericError(Exception):
    def __str__(self):
        return 'This variable MUST NOT contain numbers. Please enter it again.'
class MustBeNumericError(Exception):
    def __str__(self):
        return 'This variable MUST contain POSITIVE numbers. Please enter it again.'
class NoSearchResultError(Exception):
    def __str__(self):
        return 'There was no with data with this value in this column.\n' \
               'Try changing your search parameters'
class AvailableDepartmentsError(Exception):
    def __str__(self):
        global departmentNames
        return 'That is not a valid department. The available departments are {}.'.format(departmentNames)
class ValidNameError(Exception):
    def __str__(self):
        return 'Employee name must be entered as <First Name> <Last Name>, ' \
               'with only a single space between them.'
class AvailableColumnsError(Exception):
    def __str__(self):
        global keys
        return 'That is not a valid search field. The available fields are {}.'.format(keys)
def menu_options():
    user_option = input ('\nWhat would you like to do: ').strip()
    return user_option.title()
class user_input:
    def ID_Input():
        while True:
            try:
                emp_ID = input('Please input the employee ID: ')
                if not emp_ID.isnumeric():
                    raise MustBeNumericError
                break
            except MustBeNumericError as e:
                print(e)
        return emp_ID.strip()
    def Name_Input():
        while True:
            try:
                emp_Name = input('Please input name: ').title()
                if emp_Name.isnumeric():
                    raise MustNotBeNumericError
                elif emp_Name.count(' ') != 1:
                    raise ValidNameError
                break
            except MustNotBeNumericError as e:
                print(e)
            except ValidNameError as e:
                print(e)
        return emp_Name.strip()
    def Department_Input():
        global departmentNames
        while True:
            try:
                emp_Department = input('Please input department: ').title()
                if emp_Department.isnumeric():
                    raise MustNotBeNumericError
                elif not emp_Department in departmentNames:
                    raise AvailableDepartmentsError
                break
            except MustNotBeNumericError as e:
                print(e)
            except AvailableDepartmentsError as e:
                print(e)
        return emp_Department.strip()
    def Salary_input():
        while True:
            try:
                emp_Salary = input('Please input Salary: ')
                if not emp_Salary.isnumeric():
                    raise MustBeNumericError
                break
            except ValueError:
                print('You must enter the salary as a number')
            except MustBeNumericError as e:
                print(e)
        return emp_Salary.strip()
def get_data(fileName):
    objFile = open(fileName,'rb')
    emp_list = pickle.load(objFile)
    objFile.close()
    return emp_list
def write_data(emp_list,fileName):
    objFile = open(fileName,'wb')
    pickle.dump(emp_list,objFile)
    objFile.close()
def nonUniqueEmpID(empID,emp_list):
    global keys
    uniquecnt = 0
    for row in emp_list:
        if empID in row[keys[0]]:
            uniquecnt += 1
    return uniquecnt
def maxlen(dict):
    global keys
    '''
    This function looks at the longest string in each column and returns the longest
    length for each. This will help with formatting later on
    :param dict: The List of dictionaries
    :return: returns the max length of each column
    '''
    len_max_ID = 0
    len_max_Name = 0
    len_max_Dep = 0
    for row in dict:
        if len(row[keys[0]]) > len_max_ID:
            len_max_ID = len(row[keys[0]])
        if len(row[keys[1]]) > len_max_Name:
            len_max_Name = len(row[keys[1]])
        if len(row[keys[2]]) > len_max_Dep:
            len_max_Dep = len(row[keys[2]])
    return len_max_ID, len_max_Name, len_max_Dep
def printTable(lst,maxID,maxName,maxDep):
    global keys
    for row in lst:
        print(row[keys[0]],' '*(maxID-len(row[keys[0]])),'|',
              row[keys[1]],' '*(maxName-len(row[keys[1]])),'|',
              row[keys[2]],' '*(maxDep-len(row[keys[2]])),'|',
              row[keys[3]])
def DeleteData(lst,key,search):
    new_lst = []
    try:
        cntr = 0
        for row in lst:
            if not row[key] == search:
                new_lst.append(row)
            else:
                cntr += 1
        if cntr == 0:
            raise NoSearchResultError
        print('Data Deleted')
    except NoSearchResultError as e:
        print(e)
    return new_lst
def EditData(lst,emp_ID):
    global keys
    objlst = []
    cntr = 0
    try:
        for row in lst:
            if row[keys[0]] == emp_ID:
                cntr += 1
                objlst = row
                objlst_location = lst.index(row)
        if cntr == 0:
            raise NoSearchResultError
        cntr = 0
        for value in objlst.values():
            print(keys[cntr],':',value)
            cntr += 1
        while True:
            try:
                column = input('Which column would you like to change: ').title()
                if column == keys[0]:
                    print("You cannot change an employee's ID")
                elif column == keys[1]:
                    data = user_input.Name_Input()
                    break
                elif column == keys[2]:
                    data = user_input.Department_Input()
                    break
                elif column == keys[3]:
                    data = user_input.Salary_input()
                    break
                elif not column in keys:
                    raise AvailableColumnsError
            except AvailableColumnsError as e:
                print(e)
        lst[objlst_location][column] = data
        print('Changes have been made successfully.')
    except NoSearchResultError as e:
        print(e)


#Presentation---------------------------------------------------------------------#

try:
    employeeList = get_data(fileName)
except FileNotFoundError as e:
    print()
    print('There is currently no employee database. Creating file now.')
    write_data(employeeList,fileName)
    employeeList = get_data(fileName)
    print('File Created')
except Exception as e:
    print('There was a non-specific error')
    print('Below is the python documentation')
    print(e,e.__doc__,type(e),sep='\n')
print('\nPlease select what you would like to do from the following options:\n')
for opt in options:
    print(opt)
while True:
    while True:
        try:
            selection = menu_options()
            if not selection in options:
                raise InvalidOptionError
            break
        except InvalidOptionError as e:
            print(e)
    if selection.title() == options[0]:
        ID_Max, Name_Max, Dep_Max = maxlen(employeeList)
        printTable(employeeList,ID_Max,Name_Max,Dep_Max)
    elif selection.title() == options[1]:
        try:
            emp_ID = user_input.ID_Input()
            if nonUniqueEmpID(emp_ID,employeeList) > 0:
                raise NotUniqueEmployeeIDError
            emp_Name = user_input.Name_Input()
            emp_Dep = user_input.Department_Input()
            emp_Sal = user_input.Salary_input()
            dictrow = {keys[0]:emp_ID,keys[1]:emp_Name,keys[2]:emp_Dep,keys[3]:emp_Sal}
            employeeList.append(dictrow)
        except NotUniqueEmployeeIDError as e:
            print(e)
        except Exception as e:
            print('There was a non-specific error')
            print('Below is the python documentation')
            print(e,e.__doc__,type(e),sep='\n')
    elif selection.title() == options[2]:
        while True:
            column = input('Which column would you like to search: ').title()
            try:
                if not column in keys:
                    raise AvailableColumnsError
                break
            except AvailableColumnsError as e:
                print(e)
        print('NOTE: Any data that matches the search criteria will be deleted.')
        str = 'Which data from {} would you like to delete: '.format(employeeList[0][column])
        searchparam = input(str).title()
        employeeList = DeleteData(employeeList,column,searchparam)
    elif selection.title() == options[3]:
        emp_ID = user_input.ID_Input()
        EditData(employeeList,emp_ID)
    elif selection.title() == options[4]:
        print('Data saved to file!')
        write_data(employeeList,fileName)
    elif selection.title() == options[5]:
        print('You have exited the program!')
        break