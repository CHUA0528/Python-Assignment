from prettytable import PrettyTable
import sys
import random
import datetime
import time
import copy

#Classes definition and objects instantiation
#Classes with attributes and methods
class menu:
    def __init__(self,x):
        self.file = x #file name
        self.menu = PrettyTable(['ID','Items','Cost'])#create table for menu
        self.product = [] #listings of food and price
        self.order ={}

    def read(self):
        filename = self.file + ".txt"   #read file name
        f = open(filename,"r")
        for i in (f.read().split("\n")): #splitting the file into lines and putting it into a list
            self.product.append(i.split(','))

    def outputMenu(self): #printing the menu
        menu.read(self)
        for i in self.product:
            test = len(i)
            if test !=3:
                print("Something is wrong with txt file ~ ")
                print("1. Correct format is 1, nasi lemak, 2.5")
                print("2. Make sure there is no enter after last line")
                sys.exit()
        else:
            self.menu.add_rows(self.product) #add the list to the table

    def print(self):
        print ("~"*40)
        print("                 "+self.file.upper())
        print(self.menu ,"\n")

    def transferMenu(self):
        menu.read(self)
        #creating a dictionary to get products
        for i in self.product:
            self.order[i[0]] = i[1:]
            self.order[i[0]][1] = float(self.order[i[0]][1])

class functionMenu(menu):
    def __init__(self,tax):
        menu.__init__(self,"Menu")
        self.item = "" #store incoming added item's name
        self.quantity = 0 #store incoming added item's quantity
        self.num = 1 #record how many items are ordered
        self.priceQ = 0 #store incoming added item's price
        self.totalPrice = 0 #to store the total price
        self.bill = [] #to store the ordered items
        self.totalPayment = 0 #to store the total price
        self.taxAmount = 0 #to store the tax amount
        self.tax =tax #tax percentage
        self.invoice = PrettyTable(['No.','item','quantity','price','total']) #create a table for invoice
        self.receipt =[] #to store the receipt
        self.copyBill = [] #to store a copy of bill
        menu.transferMenu(self)

    def addItem(self):
        while(True):
            self.item = input("\nWhat would you be ordering?") #get input
            try:
                #see if if the input is in the dictionary of orderOptions
                self.order.get(self.item)[0]
            except:
                #if not in dictionary, check if it is the string "exit"
                if self.item == "exit":
                    break
                else:
                    print("Oops the option you entered isn't valid, please check and enter again ~") #reloop program for a new input
            else:
                try:
                    self.quantity = input("enter quantity desired(enter anything that is not an number to undo option): ")
                    self.quantity = int(self.quantity) #check if input is an integer
                except:
                    print ("error! not an integer, undoing option...")
                    continue
                else:
                    self.priceQ = round((self.order.get(self.item)[1] * self.quantity),2) #calculate the price of the amount of items ordered
                    newOrder = [self.order.get(self.item)[0],self.quantity,self.order.get(self.item)[1],self.priceQ] #store the order in a list
                    current = self.quantity
                    #check if bill is empty
                    if len(self.bill) == 0:
                        self.bill.append(newOrder) #append the order to bill
                    else:
                    #check for duplicates in bill
                        for i in self.bill:
                            if i[0] == newOrder[0]:  #modify the duplicate info in bill
                                i[1] += self.quantity
                                i[3] = round(i[3] + self.priceQ,2)
                                current = i[1]
                                break
                        else:
                            #wait until loops end only append to make sure no duplicates
                            self.bill.append(newOrder)
                    self.totalPrice += self.priceQ
                    print("You ordered{0} with the total quantity of {1}".format(self.order.get(self.item)[0],current))

    def removeItem(self):
        while(True):
            if (len(self.bill) > 0): #check if bill is empty or not
                functionMenu.showOrder(self,1) #show your order before removing
                removedItem = input("What would you be removing? (Choose a number Ex : 1)") #get input
                try:
                    removedItem = int(removedItem) #check if input is an integer
                except:
                    if removedItem =="exit": #check if input is the string "exit" , if yes return to main menu
                        break
                    else:
                        print("not a valid option,enter again") #reloop program for a new input
                        continue
                else:
                    for i in range(self.num): #loop through the bill to find the item to remove
                        if removedItem == i+1:
                            self.totalPrice -= self.bill[i][3] #subtract the price of the item removed from total price
                            test = self.bill[i][0] #store the name of the item removed
                            del self.bill[i]
                            print("You removed {0} from your order".format(test))
                            break
                    else:
                        print("The item you entered is not valid ~\n") #reloop program for a new input as input invalid
                        continue
            else:
                print("There is nothing to remove in your order anymore! Returning to main menu\n")
                time.sleep(1)
                break

    def editQuantity(self):
        while(True):
            if (len(self.bill) > 0):
                functionMenu.showOrder(self,1) #show your order before editing
                updatedItem = input("What would you be editing? (Choose a number Ex : 1 4)") #get input
                updatedQ = input("What would you like to change the quantity to? (Enter something larger than 0)")
                try:
                    updatedItem = int(updatedItem) #check if input is an integer
                    updatedQ = int(updatedQ)
                except:
                    if updatedItem =="exit": #check if input is the string "exit" , if yes return to main menu
                        break
                    else:
                        print("Oops the input you entered isn't valid, please check and enter again ~ ")
                        print("the option should be a number in the bill and the quanitity should be a valid number")
                        continue
                else:
                    for i in range(self.num):
                        if updatedItem == i+1: #loop through the bill to find the item to edit
                            if updatedQ < 1:   #check if the quantity is valid
                                print("You cannot update the quantity to 0 or negative, if you want to remove the item, go to remove item option\n")
                                break
                            else:
                                self.bill[i][1] = updatedQ #update the quantity of the item
                                self.totalPrice -= self.bill[i][3] #subtract the price of the item from total price
                                self.bill[i][3] = round(self.bill[i][2] * updatedQ,2) #update the price of the item
                                self.totalPrice += self.bill[i][3] #add the price of the item to total price
                                print("You updated quantity of {0} to {1} from your order\n".format(self.bill[i][0],self.bill[i][1]))
                                break
                    else:
                      print("The number you entered is not in the bill ~\n")
            else:
                print("Your order should atleast have something to be able to update\n")
                time.sleep(1)
                break

    def calculationPrice(self):
        self.taxAmount = (self.totalPrice * self.tax) / 100
        self.totalPayment = self.totalPrice + self.taxAmount

    def showOrder(self,x=0):
        called = x
        if(len(self.bill) ==0):
            print("You have not ordered anything yet!")
        else:
            self.num =1
            print("\nYour order: ")
            for i in self.bill:
                print ("{0}. {1} x{2} - RM {3} = RM{4}".format(self.num,i[0],i[1],i[2],i[3]))
                self.num+=1
        if called == 1:
            return
        else:
            input("Press any key to continue")


    def printReceipt(self):
        if(len(self.bill) ==0):
            print("You have not ordered anything yet!, returning to main menu") #chck if bill is empty
        else:
            while(True):
                j =1
                functionMenu.showOrder(self,1) #show your order before printing
                choice2 = input("Is this your final order? (y/n) : ") #get input
                if choice2 == "y": #check if input is the string "y" , if yes print receipt
                    self.copyBill = copy.deepcopy(self.bill) #copy the bill to a new list to not modify orginal list
                    for i in self.copyBill:
                        i.insert(0,j)
                        j +=1
                    self.invoice.clear_rows() #clear the invoice table to make sure no info from before
                    functionMenu.calculationPrice(self) #final price calculation
                    self.invoice.add_rows(self.copyBill) #add the bill to the invoice table
                    self.receipt = [
                    "             XU HUAN MAMAK",
                    '-'*37,'INVOICE','-'*37,
                    "Date/Time : {0} ".format(datetime.datetime.now().replace(microsecond =0)),
                    str(self.invoice),
                    "Tax ({0}%): {1}".format(self.tax,round(self.taxAmount,2)),
                    "Your subtotal    : RM{:.2f}".format(self.totalPrice),
                    "Your grand total : RM{:.2f}".format(self.totalPayment)
                    ,'-'*50,fun()] #receipt info
                    for x in range (3):  #fun loading animation
                        b = "Printing receipt" + "." * x + "*insert beep sound*"
                        print ( b , end = "\r")
                        time.sleep(0.5)
                    receiptF = open("receipt.txt",'w') #open file to write receipt
                    for l in self.receipt: #write receipt info into file
                        receiptF.write(l+"\n")
                    receiptF.close()
                    print("Receipt printed!")
                    input("Press any key to continue")
                    break
                elif choice2 == "n":
                    print("OK, returning to main menu")
                    break
                else:
                    print("not a valid option,enter again")
                    continue






#Farewell messages
def fun():
    response = ("Come again~", "Thank you for coming", "Congratz you are the 100th customer, you won nothing"
                , "Hope it does not rain on your way home", "Bye bye~", "Hope you enjoyed your meal :D, I tried to pick out the hair",
                "leave 5 stars on google thanks","下次再来")
    number=[]
    for i in range(len(response)): #create a list of numbers to be used as keys
        number.append(i+1)
    t = dict(zip(number,response)) #create a dictionary with the numbers as keys and the messages as values
    nice = random.randint(1,len(response)) #randomly pick a number to be used as key
    return (t[nice]) #return the value of the key





