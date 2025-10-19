# Connector
# CREATE DATABASE pyxcel;
# USE pyxcel;
# mysql -u root -p
import mysql.connector

current_file = ""

def check_file(name):
    con = mysql.connector.connect(username="root", password="Pict@123", host="localhost", database="pyxcel")
    cursor = con.cursor()
    cursor.execute("show tables")
    t = cursor.fetchall()
    con.close()
    global current_file
    if t:
        for i in t:
            if name in i:
                return True
    return False

    
def retrieve_files():
    con = mysql.connector.connect(username="root", password="Pict@123", host="localhost", database="pyxcel")
    cursor = con.cursor()
    cursor.execute("show tables")
    t = cursor.fetchall()
    con.close()
    return t

    
def save_file(cells, fname, option, root, menu):
    if fname != "":

        option.destroy()
        root.destroy()

        previously_occupied = []

        con = mysql.connector.connect(username="root", password="Pict@123", host="localhost", database="pyxcel")
        cursor = con.cursor()
        if not check_file(fname):
            cursor.execute(f"create table {fname} (RowNo INT NOT NULL, ColNo INT NOT NULL, Value VARCHAR(150))")
            con.commit()

            
        else:
            for p in populated:
                previously_occupied.append((p[0], p[1]))

        # con = mysql.connector.connect(username="root", password="Pict@123", host="localhost", database="pyxcel")
        # cursor = con.cursor()

        for i in cells.items():
            if i[0] in previously_occupied:
                if i[1][1] != "":
                    cursor.execute(f"update {fname} set Value='{i[1][1]}' where RowNo={i[0][0]} and ColNo={i[0][1]}")
                    con.commit() 
                else:
                    cursor.execute(f"delete from {fname} where RowNo={i[0][0]} and ColNo={i[0][1]}")
                    con.commit()
            else:
                if i[1][1] != '':
                    cursor.execute(f"insert into {fname} (RowNo, ColNo, Value) values ({i[0][0]}, {i[0][1]}, '{i[1][1]}')")
                    con.commit() 

        con.close()
        menu.destroy()
        menu_screen()

def retrieve_file(fname):
    global current_file, populated 
    current_file = fname
    if fname != "":
        con = mysql.connector.connect(username="root", password="Pict@123", host="localhost", database="pyxcel")
        cursor = con.cursor()
        cursor.execute(f"select * from {fname}")
        populated = cursor.fetchall()
        con.close()
    else:
        populated = []
    return populated
    
def delete_file(fname, menu):
    con = mysql.connector.connect(username="root", password="Pict@123", host="localhost", database="pyxcel")
    cursor = con.cursor()
    cursor.execute(f"drop table {fname}")
    con.commit()
    con.close()
    menu.destroy()
    menu_screen()






# Main window
import tkinter as tk
import tkinter.font as tkFont
from tkinter import PhotoImage 

cell_width = 50
cell_height = 20

cells = {}  # Dictionary to store {id: [entry_object, value]}
populated = []

def update_cell(event):
    w = event.widget
    value = w.get()
    cells[w.id][1] = value

def on_close(root, menu):
    win_h = 120
    win_w = 400
    b_h = 30
    b_w = 100

    large_font = tkFont.Font(size=14)
    medium_font = tkFont.Font(size=12)
    
    option = tk.Toplevel(height=win_h, width=win_w)
    option.wm_title("Save File?")

    l = tk.Label(option, text="Do you want to save your file?", font=large_font)
    l.place(x=5, y=5, width=win_w-10, height=b_h)

    if current_file == "":
        name= tk.Entry(option, font=medium_font)
        name.place(x=5, y=b_h+10, width=win_w-10, height=b_h)
    else:
        name = tk.Entry(option, font=medium_font)
        name.insert(0, current_file)

    save = tk.Button(option, text="Save", command=lambda:save_file(cells, name.get(), option, root, menu), font=medium_font)
    save.place(x=((win_w//2)-b_w)//2, y=2*b_h+10, width=b_w, height=b_h)

    cancel = tk.Button(option, text="Cancel", command=lambda:(root.destroy(), option.destroy()), font=medium_font)
    cancel.place(x=(win_w//2)+((win_w//2)-b_w)//2, y=2*b_h+10, width=b_w, height=b_h)

def menu_screen():
    files = retrieve_files()

    b_h = 30
    b_w = 100

    menu = tk.Tk()
    menu.title("Choose File")

    menu_width = "310"
    menu_height = str(b_h*(len(files)+3))
    menu.geometry(menu_width+"x"+menu_height)

    large_font = tkFont.Font(size=14)
    medium_font = tkFont.Font(size=12)
    
    l = tk.Label(menu, text="Choose an Existing file, or make a new one", font=large_font)
    l.place(x=5, y=5, width=300, height=b_h)

    dustbin = PhotoImage(file="delete.png")

    for i in range(len(files)):
        # This is a Classic Lambda in Loop Problem: lambda captures the variable i by reference, not by value. So it only takes the last value of i. So we bind the file name to each lambda beforehand
        file_name = files[i][0]
        tk.Button(menu, text=file_name, bd=0, command=lambda f=file_name: create_grid(retrieve_file(f), menu, f)).place(x=5, y=b_h*(i+1)+10, width=b_w, height=b_h)
        tk.Button(menu, image=dustbin, bd=0, command=lambda f=file_name: delete_file(f, menu)).place(x=int(menu_width)-(b_w//2)-5, y=b_h*(i+1)+10, width=b_w//2, height=b_h)



    tk.Button(menu, text="New File", command=lambda:create_grid(retrieve_file(""), menu, "Untitled")).place(x=5, y=b_h*(len(files)+1)+10, width=b_w, height=b_h)
    menu.mainloop()

    
def create_grid(populated, menu, title_text):
    root = tk.Tk()
    root.title(title_text)
    root.geometry("1200x800")

    large_font = tkFont.Font(size=14)
    medium_font = tkFont.Font(size=12)
    
    rows = 800 // cell_height
    cols = 1200 // cell_width

    cell_id = 1

    def navigate_cells(event):
        current_focus = root.focus_get()
        k = event.keysym
        if isinstance(current_focus, tk.Entry) and k in ["Up", "Down", "Left", "Right"]:
            cfid = current_focus.id
            if k == "Up":
                nfid = cells[(cfid[0]-1, cfid[1])][0].id
            elif k == "Down":
                nfid = cells[(cfid[0]+1, cfid[1])][0].id
            elif k == "Left":
                nfid = cells[(cfid[0], cfid[1]-1)][0].id
            elif k == "Right":
                nfid = cells[(cfid[0], cfid[1]+1)][0].id

            new_focus = cells[nfid][0]
            new_focus.focus_set()


    for r in range(rows):  
        for c in range(cols):
            if r == 0 and c != 0:
                label = tk.Label(root, text=chr(64+c), bd=1)
                label.id = (r, c)
                label.place(x=c * cell_width, y=r * cell_height, width=cell_width, height=cell_height) 
                cells[label.id] = [label, ""]
            elif c == 0 and r != 0:
                label = tk.Label(root, text=str(r), bd=1)
                label.id = (r, c)
                label.place(x=c * cell_width, y=r * cell_height, width=cell_width, height=cell_height) 
                cells[label.id] = [label, ""]
            elif c == 0 and r == 0:
                label = tk.Label(root)
                label.id = (r, c)
                label.place(x=c * cell_width, y=r * cell_height, width=cell_width, height=cell_height) 
                cells[label.id] = [label, ""]
            else:
                entry = tk.Entry(
                        root,
                        justify="center",
                        bd=1,                
                        highlightthickness=0
                    )
                entry.id = (r, c) # each entry object has the id (row, column) linked to it
                entry.place(x=c * cell_width, y=r * cell_height, width=cell_width, height=cell_height)
                entry.bind("<KeyRelease>", update_cell)
                entry_text = ""
                for p in populated:
                    if r==p[0] and c==p[1]:
                        entry_text = p[2]           
                entry.insert(0, entry_text) 
                # Initialize dictionary
                cells[entry.id] = [entry, entry_text] # All widgets are accessible using their ids (row, column)

            cell_id += 1   


    root.bind("<Key>", navigate_cells)
    root.protocol("WM_DELETE_WINDOW", lambda: on_close(root, menu))


    root.mainloop()


menu_screen()
