from tkinter import*
from tkinter import ttk

root = Tk()
root.geometry('1430x400')
root.resizable(0,0)
#root.config(bg="")
root.title('Sox')

arbol = ttk.Treeview(root, columns=("Pedidos", "Deposito", "Saldo", "Linea", "Tejeduria", "Ordenes programadas"))


art1 = arbol.insert("", END, text="articulo1",values=("7","4","-3","12","0","500"))
arbol.insert(art1, END, text="sub-articulo1", values=("-","-","-","10","15","?"))
arbol.insert(art1, END, text="sub-articulo2", values=("10","10","10","5","20","?"))
arbol.insert("", END, text="articulo2", values=("15","10","5","3","100","400"))
art3 = arbol.insert("", END, text="articulo3",values=("7","4","-3","12","0","500"))
arbol.insert(art3, END, text="sub-articulo1", values=("-","-","-","10","15","?"))
arbol.insert(art3, END, text="sub-articulo2", values=("10","10","10","5","20","?"))
arbol.insert("", END, text="articulo4", values=("15","10","5","3","100","400"))
arbol.insert("", END, text="articulo5", values=("15","10","5","3","100","400"))

arbol.heading("#0", text="Articulo")
arbol.heading("Pedidos", text="Pedidos")
arbol.heading("Deposito", text="Deposito")
arbol.heading("Saldo", text="Saldo")
arbol.heading("Linea", text="Linea")
arbol.heading("Tejeduria", text="Tejeduria")
arbol.heading("Ordenes programadas", text="Ordenes programadas")




arbol.place(x=10, y=10)



root.mainloop()