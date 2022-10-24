
""""
print('Hello word')

def machineQuery:

    for i in tree.get_Children():
        tree.delete(i)

    articulos = [(1, 'articulo1', 'descripcion art1', 'cant_pedidos'), (2, 'articulo2', 'descripcion art2', 'cant_pedidos')]

    for articulo in articulos:
        tree.insert(parent='', END, iid=articulo[0],text=articulo[1], values=(articulo[2], articulo[3]))

def mainQuery();
    subArticulos = [(1,'cod_articulo', 'cant_stock_linea'), (1, 'cod_articulo', 'cant_stock_linea'), (2, 'cod_articulo', 'cant_stock_linea')]
    for sub in subArticulos:
        tree.insert(parent= subArticulos[0], index=END, values=(articulo[1], articulo[2]))

----------------------------------------------------------------------FILTER----------------------------------------------------------
from tkinter import *

# First create application class


class Application(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)

        self.pack()
        self.create_widgets()

    # Create main GUI window
    def create_widgets(self):
        self.search_var = StringVar()
        self.search_var.trace("w", self.update_list)
        self.entry = Entry(self, textvariable=self.search_var, width=13)
        self.lbox = Listbox(self, width=45, height=15)

        self.entry.grid(row=0, column=0, padx=10, pady=3)
        self.lbox.grid(row=1, column=0, padx=10, pady=3)

        # Function for updating the list/doing the search.
        # It needs to be called here to populate the listbox.
        self.update_list()

    def update_list(self, *args):
        search_term = self.search_var.get()

        # Just a generic list to populate the listbox
        lbox_list = ['Adam', 'Lucy', 'Barry', 'Bob',
                     'James', 'Frank', 'Susan', 'Amanda', 'Christie']

        self.lbox.delete(0, END)

        for item in lbox_list:
                if search_term.lower() in item.lower():
                    self.lbox.insert(END, item)


root = Tk()
root.title('Filter Listbox Test')
app = Application(master=root)
app.mainloop()
---------------------------------------------------------------
scrollbarx = ttk.Scrollbar(root, orient=HORIZONTAL)
scrollbarx.configure(command=tree.xview)
tree.configure(xscrollcommand=scrollbarx.set)
scrollbarx.pack(side=BOTTOM, fill=X)
scrollbary = ttk.Scrollbar(root, orient=VERTICAL)
scrollbary.configure(command=tree.yview)
tree.configure(yscrollcommand=scrollbary.set)
scrollbary.pack(side=RIGHT, fill=Y)
"""
from cgitb import text
from fractions import Fraction
from tkinter import *
from tkinter import ttk
from traceback import print_tb

def filterFirstName(*args):
    ItemsOnTreeview = myTree.get_children()
    print("Items on treeview",ItemsOnTreeview)
    
    selections = []

    search = search_ent_var.get().capitalize()
    print("search",search)
    print(search_ent_var.get())
    for eachItem in ItemsOnTreeview:
        print("mytree.item(eachitem)",myTree.item(eachItem)['values'][2])
        print("antes del if")
        myTree.selection_remove(*myTree.selection())
        if search.lower() in myTree.item(eachItem)['values'][2]:
            print("entro al if")
            print(myTree.item(eachItem)['values'][2])
            search_var = myTree.item(eachItem)['values']
            print("search var",eachItem)
            id = eachItem
            print('id: ', id)
            myTree.delete(eachItem)
            print("Items on treeview desp delete", myTree.get_children())

            aux = myTree.insert("", 0,values=search_var)
            print('aux: ', aux)
            print("Items on treeview desp insert", myTree.get_children())
            selections.append(aux)
            
            print("selections: ", selections)
    print('search completed')
    print("Items on treeview antes select", myTree.get_children())  
    myTree.selection_set(selections)
    print("Items on treeview desp select", myTree.get_children())      
        


column = ['id', 'passport', 'fullname', "dob"]
data = [
    (1, '123456', 'ana belen', '11 de julio'),
    (2, '123456', 'pepe', '11 de julio'),
    (3, '123456', 'martin', '11 de julio'),
    (4, '123456', 'estela', '11 de julio'),
    (5, '123456', 'eric', '11 de julio'),
    (6, '123456', 'toto', '11 de julio'),
    (7, '123456', 'pablo', '11 de julio'),
    (8, '123456', 'feli', '11 de julio'),
    (9, '123456', 'loren', '11 de julio'),
    (10, '123456', 'ezequ', '11 de julio'),
    (11, '123456', 'florencia', '11 de julio'),
    (12, '123456', 'jose', '11 de julio'),
    (13, '123456', 'luis', '11 de julio'),
    (14, '123456', 'agustin', '11 de julio'),
    (15, '123456', 'mica', '11 de julio'),
    
]

root = Tk()
root.geometry("600x500")

search_ent_var = StringVar()

search_by = ttk.Combobox(root, values=column)
search_by.current(2)
search_by.grid(row=0, column=0)
tree_Frame = Frame(root)
tree_Frame.place(x=10, y=50, width=500, height=300)
myTree = ttk.Treeview(tree_Frame)
search_ent = Entry(root, textvariable= search_ent_var)
search_ent.grid(row=0, column=1, padx=10)

search_ent_var.trace("w", filterFirstName)






myTree["columns"] = column

for i in column:
    myTree.column(i, width=80)
    myTree.heading(i, text=i.capitalize())
myTree["show"] = "headings"
myTree.pack()


for each in data:
    myTree.insert("", 0, values=each)

root.mainloop()

