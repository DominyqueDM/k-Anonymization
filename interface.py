from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from run import get_results
from tools.read_adult_data import read_data as read_adult
from tools.read_adult_data import read_tree as read_adult_tree

DEFAULT_K = 2
DATA = read_adult()
A_TREES = read_adult_tree()

window = tk.Tk()
window.title("Anonymization Algorithms") 
window.geometry("600x500")
welcomelabel = tk.Label(text="Welcome to Anonymisation solutions", width= 30, height= 3, font= ('Helvetica', 18, 'bold'))
welcomelabel.pack()

#Intro text
intolabel = tk.Label(text= "We are all aware that everyday data is being collected from multiple entities: governments, corporations, accepting cookies! This is done to harvets more information about customers to get to know them better; to make better decisions for consumers. However, some data that is collected may contain highly sensitive information.", wraplength= 500)
intolabel.pack()
desclabel = tk.Label(text="Therefore, in order to protect the privacy of individuals, different methods and tools have been created to ensure that data remains useful whilst preserving individual privacy", wraplength= 500)
desclabel.pack()
optlabel = tk.Label(text= "Here we are showing two different solutions. Please click one to find out more about it:", height= 3, justify="left")
optlabel.pack()

#Function to open K cluster
def choiceBranch():
    if (choice.get() == OPTIONS[0]):
        newWindow = Toplevel(window)
        newWindow.title("Efficient k-Anon with Clustering")
        newWindow.geometry("600x500")
        Label(newWindow, text="K-Anonymization with Clustering Techniques", font=('Helvetica', 18, 'bold')).pack()
        Label(newWindow, text="The key idea of this alogorithm is that the k-anonymization problem can be viewed as a clustering problem. Meaning that we transform the k-anonymity requirement into a clustering problem where we want to find a set of clusters each containing at least k-records.", wraplength = 500).pack()
        Label(newWindow, text="And it is important to remember that through this anonymization process, we want to ensure the data is still useful. This algorithm aids in this as we want the records in a cluster to be as similar to each other as possible which makes certain that less ditortion is required when the records in a cluster are modified to have the same quasi-identifier value.", wraplength= 500).pack()
        Label(newWindow, text="  ").pack()
        Label(newWindow, text="IMPORTANT: This alogithm has been enforced with a hierarchy based generalisation. This means that if you are using your own data files, you will need to also add your relationship files.", wraplength=500).pack()
        Label(newWindow, text= "  ").pack()
        Label(newWindow, text= "Running the algorithm:", font='Helvetica 14 bold').pack()
        Label(newWindow, text="> You can run it by using the pre-loaded data").pack()
        Label(newWindow, text="  ").pack()
        Button(newWindow, text="Run with pre-loaded data", padx=2, command=preLoaded).pack()
        Label(newWindow, text="  ").pack()
        Label(newWindow, text="> Using your own files").pack()
        Button3= Button(newWindow, text='Upload file', command= uploadMainFile).pack()
    else:
        newWindow = Toplevel(window)
        newWindow.title("Mondrain multidimensional k-anonymity")
        newWindow.geometry("600x500")   
        #Simon's part to go here     
def preLoaded():
    newWindow = Toplevel(window)
    newWindow.title("Efficient k-Anon with Clustering: PreLoaded Running")
    newWindow.geometry("600x500")
    Label(newWindow, text="Running of the K-Anonymisation using Clustering", font=('Helvetica', 18, 'bold')).pack()
    Label(newWindow, text="You have chosen to run the program using the preloaded data.").pack()
    Label(newWindow, text="In this dataset, the main file has the following columns: age, workclass, education, marital status, occupation, race, sex, hours working per week, country of origin and income", wraplength=500).pack()
    Label(newWindow, text="PLEASE NOTE: The generalisation hierarchies can be found where the main dataset is (adult.data)").pack()
    Label(newWindow, text="7 attributes have been chosen as quasi-identifiers: age, workclass, marital status, occupation, sex, hours per week and income", wraplength=500).pack()
    Label(newWindow, text="There is currently 1000 rows of data in adult.data").pack()

def uploadMainFile(event=None):
    filename = filedialog.askopenfilename()
    print('Selected:', filename)


#Create drop down menu. More options can be easily added in the future
OPTIONS = [
"Efficient K-Anonymization Using Clustering Techniques",
"Mondrain multidimensional k-anonymity",
] #etc

choice = StringVar(window)
choice.set(OPTIONS[0]) # default value

listChoices = OptionMenu(window, choice, *OPTIONS)
listChoices.pack()

Button(window, text="Submit choice", wraplength= 150, pady=10, fg= 'black', command= choiceBranch).pack()


window.mainloop()