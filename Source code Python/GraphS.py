import tkinter as tk                # python 3
from tkinter import font  as tkfont # python 3
from tkinter import scrolledtext
import matplotlib.pyplot as plt
import numpy as np
import math

import mysql.connector
from django.db import connection
import MySQLdb
import pandas as pd



class graphS(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.geometry("600x700")
        self.resizable(0,0)
        self.title("GraphS A simple graph simulation software")

        self.shared_data = {
            "ip": tk.StringVar(),
            "dbname": tk.StringVar(),
            "tablename" :tk.StringVar(),
            "username": tk.StringVar(),
            "password": tk.StringVar(),
            "table_information": [],
            "database_information" : [],
            "FilePath" : tk.StringVar(),
            "File_information" :[],


        }


        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, DirectInput, PointInput, StatisticalInputPoint, StatisticalInputRange,
                  DatabaseInput_FirstPage,DatabaseInput_SecondPage,Excel_CSV_file_FirstPage,Excel_CSV_file_SecondPage
                  ,error_show_database
                  ,error_show_can_not_draw_pie_diagram
                  ,error_show_can_not_draw_pie_diagram_database
                  ,error_show_filepath
                  ,error_show__pie_diagram_filepath):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


    def get_page(self, page_class):
        return self.frames[page_class]


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Please choose a method", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)


        v = tk.IntVar()
        b1 = tk.Button(self, text="Direct input" ,   padx=0, font=("", 12, "bold"),
                      command=lambda: controller.show_frame("DirectInput") )
        b2 = tk.Button(self, text="Database input",  padx=0,
                      command=lambda: controller.show_frame("DatabaseInput_FirstPage"),font=("", 12, "bold") )
        b3 = tk.Button(self, text="Excel or CSV file input",  padx=0,
                      command=lambda: controller.show_frame("Excel_CSV_file_FirstPage"),font=("", 12, "bold") )

        b1.pack(expand=1)
        b2.pack(expand=1)
        b3.pack(expand=1)



class DirectInput(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Please choose a method", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"),pady = 10)
        button.pack()

        b1 = tk.Button(self, text="Point input" ,   padx=0, font=("", 12, "bold"),
                      command=lambda: controller.show_frame("PointInput") )
        b2 = tk.Button(self, text="Statistical input [points]",  padx=0,
                      command=lambda: controller.show_frame("StatisticalInputPoint"),font=("", 12, "bold") )

        b3 = tk.Button(self, text="Statistical input [range]",  padx=0,
                      command=lambda: controller.show_frame("StatisticalInputRange"),font=("", 12, "bold") )

        b1.pack(expand=1)
        b2.pack(expand=1)
        b3.pack(expand=1)



class PointInput(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller



        button = tk.Button(self, text="Go back",
                           command=lambda: controller.show_frame("DirectInput"),pady = 10,width=20)
        button.pack()

        label = tk.Label(self, text="Please input x and y like this : ", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        label = tk.Label(self, text="x1 y1, x2 y2, ..., x(n) y(n)  ", font=(controller.title_font,15))
        label.pack(side="top", fill="x", pady=10)



        scrT = scrolledtext.ScrolledText(self,width = 30, height = 7, wrap = tk.WORD,
                                         font=(controller.title_font,15))
        scrT.pack()

        label = tk.Label(self, text="Graph size[Default value (5 5) ]",
                         font=(controller.title_font,10),anchor='w')
        label.pack(side="top",fill='both',padx=70, pady=10)


        graphSize = tk.StringVar()
        e = tk.Entry(self, textvariable=graphSize,width=58)
        e.pack(pady =10)


        label = tk.Label(self, text="X and Y labels ",
                         font=(controller.title_font,10),anchor='w')
        label.pack(side="top",fill='both',padx=70, pady=10)

        both_labels = tk.StringVar()
        e = tk.Entry(self, textvariable=both_labels,width=58)
        e.pack(pady =10)

        button = tk.Button(self, text="Draw the points only",anchor='w',
                           command=lambda: retrieve_input(1),padx=70,pady = 10)
        button.pack()

        button = tk.Button(self, text="Draw the points and save as",anchor='w',
                           command=lambda: retrieve_input(2),padx=70,pady = 10)
        button.pack()


        pdfFile = tk.StringVar()
        e = tk.Entry(self, textvariable=pdfFile,width=58)
        e.pack(pady =10)


        def retrieve_input(choice):

            inputValue = scrT.get("1.0", "end-1c")
            inputValue = inputValue.replace(',',' ')
            inputData = inputValue.split()

            labels_name = both_labels.get()
            pdfFileName = pdfFile.get()
            graphDimension = graphSize.get()

            gS = []
            if  graphDimension== "" :
                gS.append(5)
                gS.append(5)
            else :
                a = graphDimension.split()
                for i in range(0,len(a)):
                    gS.append(int(a[i]))

            label = []
            if  labels_name== "" :
                label.append("X-Data")
                label.append("Frequency")
            else :
                a = labels_name.split()
                for i in range(0,len(a)):
                    label.append(a[i])




            x_y = []
            x = []
            y = []

            # Adding 0 in inputData if user inputs extra x but not in y
            if len(inputData)% 2 != 0:
                inputData.append(0)

            for i in range(0,len(inputData),2):
                    x_y.append([int(inputData[i]),int(inputData[i+1])])

            x_y  =sorted(x_y)

            for i in range(0,len(x_y)):
                x.append(int(x_y[i][0]))
                y.append(int(x_y[i][1]))

            plt.rcParams["figure.figsize"] = (gS[0], gS[1])
            f = plt.figure()
            plt.plot(x, y, linewidth=3)
            plt.xlabel(label[0], fontsize=10)

            # Set y axes label.
            plt.ylabel(label[1], fontsize=10)

            # Set the x, y axis tick marks text size.
            plt.tick_params(axis='both', labelsize=9)
            plt.xticks(np.arange(min(x), max(x) + 1, 1.0))
            plt.yticks(np.arange(min(y), max(y) + 1, 1.0))
            ax = plt.subplot()
            ax.axhline(y=0, color='k')
            ax.axvline(x=0, color='k')

            if choice ==2 :
                if pdfFileName == "":
                    f.savefig("graph.pdf", bbox_inches='tight')
                else :
                    f.savefig(pdfFileName+".pdf", bbox_inches='tight')


            plt.show()





class StatisticalInputPoint(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        button = tk.Button(self, text="Go back",
                           command=lambda: controller.show_frame("DirectInput"), pady=10, width=20)
        button.pack()

        label = tk.Label(self, text="Please input x like this : ", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        label = tk.Label(self, text="x1 x2 x3 ...  x(n) ", font=(controller.title_font, 15))
        label.pack(side="top", fill="x", pady=10)

        scrT = scrolledtext.ScrolledText(self, width=30, height=7, wrap=tk.WORD,
                                         font=(controller.title_font, 15))
        scrT.pack()

        label = tk.Label(self, text="Graph size[Default value (5 5) ]",
                         font=(controller.title_font, 10), anchor='w')
        label.pack(side="top", fill='both', padx=70, pady=10)


        graphSize = tk.StringVar()
        e = tk.Entry(self, textvariable=graphSize, width=58)
        e.pack(pady=10)

        label = tk.Label(self, text="X and Y labels ",
                         font=(controller.title_font, 10), anchor='w')
        label.pack(side="top", fill='both', padx=70, pady=10)

        both_labels = tk.StringVar()
        e = tk.Entry(self, textvariable=both_labels, width=58)
        e.pack(pady=10)

        button = tk.Button(self, text="Draw the Bar diagram", anchor='w',
                           command=lambda: retrieve_input(1), padx=70, pady=10)
        button.pack()

        button = tk.Button(self, text="Draw Bar diagram and save as", anchor='w',
                           command=lambda: retrieve_input(2), padx=70, pady=10)
        button.pack()

        pdfFile = tk.StringVar()
        e = tk.Entry(self, textvariable=pdfFile, width=58)
        e.pack(pady=10)

        def retrieve_input(choice):

            inputValue = scrT.get("1.0", "end-1c")
            inputValue = inputValue.replace(',', ' ')
            inputData = inputValue.split()


            labels_name = both_labels.get()
            graphDimension = graphSize.get()

            gS = []
            if  graphDimension== "" :
                gS.append(5)
                gS.append(5)
            else :
                a = graphDimension.split()
                for i in range(0,len(a)):
                    gS.append(int(a[i]))

            label = []
            if  labels_name== "" :
                label.append("X-Data")
                label.append("Frequency")
            else :
                a = labels_name.split()
                for i in range(0,len(a)):
                    label.append(a[i])

            #Finish dimension of graph

            x = []

            for i in range(0, len(inputData)):
                x.append(int(inputData[i]))

            N = len(x)
            lowest_value = min(x)
            highest_value = max(x)

            graph_data = []

            r = highest_value - lowest_value

            k = math.floor(1 + 3.322 * math.log10(N))

            h = math.ceil(r / k)

            graph_dataX = []
            graph_dataY = []

            for i in range(0, k):
                tali = 0
                for j in range(0, len(x)):
                    if x[j] >= lowest_value and x[j] <= lowest_value + h - 1:
                        tali += 1

                sequ = str(lowest_value) + "-" + str((lowest_value + h - 1))
                graph_dataX.append(sequ)
                graph_dataY.append(tali)
                lowest_value += h


            plt.rcParams["figure.figsize"] = (gS[0], gS[1])
            f = plt.figure()
            x = np.arange(len(graph_dataX))
            plt.bar(x, graph_dataY, align='center', alpha=0.5)
            plt.xticks(x, graph_dataX)
            plt.yticks(np.arange(min(graph_dataY), max(graph_dataY) + 1, 1))
            plt.xlabel(label[0])
            plt.ylabel(label[1])




            #File saving
            if choice == 2:
                pdfFileName = pdfFile.get()

                if pdfFileName == "":
                    f.savefig("graph.pdf", bbox_inches='tight')
                else:
                    f.savefig(pdfFileName + ".pdf", bbox_inches='tight')

            plt.show()


class StatisticalInputRange(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        button = tk.Button(self, text="Go back",
                           command=lambda: controller.show_frame("DirectInput"), pady=10, width=20)
        button.pack()

        label = tk.Label(self, text="Please input range like this : ", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        label = tk.Label(self, text="string1 y1, string2 y2,...string(n) y(n) ", font=(controller.title_font, 15))
        label.pack(side="top", fill="x", pady=10)

        scrT = scrolledtext.ScrolledText(self, width=30, height=7, wrap=tk.WORD,
                                         font=(controller.title_font, 15))
        scrT.pack()

        label = tk.Label(self, text="Graph size[Default value (10 10) ]",
                         font=(controller.title_font, 10), anchor='w')
        label.pack(side="top", fill='both', padx=150, pady=10)


        graphSize = tk.StringVar()
        e = tk.Entry(self, textvariable=graphSize, width=58)
        e.pack(pady=10)

        label = tk.Label(self, text="X and Y labels ",font=(controller.title_font, 10), anchor='w')
        label.pack(side="top", fill='both', padx=70, pady=10)
        both_labels = tk.StringVar()
        e = tk.Entry(self, textvariable=both_labels, width=58)
        e.pack(pady=10)

        button = tk.Button(self, text="Draw Bar diagram", anchor='w',
                           command=lambda: retrieve_input(1), padx=50, pady=7)
        button.pack()

        button = tk.Button(self, text="Draw pie diagram", anchor='w',
                           command=lambda: retrieve_input(2), padx=50, pady=7)
        button.pack()

        button = tk.Button(self, text="Draw Bar and pie diagram", anchor='w',
                           command=lambda: retrieve_input(3), padx=50, pady=7)
        button.pack()

        button = tk.Button(self, text="Draw both and save as", anchor='w',
                           command=lambda: retrieve_input(4), padx=50, pady=7)
        button.pack()


        pdfFile = tk.StringVar()
        e = tk.Entry(self, textvariable=pdfFile, width=58)
        e.pack(pady=10)

        def retrieve_input(choice):



            inputValue = scrT.get("1.0", "end-1c")
            inputValue = inputValue.replace(',', ' ')
            inputData = inputValue.split()




            if len(inputData)% 2 != 0:
                inputData.append(0)

            #Calculation
            x_y = []
            graph_dataX = []
            graph_dataY = []

            for i in range(0,len(inputData),2):
                    x_y.append([inputData[i],int(inputData[i+1])])

            x_y  =sorted(x_y)

            for i in range(0,len(x_y)):
                graph_dataX.append(x_y[i][0])
                graph_dataY.append(int(x_y[i][1]))


            pie_diagram_available = 1
            #Cheking if negetive value is contained so no pie diagram available
            for i in range(0,len(graph_dataY)):
                if int(graph_dataY[i])<0:
                    pie_diagram_available = 0
                    break



            labels_name = both_labels.get()
            graphDimension = graphSize.get()

            gS = []
            if  graphDimension== "" :
                gS.append(5)
                gS.append(5)
            else :
                a = graphDimension.split()
                for i in range(0,len(a)):
                    gS.append(int(a[i]))

            label = []
            if  labels_name== "" :
                label.append("X-Data")
                label.append("Frequency")
            else :
                a = labels_name.split()
                for i in range(0,len(a)):
                    label.append(a[i])

            #Finish dimension of graph




            if choice == 1 :
                plt.rcParams["figure.figsize"] = (gS[0], gS[1])
                f = plt.figure()
                x = np.arange(len(graph_dataX))
                plt.bar(x, graph_dataY, align='center', alpha=0.5)
                plt.xticks(x, graph_dataX)
                plt.xlabel(label[0])
                plt.ylabel(label[1])
                ax = plt.subplot()
                ax.axhline(y=0, color='k')
                plt.show()


            if choice == 2 and pie_diagram_available == 1:
                plt.rcParams["figure.figsize"] = (gS[0], gS[1])
                f = plt.figure()
                plt.pie(graph_dataY, labels=graph_dataX,
                        autopct='%1.1f%%', shadow=True, startangle=140)
                plt.axis('equal')
                plt.show()



            if choice == 2 and pie_diagram_available == 0:
                controller.show_frame("error_show_can_not_draw_pie_diagram")


            if choice == 3 and pie_diagram_available == 1:
                plt.rcParams["figure.figsize"] = (gS[0], gS[1])
                f = plt.figure()
                plt.subplot(211)
                x = np.arange(len(graph_dataX))
                plt.bar(x, graph_dataY, align='center', alpha=0.5)
                plt.xticks(x, graph_dataX)
                plt.xlabel(label[0])
                plt.ylabel(label[1])
                ax = plt.subplot(211)
                ax.axhline(y=0, color='k')
                plt.title(("Bar Diagram"))
                plt.subplot(212)
                plt.pie(graph_dataY, labels=graph_dataX,
                        autopct='%1.1f%%', shadow=True, startangle=140)
                plt.axis('equal')
                plt.title(("Pie Diagram"))
                plt.show()



            if choice == 3 and pie_diagram_available == 0:
                controller.show_frame("error_show_can_not_draw_pie_diagram")



            #File saving
            if choice == 4 and pie_diagram_available == 1:
                plt.rcParams["figure.figsize"] = (gS[0], gS[1])
                f = plt.figure()
                plt.subplot(211)
                x = np.arange(len(graph_dataX))
                plt.bar(x, graph_dataY, align='center', alpha=0.5)
                plt.xticks(x, graph_dataX)
                plt.xlabel(label[0])
                plt.ylabel(label[1])
                ax = plt.subplot(211)
                ax.axhline(y=0, color='k')
                plt.title(("Bar Diagram"))

                plt.subplot(212)
                plt.pie(graph_dataY, labels=graph_dataX,
                        autopct='%1.1f%%', shadow=True, startangle=140)
                plt.axis('equal')
                plt.title(("Pie Diagram"))



                pdfFileName = pdfFile.get()
                if pdfFileName == "":
                    f.savefig("graph.pdf", bbox_inches='tight')
                else:
                    f.savefig(pdfFileName + ".pdf", bbox_inches='tight')

                plt.show()



            if choice == 4 and pie_diagram_available == 0:
                plt.rcParams["figure.figsize"] = (gS[0], gS[1])
                f = plt.figure()
                x = np.arange(len(graph_dataX))
                plt.bar(x, graph_dataY, align='center', alpha=0.5)
                plt.xticks(x, graph_dataX)
                plt.xlabel(label[0])
                plt.ylabel(label[1])
                ax = plt.subplot()
                ax.axhline(y=0, color='k')

                pdfFileName = pdfFile.get()

                if pdfFileName == "":
                    f.savefig("graph.pdf", bbox_inches='tight')
                else:
                    f.savefig(pdfFileName + ".pdf", bbox_inches='tight')

                plt.show()






class DatabaseInput_FirstPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.labels_and_buttons()


    def  labels_and_buttons(self):



        controller = self.controller
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"),pady = 10)
        button.pack()

        label = tk.Label(self, text="Please fill the textboxes ", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)



        label = tk.Label(self, text="Ip address of the database ", font=(controller.title_font,13))
        label.pack(side="top", fill="x", pady=10)

        e = tk.Entry(self, textvariable=self.controller.shared_data["ip"], width=58)
        e.pack(pady=7)



        label = tk.Label(self, text="Database name ", font=(controller.title_font,13))
        label.pack(side="top", fill="x", pady=10)

        e = tk.Entry(self, textvariable=self.controller.shared_data["dbname"], width=58)
        e.pack(pady=7)

        label = tk.Label(self, text="Table name ", font=(controller.title_font,13))
        label.pack(side="top", fill="x", pady=10)

        e = tk.Entry(self, textvariable=self.controller.shared_data["tablename"], width=58)
        e.pack(pady=7)

        label = tk.Label(self, text="Database user name ", font=(controller.title_font,13))
        label.pack(side="top", fill="x", pady=10)


        e = tk.Entry(self, textvariable=self.controller.shared_data["username"], width=58)
        e.pack(pady=7)

        label = tk.Label(self, text="Database password(Leave blank if not password) ", font=(controller.title_font,13))
        label.pack(side="top", fill="x", pady=10)


        e = tk.Entry(self, textvariable=self.controller.shared_data["password"], width=58)
        e.pack(pady=7)



        b1 = tk.Button(self, text="Enter database information" ,state="active",  padx=0,pady=0, font=("", 12, "bold"),width = 20,
                      command=lambda: database_info() )
        b1.pack(expand=1)
        b2 = tk.Button(self, text="Proceed" ,state="disabled",  padx=0,pady=0, font=("", 12, "bold"),width = 20,
                      command=lambda : show_second_page(self) )
        b2.pack(expand=1)


        def database_info():

            b1.configure(state = "disabled")
            b2.configure(state="active")

            ip = controller.shared_data['ip'].get()
            dbname = controller.shared_data['dbname'].get()
            tablename = controller.shared_data['tablename'].get()
            username = controller.shared_data['username'].get()
            password = controller.shared_data['password'].get()



            exception_raised = 0
            if ip == "" and dbname == "" and tablename == "" and username == "" and password == "":
                exception_raised =1


            try:
                connection = MySQLdb.connect(host=ip, user=username, password=password, db=dbname)
            except Exception as e:
                exception_raised = 1


            if exception_raised ==1 :
                b1.configure(state ="active")
                b2.configure(state="disabled")
                error_show_database()

            elif(exception_raised ==0) :
                cursor = connection.cursor()
                #cursor.execute("SHOW TABLES ")
                cursor.execute("DESCRIBE "+tablename)
                result = cursor.fetchall()
                for i in range(0,len(result)):
                    controller.shared_data['table_information'].append(result[i][0])


        def show_second_page(self):
            self.controller.show_frame("DatabaseInput_SecondPage")
            page1 = self.controller.get_page("DatabaseInput_SecondPage")
            page1.database_info()

        def error_show_database():
            controller.show_frame("error_show_database")









class DatabaseInput_SecondPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        button = tk.Button(self, text="Go back",width = 50,
                           command=lambda: controller.show_frame("StartPage"), pady=10)
        button.pack()

        label = tk.Label(self, text="Please select X-axis and Y-axis data",pady = 10,font=("", 10, "bold"))
        label.pack()


    def database_info(self):

        table_infoX = self.controller.shared_data['table_information']
        table_infoY = table_infoX.copy()

        for i in range(0,len(table_infoX)):
            table_infoY.append("count("+table_infoX[i]+")")

        for i in range(0,len(table_infoX)):
            table_infoY.append("avg("+table_infoX[i]+")")



        label = tk.Label(self, text="Select coloumn as X-axis data",pady = 10,font=("", 12, "bold"))
        label.pack()
        v1 = tk.StringVar()
        v1.set(table_infoX[0])
        w1 = tk.OptionMenu(self, v1, *table_infoX)
        w1.config(width= 40,font=("", 12, "bold"))
        w1.pack()


        label = tk.Label(self, text="Select coloumn as Y-axis data",pady = 10,font=("", 12, "bold"))
        label.pack()
        v2 = tk.StringVar()
        v2.set(table_infoY[0])
        w2 = tk.OptionMenu(self, v2, *table_infoY)
        w2.config(width= 40,font=("", 12, "bold"),pady= 7)
        w2.pack()

        #blank space text
        label = tk.Label(self, text="    ",pady = 10,font=("", 12, "bold"))
        label.pack()


        label = tk.Label(self, text="Graph size[Default value (5 5) ]",
                         font=(self.controller.title_font, 10), anchor='w')
        label.pack(side="top", fill='both', padx=70, pady=7)
        graphSize = tk.StringVar()
        e = tk.Entry(self, textvariable=graphSize, width=58)
        e.pack(pady=10)


        label = tk.Label(self, text="X and Y labels",font=(self.controller.title_font, 10), anchor='w')
        label.pack(side="top", fill='both', padx=70, pady=10)
        both_labels = tk.StringVar()
        e = tk.Entry(self, textvariable=both_labels, width=58)
        e.pack(pady=10)

        #Button show


        button = tk.Button(self, text="Draw Bar diagram", anchor='w',
                           command=lambda: retrieve_input(1), padx=50, pady=7)
        button.pack()

        button = tk.Button(self, text="Draw pie diagram", anchor='w',
                           command=lambda: retrieve_input(2), padx=50, pady=7)
        button.pack()

        button = tk.Button(self, text="Draw Bar and pie diagram", anchor='w',
                           command=lambda: retrieve_input(3), padx=50, pady=7)
        button.pack()


        button = tk.Button(self, text="Draw both diagram and save as", anchor='w',
                           command=lambda: retrieve_input(4), padx=70, pady=10)
        button.pack()
        pdfFile = tk.StringVar()
        e = tk.Entry(self, textvariable=pdfFile, width=58)
        e.pack(pady=10)


        def retrieve_input(choice):


            inputX_col = v1.get()
            inputY_col = v2.get()



            ip = self.controller.shared_data["ip"].get()
            dbname = self.controller.shared_data["dbname"].get()
            tablename = self.controller.shared_data["tablename"].get()
            username = self.controller.shared_data["username"].get()
            password = self.controller.shared_data["password"].get()
            table_information = table_infoX
            avg_col = []
            count_col = []

            for i in range(0,len(table_information)):
                avg_col.append(["avg("+table_information[i]+")",table_information[i]])

            for i in range(0,len(table_information)):
                count_col.append(["count(" + table_information[i] + ")", table_information[i]])

            #This part directs that whether count choosen or two coloumns choosen

            coloumn_choosen_type = 0
            index = 0
            for i in range(0, len(table_information)):
                if table_information[i] == inputY_col:
                    coloumn_choosen_type = 1
                    break

            for i in range(0, len(avg_col)):
                if avg_col[i][0] == inputY_col:
                    coloumn_choosen_type = 2
                    index = i
                    break

            for i in range(0, len(count_col)):
                if count_col[i][0] == inputY_col:
                    coloumn_choosen_type = 3
                    index = i
                    break

            try:
                connection = MySQLdb.connect(host=ip, user=username, password=password, db=dbname)
            except Exception as e:
                print("")


            if coloumn_choosen_type == 1:
                query = "select "+inputX_col+","+inputY_col+" from "+ tablename +" group by "+inputX_col
                cursor = connection.cursor()
                cursor.execute(query)
                result = cursor.fetchall()

            elif coloumn_choosen_type == 2: # fetches average data
                query = "select " + inputX_col + ",avg("+avg_col[index][1]+") from " + tablename + " group by " + inputX_col
                cursor = connection.cursor()
                cursor.execute(query)
                result = cursor.fetchall()

            elif coloumn_choosen_type == 3:# fetches Count data

                query = "select " + inputX_col + ",count("+avg_col[index][1]+") from " + tablename + " group by " + inputX_col
                cursor = connection.cursor()
                cursor.execute(query)
                result = cursor.fetchall()



            #Calculation

            graph_dataX = []
            graph_dataY = []
            for i in range(0,len(result)):
                graph_dataX.append(result[i][0])
                graph_dataY.append(result[i][1])



            pie_diagram_available = 1
            #Cheking if negetive value is contained so no pie diagram available
            for i in range(0,len(graph_dataY)):
                if int(graph_dataY[i])<0:
                    pie_diagram_available = 0
                    break



            labels_name = both_labels.get()
            graphDimension = graphSize.get()

            gS = []
            if  graphDimension== "" :
                gS.append(5)
                gS.append(5)
            else :
                a = graphDimension.split()
                for i in range(0,len(a)):
                    gS.append(int(a[i]))

            label = []
            if  labels_name== "" :
                label.append("X-Data")
                label.append("Frequency")
            else :
                a = labels_name.split()
                for i in range(0,len(a)):
                    label.append(a[i])

            #Finish dimension of graph



            if choice == 1 :
                plt.rcParams["figure.figsize"] = (gS[0], gS[1])
                f = plt.figure()
                x = np.arange(len(graph_dataX))
                plt.bar(x, graph_dataY, align='center', alpha=0.5)
                plt.xticks(x, graph_dataX)
                plt.xlabel(label[0])
                plt.ylabel(label[1])
                ax = plt.subplot()
                ax.axhline(y=0, color='k')
                plt.show()


            if choice == 2 and pie_diagram_available == 1:
                plt.rcParams["figure.figsize"] = (gS[0], gS[1])
                f = plt.figure()
                plt.pie(graph_dataY, labels=graph_dataX,
                        autopct='%1.1f%%', shadow=True, startangle=140)
                plt.axis('equal')
                plt.show()



            if choice == 2 and pie_diagram_available == 0:
                self.controller.show_frame("error_show_can_not_draw_pie_diagram_database")


            if choice == 3 and pie_diagram_available == 1:
                plt.rcParams["figure.figsize"] = (gS[0], gS[1])
                f = plt.figure()
                plt.subplot(211)
                x = np.arange(len(graph_dataX))
                plt.bar(x, graph_dataY, align='center', alpha=0.5)
                plt.xticks(x, graph_dataX)
                plt.xlabel(label[0])
                plt.ylabel(label[1])
                ax = plt.subplot(211)
                ax.axhline(y=0, color='k')
                plt.title(("Bar Diagram"))
                plt.subplot(212)
                plt.pie(graph_dataY, labels=graph_dataX,
                        autopct='%1.1f%%', shadow=True, startangle=140)
                plt.axis('equal')
                plt.title(("Pie Diagram"))
                plt.show()



            if choice == 3 and pie_diagram_available == 0:
                self.controller.show_frame("error_show_can_not_draw_pie_diagram_database")



            #File saving
            if choice == 4 and pie_diagram_available == 1:
                plt.rcParams["figure.figsize"] = (gS[0], gS[1])
                f = plt.figure()
                plt.subplot(211)
                x = np.arange(len(graph_dataX))
                plt.bar(x, graph_dataY, align='center', alpha=0.5)
                plt.xticks(x, graph_dataX)
                plt.xlabel(label[0])
                plt.ylabel(label[1])
                ax = plt.subplot(211)
                ax.axhline(y=0, color='k')
                plt.title(("Bar Diagram"))

                plt.subplot(212)
                plt.pie(graph_dataY, labels=graph_dataX,
                        autopct='%1.1f%%', shadow=True, startangle=140)
                plt.axis('equal')
                plt.title(("Pie Diagram"))



                pdfFileName = pdfFile.get()
                if pdfFileName == "":
                    f.savefig("graph.pdf", bbox_inches='tight')
                else:
                    f.savefig(pdfFileName + ".pdf", bbox_inches='tight')

                plt.show()



            if choice == 4 and pie_diagram_available == 0:
                plt.rcParams["figure.figsize"] = (gS[0], gS[1])
                f = plt.figure()
                x = np.arange(len(graph_dataX))
                plt.bar(x, graph_dataY, align='center', alpha=0.5)
                plt.xticks(x, graph_dataX)
                plt.xlabel(label[0])
                plt.ylabel(label[1])
                ax = plt.subplot()
                ax.axhline(y=0, color='k')

                pdfFileName = pdfFile.get()

                if pdfFileName == "":
                    f.savefig("graph.pdf", bbox_inches='tight')
                else:
                    f.savefig(pdfFileName + ".pdf", bbox_inches='tight')

                plt.show()




class Excel_CSV_file_FirstPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.labels_and_buttons()


    def  labels_and_buttons(self):


        controller = self.controller
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"),pady = 10)
        button.pack()

        label = tk.Label(self, text="Please specify the file path ", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        e = tk.Entry(self, textvariable=self.controller.shared_data["FilePath"], width=58)
        e.pack(pady=7)


        b1 = tk.Button(self, text="Click here to proceed" ,state="active",  padx=0,pady=0, font=("", 12, "bold"),width = 20,
                      command=lambda: file_info() )
        b1.pack(expand=1)
        b2 = tk.Button(self, text="Proceed" ,state="disabled",  padx=0,pady=0, font=("", 12, "bold"),width = 20,
                      command=lambda : show_second_page(self) )
        b2.pack(expand=1)

        def file_info():

            b1.configure(state = "disabled")
            b2.configure(state="active")

            FilePath = controller.shared_data['FilePath'].get()


            exception_raised = 0
            try:
                df = pd.read_excel(FilePath)
            except Exception as e:
                exception_raised = 1


            if exception_raised ==1 :
                b1.configure(state ="active")
                b2.configure(state="disabled")
                error_show_filepath()

            elif(exception_raised ==0) :

                a = list(df)
                for i in range(0,len(a)):
                    controller.shared_data['File_information'].append(a[i])


        def show_second_page(self):
            self.controller.show_frame("Excel_CSV_file_SecondPage")
            page1 = self.controller.get_page("Excel_CSV_file_SecondPage")
            page1.file_info()

        def error_show_filepath():
            controller.show_frame("error_show_filepath")





class Excel_CSV_file_SecondPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        button = tk.Button(self, text="Go back",width = 50,
                           command=lambda: controller.show_frame("StartPage"), pady=10)
        button.pack()

        label = tk.Label(self, text="Please select X-axis and Y-axis data",pady = 10,font=("", 10, "bold"))
        label.pack()


    def file_info(self):

        table_infoX = self.controller.shared_data['File_information']
        table_infoY = table_infoX.copy()

        for i in range(0,len(table_infoX)):
            table_infoY.append("count("+table_infoX[i]+")")

        for i in range(0,len(table_infoX)):
            table_infoY.append("avg("+table_infoX[i]+")")



        label = tk.Label(self, text="Select coloumn as X-axis data",pady = 10,font=("", 12, "bold"))
        label.pack()
        v1 = tk.StringVar()
        v1.set(table_infoX[0])
        w1 = tk.OptionMenu(self, v1, *table_infoX)
        w1.config(width= 40,font=("", 12, "bold"))
        w1.pack()


        label = tk.Label(self, text="Select coloumn as Y-axis data",pady = 10,font=("", 12, "bold"))
        label.pack()
        v2 = tk.StringVar()
        v2.set(table_infoY[0])
        w2 = tk.OptionMenu(self, v2, *table_infoY)
        w2.config(width= 40,font=("", 12, "bold"),pady= 7)
        w2.pack()

        #blank space text
        label = tk.Label(self, text="    ",pady = 10,font=("", 12, "bold"))
        label.pack()


        label = tk.Label(self, text="Graph size[Default value (5 5) ]",
                         font=(self.controller.title_font, 10), anchor='w')
        label.pack(side="top", fill='both', padx=70, pady=7)
        graphSize = tk.StringVar()
        e = tk.Entry(self, textvariable=graphSize, width=58)
        e.pack(pady=10)

        label = tk.Label(self, text="X and Y labels",font=(self.controller.title_font, 10), anchor='w')
        label.pack(side="top", fill='both', padx=70, pady=10)
        both_labels = tk.StringVar()
        e = tk.Entry(self, textvariable=both_labels, width=58)
        e.pack(pady=10)
        #Button show


        button = tk.Button(self, text="Draw Bar diagram", anchor='w',
                           command=lambda: retrieve_input(1), padx=50, pady=7)
        button.pack()

        button = tk.Button(self, text="Draw pie diagram", anchor='w',
                           command=lambda: retrieve_input(2), padx=50, pady=7)
        button.pack()

        button = tk.Button(self, text="Draw Bar and pie diagram", anchor='w',
                           command=lambda: retrieve_input(3), padx=50, pady=7)
        button.pack()


        button = tk.Button(self, text="Draw both diagram and save as", anchor='w',
                           command=lambda: retrieve_input(4), padx=70, pady=10)
        button.pack()
        pdfFile = tk.StringVar()
        e = tk.Entry(self, textvariable=pdfFile, width=58)
        e.pack(pady=10)


        def retrieve_input(choice):


            inputX_col = v1.get()
            inputY_col = v2.get()



            file_information = table_infoX
            avg_col = []
            count_col = []

            for i in range(0,len(file_information)):
                avg_col.append(["avg("+file_information[i]+")",file_information[i]])

            for i in range(0,len(file_information)):
                count_col.append(["count(" + file_information[i] + ")", file_information[i]])

            #This part directs that whether count choosen or two coloumns choosen

            coloumn_choosen_type = 0
            index = 0
            for i in range(0, len(file_information)):
                if file_information[i] == inputY_col:
                    coloumn_choosen_type = 1
                    break

            for i in range(0, len(avg_col)):
                if avg_col[i][0] == inputY_col:
                    coloumn_choosen_type = 2
                    index = i
                    break

            for i in range(0, len(count_col)):
                if count_col[i][0] == inputY_col:
                    coloumn_choosen_type = 3
                    index = i
                    break


            df = pd.read_excel(self.controller.shared_data['FilePath'].get())

            if coloumn_choosen_type == 1:

                result = []
                for index, row in df.iterrows():
                    result.append([row[inputX_col], row[inputY_col]])

            elif coloumn_choosen_type == 2: # fetches average data


                result = []

                if inputX_col == avg_col[index][1]:
                    query = df.groupby(inputX_col).mean()
                    for name in query.index:
                        result.append([name, query.loc[name][0]])
                else :
                    query = df[[inputX_col, avg_col[index][1]]].groupby([inputX_col]).agg(['mean'])
                    for name in query.index:
                        result.append([name, query.loc[name][0]])

            elif coloumn_choosen_type == 3:# fetches Count data

                result = []

                if inputX_col == count_col[index][1]:

                    query = df.groupby(inputX_col).count()
                    for name in query.index:
                        result.append([name, query.loc[name][0]])

                else :
                    query = df[[inputX_col, count_col[index][1]]].groupby([inputX_col]).agg(['count'])
                    for name in query.index:
                        result.append([name, query.loc[name][0]])


            #Calculation

            graph_dataX = []
            graph_dataY = []
            for i in range(0,len(result)):
                graph_dataX.append(result[i][0])
                graph_dataY.append(result[i][1])



            pie_diagram_available = 1
            #Cheking if negetive value is contained so no pie diagram available
            if type(graph_dataY[0]) is int:
                for i in range(0,len(graph_dataY)):
                    if int(graph_dataY[i])<0:
                        pie_diagram_available = 0
                        break

            if type(graph_dataY[0]) is str:
                pie_diagram_available = 0

            labels_name = both_labels.get()
            graphDimension = graphSize.get()

            gS = []
            if  graphDimension== "" :
                gS.append(5)
                gS.append(5)
            else :
                a = graphDimension.split()
                for i in range(0,len(a)):
                    gS.append(int(a[i]))

            label = []
            if  labels_name== "" :
                label.append("X-Data")
                label.append("Frequency")
            else :
                a = labels_name.split()
                for i in range(0,len(a)):
                    label.append(a[i])

            #Finish dimension of graph



            if choice == 1 :
                plt.rcParams["figure.figsize"] = (gS[0], gS[1])
                f = plt.figure()
                x = np.arange(len(graph_dataX))
                plt.bar(x, graph_dataY, align='center', alpha=0.5)
                plt.xticks(x, graph_dataX)
                plt.xlabel(label[0])
                plt.ylabel(label[1])
                ax = plt.subplot()
                ax.axhline(y=0, color='k')
                plt.show()


            if choice == 2 and pie_diagram_available == 1:
                plt.rcParams["figure.figsize"] = (gS[0], gS[1])
                f = plt.figure()
                plt.pie(graph_dataY, labels=graph_dataX,
                        autopct='%1.1f%%', shadow=True, startangle=140)
                plt.axis('equal')
                plt.show()



            if choice == 2 and pie_diagram_available == 0:
                self.controller.show_frame("error_show__pie_diagram_filepath")


            if choice == 3 and pie_diagram_available == 1:
                plt.rcParams["figure.figsize"] = (gS[0], gS[1])
                f = plt.figure()
                plt.subplot(211)
                x = np.arange(len(graph_dataX))
                plt.bar(x, graph_dataY, align='center', alpha=0.5)
                plt.xticks(x, graph_dataX)
                plt.xlabel(label[0])
                plt.ylabel(label[1])
                ax = plt.subplot(211)
                ax.axhline(y=0, color='k')
                plt.title(("Bar Diagram"))
                plt.subplot(212)
                plt.pie(graph_dataY, labels=graph_dataX,
                        autopct='%1.1f%%', shadow=True, startangle=140)
                plt.axis('equal')
                plt.title(("Pie Diagram"))
                plt.show()



            if choice == 3 and pie_diagram_available == 0:
                self.controller.show_frame("error_show__pie_diagram_filepath")



            #File saving
            if choice == 4 and pie_diagram_available == 1:
                plt.rcParams["figure.figsize"] = (gS[0], gS[1])
                f = plt.figure()
                plt.subplot(211)
                x = np.arange(len(graph_dataX))
                plt.bar(x, graph_dataY, align='center', alpha=0.5)
                plt.xticks(x, graph_dataX)
                plt.xlabel(label[0])
                plt.ylabel(label[1])
                ax = plt.subplot(211)
                ax.axhline(y=0, color='k')
                plt.title(("Bar Diagram"))

                plt.subplot(212)
                plt.pie(graph_dataY, labels=graph_dataX,
                        autopct='%1.1f%%', shadow=True, startangle=140)
                plt.axis('equal')
                plt.title(("Pie Diagram"))



                pdfFileName = pdfFile.get()
                if pdfFileName == "":
                    f.savefig("graph.pdf", bbox_inches='tight')
                else:
                    f.savefig(pdfFileName + ".pdf", bbox_inches='tight')

                plt.show()



            if choice == 4 and pie_diagram_available == 0:
                plt.rcParams["figure.figsize"] = (gS[0], gS[1])
                f = plt.figure()
                x = np.arange(len(graph_dataX))
                plt.bar(x, graph_dataY, align='center', alpha=0.5)
                plt.xticks(x, graph_dataX)
                plt.xlabel(label[0])
                plt.ylabel(label[1])
                ax = plt.subplot()
                ax.axhline(y=0, color='k')

                pdfFileName = pdfFile.get()

                if pdfFileName == "":
                    f.savefig("graph.pdf", bbox_inches='tight')
                else:
                    f.savefig(pdfFileName + ".pdf", bbox_inches='tight')

                plt.show()



class error_show_database(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="There is an error connecting to the database", pady=10, font=("", 10, "bold"))
        label.pack()
        button = tk.Button(self, text="Please try again", width=50,
                           command= lambda : show_first_page(), pady=10)
        button.pack()


        def show_first_page():
            self.controller.show_frame("DatabaseInput_FirstPage")


class error_show_can_not_draw_pie_diagram(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Can not draw Pie diagram as negetive values are included. Only Bar diagram.", pady=10, font=("", 10, "bold"))
        label.pack()
        button = tk.Button(self, text="Please try again", width=50,
                           command=lambda: go_back() , pady=10)
        button.pack()

        def go_back():
            self.controller.show_frame("StatisticalInputRange")

class error_show_can_not_draw_pie_diagram_database(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Can not draw Pie diagram as negetive values are included. Only Bar diagram.", pady=10, font=("", 10, "bold"))
        label.pack()
        button = tk.Button(self, text="Please try again", width=50,
                           command=lambda: go_back() , pady=10)
        button.pack()

        def go_back():
            self.controller.show_frame("DatabaseInput_SecondPage")


class error_show_filepath(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Can not find the file", pady=10, font=("", 10, "bold"))
        label.pack()
        button = tk.Button(self, text="Please try again", width=50,
                           command=lambda: go_back() , pady=10)
        button.pack()

        def go_back():
            self.controller.show_frame("Excel_CSV_file_FirstPage")

class error_show__pie_diagram_filepath(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Can not draw Pie diagram as negetive index or string is here", pady=10, font=("", 10, "bold"))
        label.pack()
        button = tk.Button(self, text="Please try again", width=50,
                           command=lambda: go_back() , pady=10)
        button.pack()

        def go_back():
            self.controller.show_frame("Excel_CSV_file_SecondPage")

if __name__ == "__main__":
    app = graphS()
    app.mainloop()