from prettytable import PrettyTable
import menu
import sys

#instance of class
foodMenu = menu.menu("Menu")

#printing of menu
print("WELCOME TO CHOON FEI MAMAK")
foodMenu.outputMenu() #initialization of menu
foodMenu.print()    #printing menu

#tax percetange
tax = 5

#instance of functions in class
orderFunctions = menu.functionMenu(5)

#dictionary of functions
mainMenu = {"1": ("Add food into order",orderFunctions.addItem),
            "2":("Remove food from order",orderFunctions.removeItem),
            "3":("Edit quantity of food in order", orderFunctions.editQuantity),
            "4":("Show my order",orderFunctions.showOrder),
            "5":("Print invoice",orderFunctions.printReceipt)}

while(True):
    print("""
    INSTRUCTIONS:
    Enter the number desired to pick an option (Ex : 1)
    Enter "exit" to exit anything , even the program or the option you are in :D
    """)
    for i in mainMenu:
        print("{0}. {1}".format(i,mainMenu.get(i)[0])) #print the main menu with the functions
    try:
        function = input("What would you like to do:  ")
        mainMenu.get(function)[1]() #get the function from the dictionary and call it
    except:
        if function =="exit":
            print(menu.fun()) #exit function
            sys.exit()
        else:
            print("Oops the option you entered isn't valid ~\n") #reloop program for a new input as input is invalid
    else:
        foodMenu.print() #print menu after every function
