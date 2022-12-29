
--------------------------------------------
#What this line does is it asks the viewer for two input responses. It asks them to
#record how many hours and what the rate per hour is
hrs = input("Enter Hours:")
rph = input("Enter rate per hour:")

#because hrs and rph are string values, by applying the float command, we command
# make them not string values and instead number values. Or whatever the fuck
# we can turn the hrs and rph variables into numbers at the same time that
# we accomplish the equation. Two Birds, one cum.

float_pay=float(rph)*float(hrs)

#Something important to note is the space inside of the 'Pay: '.
# Furthermore, we can't add a string and a number together, idk why.
# But we can circumvent this by doing str(float_pay), which turns
#it into a string. LOL

print('Pay: '+str(float_pay))
-------------------------------------------------
largest = None
smallest = None
while True:
    try:
        num = input("Enter a number:")
        if num == "done":
            break
        n = int(num)
        if largest == None or largest < n:
            largest = n
        elif smallest == None or smallest > n:
            smallest = n
    except:
        print("Invalid Input")

print("Maximum value is", largest)
print("Minimum value is", smallest)
-------------------------------------------------
#Python will go line by line.
if x < 2 :
    print('Small')
# This is the first layer, where it tries to find whether its small or not.
# If the above isn't true, by using ELIF, you can add one more layer
# To figure out something
elif x < 10 :
    print('Medium')
#Then if none of the above are true, there is only one remaining option.
else :
    print('LARGE')
print('All done')
# it's kinda like a logic flow map
------------------------------------------------------
hrs = input("Enter Hours:")
rph = input("Rate per hour:")
#I request an input from the user, I assign their input to the hrs and rph values.
# the float() converts the numbers stored in the string to a numerical point number with a decimal.
# this is good for precision
h = float(hrs)
rate = float(rph)
# After they provide the values I then convert those values into numeric values
# (or something idk tbh), which is important because we're gonna be doing number shit yk
if h <= 40:
    pay = h*rate

elif h > 40:
	pay = ((h-40)*rate*1.5) + rate*40

print(str(pay))
--------------------------------------------------------
def computepay(h, r): #hours and rate as two variables
    if h <= 40: #if hours are less than or equal to 40
        return h*r # normal pay is applied
    elif h > 40: #if hours exceed 40
        return ((h-40) * r * 1.5) + r*40 # (h-40) gets excess hours, is multiplied then by the normal and increased pay
        # then the rest of the 40 hours count as normal

hrs = input("Enter Hours:")
rph = input("Rate per hour:")
h = float(hrs)
r = float(rph)

p = computepay(45, 10.5)
print("Pay", p)
-----------------------------------------------------------
from pathlib import Path # imports path command
fname = input("Enter file name: ")# stores an input on a variable
fh = (Path('/Users/baltasar/Documents/Python') / fname) #goes to directory then opens whatever user put in
fhcontent = fh.read_text() #reads and stores the text on another variable,
print(fhcontent.upper()) #prints the read text and capitalises it

-----------------------------------------------------------
fname = input("Enter file name: ")
try:
    fh = open(fname) #this functions as a loop so that if u mispell the filename you can just try again
except:
    print('file cannot be found:', fname)

count = 0 #creating variable to store number of lines in
x = 0 # creating variable to store the list of values in it
for line in fh:
    if not line.startswith("X-DSPAM-Confidence:"): #skips irrelevant lines.
        continue
    x = float(line.split(':')[1].rstrip()) + x #Isolates the number, then aggregates it to x
    count = count + 1 #At the same time, it increases the count by 1

output = x/count #calculates average
print('Average spam confidence:', output)
-----------------------------------------------------------
from time import sleep
friends = ['joseph', 'obama', 'monica']
for friend in friends:
    print("Happy New Year", friend.capitalize())
    sleep(1)
print("done!")

print(friends[2])
-----------------------------------------------------------
fname = input('Enter filename:')
try:
    fh = open(fname)
except:
    print('file not found', fname)
lst = list()

for line in fh:
    words = fh.read().split() # Seperate all of the words in the file individually, and transform it into a list
    for word in words: # It will go through each item in the list
        if word not in lst: #If the word is not in the list,
            lst.append(word) #Adds the item (word) to the list
    lst.sort() # sorts list
print(lst) # prints list
-----------------------------------------------------------
fname = input("Enter file name: ")

if len(fname) < 1:
    fname = "mbox-short.txt" # just so u can press enter immediately
count = 0 # assigns place to store variable

try:
    fh = open(fname) # loop
except:
    print("Unable to find file:", fname)

for line in fh:
    if not line.startswith('From:'): #Ignores lines that do not start 'From:'
        continue
    print(line.split(':')[1].strip())# tells the program to isolate the word to the right of the : in From:
    count = 1 + count # counts the amount of times texts with the above conditions were found
print("There were", count, "lines in the file with From as the first word")
-----------------------------------------------------------
name = input("Enter file:")
if len(name) < 1: # This way you can just press enter and do it automatically
    name = "mbox-short.txt"


emails = dict() # establishing dictionary
adr = list() # establishing list

fh = open(name) 
for line in fh:
    if not line.startswith('From '): # Skips lines that do not start with 'From '
        continue 
    if line.startswith('From '): # If the line starts with 'From '
        adr.append(line.split(' ')[1].rstrip()) # it will get the word to the right of it
for mail in adr: # For every mail in the list, it will add it to the dictionary and will give it a value of +1
    emails[mail] = emails.get(mail, 0) + 1 # So if it sees an email address it adds it and gives it a value of +1. 
                                                            # If it sees the same address again it will just add another +1 to its value
maxi = max(emails, key=emails.get) # gets email with highest value
print(mail, emails[maxi]) # I don't know why printing 'mail' just automatically works.
-----------------------------------------------------------
name = input("Enter file:") #Usual bullshit
if len(name) < 1:
    name = "mbox-short.txt"
fh = open(name)

hours = list() # Establishing a list
slice1 = slice(2) #This is to isolate the hour value
times = dict() # dictionary
lst = list() # establishing anotha list

for line in fh:
    if not line.startswith('From '): # ignores lines that dont start witth 'From '
        continue #
    if line.startswith('From '):                            # If the line starts with 'From ' it isolates the timestamp on the 5th index of the line
        hours.append(line.split()[5].strip()[slice1]) # then 
        
for time in hours:
    times[time] = times.get(time, 0) + 1
    
for val, key in times.items(): # Because dictionaries hold two variables, a key and a value - one needs to specify that the loop is accounting for two variables
    newtup = (val, key) # Establishes a Tuple. It only has one key-value pair at a time and 
    lst.append(newtup)# the value is then added to a list. Effectively creating a list of tuples.

lst = sorted(lst, reverse = False) # Modifies the existing list, sorting it. reverse = False orders it from lowest to highest.

for val, key in lst: # By creating a loop to go through the list printing each item individually
    print(val, key)    # it creates a nice, readable list of the values.
-----------------------------------------------------------