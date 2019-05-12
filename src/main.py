import sys
sys.setrecursionlimit(5000)
import numpy as np

from math import sin,cos,sqrt,exp,fabs,tan,log,fmod
import parser
from sympy import *
import matplotlib.pyplot as plt
from matplotlib import cm
import NelderMead as opt
import importlib
importlib.import_module('mpl_toolkits.mplot3d').Axes3D

from tkinter import *
from tkinter import scrolledtext


def undefiniedVariables(function):
    F= parser.expr(function).compile()
    variables= F.co_names
    var=[]  #remove math variables
    for i in variables:
        if(i != 'sin' and i != 'cos' and i != 'sqrt' and i != 'exp' and i != 'tan' 
                       and i != 'fabs' and i != 'log'):
            var.append(i) 
    return var       
def func(function, start):

    var = undefiniedVariables(function)
    mapa=dict(zip(var,start))
#     print(var)
#     print(map)
    return (sympify(function).evalf(subs=mapa))
    
    
def plot3D(equation,history):

    expr11 = simplify(equation).as_expr()

    var = undefiniedVariables(equation)

    f = lambdify((var[0], var[1]), expr11, 'numpy')
    a = np.linspace(-5,5, 1000)
    b = np.linspace(-5,5, 1000)
    x, y = np.meshgrid(a, b)
    
    fig=plt.figure()
    ax = fig.gca(projection='3d')
    ax.plot_surface(x, y, f(x,y), cmap=cm.coolwarm , 
                       linewidth=0, antialiased=False)
    ax.set_xlabel(var[0]+' axis')
    ax.set_ylabel(var[1]+' axis')
    ax.set_zlabel('F('+var[0]+','+var[1]+') axis')
    plt.title('Wykres funkcji')

    tabl1=[]
    tabl2=[]
    tabl3=[]

    for i in range(len(history)):
            x1 = (history[i][0][0])
            y1 = (history[i][0][1])
            z1 = (history[i][1])
            tabl1.append([x1,y1,z1])
            if (fmod(i, 2)==0):
                tabl2.append([x1,y1,z1])
            if (fmod(i, 3)==0):
                tabl3.append([x1,y1,z1])     

    tabl1=np.array(tabl1)
    tabl2=np.array(tabl2)
    tabl3=np.array(tabl3)
    ax.plot(tabl1[:,0],tabl1[:,1],tabl1[:,2], color='r')
    ax.plot(tabl2[:,0],tabl2[:,1],tabl2[:,2], color='r')
    ax.plot(tabl3[:,0],tabl3[:,1],tabl3[:,2], color='r')
          
    
    ### contour ###
    plt.figure()
    CS = plt.contour(x, y, f(x, y),11,
                 linewidths=np.arange(.5, 4, .5),
                 colors=('r', 'green', 'blue', (1, 1, 0), '#afeeee', '1')
                 )
    plt.clabel(CS, fontsize=12, inline=1)
    plt.xlabel(var[0]+' axis')
    plt.ylabel(var[1]+' axis')
    plt.title('Wykres warstwic')
    plt.show()
    
    ### GUI ####

class Window(Frame):

    # Define settings upon initialization. Here you can specify
    def __init__(self, master=None):
        
        # parameters that you want to send through the Frame class. 
        Frame.__init__(self, master)   

        #reference to the master widget, which is the tk window                 
        self.master = master

        #with that, we want to then run init_window, which doesn't yet exist
        self.init_window()

    #Creation of init_window
    def init_window(self):

        # changing the title of our master widget      
        self.master.title("Simplex v0.1")

        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)

        # creating a menu instance
        menu = Menu(self.master)
        self.master.config(menu=menu)

        # create the file object)
        file = Menu(menu)

        # adds a command to the menu option, calling it exit, and the
        # command it runs on event is client_exit
#         file.add_command(label="Exit", command=self.client_exit)

        #added "file" to our menu
        menu.add_cascade(label="File", menu=file)

        # adds a command to the menu option, calling it exit, and the
        # command it runs on event is client_exit
#         file.add_command(label="Exit", command=self.client_exit())

        #     #funkcja
        txt1 = Label(self, text="Wpisz funkcje: ")
        txt1.grid(column=0, row=2)
        self.getfcn = Entry(self,width=40)
        self.getfcn.grid(column=1, row=2)
        self.getfcn.insert(0,function)
        
        txt2 = Label(self, text="Wpisz wartosci punktu startowego: ")
        txt2.grid(column=0, row=4)
        self.getx0= Entry(self,width=40)
        self.getx0.grid(column=1, row=4)
        self.getx0.insert(0,x0)

        txt3 = Label(self, text="Wpisz dopuszczalna wartosc bledu: ")
        txt3.grid(column=0, row=6)
        self.geterr= Entry(self,width=40)
        self.geterr.grid(column=1, row=6)
        self.geterr.insert(0,epsilon)

        Label(self, text="Odpowiedz konsoli: ").grid(column=0, row=10)
        consoleWindow = scrolledtext.ScrolledText(self,width=50,height=10)
        consoleWindow.grid(column=0,row=11)

        Label(self, text="Punkty simplexu: ").grid(column=1, row=10)
        simplex = scrolledtext.ScrolledText(self,width=60,height=10)
        simplex.grid(column=1,row=11)
        
        startBtn = Button(self, text="START", command=lambda:self.startButton(consoleWindow,simplex))
        startBtn.grid(column=1, row=8)
        
        #added "file" to our menu
#         menu.add_cascade(label="Edit", menu=edit)
        
    def startButton(self,conWind,simplex):
        #clear colsole
        conWind.delete('1.0', END)
        simplex.delete('1.0', END)
        
        #init variables
        function = self.getfcn.get()
        tmp = re.findall(r'-?\d+\.?\d*', self.getx0.get())
        x0=[]
        print("test ",tmp)
        for i in tmp:
            x0.append(float(i))
        x0= np.array(x0)
        epsilon = self.geterr.get()        
        
        #start main
        if(len(undefiniedVariables(function)) != len(x0)):
            print("ERROR: Number of function variables is not same as length of initial point ")
            print("Unknown variables: ",len(undefiniedVariables(function)), ": ",undefiniedVariables(function))
            print("Initial point: ",len(x0),": ",x0)
            conWind.insert(INSERT, "BLAD: Liczba zmiennych funkcji rozna od dlugosci punktu x0\n")
            conWind.insert(INSERT, "Nieznane zmienne: "+str(len(undefiniedVariables(function)))+": "\
                           + str(undefiniedVariables(function))+"\n")
            conWind.insert(INSERT, "Punkt poczatkowy: "+str(len(x0))+": "+str(x0)+"\n")                      
        else:
            if(len(undefiniedVariables(function))<1):
                print("Equation is less than 1 dimensional")
                conWind.insert(INSERT, "BLAD: Liczba wymiarow mniejsza od 1\n")
            else:
                print ("x0  =  ",x0)
                conWind.insert(INSERT, "x0 = "+str(x0)+"\n")
                conWind.insert(INSERT, "f = "+function+"\n")    
                NM = opt.NelderMead(function,maxIterationNumber)
                
                NM.runSimplex(x0, epsilon , len(x0))
                conWind.insert(INSERT, "minimum = "+str(NM.returnDATA()[0][0])+"\n")
                conWind.insert(INSERT, "f(min) = "+str(NM.returnDATA()[0][1])+"\n")
                conWind.insert(INSERT, "Iteration = "+str(NM.returnIter())+"\n")
                conWind.insert(INSERT, "E = "+str(NM.returnErr())+"\n")
                if(NM.returnErr()>1):
                    conWind.insert(INSERT, "Funkcja prawdopodobnie zmierza do nieskonczonosci lokalne minimum jest nieznane\n")
                    print("Function probably ran to infinity, local minimum not known")
                hist = NM.returnHistory()
                for i in hist:
                    simplex.insert(INSERT, str(i)+"\n")
                if(dim==2):
                    plot3D(function,NM.returnHistory())
                
        
  
        
    def client_exit(self):
        exit()
    
if __name__ == "__main__":

    ### input ###
    maxIterationNumber=100;
    epsilon = 0.001
    
    alfa= 1
    beta=0.5
    gamma=2
    x0=[1 , 1]  
    x0= np.array(x0) #punkt startowy
    function = "x**2 + y**2"
    
    dim=len(undefiniedVariables(function))    
##### Process example method #####
#     function = "x1**4 +  x1**2 +x2**4 + x2**2" 
#     function = "sin(x1)*sin(x2)*exp(-x1**2-x2**2)"
#     function = "x1**2 +4*x1 -1"
#     function = "x1**3 - cos(x2) +x3 -exp(qx2+x4)"
#     function = "x1**3 - log(fabs(cos(x2))) +x3*x2 -exp(x2+x4)"
#     function = "x1**3 - log(fabs(cos(x2))) +x3*x2 -exp(x2+x4)- log(fabs(y))+exp(z)"
#     function ( )



#     if(len(undefiniedVariables(function)) != len(x0)):
#         print("ERROR: Number of function variables is not same as length of initial point ")
#         print("Unknown variables: ",len(undefiniedVariables(function)), ": ",undefiniedVariables(function))
#         print("Initial point: ",len(x0),": ",x0)
#     else:
#         if(len(undefiniedVariables(function))<1):
#             print("Equation is less than 1 dimensional")
#         else:
#             print ("x0  =  ",x0)
#     #         print(undefiniedVariables(function))
#     #         print(dict(zip(undefiniedVariables(function),x0)))
#             NM = opt.NelderMead(function,maxIterationNumber);
#            
#             NM.runSimplex(x0, epsilon , dim)
#     #         print(NM.returnHistory())
#             if(dim==2):
#                 plot3D(function,NM.returnHistory())
#             if(NM.returnErr()>1):
#                 print("Function probably ran to infinity, local minimum not known")
###############################################
    
    root = Tk()
    root.geometry('875x400')
    app = Window(root)
    root.mainloop()
        