# Capstone of Boston Bijold: 
# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
import plotly.express as px
from fuzzywuzzy import process
from csv import writer


"""
Import of recorded transactions
"""
attributes = ['Description', 'Account', 'Amount', 'DID', 'AID']

data_file = pd.read_csv('expenses.csv', header=0, names = attributes) #df: datafile
#Convert to Numpyarray 
df = pd.DataFrame(data_file).to_numpy()

"""
import of common descriptions
"""
UDAttributes = ["ID", "Description", "TimesUsed"]
#lables the CSV first row. 
UD = pd.read_csv('Descriptions.csv', names = UDAttributes)
#Reads the CSV to the program
#print(UD.head())
lable = UD.Description
#Extracts the Description column only for lable checking in Fuzzy. 

"""
Import Chart of Accounts list with AIDs
"""
AccountLables = ["AID", "Account"]
Account_List = pd.read_csv('Account_List.csv',header = 0, names = AccountLables)
#print(Account_List)
#print(type(Account_List))
Account_List = pd.DataFrame(Account_List).to_numpy()
#print(type(Account_List))


def append_list_as_row(file_name, element_list):
    with open(file_name, 'a+', newline='') as write_obj:
        csv_writer = writer(write_obj)
        csv_writer.writerow(element_list)


def DataFilter(Transactions, FuzzyID):
    #print(FuzzyID)
    filtered = np.where(Transactions[:,3] == FuzzyID)
    x = filtered[0]
    #print(Transactions[x])
    test = Transactions[x]
    results = pd.DataFrame(test)
    x = np.array(results.iloc[:, 2: 4])
    y = np.array(results.iloc[:, 4])
    y = y.astype('int')
    #print(y)
    #print(x)

    return(x,y)

def KNN_Algorithm(x, y, FuzzyDID, UserPrice):
    knn = KNeighborsClassifier(n_neighbors=3, n_jobs=-1) 
    one_knn = KNeighborsClassifier(n_neighbors=1, n_jobs=-1) 
    knn.fit(x,y)
    one_knn.fit(x,y)
    test = [[UserPrice, FuzzyDID]]

    try:
        recommendation = knn.predict(test)
    except:
        #print('Too little data for K=3')
        recommendation = one_knn.predict(test)
    #print(recommendation)
    
    return recommendation

"""
Fuzzy String Matching
""" 

def get_matches(query, choices, limit=200):
    results = process.extract(query, choices, limit=limit)
    return results

def fuzzy_percent(fuzzy):
    results = fuzzy[0]
    print(fuzzy)
    #print(results)
    if results == None:
        #TODO
        return results 
    if results[1] <95:
        #print(results[1])
        results = None
        return results
    else:
        #print(results)
        return results[2]
    
def fuzzy_account_percent(fuzzy):
    results = fuzzy[0]
    #print(results)
    if results == None:
        #TODO
        return results 
    if results[1] <65:
        #print(results[1])
        results = None
        return results
    else:
        results = results[0]
        resultsAID = results[0]
        resultsacc = results[1]
        return resultsAID, resultsacc


"""
Enter Transaction
"""
def enter_transaction():

    UserDescription = input("Enter transaction description: ")
    UserPrice = input("Enter transaction price: ")
    UserPrice = float(UserPrice)

    fuzzy = get_matches(UserDescription, lable)
    fuzzyDID = fuzzy_percent(fuzzy)

    """
    user inputs for KNN- UserPrice and fuzzyDID 
    """

    if fuzzyDID != None:
        filtered_DID = DataFilter(df, fuzzyDID)
        recommendation = KNN_Algorithm(filtered_DID[0], filtered_DID[1], 
                                    fuzzyDID, UserPrice)

        
        #print('AID = ', recommendation)
        result = np.where(Account_List == recommendation)
        #print('AID Location ', result[0])
        #print(Account_List[result[0]])
        x = result[0]
        Account = Account_List[x[0]]
        Account = Account[1]
        print('Recommended account: ', Account)
        
        confirmation= input("Is this account correct? (yes/no): ")
        if confirmation == 'yes':
            newtransaction = [UserDescription, Account, UserPrice, fuzzyDID,
                              recommendation[0]]
            newDescription = [fuzzyDID, UserDescription, 1]
            #if fuzzy% <100 > 90 add description with same DID 
            #print(newtransaction)
            append_list_as_row('expenses.csv', newtransaction)
            print("Thank you, your transaction has been stored.")
        else:
            newaccount = input('Enter the account name you would like to use:')
            afuzzy= get_matches(newaccount, Account_List)
            fuzzyacc = fuzzy_account_percent(afuzzy)
            print('Did you mean', fuzzyacc[1], '?')
            answer = input('(yes/no): ')
            if answer == 'yes':
                newtransaction = [UserDescription, fuzzyacc[1], UserPrice, fuzzyDID,
                                  fuzzyacc[0]]
                #print(newtransaction)
                append_list_as_row('expenses.csv', newtransaction)
                print('Thank you, your transaction has been added.')
                print('')
            
    else: 
        #TODO
        print("no recommendation available")




menu_options = {
    1: 'Enter Transaction:',
    2: 'View All Transactions:',
    3: 'View Specific Transactions',
    4: 'View Amount Spent Per Account',
    5: 'Exit',
}

def print_menu():
    for key in menu_options.keys():
        print (key, '--', menu_options[key] )

def option1():
     print('--Enter Transaction-- ')
     enter_transaction()

def option2():
     print('--All Transactions-- ')
    
     alltrans = pd.read_csv('expenses.csv', header=0, names = attributes)
     fig = px.scatter(alltrans, x = 'DID', y = 'Amount', color='Account')
     fig.show()
     return

def option3():
     print('--View Amount Spent Per Description--')
     view_trans = input('Enter a transaction description to view: ')
     fuzzy = get_matches(view_trans, lable)
     print('The matching description is: ', fuzzy[0][0])
     fuzzyDID = fuzzy_percent(fuzzy)
     #print(fuzzyDID)
     if fuzzyDID != None:
         alltrans = pd.read_csv('expenses.csv', header=0, names = attributes)
         rslt_df = alltrans[alltrans['DID']== fuzzyDID]
         total = rslt_df['Amount'].sum()
         print('With a total amount spent of: $', total)
         #total = data_file['Amount'].sum()
         #print('Total amount spent: ', total)
         fig = px.pie(rslt_df, values='Amount', names='Account')
         fig.show()
     else:
         print('No data available.')
          
     
def option4():
     print('--View Amount Spent Per Account--')
     alltrans = pd.read_csv('expenses.csv', header=0, names = attributes)
     total = alltrans['Amount'].sum()
     print('Total amount spent: $', total)
     fig = px.pie(data_file, values='Amount', names='Account')
     fig.show()

if __name__=='__main__':
    print('')
    print('')
    print('*** Welcome to the Account Suggestion System ***')
    while(True):
        print_menu()
        option = ''
        try:
            option = int(input('Enter your choice: '))
        except:
            print('Wrong input. Please enter a number ...')
        #Check what choice was entered and act accordingly
        if option == 1:
           option1()
        elif option == 2:
            option2()
        elif option == 3:
            option3()
        elif option == 4:
            option4()
        elif option == 5:
            print('Thank you')
            exit()
        else:
            print('Invalid option. Please enter a number between 1 and 5.')

print('Done')