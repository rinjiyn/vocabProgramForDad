# // Importing Default Python libraries, these libraries are default meaning they come with the Python installation.
# // Some libraries that other programmers use are external, meaning you have to install the library externally into
# // your IDE, (Visual Code Studio).
import tkinter as tk
import random
import threading
import time
import os

#open ('set1.txt', 'r')


# // If you find yourself re-using code constantly, turn them into functions and call them instead.
# // I called these functions multiple times in my code.
def grammarize(string):
    newstring =  str(string)
    return newstring.strip().lower().capitalize()

def deleteChildren(frame):
    for widget in frame.winfo_children():
        widget.destroy()



# // Creating a class called MyGUI. KIND OF using an Object-Oriented Programming approach. (OOP)
class MyGUI:
    # // When calling the class "MyGUI", this "function" is instantly called when you "initialize" (__init__) MyGUI()
    def __init__(self):
    # // The self variable is used to represent the instance of the class which is often used in OOP.
        self.storeddict = {}
        self.currentpair = None
 
        self.root = tk.Tk()

        self.root.geometry("1000x800")

        self.root.tk_setPalette(background = "Dark Gray")

        self.label = tk.Label(self.root, text="Type out your Vocabulary Words and its definition!", font=('Arial', 20))
        self.label.pack(padx=10, pady=10)

        self.mainFrame = tk.Frame(self.root)
        self.mainFrame.pack(padx=10, pady=10)

        self.construct_mainmenu()

        self.root.mainloop()

    

    def construct_mainmenu(self):
        self.label.configure(text="Type out your Vocabulary Words and its definition!")

        textboxFrame = tk.Frame(self.mainFrame)
        textboxFrame.columnconfigure(0, weight= 1, pad=50)
        textboxFrame.columnconfigure(1, weight= 1, pad=50)
        textboxFrame.pack(padx=10, pady=50)

        labelt1 = tk.Label(textboxFrame, text="Your word here:", font=('Arial', 14))
        labelt1.grid(row=0, column=0)

        labelt2 = tk.Label(textboxFrame, text="It's definition here:", font=('Arial', 14))
        labelt2.grid(row=0, column=1)

        self.textbox = tk.Text(textboxFrame, height = 5, width = 25, wrap='word', font=('Arial', 16))
        self.textbox.grid(row=1, column=1)

        self.entrybox = tk.Entry(textboxFrame, width=15, font=('Arial', 16))
        self.entrybox.grid(row=1, column = 0)


        buttonFrame = tk.Frame(self.mainFrame)
        buttonFrame.columnconfigure(0, weight = 1, pad=35)
        buttonFrame.columnconfigure(1, weight = 1, pad=35)
        buttonFrame.columnconfigure(2, weight = 1, pad=35)
        buttonFrame.pack(padx=10,pady=45)

        nextButton = tk.Button(buttonFrame, text="Input next word.", font=('Arial', 18), command=self.nextclicked)
        nextButton.grid(row=0, column =2)

        testButton = tk.Button(buttonFrame, text="Let's Play!", font=('Arial', 18), command=self.start_game)
        testButton.grid(row=0,column=1)

        txtDocFrame = tk.Frame(self.mainFrame)
        txtDocFrame.columnconfigure(0, weight=1, pad=10)
        txtDocFrame.columnconfigure(1, weight=1, pad=10)
        txtDocFrame.pack(padx=10,pady=50)

        useTxtDocLabel = tk.Label(txtDocFrame, text="Have a vocab set you want to use? \nType out the txt file name below:")
        useTxtDocLabel.grid(row=0,column=0)

        useTxtDocButton = tk.Button(txtDocFrame, text="Enter", font=('Arial', 18), command=self.importDoc)
        useTxtDocButton.grid(row=1,column=1)

        self.useTxtDocEntry = tk.Entry(txtDocFrame, width=12, font=('Arial', 16))
        self.useTxtDocEntry.grid(row=1,column=0)


    def importDoc(self):
        txtdocstr = self.useTxtDocEntry.get()
        currentdir = os.path.dirname(__file__)
        filedir = currentdir + "/Sets/" + txtdocstr + ".txt" 

        if len(txtdocstr.strip()) >= 1:
            try:
                f = open(filedir, 'r')
            except FileNotFoundError:
                print("File could not be found")
                thread = threading.Thread(target=self.changeLabelText, args=("File not found...","Red",30))
                thread.start()

            with open(filedir, 'r') as f:
                content = f.readlines()
                for v in content:
                    if v.startswith("#"):
                        continue
                    string = v.strip("\n")
                    seperated = string.split("=")
                    
                    self.storeddict[grammarize(seperated[0])] = {
                        "definition" : grammarize(seperated[1]),
                        "picked" : False
                    }

            f.close()
            thread = threading.Thread(target=self.changeLabelText, args=("Successfully Imported!","Green",30))
            thread.start()
            print(f.closed)
            print(self.storeddict)

    def nextclicked(self):
        textboxstr = self.textbox.get("1.0", tk.END)
        entryboxstr = self.entrybox.get()

        

        if len(entryboxstr.strip()) >= 1 and len(textboxstr.strip()) >= 1:

            self.storeddict[ grammarize(entryboxstr) ] = {
                "definition" : grammarize(textboxstr),
                "picked" : False
            }

            self.entrybox.delete('0', tk.END)
            self.textbox.delete('1.0', tk.END)
            
            for k,v in self.storeddict.items():
                print("Key: " + k, "  Value: "+  str(v))
            print("------------------")


    def start_game(self):
        if len(self.storeddict) < 1:
            print("no")
        else:
            print("yay")
            deleteChildren(self.mainFrame)
            
            self.construct_game()

    

    def construct_game(self):

        self.label.configure(text="What's the word that matches with this definition?")

        self.labeldict = tk.Label(self.mainFrame, text="", font=('Arial', 20))
        self.labeldict.pack(padx=10, pady=100)
        
        self.entrybox = tk.Entry(self.mainFrame, width=15, font=('Arial', 14))
        self.entrybox.pack(padx=10,pady=10)

        enterButton = tk.Button(self.mainFrame, text="Enter", font=('Arial', 14), command=self.enter_answer)
        enterButton.pack(padx=1,pady=0)

        optionFrame = tk.Frame(self.mainFrame)
        optionFrame.columnconfigure(0, weight=1, pad=35)
        optionFrame.columnconfigure(1,weight=1, pad=35)
        optionFrame.columnconfigure(2,weight=1,pad=35)
        optionFrame.pack(padx=10,pady=75)

        skipButton = tk.Button(optionFrame, text = "Skip!", font=('Arial', 14), command=self.skip_question)
        skipButton.grid(row=0, column=2)

        endButton = tk.Button(optionFrame, text = "End Game", font=('Arial', 14), command=self.new_game)
        endButton.grid(row=0, column=1)

        hintButton = tk.Button(optionFrame, text = "Hint?", font=('Arial', 14), command=self.hint)
        hintButton.grid(row=0, column=0)

        self.pickPair()

    def pickPair(self):
        listedDict = list(self.storeddict.items())

        print(listedDict)

        for k,v in self.storeddict.items():
            if v["picked"] == True:
                print("tehee")
                listedDict.remove((k,v))

        if len(listedDict) < 1:
            self.end_game(True)
            return
            

        pickedPair = k,v = random.choice(listedDict)

        print("Picked is:")
        self.currentpair = pickedPair
        print(self.currentpair)

        selectedKey = self.storeddict[pickedPair[0]]
        selectedKey["picked"] = True
        
        print("stored is:")
        for k,v in self.storeddict.items():
                print("Key: " + k, "  Value: "+  str(v))
        print("------------------")

        
        self.labeldict.configure(text=str(selectedKey["definition"]))

    def changeLabelText(self,text,color,size):
        tempLabel = tk.Label(self.root, text=text, font=('Arial', size), background=color)
        tempLabel.place(x=600,y=350)
        time.sleep(1.15)
        tempLabel.destroy()

    
    def enter_answer(self):
        entryboxstr = self.entrybox.get()

        if grammarize(entryboxstr) == self.currentpair[0]:
            print("nice")

            thread = threading.Thread(target=self.changeLabelText, args=("Nice!","Green",30))
            thread.start()

            self.entrybox.delete('0', tk.END)
            self.pickPair()
        else:
            print("wrong")
            thread = threading.Thread(target=self.changeLabelText, args=("Nope. Try again.","Red",30))
            thread.start()
            self.entrybox.delete('0', tk.END)

    def end_game(self, bool):
        if bool == True:
            deleteChildren(self.mainFrame)

            self.label.configure(text="You completed all of them! Want to do it again?")
            
            tempFrame = tk.Frame(self.mainFrame)
            tempFrame.columnconfigure(0, weight=1, pad=35)
            tempFrame.columnconfigure(1,weight=1, pad=35)
            tempFrame.pack(padx=10,pady=75)

            yesButton = tk.Button(tempFrame, text = "Yes!", font=('Arial', 14), command=self.restart_game)
            yesButton.grid(row=0, column=0)

            noButton = tk.Button(tempFrame, text = "Nah", font=('Arial', 14), command=self.new_game)
            noButton.grid(row=0, column=1)

    def hint(self):
        word = str(self.currentpair[0])

        thread = threading.Thread(target=self.changeLabelText, args=("The first letter of the word is '" + word[0] + "' !","Yellow",14))
        thread.start()

    def skip_question(self):
        selectedKey = self.storeddict[self.currentpair[0]]
        selectedKey["picked"] = False

        self.entrybox.delete('0', tk.END)
        self.pickPair()

    def new_game(self):
        deleteChildren(self.mainFrame)
        self.currentpair = None
        self.storeddict = {}
        self.construct_mainmenu()
    
    def restart_game(self):
        deleteChildren(self.mainFrame)
        self.currentpair = None

        for k,v in self.storeddict.items():
            if v["picked"] == True:
                v["picked"] = False
        
        self.construct_game()

MyGUI()