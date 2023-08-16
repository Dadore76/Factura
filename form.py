from tkinter import *
from factura import create_pdf, open_pdf

### Create Form
form = Tk()

### Form Title
form.title("Factura")

### Form Size
form.geometry("600x300")

### Controls
# Frame
frm_header = Frame(form, width=600, height=100)
frm_header.pack() 

frm_buttons = Frame(form, width=600, height=100)
frm_buttons.pack()

# Label
lbl_fecha = Label(frm_header, text="Fecha:")
lbl_fecha.grid(row=0, column=0)
lbl_fecha.config(padx=10,pady=10)

txt_fecha = Entry(frm_header)
txt_fecha.grid(row=0, column=1)

# Button
btn_crear = Button(frm_buttons, text="Generar PDF", command=create_pdf)
btn_crear.grid(row=0, column=0)
# btn_crear.pack(side='left')
btn_abrir = Button(frm_buttons, text="Abrir PDF", command=open_pdf)
btn_abrir.grid(row=0, column=1)



# Ejecutar Form
form.mainloop()