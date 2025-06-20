"""
project: open_data_analysis_Mg
creator : Gabriel Marchive
version : v 1.0
date: 18/06/2025
"""

#----------------------
# imported lib and file
#----------------------

# file
import calcule as cll
import graph_plan_exp as gpe
# standar py-lib
import numpy as np
import csv 
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import *
from matplotlib.figure import Figure
from matplotlib.ticker import LinearLocator
from matplotlib import cm
from tkinter.filedialog import asksaveasfile
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)


#--------------------------------------------------
# global variable
#--------------------------------------------------
loaded_data = []


#--------------------------------------------------
# import, save, operation on external data fonction
#--------------------------------------------------

def import_data():
    global loaded_data
    Wchosefile = tk.Toplevel(root)
    Wchosefile.title("Chose file")
    filename = askopenfilename(title="open csv data file",filetypes=[('csv','.csv'),('all files','.*')])
    content = cll.data_recup(filename)
    loaded_data.append([filename,content[0],content[1]])
    tk.Label(Wchosefile, text="Le fichier "+filename+ " comprend: ").pack(padx=10, pady=10)
    tk.Label(Wchosefile, text=str(len(content[0]))+" point experimentaux").pack(padx=10, pady=10)
    tk.Label(Wchosefile, text=str(len(content[0][0]))+" variables").pack(padx=10, pady=10)
    tk.Label(Wchosefile, text="information correcte ?").pack(padx=10, pady=10)
    tk.Button(Wchosefile, text='Non', command=lambda: [import_data_no(), Wchosefile.destroy()]).pack(side = tk.LEFT ,padx=10, pady=5)
    tk.Button(Wchosefile, text='Oui', command=lambda: [import_data_yes(), Wchosefile.destroy()]).pack(side = tk.RIGHT ,padx=10, pady=5)
    return

def import_data_yes():
    global loaded_data
    root_treeview.insert("",tk.END,text = loaded_data[-1][0],values=(len(loaded_data[-1][1][0]),len(loaded_data[-1][1])))
    result =np.ndarray.tolist(loaded_data[-1][2])
    with open("saved_data.csv", "a") as csvfile:  
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["start"])
        csvwriter.writerow([loaded_data[-1][0]])   
        for i in range(len(loaded_data[-1][1])):
            row = np.array(np.append(loaded_data[-1][1][i],result[i]))
            csvwriter.writerows([row])
        csvwriter.writerow(["end"])  
    csvfile.close()
    root_label1.config(text="data set imported with succes")
    return

def import_data_no():
    global loaded_data
    loaded_data.pop()
    root_label1.config(text="invalid data set")
    return


def view_data():
    global loaded_data
    index_disp = treeview_select_item()
    display_data_window = tk.Toplevel(root)
    display_data_window.title(loaded_data[index_disp][0])
    list_name_treeview = ()
    for i in range(np.shape(loaded_data[index_disp][1])[1]):
        list_name_treeview = list_name_treeview + ("variable num "+str(i+1),)
    for i in range(np.shape(loaded_data[index_disp][2])[1]):
        list_name_treeview = list_name_treeview + ("result num "+str(i+1),)
    display_data_treeview = ttk.Treeview(display_data_window,columns=list_name_treeview, show="headings")
    for i in range(len(list_name_treeview)):
        display_data_treeview.heading(list_name_treeview[i], text=list_name_treeview[i])
    for i in range(np.shape(loaded_data[index_disp][1])[0]):
        tuple_data = ()
        for a in range(np.shape(loaded_data[index_disp][1])[1]):
            tuple_data = tuple_data + (loaded_data[index_disp][1][i][a],)
        for a in range(np.shape(loaded_data[index_disp][2])[1]):
            tuple_data = tuple_data + (loaded_data[index_disp][2][i][a],)
        display_data_treeview.insert("",tk.END,values=tuple_data)

    v_scrollbar2 = ttk.Scrollbar(display_data_window, orient=tk.VERTICAL, command=display_data_treeview.yview)
    display_data_treeview.configure(yscrollcommand=v_scrollbar2.set)

    display_data_treeview.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    v_scrollbar2.pack(side=tk.RIGHT, fill=tk.Y)
    return

def delete_data():
    global loaded_data
    result = []
    index_item_del = treeview_select_item()
    load_data_from_saved_file()
    for a in range(len(loaded_data)):
        result.append(np.ndarray.tolist(loaded_data[a][2]))
    with open("saved_data.csv", "w") as csvfile:  
        csvwriter = csv.writer(csvfile)
        for a in range(len(loaded_data)):
            if a != index_item_del:
                csvwriter.writerow(["start"])
                csvwriter.writerow([loaded_data[a][0]])   
                for i in range(len(loaded_data[a][1])):
                    row = np.array(np.append(loaded_data[a][1][i],result[a][i]))
                    csvwriter.writerows([row])
                csvwriter.writerow(["end"])  
    csvfile.close()
    load_data_from_saved_file()
    return

def load_data_from_saved_file():
    global loaded_data
    root_treeview.delete(*root_treeview.get_children())
    loaded_data = []
    with open("saved_data.csv", mode = "r") as datafile:
        csvFile = csv.reader(datafile)
        a = 0
        for line in csvFile:
            if line == ["start"]:
                a += 1
            elif line == ["end"]:
                loaded_data[-1][1] = np.asarray(loaded_data[-1][1],dtype=float)
                loaded_data[-1][2] = np.asarray(loaded_data[-1][2],dtype=float)
                loaded_data[-1][2] = np.reshape(loaded_data[-1][2],(np.shape(loaded_data[-1][2])[0],1))
                root_treeview.insert("",tk.END,text=loaded_data[-1][0],values=(len(loaded_data[-1][1][0]),len(loaded_data[-1][1])))
                a = 0
            elif a == 1:
                loaded_data.append([line[0],[],[]])
                a += 1
            elif a == 2: 
                #print(line[:-1],line)
                loaded_data[-1][1].append(line[:-1])
                loaded_data[-1][2].append(line[-1])
    datafile.close()             
    return
#--------------------------------------------------
# call fonction
#--------------------------------------------------

def experiment_plan_analysis():
    global loaded_data,alpha_entry,valeur_entry
    index = treeview_select_item()
    epa_window1 = tk.Toplevel(root)
    epa_window1.title(loaded_data[index][0])
    epa_window1.geometry("150x150")
    tk.Label(epa_window1,text="Alpha:").pack()
    alpha_entry = tk.Entry(epa_window1,width=5)
    alpha_entry.insert(0,"0.05")
    alpha_entry.pack()
    tk.Label(epa_window1,text="valeur:").pack()
    valeur_entry = tk.Entry(epa_window1,width=6)
    valeur_entry.insert(0,"0.25")
    valeur_entry.pack()
    tk.Button(epa_window1,text="start analysis",command=lambda : [epa_start(),epa_window1.destroy()]).pack()
    
def epa_start():
    global loaded_data,alpha_entry,valeur_entry
    alpha = float(alpha_entry.get())
    valeur = float(valeur_entry.get())
    index = treeview_select_item()
    epa_window = tk.Toplevel(root)
    epa_window.title(loaded_data[index][0])
    epa_window.geometry("500x500")
    model,poly_exp,info_exp = cll.estimation_statistique_simple(loaded_data[index][1],loaded_data[index][2],alpha,valeur)
    epa_label1 = tk.Label(epa_window,text="alpha = " + str(alpha) + ", valeur = " + str(valeur))
    epa_text1 = tk.Text(epa_window,height=3)
    epa_text1.insert(tk.END,
    "DOFfit = " + str(info_exp[0]) + "                 " + "Sfit = " + str(info_exp[3]) + "\n" +
    "DOFexp = " + str(info_exp[1]) + "                 " + "Sexp = " + str(info_exp[4]) + "\n" +                                
    "DOFres = " + str(info_exp[2]) + "                 " + "Sres = " + str(info_exp[5])
                            )
    epa_treeview = ttk.Treeview(epa_window,columns=("name","value","erreur"), show="headings")
    epa_treeview.heading("name",text="name")
    epa_treeview.heading("value",text="value")
    epa_treeview.heading("erreur",text="erreur")
    for i in range(len(poly_exp)):
        tuple_data = (poly_exp[i][0],poly_exp[i][1],poly_exp[i][2])
        if abs(poly_exp[i][1]) >= abs(poly_exp[i][2]) :
            epa_treeview.insert("",tk.END,values=tuple_data,tags=("ok",))
        else :
            epa_treeview.insert("",tk.END,values=tuple_data,tags=("not_ok",))

    epa_treeview.tag_configure('ok', background='green')
    epa_treeview.tag_configure('not_ok', background='red')        
    epa_label1.pack()
    epa_text1.pack()
    tk.Label(epa_window,text="ANOVA test: " +cll.ANOVA_test(info_exp[3]/info_exp[4],alpha,info_exp[0],info_exp[1])).pack()
    v_scrollbar3 = ttk.Scrollbar(epa_window, orient=tk.VERTICAL, command=epa_treeview.yview)
    epa_treeview.configure(yscrollcommand=v_scrollbar3.set)

    epa_treeview.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    v_scrollbar3.pack(side=tk.RIGHT, fill=tk.Y)    
    return

def information_matrix():
    global loaded_data
    index = treeview_select_item()
    cll.visuel_info_matrix(cll.information_matrix(loaded_data[index][1]))
    return

def experiment_plan_analysis_graph():
    global loaded_data
    index = treeview_select_item()
    gpe.graph(cll.model(loaded_data[index][1],loaded_data[index][2]))
    return

def experiment_plan_analysis_export_report():
    return

#--------------------------------------------------
# other fonction
#--------------------------------------------------

def treeview_select_item():
    selection1 = root_treeview.focus()
    child_root_treeview = root_treeview.get_children()
    if type(child_root_treeview) != tuple:
        return 0
    print(child_root_treeview,selection1)
    aled = child_root_treeview.index(selection1)
    return aled

#--------------------------------------------------
# root element
#--------------------------------------------------
root = tk.Tk()

root_title = root.title("open data analysis v1.0")
root_label1 = tk.Label(text="welcome")
root_label1.pack(side=tk.TOP)

# Menus
root_menu = tk.Menu(root)

child_menu1 = tk.Menu(root_menu,tearoff=0)
child_menu1.add_command(label="data analysis",command=experiment_plan_analysis)
child_menu1.add_command(label="information matrix",command=information_matrix)
child_menu1.add_command(label="symulation graph",command=experiment_plan_analysis_graph)
child_menu1.add_command(label="export report",command=experiment_plan_analysis_export_report)
root_menu.add_cascade(label="experiment plan analysis",menu=child_menu1)

child_menu2 = tk.Menu(root_menu,tearoff=0)
child_menu2.add_command(label="exit",command=root.quit)
root_menu.add_cascade(label="window",menu=child_menu2)

root.config(menu=root_menu)

# data selection

root_treeview = ttk.Treeview(root,columns=("number of variable","number of data point"))
root_treeview.heading("#0", text="name")
root_treeview.heading("number of variable", text="number of variable")
root_treeview.heading("number of data point", text="number of data point")
v_scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=root_treeview.yview)
root_treeview.configure(yscrollcommand=v_scrollbar.set)
root_treeview.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

#root botton
root_bt_import = tk.Button(root,text="import data",command=import_data)
root_bt_reload = tk.Button(root,text="reload",command=load_data_from_saved_file)
root_bt_view = tk.Button(root,text="view data",command=view_data)
root_bt_delete = tk.Button(root,text="delete data",command=delete_data)
root_bt_import.pack(side=tk.RIGHT)
root_bt_reload.pack(side=tk.RIGHT)
root_bt_view.pack(side=tk.RIGHT)
root_bt_delete.pack(side=tk.RIGHT)

#init_fonction
load_data_from_saved_file()




root.mainloop()