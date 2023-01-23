from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from run import write_to_file, get_graph
from clustering import clustering_based_k_anon
from tools.read_adult_data import read_data as read_adult
from tools.read_adult_data import read_tree as read_adult_tree
import sys
import copy
import pdb
import random
import cProfile
import matplotlib.pyplot as plt

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
    Label(newWindow, text="  ").pack()
    Button(newWindow, text='Run Program', command= runCluster, bg='red', fg='white').pack()
    Label(newWindow, text="Please note that the program takes a few minutes to run").pack()
    Label(newWindow, text="   ").pack()
    Label(newWindow, text="If you would like a more detailed explanation as to how this works, please click the button below").pack()
    Button(newWindow, text='Explain Please', command= explanations).pack()

def runCluster():
    newWindow = Toplevel(window)
    newWindow.title("Efficient k-Anon with Clustering: PreLoaded Running")
    newWindow.geometry("700x700")
    Label(newWindow, text="Running the clustering based K-Anonymisation algorithm...",font=('Helvetica', 18, 'bold')).pack()
    Label(newWindow, text="K starts at 2 and increments until 10. A countdown will appear of the k's as the program progresses.")
    data = read_adult()
    a_trees= read_adult_tree()
    data_back = copy.deepcopy(data)
    k=2
    x= []
    y= []
    while (k<11):
        Label(newWindow, text="k is: %d" %k).pack()
        result, eval_result = clustering_based_k_anon(a_trees, data, k)
        write_to_file(result, k)
        data = copy.deepcopy(data_back)
        Label(newWindow, text="NCP (degree of information loss): %0.2f" % eval_result[0] + "%").pack()
        x.append(k)
        y.append(eval_result[0])
        Label(newWindow, text="Running time: %0.2f" % eval_result[1] + " seconds").pack()
        print()
        k= k+1
    get_graph(x, y)

def explanations():
    newWindow = Toplevel(window)
    myscrollbar=Scrollbar(newWindow,orient="vertical")
    myscrollbar.pack(side="right",fill="y")
    newWindow.title("Detailed Explanations of the Efficient K-Anonymization Program")
    newWindow.geometry("800x500")
    Label(newWindow, text="Steps in the K-Anonymization Process",font=('Helvetica', 18, 'bold')).pack()
    Label(newWindow, text="    ").pack()
    Label(newWindow, text="Step 1: Datasets and generalisation", font=(14)).pack()
    Label(newWindow, text="For each of the quasi-identifiers, a hierachy generalisation was done such examples are: adult_workclass and adult_race").pack()
    Label(newWindow, text="The data is read and stored in trees and based on what the generalisation hierarchies dictate, then certain data values will be overwritten with an asterisk (*)").pack()
    Label(newWindow, text="It is very important that the generalisation hierarchies do not have unnecessary generalisations otherwise information loss is increased").pack()
    Label(newWindow, text="    ").pack()
    Label(newWindow, text="Step 2: Making the Clusters", font=(14)).pack()
    Label(newWindow, text="Firstly, a random record, lets call it Ri, is picked from the data set and we make this a cluster, let's call it C1.").pack()
    Label(newWindow, text="Then we chose a record, Rj that makes information loss minimal: IL(C1 U { Rj}).").pack()
    Label(newWindow, text="We repeat this process until |C1| = k").pack()
    Label(newWindow, text="When |C1| reaches k, we chose a record that is furthest from Ri and repeat the clustering process until there are less than k records left.").pack()
    Label(newWindow, text="With the leftover clusters, we iterate over them and insert each record into a cluster with respect to which the increment of information loss is minimal").pack()
    Label(newWindow, text="It is important to note that the number of clusters is not a requirement HOWEVER, each cluster must have at least k records").pack()
    Label(newWindow, text="   ").pack()
    Label(newWindow, text="Step 3: Metrics", font=(14)).pack()
    Label(newWindow, text="There are two metrics being tested: running time and degree of information loss").pack()
    Label(newWindow, text="We can see that the program does take a minute or two to complete running and that is because it is running for k=2, k=3 and so on until k=10").pack()
    Label(newWindow, text="This is so as to give you an idea of how changing the value of k, can affect the utility of information").pack()
    Label(newWindow, text="   ").pack()
    Button(newWindow, text='Open Activity Section', command= openActivity).pack()

def openActivity():
    newWindow = Toplevel(window)
    newWindow.title("Activity")
    newWindow.geometry("800x500")
    Label(newWindow, text="Activity", font=(14)).pack()
    Label(newWindow, text="Here you will be able to open one of the anonymised text files and analyse it. There is a text file for each value of k").pack()
    Label(newWindow, text="You can press 'back' to go ro the previous screen and open another activity screen so that you can place them side by side for comparisons.").pack()
    txtarea = Text(newWindow, width=80, height=20)
    txtarea.pack(pady=20)
    path = Entry(newWindow)
    path.pack(side=LEFT, expand=True, fill=X, padx=20)
    Button(newWindow, text="Open File", command= openFile(path, txtarea)).pack(side=RIGHT, expand=True, fill=X, padx=20)
    Button(newWindow, text='Back', command= explanations).pack()

def openFile(path, txtarea):
    tf= filedialog.askopenfilename(title="Open Data File", filetypes=(("Data Files", "*.data"),))
    path.insert(END, tf)
    tf = open(tf, 'r')
    data= tf.read()
    txtarea.insert(END, data)
    tf.close()


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