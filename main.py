# Connector
# CREATE DATABASE pyxcel;
# USE pyxcel;
# CREATE TABLE data (RowNo INT NOT NULL, ColNo INT NOT NULL, Value VARCHAR(150));
import pickle 
import mysql.connector

def pickle_object(cell):
    b_cell = pickle.dumps(cell)
    return b_cell

def check_file(name):
    con = mysql.connector.connect(username="root", password="Pict@123", host="localhost", database="pyxcel")
    cursor = con.cursor()
    cursor.execute("show tables")
    t = cursor.fetchall()
    con.close()
    if name in t[0]:
        return True
    else:
        return False

    
def retrieve_files():
    con = mysql.connector.connect(username="root", password="Pict@123", host="localhost", database="pyxcel")
    cursor = con.cursor()
    cursor.execute("show tables")
    t = cursor.fetchall()
    con.close()
    return t

    
def save_file(cells, fname):
    if not check_file(fname):
        con = mysql.connector.connect(username="root", password="Pict@123", host="localhost", database="pyxcel")
        cursor = con.cursor()
        cursor.execute(f"create table {fname} (RowNo INT NOT NULL, ColNo INT NOT NULL, Value VARCHAR(150))")
        con.commit()
        con.close()
    else:
        pass
    con = mysql.connector.connect(username="root", password="Pict@123", host="localhost", database="pyxcel")
    cursor = con.cursor()
    for i in cells.items():
        if i[1][1] != '':
            cursor.execute(f"insert into {fname} (RowNo, ColNo, Value) values ({i[0][0]}, {i[0][1]}, '{i[1][1]}')")
            print("Done")
            con.commit()
    con.close()
    root.destroy

def retrieve_file(fname):
    con = mysql.connector.connect(username="root", password="Pict@123", host="localhost", database="pyxcel")
    cursor = con.cursor()
    cursor.execute(f"select * from {fname}")
    populated = cursor.fetchall()
    con.close()
    return populated
    
    





# Main window
import tkinter as tk
import tkinter.font as tkFont

cell_width = 50
cell_height = 20

cells = {}  # Dictionary to store {id: [entry_object, value]}
populated = retrieve_file("data")
print(populated)

def update_cell(event):
    w = event.widget
    value = w.get()
    cells[w.id][1] = value



            

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
        

    
def on_close(root):
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

    name = tk.Entry(option, font=medium_font)
    name.place(x=5, y=b_h+10, width=win_w-10, height=b_h)

    save = tk.Button(option, text="Save", command=lambda: save_file(cells, name.get()), font=medium_font)
    save.place(x=((win_w//2)-b_w)//2, y=2*b_h+10, width=b_w, height=b_h)

    cancel = tk.Button(option, text="Cancel", command=lambda:(root.destroy(), option.destroy()), font=medium_font)
    cancel.place(x=(win_w//2)+((win_w//2)-b_w)//2, y=2*b_h+10, width=b_w, height=b_h)

def menu_screen():
    menu = tk.Tk()
    menu.title("Choose File")
    menu.geometry("310x200")

    b_h = 30
    b_w = 100

    large_font = tkFont.Font(size=14)
    medium_font = tkFont.Font(size=12)
    
    files = retrieve_files()
    i=1
    
    l = tk.Label(menu, text="Choose an Existing file, or make a new one", font=medium_font)
    l.place(x=5, y=5, width=300, height=b_h)
    
    for f in files:
        print(retrieve_file(f[0]))
        tk.Button(menu, text=f[0],command=lambda: create_grid(retrieve_file(f[0])), font=medium_font).place(x=5, y=b_h*i+10, width=b_w, height=b_h)
        i+=1

    tk.Button(menu, text="New File",command=create_grid, font=medium_font).place(x=5, y=b_h*(i)+10, width=b_w, height=b_h)
    menu.mainloop()

    
def create_grid(populated={}):
    root = tk.Tk()
    root.title("Pyxcel")
    root.geometry("1200x800")

    large_font = tkFont.Font(size=14)
    medium_font = tkFont.Font(size=12)
    
    rows = 800 // cell_height
    cols = 1200 // cell_width

    cell_id = 1
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
    root.protocol("WM_DELETE_WINDOW", lambda: on_close(root))


    root.mainloop()


menu_screen()
