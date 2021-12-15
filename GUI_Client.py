import tkinter as tk
import mysql.connector
import hashlib
from tkinter import ttk
from datetime import datetime
import os
from dotenv import load_dotenv


load_dotenv()
HEIGHT, WIDTH = 800, 1300
COLOR1, COLOR2, COLOR3 = '#00256B', '#4782EE', '#203A6B'
TEXT_COLOR = 'white'
FONT_HEADLINE = ('Helvetica', 32)
FONT_BODY = ('Helvetica', 14)
COLUMNS_CARDS = ('Card ID', 'Card Name', 'Set Name', 'Set ID', 'Rarity', 'Foil?', 'Price in €',
                 'Date Created', 'Created by')
COLUMNS_QUEUE = ('Card Name', 'Set Name', 'Set ID', 'Rarity', 'Foil?')
RARITIES = ('Uncommon', 'Rare', 'Mythical')
FOIL = ('No', 'Yes')

db = mysql.connector.connect(
    host=os.environ['IP'],
    user=os.environ['USER'],
    passwd=os.environ['PASSWORD'],
    database='testdb'
    )

root = tk.Tk()
root.title('MtG Card Manager')
root.minsize(WIDTH, HEIGHT)

user_name = tk.StringVar()
password = tk.StringVar()

# Create variables for entry fields
var_cardname = tk.StringVar()
var_setname = tk.StringVar()
var_setid = tk.StringVar()
var_rarity = tk.StringVar()
var_foil = tk.StringVar()
# Create variables for checkboxes
var_c_cardname = tk.IntVar()
var_c_setname = tk.IntVar()
var_c_setid = tk.IntVar()
var_c_rarity = tk.IntVar()
var_c_foil = tk.IntVar()

style_app = ttk.Style()
style_app.theme_use('alt')

global counter_add
counter_add = 0

frame = tk.Frame(root)
frame.place(relwidth=1, relheight=1)


# Define switch functions
def switch_overview():

    def get_detail_id():
        cur_item = tree_overview_cards.focus()
        loc_value = tree_overview_cards.item(cur_item, 'values')
        switch_detail(loc_value[0])

    frame_welcome.destroy()

    # Start for overview page
    frame_overview = tk.Frame(frame, bg=COLOR2)
    frame_overview.place(relheight=1, relwidth=1)

    # Start for overview header
    frame_overview_header = tk.Frame(frame_overview, bg=COLOR1)
    frame_overview_header.place(relwidth=0.98, height=60, relx=0.02, rely=0.05, anchor='nw')

    label_overview_header = tk.Label(frame_overview_header,
                                     text='Overview Cards',
                                     font=FONT_HEADLINE,
                                     bg=COLOR1,
                                     foreground=TEXT_COLOR)
    label_overview_header.grid(column=0, row=0)
    # End overview header

    frame_overview_treeview = tk.Frame(frame_overview, bg=COLOR2)
    frame_overview_treeview.place(width=800, height=400, relx=0.02, rely=0.2)

    # Start treeview box
    tree_overview_cards = ttk.Treeview(frame_overview_treeview)
    tree_overview_cards['columns'] = COLUMNS_CARDS

    tree_overview_cards.column('#0', width=0, stretch='no')
    tree_overview_cards.column('Card ID', width=10, minwidth=10)
    tree_overview_cards.column('Card Name', width=50, minwidth=10)
    tree_overview_cards.column('Set Name', width=180, minwidth=10)
    tree_overview_cards.column('Set ID', width=20, minwidth=10)
    tree_overview_cards.column('Rarity', width=50, minwidth=10)
    tree_overview_cards.column('Foil?', width=10, minwidth=10)
    tree_overview_cards.column('Price in €', width=20, minwidth=10)
    tree_overview_cards.column('Date Created', width=100, minwidth=10)
    tree_overview_cards.column('Created by', width=40, minwidth=10)

    tree_overview_cards.heading('Card ID', text='Card ID', anchor='w')
    tree_overview_cards.heading('Card Name', text='Card Name', anchor='w')
    tree_overview_cards.heading('Set Name', text='Set Name', anchor='w')
    tree_overview_cards.heading('Set ID', text='Set ID', anchor='w')
    tree_overview_cards.heading('Rarity', text='Rarity', anchor='w')
    tree_overview_cards.heading('Foil?', text='Foil?', anchor='w')
    tree_overview_cards.heading('Price in €', text='Price in €', anchor='w')
    tree_overview_cards.heading('Date Created', text='Date Created', anchor='w')
    tree_overview_cards.heading('Created by', text='Created by', anchor='w')

    mycursor = db.cursor()
    mycursor.execute('SELECT * FROM Cards')
    counter = 0
    for card_id, card_name, set_name, set_id, rarity, foil, price, date_created, created_by in mycursor:
        tree_overview_cards.insert(parent='', index='end', iid=counter, text='', values=(card_id,
                                                                                         card_name,
                                                                                         set_name,
                                                                                         set_id,
                                                                                         rarity,
                                                                                         foil,
                                                                                         price,
                                                                                         date_created,
                                                                                         created_by))
        counter += 1

    tree_overview_cards.place(relwidth=1, relheight=0.8, relx=0, rely=0, anchor='nw')
    # End Treeview

    # Start Treeview Buttons
    frame_overview_tv_buttons = tk.Frame(frame_overview_treeview, bg=COLOR2)
    frame_overview_tv_buttons.place(relwidth=1, relheight=0.2, relx=0, rely=0.8, anchor='nw')

    button_overview_edit = tk.Button(frame_overview_tv_buttons,
                                     text='Edit Card',
                                     font=FONT_BODY,
                                     bg=COLOR3,
                                     foreground=TEXT_COLOR,
                                     state='normal',
                                     command=switch_edit)
    button_overview_edit.grid(column=0, row=0, padx=20, pady=10)

    button_overview_detail = tk.Button(frame_overview_tv_buttons,
                                       text='Show Details',
                                       font=FONT_BODY,
                                       bg=COLOR3,
                                       foreground=TEXT_COLOR,
                                       state='normal',
                                       command=get_detail_id)
    button_overview_detail.grid(column=1, row=0, padx=20, pady=10)

    button_overview_delete = tk.Button(frame_overview_tv_buttons,
                                       text='Delete Card',
                                       font=FONT_BODY,
                                       bg=COLOR3,
                                       foreground=TEXT_COLOR,
                                       state='normal')
    button_overview_delete.grid(column=2, row=0, padx=20, pady=10)
    # End treeview buttons
    # End treeview box

    # Start Navigation buttons
    frame_overview_functions = tk.Frame(frame_overview, bg=COLOR2)
    frame_overview_functions.place(width=500, height=50, relx=0.02, rely=0.92, anchor='nw')

    button_overview_overview = tk.Button(frame_overview_functions,
                                         text='Overview Cards',
                                         font=FONT_BODY,
                                         bg=COLOR3,
                                         foreground=TEXT_COLOR,
                                         state='disabled',
                                         command=switch_overview)
    button_overview_overview.grid(column=0, row=0, padx=10)

    button_overview_search = tk.Button(frame_overview_functions,
                                       text='Search Cards',
                                       font=FONT_BODY,
                                       bg=COLOR3,
                                       foreground=TEXT_COLOR,
                                       state='normal',
                                       command=switch_search)
    button_overview_search.grid(column=1, row=0, padx=10)

    button_overview_add = tk.Button(frame_overview_functions,
                                    text='Add new Cards',
                                    font=FONT_BODY,
                                    bg=COLOR3,
                                    foreground=TEXT_COLOR,
                                    state='normal',
                                    command=switch_add)
    button_overview_add.grid(column=2, row=0, padx=10)


def switch_search():

    frame_welcome.destroy()

    # Start search page
    frame_search = tk.Frame(frame, bg=COLOR2)
    frame_search.place(relheight=1, relwidth=1)

    # Start search header
    frame_search_header = tk.Frame(frame_search, bg=COLOR1)
    frame_search_header.place(relwidth=0.98, height=60, relx=0.02, rely=0.05, anchor='nw')

    label_search_header = tk.Label(frame_search_header,
                                   text='Search Database',
                                   bg=COLOR1,
                                   font=FONT_HEADLINE,
                                   foreground=TEXT_COLOR)
    label_search_header.grid(column=0, row=0)
    # End Search Header

    # Start Search Options
    frame_search_options = tk.Frame(frame_search, bg=COLOR1)
    frame_search_options.place(height=100, relwidth=0.98, relx=0.02, rely=0.2, anchor='nw')

    label_search_cname = tk.Label(frame_search_options,
                                  text='Card Name',
                                  bg=COLOR1,
                                  font=FONT_BODY,
                                  foreground=TEXT_COLOR)
    label_search_cname.grid(column=0, row=0, padx=5, pady=5, sticky='w')

    label_search_sname = tk.Label(frame_search_options,
                                  text='Set Name',
                                  bg=COLOR1,
                                  font=FONT_BODY,
                                  foreground=TEXT_COLOR)
    label_search_sname.grid(column=0, row=1, padx=5, pady=5, sticky='w')

    label_search_rarity = tk.Label(frame_search_options,
                                   text='Rarity',
                                   bg=COLOR1,
                                   font=FONT_BODY,
                                   foreground=TEXT_COLOR)
    label_search_rarity.grid(column=4, row=0, padx=5, pady=5, sticky='w')

    label_search_foil = tk.Label(frame_search_options,
                                 text='Foil?',
                                 bg=COLOR1,
                                 font=FONT_BODY,
                                 foreground=TEXT_COLOR)
    label_search_foil.grid(column=4, row=1, padx=5, pady=5, sticky='w')

    entry_search_cname = tk.Entry(frame_search_options, textvariable=var_cardname, foreground='black')
    entry_search_cname.grid(column=1, row=0, padx=5, pady=5, sticky='w')

    entry_search_sname = tk.Entry(frame_search_options, textvariable=var_setname, foreground='black')
    entry_search_sname.grid(column=1, row=1, padx=5, pady=5, sticky='w')

    dropdown_search_rarity = tk.OptionMenu(frame_search_options, var_rarity, *RARITIES)
    dropdown_search_rarity.config(width=12)
    var_rarity.set(RARITIES[0])
    dropdown_search_rarity.grid(column=5, row=0, padx=10, pady=5, sticky='w')

    dropdown_search_foil = tk.OptionMenu(frame_search_options, var_foil, *FOIL)
    dropdown_search_foil.config(width=12)
    var_foil.set(FOIL[0])
    dropdown_search_foil.grid(column=5, row=1, padx=10, pady=5, sticky='w')

    button_search_cname = tk.Button(frame_search_options,
                                    text='Search',
                                    bg=COLOR3,
                                    font=FONT_BODY,
                                    foreground=TEXT_COLOR,
                                    state='normal')
    button_search_cname.grid(column=2, row=0, padx=10, pady=5)

    button_search_sname = tk.Button(frame_search_options,
                                    text='Search',
                                    bg=COLOR3,
                                    font=FONT_BODY,
                                    foreground=TEXT_COLOR,
                                    state='normal')
    button_search_sname.grid(column=2, row=1, padx=10, pady=5)

    button_search_rarity = tk.Button(frame_search_options,
                                     text='Search',
                                     bg=COLOR3,
                                     font=FONT_BODY,
                                     foreground=TEXT_COLOR,
                                     state='normal')
    button_search_rarity.grid(column=6, row=0, padx=10, pady=5)

    button_search_foil = tk.Button(frame_search_options,
                                   text='Search',
                                   bg=COLOR3,
                                   font=FONT_BODY,
                                   foreground=TEXT_COLOR,
                                   state='normal')
    button_search_foil.grid(column=6, row=1, padx=10, pady=5)

    frame_search_options_space1 = tk.Frame(frame_search_options, bg=COLOR1)
    frame_search_options_space1.grid(column=3, row=1, padx=60, pady=5)
    # End search options

    # Start search treeview
    frame_search_treeview = tk.Frame(frame_search, bg=COLOR1)
    frame_search_treeview.place(width=800, height=400, relx=0.02, rely=0.4)

    tree_search_cards = ttk.Treeview(frame_search_treeview)
    tree_search_cards['columns'] = COLUMNS_CARDS

    tree_search_cards.column('#0', width=0, stretch='no')
    tree_search_cards.column('Card ID', width=10, minwidth=10)
    tree_search_cards.column('Card Name', width=50, minwidth=10)
    tree_search_cards.column('Set Name', width=50, minwidth=10)
    tree_search_cards.column('Rarity', width=50, minwidth=10)
    tree_search_cards.column('Foil?', width=10, minwidth=10)
    tree_search_cards.column('Price in €', width=20, minwidth=10)

    tree_search_cards.heading('Card ID', text='Card ID', anchor='w')
    tree_search_cards.heading('Card Name', text='Card Name', anchor='w')
    tree_search_cards.heading('Set Name', text='Set Name', anchor='w')
    tree_search_cards.heading('Rarity', text='Rarity', anchor='w')
    tree_search_cards.heading('Foil?', text='Foil?', anchor='w')
    tree_search_cards.heading('Price in €', text='Price in €', anchor='w')

    tree_search_cards.insert(parent='', index='end', iid=0, text='', values=(12,
                                                                             'Spare Dagger',
                                                                             'AitFR',
                                                                             'Common',
                                                                             'No',
                                                                             0.01))
    tree_search_cards.place(relwidth=1, relheight=0.8, relx=0, rely=0, anchor='nw')

    # Start Treeview Buttons
    frame_search_tv_buttons = tk.Frame(frame_search_treeview, bg=COLOR2)
    frame_search_tv_buttons.place(relwidth=1, relheight=0.2, relx=0, rely=0.8, anchor='nw')

    button_search_edit = tk.Button(frame_search_tv_buttons,
                                   text='Edit Card',
                                   font=FONT_BODY,
                                   bg=COLOR3,
                                   foreground=TEXT_COLOR,
                                   state='normal',
                                   command=switch_edit)
    button_search_edit.grid(column=0, row=0, padx=20, pady=10)

    button_search_detail = tk.Button(frame_search_tv_buttons,
                                     text='Show Details',
                                     font=FONT_BODY,
                                     bg=COLOR3,
                                     foreground=TEXT_COLOR,
                                     state='normal',
                                     command=switch_detail)
    button_search_detail.grid(column=1, row=0, padx=20, pady=10)

    button_search_delete = tk.Button(frame_search_tv_buttons,
                                     text='Delete Card',
                                     font=FONT_BODY,
                                     bg=COLOR3,
                                     foreground=TEXT_COLOR,
                                     state='normal')
    button_search_delete.grid(column=2, row=0, padx=20, pady=10)
    # End Treeview

    # Start Navigation buttons
    frame_search_functions = tk.Frame(frame_search, bg=COLOR2)
    frame_search_functions.place(width=500, height=50, relx=0.02, rely=0.92, anchor='nw')

    button_search_overview = tk.Button(frame_search_functions,
                                       text='Overview Cards',
                                       font=FONT_BODY,
                                       bg=COLOR3,
                                       foreground=TEXT_COLOR,
                                       state='normal',
                                       command=switch_overview)
    button_search_overview.grid(column=0, row=0, padx=10)

    button_search_search = tk.Button(frame_search_functions,
                                     text='Search Cards',
                                     font=FONT_BODY,
                                     bg=COLOR3,
                                     foreground=TEXT_COLOR,
                                     state='disabled',
                                     command=switch_search)
    button_search_search.grid(column=1, row=0, padx=10)

    button_search_add = tk.Button(frame_search_functions,
                                  text='Add new Cards',
                                  font=FONT_BODY,
                                  bg=COLOR3,
                                  foreground=TEXT_COLOR,
                                  state='normal',
                                  command=switch_add)
    button_search_add.grid(column=2, row=0, padx=10)
    # End navigation


def switch_add():

    def add_queue():
        global counter_add
        tree_add_cards.insert(parent='', index='end', iid=counter_add, text='', values=(var_cardname.get(),
                                                                                        var_setname.get(),
                                                                                        var_setid.get(),
                                                                                        var_rarity.get(),
                                                                                        var_foil.get()))

        var_cardname.set('')
        var_setname.set('')
        var_setid.set('')
        var_rarity.set(RARITIES[0])
        var_foil.set(FOIL[0])

        counter_add += 1

    def add_delete_entries():
        for record in tree_add_cards.get_children():
            tree_add_cards.delete(record)

    def add_delete_entry():
        for record in tree_add_cards.selection():
            tree_add_cards.delete(record)

    frame_welcome.destroy()

    frame_add = tk.Frame(frame, bg=COLOR2)
    frame_add.place(relwidth=1, relheight=1)

    # Start add header
    frame_add_header = tk.Frame(frame_add, bg=COLOR1)
    frame_add_header.place(relwidth=0.98, height=60, relx=0.02, rely=0.05, anchor='nw')

    label_add_header = tk.Label(frame_add_header,
                                text='Add new Card',
                                bg=COLOR1,
                                font=FONT_HEADLINE,
                                foreground=TEXT_COLOR)
    label_add_header.place(x=5, rely=0.5, anchor='w')
    # End add Header

    # Start Input
    frame_add_input = tk.Frame(frame_add, bg=COLOR1)
    frame_add_input.place(relwidth=0.98, height=200, relx=0.02, rely=0.15, anchor='nw')

    label_add_cname = tk.Label(frame_add_input,
                               text='Card Name',
                               bg=COLOR1,
                               font=FONT_BODY,
                               foreground=TEXT_COLOR)
    label_add_cname.grid(column=0, row=0, padx=5, pady=5, sticky='w')

    label_add_sname = tk.Label(frame_add_input,
                               text='Set Name',
                               bg=COLOR1,
                               font=FONT_BODY,
                               foreground=TEXT_COLOR)
    label_add_sname.grid(column=0, row=1, padx=5, pady=5, sticky='w')

    label_add_sid = tk.Label(frame_add_input,
                             text='Set ID Number',
                             bg=COLOR1,
                             font=FONT_BODY,
                             foreground=TEXT_COLOR)
    label_add_sid.grid(column=0, row=2, padx=5, pady=5, sticky='w')

    label_add_rarity = tk.Label(frame_add_input,
                                text='Rarity',
                                bg=COLOR1,
                                font=FONT_BODY,
                                foreground=TEXT_COLOR)
    label_add_rarity.grid(column=3, row=0, padx=5, pady=5, sticky='w')

    label_add_foil = tk.Label(frame_add_input,
                              text='Foil?',
                              bg=COLOR1,
                              font=FONT_BODY,
                              foreground=TEXT_COLOR)
    label_add_foil.grid(column=3, row=1, padx=5, pady=5, sticky='w')

    entry_add_cname = tk.Entry(frame_add_input, textvariable=var_cardname, foreground='black')
    entry_add_cname.grid(column=1, row=0, padx=5, pady=5)

    entry_add_sname = tk.Entry(frame_add_input, textvariable=var_setname, foreground='black')
    entry_add_sname.grid(column=1, row=1, padx=5, pady=5)

    entry_add_sid = tk.Entry(frame_add_input, textvariable=var_setid, foreground='black')
    entry_add_sid.grid(column=1, row=2, padx=5, pady=5)

    frame_add_input_placeholder = tk.Frame(frame_add_input, bg=COLOR1)
    frame_add_input_placeholder.grid(column=2, row=0, padx=60)

    dropdown_add_rarity = tk.OptionMenu(frame_add_input, var_rarity, *RARITIES)
    dropdown_add_rarity.config(width=12)
    var_rarity.set(RARITIES[0])
    dropdown_add_rarity.grid(column=4, row=0, padx=10, pady=5, sticky='w')

    dropdown_add_foil = tk.OptionMenu(frame_add_input, var_foil, *FOIL)
    dropdown_add_foil.config(width=12)
    var_foil.set(FOIL[0])
    dropdown_add_foil.grid(column=4, row=1, padx=10, pady=5, sticky='w')

    button_add_aqueue = tk.Button(frame_add_input,
                                  text='Submit to Queue',
                                  bg=COLOR3,
                                  font=FONT_BODY,
                                  foreground=TEXT_COLOR,
                                  state='normal',
                                  command=add_queue)
    button_add_aqueue.place(relx=0.1, rely=0.7, anchor='nw')
    # End input

    # Start queue
    frame_add_queue = tk.Frame(frame_add, bg=COLOR2)
    frame_add_queue.place(width=1000, height=300, relx=0.02, rely=0.45, anchor='nw')

    tree_add_cards = ttk.Treeview(frame_add_queue)
    tree_add_cards['columns'] = COLUMNS_QUEUE

    tree_add_cards.column('#0', width=0, stretch='no')
    tree_add_cards.column('Card Name', width=50, minwidth=10)
    tree_add_cards.column('Set Name', width=50, minwidth=10)
    tree_add_cards.column('Set ID', width=50, minwidth=10)
    tree_add_cards.column('Rarity', width=50, minwidth=10)
    tree_add_cards.column('Foil?', width=10, minwidth=10)

    tree_add_cards.heading('Card Name', text='Card Name', anchor='w')
    tree_add_cards.heading('Set Name', text='Set Name', anchor='w')
    tree_add_cards.heading('Set ID', text='Set ID', anchor='w')
    tree_add_cards.heading('Rarity', text='Rarity', anchor='w')
    tree_add_cards.heading('Foil?', text='Foil?', anchor='w')

    tree_add_cards.place(relwidth=1, relheight=0.8, relx=0, rely=0, anchor='nw')

    frame_add_queue_buttons = tk.Frame(frame_add_queue, bg=COLOR2)
    frame_add_queue_buttons.place(relwidth=1, relheight=0.2, relx=0, rely=0.8, anchor='nw')

    button_add_submit = tk.Button(frame_add_queue_buttons,
                                  text='Submit Entries to DB',
                                  bg=COLOR3,
                                  font=FONT_BODY,
                                  foreground=TEXT_COLOR,
                                  state='normal')
    button_add_submit.grid(column=0, row=0, padx=10, pady=10)

    button_add_deleteone = tk.Button(frame_add_queue_buttons,
                                     text='Delete Entry',
                                     bg=COLOR3,
                                     font=FONT_BODY,
                                     foreground=TEXT_COLOR,
                                     state='normal',
                                     command=add_delete_entry)
    button_add_deleteone.grid(column=1, row=0, padx=10, pady=10)

    button_add_deleteall = tk.Button(frame_add_queue_buttons,
                                     text='Delete all Entries',
                                     bg=COLOR3,
                                     font=FONT_BODY,
                                     foreground=TEXT_COLOR,
                                     state='normal',
                                     command=add_delete_entries)
    button_add_deleteall.grid(column=2, row=0, padx=10, pady=10)
    # End queue

    # Start navigation
    frame_add_functions = tk.Frame(frame_add, bg=COLOR2)
    frame_add_functions.place(width=500, height=50, relx=0.02, rely=0.92, anchor='nw')

    button_add_overview = tk.Button(frame_add_functions,
                                    text='Overview Cards',
                                    font=FONT_BODY,
                                    bg=COLOR3,
                                    foreground=TEXT_COLOR,
                                    state='normal',
                                    command=switch_overview)
    button_add_overview.grid(column=0, row=0, padx=10)

    button_add_search = tk.Button(frame_add_functions,
                                  text='Search Cards',
                                  font=FONT_BODY,
                                  bg=COLOR3,
                                  foreground=TEXT_COLOR,
                                  state='normal',
                                  command=switch_search)
    button_add_search.grid(column=1, row=0, padx=10)

    button_add_add = tk.Button(frame_add_functions,
                               text='Add new Cards',
                               font=FONT_BODY,
                               bg=COLOR3,
                               foreground=TEXT_COLOR,
                               state='disabled',
                               command=switch_add)
    button_add_add.grid(column=2, row=0, padx=10)
    # End navigation


def switch_edit():

    def check_cname():
        if var_c_cardname.get() == 0:
            entry_edit_cname.config(state='disabled')
        else:
            entry_edit_cname.config(state='normal')

    def check_sname():
        if var_c_setname.get() == 0:
            entry_edit_sname.config(state='disabled')
        else:
            entry_edit_sname.config(state='normal')

    def check_sid():
        if var_c_setid.get() == 0:
            entry_edit_sid.config(state='disabled')
        else:
            entry_edit_sid.config(state='normal')

    def check_rarity():
        if var_c_rarity.get() == 0:
            dropdown_edit_rarity.config(state='disabled')
        else:
            dropdown_edit_rarity.config(state='normal')

    def check_foil():
        if var_c_foil.get() == 0:
            dropdown_edit_foil.config(state='disabled')
        else:
            dropdown_edit_foil.config(state='normal')

    frame_welcome.destroy()

    frame_edit = tk.Frame(frame, bg=COLOR2)
    frame_edit.place(relwidth=1, relheight=1)

    # Start header
    frame_edit_header = tk.Frame(frame_edit, bg=COLOR1)
    frame_edit_header.place(relwidth=0.98, height=60, relx=0.02, rely=0.05, anchor='nw')

    label_edit_header = tk.Label(frame_edit_header,
                                 text='Edit Card',
                                 bg=COLOR1,
                                 font=FONT_HEADLINE,
                                 foreground=TEXT_COLOR)
    label_edit_header.place(x=5, rely=0.5, anchor='w')
    # End edit Header

    # Start input
    frame_edit_input = tk.Frame(frame_edit, bg=COLOR1)
    frame_edit_input.place(relwidth=0.98, height=300, relx=0.02, rely=0.15, anchor='nw')

    label_edit_input_edit1 = tk.Label(frame_edit_input,
                                      text='Edit',
                                      bg=COLOR1,
                                      font=FONT_BODY,
                                      foreground=TEXT_COLOR)
    label_edit_input_edit1.grid(column=0, row=0, padx=5, pady=5)

    label_edit_input_edit2 = tk.Label(frame_edit_input,
                                      text='Edit',
                                      bg=COLOR1,
                                      font=FONT_BODY,
                                      foreground=TEXT_COLOR)
    label_edit_input_edit2.grid(column=4, row=0, padx=5, pady=5)

    label_edit_input_cname = tk.Label(frame_edit_input,
                                      text='Card Name',
                                      bg=COLOR1,
                                      font=FONT_BODY,
                                      foreground=TEXT_COLOR)
    label_edit_input_cname.grid(column=1, row=1, padx=5, pady=5, sticky='w')

    label_edit_input_sname = tk.Label(frame_edit_input,
                                      text='Set Name',
                                      bg=COLOR1,
                                      font=FONT_BODY,
                                      foreground=TEXT_COLOR)
    label_edit_input_sname.grid(column=1, row=2, padx=5, pady=5, sticky='w')

    label_edit_input_sid = tk.Label(frame_edit_input,
                                    text='Set ID',
                                    bg=COLOR1,
                                    font=FONT_BODY,
                                    foreground=TEXT_COLOR)
    label_edit_input_sid.grid(column=1, row=3, padx=5, pady=5, sticky='w')

    label_edit_input_rarity = tk.Label(frame_edit_input,
                                       text='Rarity',
                                       bg=COLOR1,
                                       font=FONT_BODY,
                                       foreground=TEXT_COLOR)
    label_edit_input_rarity.grid(column=5, row=1, padx=5, pady=5, sticky='w')

    label_edit_input_foil = tk.Label(frame_edit_input,
                                     text='Foil?',
                                     bg=COLOR1,
                                     font=FONT_BODY,
                                     foreground=TEXT_COLOR)
    label_edit_input_foil.grid(column=5, row=2, padx=5, pady=5, sticky='w')

    checkbox_edit_cname = tk.Checkbutton(frame_edit_input, bg=COLOR1, variable=var_c_cardname, command=check_cname)
    checkbox_edit_cname.grid(column=0, row=1)

    checkbox_edit_sname = tk.Checkbutton(frame_edit_input, bg=COLOR1, variable=var_c_setname, command=check_sname)
    checkbox_edit_sname.grid(column=0, row=2)

    checkbox_edit_sid = tk.Checkbutton(frame_edit_input, bg=COLOR1, variable=var_c_setid, command=check_sid)
    checkbox_edit_sid.grid(column=0, row=3)

    checkbox_edit_rarity = tk.Checkbutton(frame_edit_input, bg=COLOR1, variable=var_c_rarity, command=check_rarity)
    checkbox_edit_rarity.grid(column=4, row=1)

    checkbox_edit_foil = tk.Checkbutton(frame_edit_input, bg=COLOR1, variable=var_c_foil, command=check_foil)
    checkbox_edit_foil.grid(column=4, row=2)

    entry_edit_cname = tk.Entry(frame_edit_input, foreground='black', state='disabled', textvariable=var_cardname)
    entry_edit_cname.grid(column=2, row=1, padx=5, pady=5)

    entry_edit_sname = tk.Entry(frame_edit_input, foreground='black', state='disabled', textvariable=var_setname)
    entry_edit_sname.grid(column=2, row=2, padx=5, pady=5)

    entry_edit_sid = tk.Entry(frame_edit_input, foreground='black', state='disabled', textvariable=var_setid)
    entry_edit_sid.grid(column=2, row=3, padx=5, pady=5)

    frame_edit_input_placeholder = tk.Frame(frame_edit_input, bg=COLOR1)
    frame_edit_input_placeholder.grid(column=3, row=0, padx=60)

    dropdown_edit_rarity = tk.OptionMenu(frame_edit_input, var_rarity, *RARITIES)
    dropdown_edit_rarity.config(width=12, state='disabled')
    var_rarity.set(RARITIES[0])
    dropdown_edit_rarity.grid(column=6, row=1, padx=5, pady=5)

    dropdown_edit_foil = tk.OptionMenu(frame_edit_input, var_foil, *FOIL)
    dropdown_edit_foil.config(width=12, state='disabled')
    var_foil.set(FOIL[0])
    dropdown_edit_foil.grid(column=6, row=2, padx=5, pady=5)

    frame_edit_input_buttons = tk.Frame(frame_edit_input, bg=COLOR1)
    frame_edit_input_buttons.place(height=120, relwidth=1, relx=0, rely=1, anchor='sw')

    button_edit_commit = tk.Button(frame_edit_input_buttons,
                                   text='Submit Changes',
                                   bg=COLOR3,
                                   font=FONT_BODY,
                                   foreground=TEXT_COLOR,
                                   state='normal')
    button_edit_commit.grid(column=0, row=0, padx=10, pady=10, sticky='w')

    button_edit_reset = tk.Button(frame_edit_input_buttons,
                                  text='Reset',
                                  bg=COLOR3,
                                  font=FONT_BODY,
                                  foreground=TEXT_COLOR,
                                  state='normal')
    button_edit_reset.grid(column=1, row=0, padx=10, pady=10)

    button_edit_details = tk.Button(frame_edit_input_buttons,
                                    text='See Cards Details',
                                    bg=COLOR3,
                                    font=FONT_BODY,
                                    foreground=TEXT_COLOR,
                                    state='normal')
    button_edit_details.grid(column=0, row=1, padx=10, pady=10)
    # End Input

    # Start navigation
    frame_edit_functions = tk.Frame(frame_edit, bg=COLOR2)
    frame_edit_functions.place(width=500, height=50, relx=0.02, rely=0.92, anchor='nw')

    button_edit_overview = tk.Button(frame_edit_functions,
                                     text='Overview Cards',
                                     font=FONT_BODY,
                                     bg=COLOR3,
                                     foreground=TEXT_COLOR,
                                     state='normal',
                                     command=switch_overview)
    button_edit_overview.grid(column=0, row=0, padx=10)

    button_edit_search = tk.Button(frame_edit_functions,
                                   text='Search Cards',
                                   font=FONT_BODY,
                                   bg=COLOR3,
                                   foreground=TEXT_COLOR,
                                   state='normal',
                                   command=switch_search)
    button_edit_search.grid(column=1, row=0, padx=10)

    button_edit_add = tk.Button(frame_edit_functions,
                                text='Add new Cards',
                                font=FONT_BODY,
                                bg=COLOR3,
                                foreground=TEXT_COLOR,
                                state='normal',
                                command=switch_add)
    button_edit_add.grid(column=2, row=0, padx=10)
    # End navigation


def switch_detail(detail_id):

    print(detail_id)

    frame_welcome.destroy()

    frame_detail = tk.Frame(frame, bg=COLOR2)
    frame_detail.place(relwidth=1, relheight=1)

    # Get values from db
    mycursor = db.cursor()
    mycursor.execute('SELECT * FROM Cards WHERE Card_ID = %s' % detail_id)

    for x in mycursor:
        detail_value_cid = x[0]
        detail_value_cname = x[1]
        detail_value_sname = x[2]
        detail_value_sid = x[3]
        detail_value_rarity = x[4]
        detail_value_foil = x[5]
        detail_value_price = x[6]
        detail_value_cdate = x[7]
        detail_value_cuser = x[8]

    # Start detail head
    frame_detail_header = tk.Frame(frame_detail, bg=COLOR1)
    frame_detail_header.place(relwidth=0.98, height=60, relx=0.02, rely=0.05, anchor='nw')

    label_detail_header = tk.Label(frame_detail_header,
                                   text='Card Details: %s - "%s"' % (detail_value_cid, detail_value_cname),
                                   bg=COLOR1,
                                   font=FONT_HEADLINE,
                                   foreground=TEXT_COLOR)
    label_detail_header.place(relx=0, rely=0.5, anchor='w')
    # End detail header

    # Start Detail Labels
    frame_detail_details = tk.Frame(frame_detail, bg=COLOR1)
    frame_detail_details.place(relwidth=0.98, height=250, relx=0.02, rely=0.15, anchor='nw')

    label_detail_ident_dbid = tk.Label(frame_detail_details,
                                       text='Database ID',
                                       bg=COLOR1,
                                       font=FONT_BODY,
                                       foreground=TEXT_COLOR)
    label_detail_ident_dbid.grid(column=0, row=0, padx=5, pady=5, sticky='w')

    label_detail_ident_cname = tk.Label(frame_detail_details,
                                        text='Card Name',
                                        bg=COLOR1,
                                        font=FONT_BODY,
                                        foreground=TEXT_COLOR)
    label_detail_ident_cname.grid(column=0, row=1, padx=5, pady=5, sticky='w')

    label_detail_ident_sname = tk.Label(frame_detail_details,
                                        text='Set Name',
                                        bg=COLOR1,
                                        font=FONT_BODY,
                                        foreground=TEXT_COLOR)
    label_detail_ident_sname.grid(column=0, row=2, padx=5, pady=5, sticky='w')

    label_detail_ident_sid = tk.Label(frame_detail_details,
                                      text='Set ID',
                                      bg=COLOR1,
                                      font=FONT_BODY,
                                      foreground=TEXT_COLOR)
    label_detail_ident_sid.grid(column=0, row=3, padx=5, pady=5, sticky='w')

    label_detail_ident_rarity = tk.Label(frame_detail_details,
                                         text='Rarity',
                                         bg=COLOR1,
                                         font=FONT_BODY,
                                         foreground=TEXT_COLOR)
    label_detail_ident_rarity.grid(column=0, row=4, padx=5, pady=5, sticky='w')

    label_detail_ident_foil = tk.Label(frame_detail_details,
                                       text='Foil?',
                                       bg=COLOR1,
                                       font=FONT_BODY,
                                       foreground=TEXT_COLOR)
    label_detail_ident_foil.grid(column=0, row=5, padx=5, pady=5, sticky='w')

    label_detail_ident_date_added = tk.Label(frame_detail_details,
                                             text='Date added',
                                             bg=COLOR1,
                                             font=FONT_BODY,
                                             foreground=TEXT_COLOR)
    label_detail_ident_date_added.grid(column=3, row=0, padx=5, pady=5, sticky='w')

    label_detail_ident_added_by = tk.Label(frame_detail_details,
                                           text='Added by',
                                           bg=COLOR1,
                                           font=FONT_BODY,
                                           foreground=TEXT_COLOR)
    label_detail_ident_added_by.grid(column=3, row=1, padx=5, pady=5, sticky='w')

    label_detail_ident_date_changed = tk.Label(frame_detail_details,
                                               text='Date of Last Change',
                                               bg=COLOR1,
                                               font=FONT_BODY,
                                               foreground=TEXT_COLOR)
    label_detail_ident_date_changed.grid(column=3, row=2, padx=5, pady=5, sticky='w')

    label_detail_ident_changed_by = tk.Label(frame_detail_details,
                                             text='Changed by',
                                             bg=COLOR1,
                                             font=FONT_BODY,
                                             foreground=TEXT_COLOR)
    label_detail_ident_changed_by.grid(column=3, row=3, padx=5, pady=5, sticky='w')

    label_detail_ident_price_added = tk.Label(frame_detail_details,
                                              text='Price when added',
                                              bg=COLOR1,
                                              font=FONT_BODY,
                                              foreground=TEXT_COLOR)
    label_detail_ident_price_added.grid(column=6, row=0, padx=5, pady=5, sticky='w')

    label_detail_ident_price_current = tk.Label(frame_detail_details,
                                                text='Current Price',
                                                bg=COLOR1,
                                                font=FONT_BODY,
                                                foreground=TEXT_COLOR)
    label_detail_ident_price_current.grid(column=6, row=1, padx=5, pady=5, sticky='w')

    label_detail_ident_change_life = tk.Label(frame_detail_details,
                                              text='Price Change since added',
                                              bg=COLOR1,
                                              font=FONT_BODY,
                                              foreground=TEXT_COLOR)
    label_detail_ident_change_life.grid(column=6, row=2, padx=5, pady=5, sticky='w')

    label_detail_ident_change_recent = tk.Label(frame_detail_details,
                                                text='Price Change last 30 Days',
                                                bg=COLOR1,
                                                font=FONT_BODY,
                                                foreground=TEXT_COLOR)
    label_detail_ident_change_recent.grid(column=6, row=4, padx=5, pady=5, sticky='w')

    label_detail_unit_eur1 = tk.Label(frame_detail_details,
                                      text='€',
                                      bg=COLOR1,
                                      font=FONT_BODY,
                                      foreground=TEXT_COLOR)
    label_detail_unit_eur1.grid(column=8, row=0, padx=5, pady=5, sticky='w')

    label_detail_unit_eur2 = tk.Label(frame_detail_details,
                                      text='€',
                                      bg=COLOR1,
                                      font=FONT_BODY,
                                      foreground=TEXT_COLOR)
    label_detail_unit_eur2.grid(column=8, row=1, padx=5, pady=5, sticky='w')

    label_detail_unit_eur3 = tk.Label(frame_detail_details,
                                      text='€',
                                      bg=COLOR1,
                                      font=FONT_BODY,
                                      foreground=TEXT_COLOR)
    label_detail_unit_eur3.grid(column=8, row=2, padx=5, pady=5, sticky='w')

    label_detail_unit_eur4 = tk.Label(frame_detail_details,
                                      text='€',
                                      bg=COLOR1,
                                      font=FONT_BODY,
                                      foreground=TEXT_COLOR)
    label_detail_unit_eur4.grid(column=8, row=4, padx=5, pady=5, sticky='w')

    label_detail_unit_proz1 = tk.Label(frame_detail_details,
                                       text='%',
                                       bg=COLOR1,
                                       font=FONT_BODY,
                                       foreground=TEXT_COLOR)
    label_detail_unit_proz1.grid(column=8, row=3, padx=5, pady=5, sticky='w')

    label_detail_unit_proz2 = tk.Label(frame_detail_details,
                                       text='%',
                                       bg=COLOR1,
                                       font=FONT_BODY,
                                       foreground=TEXT_COLOR)
    label_detail_unit_proz2.grid(column=8, row=5, padx=5, pady=5, sticky='w')

    label_detail_value_dbid = tk.Label(frame_detail_details,
                                       bg=COLOR2,
                                       font=FONT_BODY,
                                       foreground=TEXT_COLOR)
    label_detail_value_dbid.grid(column=1, row=0, padx=5, pady=5, sticky='ew')

    label_detail_value_cname = tk.Label(frame_detail_details,
                                        bg=COLOR2,
                                        font=FONT_BODY,
                                        foreground=TEXT_COLOR)
    label_detail_value_cname.grid(column=1, row=1, padx=5, pady=5, sticky='ew')

    label_detail_value_sname = tk.Label(frame_detail_details,
                                        bg=COLOR2,
                                        font=FONT_BODY,
                                        foreground=TEXT_COLOR)
    label_detail_value_sname.grid(column=1, row=2, padx=5, pady=5, sticky='ew')

    label_detail_value_sid = tk.Label(frame_detail_details,
                                      bg=COLOR2,
                                      font=FONT_BODY,
                                      foreground=TEXT_COLOR)
    label_detail_value_sid.grid(column=1, row=3, padx=5, pady=5, sticky='ew')

    label_detail_value_rarity = tk.Label(frame_detail_details,
                                         bg=COLOR2,
                                         font=FONT_BODY,
                                         foreground=TEXT_COLOR)
    label_detail_value_rarity.grid(column=1, row=4, padx=5, pady=5, sticky='ew')

    label_detail_value_foil = tk.Label(frame_detail_details,
                                       bg=COLOR2,
                                       font=FONT_BODY,
                                       foreground=TEXT_COLOR)
    label_detail_value_foil.grid(column=1, row=5, padx=5, pady=5, sticky='ew')

    label_detail_value_date_added = tk.Label(frame_detail_details,
                                             bg=COLOR2,
                                             font=FONT_BODY,
                                             foreground=TEXT_COLOR)
    label_detail_value_date_added.grid(column=4, row=0, padx=5, pady=5, sticky='ew')

    label_detail_value_added_by = tk.Label(frame_detail_details,
                                           bg=COLOR2,
                                           font=FONT_BODY,
                                           foreground=TEXT_COLOR)
    label_detail_value_added_by.grid(column=4, row=1, padx=5, pady=5, sticky='ew')

    label_detail_value_date_changed = tk.Label(frame_detail_details,
                                               bg=COLOR2,
                                               font=FONT_BODY,
                                               foreground=TEXT_COLOR)
    label_detail_value_date_changed.grid(column=4, row=2, padx=5, pady=5, sticky='ew')

    label_detail_value_changed_by = tk.Label(frame_detail_details,
                                             bg=COLOR2,
                                             font=FONT_BODY,
                                             foreground=TEXT_COLOR)
    label_detail_value_changed_by.grid(column=4, row=3, padx=5, pady=5, sticky='ew')

    label_detail_value_price_added = tk.Label(frame_detail_details,
                                              bg=COLOR2,
                                              font=FONT_BODY,
                                              foreground=TEXT_COLOR)
    label_detail_value_price_added.grid(column=7, row=0, padx=5, pady=5, sticky='ew')

    label_detail_value_price_current = tk.Label(frame_detail_details,
                                                bg=COLOR2,
                                                font=FONT_BODY,
                                                foreground=TEXT_COLOR)
    label_detail_value_price_current.grid(column=7, row=1, padx=5, pady=5, sticky='ew')

    label_detail_value_change_life_eur = tk.Label(frame_detail_details,
                                                  bg=COLOR2,
                                                  font=FONT_BODY,
                                                  foreground=TEXT_COLOR)
    label_detail_value_change_life_eur.grid(column=7, row=2, padx=5, pady=5, sticky='ew')

    label_detail_value_change_life_proz = tk.Label(frame_detail_details,
                                                   bg=COLOR2,
                                                   font=FONT_BODY,
                                                   foreground=TEXT_COLOR)
    label_detail_value_change_life_proz.grid(column=7, row=3, padx=5, pady=5, sticky='ew')

    label_detail_value_change_recent_eur = tk.Label(frame_detail_details,
                                                    bg=COLOR2,
                                                    font=FONT_BODY,
                                                    foreground=TEXT_COLOR)
    label_detail_value_change_recent_eur.grid(column=7, row=4, padx=5, pady=5, sticky='ew')

    label_detail_value_change_recent_proz = tk.Label(frame_detail_details,
                                                     bg=COLOR2,
                                                     font=FONT_BODY,
                                                     foreground=TEXT_COLOR)
    label_detail_value_change_recent_proz.grid(column=7, row=5, padx=5, pady=5, sticky='ew')

    label_detail_value_dbid.config(text=detail_value_cid)
    label_detail_value_cname.config(text=detail_value_cname)
    label_detail_value_sname.config(text=detail_value_sname)
    label_detail_value_sid.config(text=detail_value_sid)
    label_detail_value_rarity.config(text=detail_value_rarity)
    label_detail_value_foil.config(text=detail_value_foil)

    label_detail_value_date_added.config(text=detail_value_cdate)
    label_detail_value_added_by.config(text=detail_value_cuser)
    label_detail_value_date_changed.config(text='test')
    label_detail_value_changed_by.config(text='test')

    label_detail_value_price_added.config(text='test')
    label_detail_value_price_current.config(text=detail_value_price)
    label_detail_value_change_life_eur.config(text='test')
    label_detail_value_change_life_proz.config(text='test')
    label_detail_value_change_recent_eur.config(text='test')
    label_detail_value_change_recent_proz.config(text='test')

    frame_detail_details_1 = tk.Frame(frame_detail_details, bg=COLOR1)
    frame_detail_details_1.grid(column=2, row=0, ipadx=10)

    frame_detail_details_2 = tk.Frame(frame_detail_details, bg=COLOR1)
    frame_detail_details_2.grid(column=5, row=0, ipadx=10)

    frame_detail_details_5 = tk.Frame(frame_detail_details, bg=COLOR1)
    frame_detail_details_5.grid(column=1, row=6, ipadx=170)

    frame_detail_details_4 = tk.Frame(frame_detail_details, bg=COLOR1)
    frame_detail_details_4.grid(column=4, row=6, ipadx=70)

    frame_detail_details_5 = tk.Frame(frame_detail_details, bg=COLOR1)
    frame_detail_details_5.grid(column=7, row=6, ipadx=32)
    # End details label

    # Start navigation
    frame_detail_functions = tk.Frame(frame_detail, bg=COLOR2)
    frame_detail_functions.place(width=500, height=50, relx=0.02, rely=0.92, anchor='nw')

    button_detail_overview = tk.Button(frame_detail_functions,
                                       text='Overview Cards',
                                       font=FONT_BODY,
                                       bg=COLOR3,
                                       foreground=TEXT_COLOR,
                                       state='normal',
                                       command=switch_overview)
    button_detail_overview.grid(column=0, row=0, padx=10)

    button_detail_search = tk.Button(frame_detail_functions,
                                     text='Search Cards',
                                     font=FONT_BODY,
                                     bg=COLOR3,
                                     foreground=TEXT_COLOR,
                                     state='normal',
                                     command=switch_search)
    button_detail_search.grid(column=1, row=0, padx=10)

    button_detail_add = tk.Button(frame_detail_functions,
                                  text='Add new Cards',
                                  font=FONT_BODY,
                                  bg=COLOR3,
                                  foreground=TEXT_COLOR,
                                  state='normal',
                                  command=switch_add)
    button_detail_add.grid(column=2, row=0, padx=10)
    # End navigation


def login():
    user_name_temp = user_name.get()
    mycursor = db.cursor()
    mycursor.execute('SELECT pw_hash FROM Users WHERE login_name = %s', (user_name_temp, ))
    pw_value = mycursor.fetchone()

    if True:  # pw_value is not None:
        if True:  # pw_value[0] == hashlib.sha1(password.get().encode('ascii')).hexdigest():
            button_welcome_search.config(state='normal')
            button_welcome_overview.config(state='normal')
            button_welcome_add.config(state='normal')

            label_login_fail.grid_forget()
            label_login_no_user.grid_forget()

            entry_login_name.config(state='disabled')
            entry_login_pw.config(state='disabled')
            button_login.config(state='disabled')
        else:
            label_login_fail.grid(column=3, row=1, padx=10)
            label_login_no_user.grid_forget()
    else:
        label_login_no_user.grid(column=3, row=0, padx=10)
        label_login_fail.grid_forget()


# Start for welcome page
frame_welcome = tk.Frame(frame, bg=COLOR2)
frame_welcome.place(relheight=1, relwidth=1)

# Start for welcome text
frame_welcome_text = tk.Frame(frame_welcome, bg=COLOR1)
frame_welcome_text.place(relwidth=0.98, height=110, relx=0.02, rely=0.05, anchor='nw')

label_headline_welcome = tk.Label(frame_welcome_text,
                                  text='Welcome',
                                  foreground=TEXT_COLOR,
                                  bg=COLOR1,
                                  font=FONT_HEADLINE)
label_headline_welcome.grid(column=0, row=0, sticky='nw')

label_body_welcome = tk.Label(frame_welcome_text,
                              text='Welcome to my little presentation of a SQL-Database for \n'
                                   'Magic the Gathering Cards',
                              foreground=TEXT_COLOR,
                              bg=COLOR1,
                              font=FONT_BODY,
                              justify=tk.LEFT)
label_body_welcome.grid(column=0, row=1, sticky='nw')
# End for welcome text

# Start for welcome login
frame_welcome_login = tk.Frame(frame_welcome, bg=COLOR1)
frame_welcome_login.place(relwidth=0.98, height=135, relx=0.02, rely=0.3, anchor='nw')

label_login_name = tk.Label(frame_welcome_login, text='Username:', font=FONT_BODY, foreground=TEXT_COLOR, bg=COLOR1)
label_login_name.grid(column=0, row=0, pady=10)

label_login_pw = tk.Label(frame_welcome_login, text='Password:', fon=FONT_BODY, foreground=TEXT_COLOR, bg=COLOR1)
label_login_pw.grid(column=0, row=1)

entry_login_name = tk.Entry(frame_welcome_login, textvariable=user_name, fg='black')
entry_login_name.grid(column=1, row=0, ipadx=20, padx=10)

entry_login_pw = tk.Entry(frame_welcome_login, textvariable=password, fg='black', show='*')
entry_login_pw.grid(column=1, row=1, ipadx=20, padx=10)

frame_welcome_login_placeholder = tk.Frame(frame_welcome_login, bg=COLOR1)
frame_welcome_login_placeholder.grid(column=2, row=0, ipadx=20)

label_login_fail = tk.Label(frame_welcome_login,
                            text='Wrong password. Please try again.',
                            bg=COLOR1,
                            font=FONT_BODY,
                            foreground='red')

label_login_no_user = tk.Label(frame_welcome_login,
                               text='User could not be found. Try again',
                               bg=COLOR1,
                               font=FONT_BODY,
                               foreground='red')

button_login = tk.Button(frame_welcome_login,
                         text='Login',
                         font=FONT_BODY,
                         bg=COLOR3,
                         foreground=TEXT_COLOR,
                         command=login)
button_login.grid(column=0, row=2, pady=10)
# End Login Frame

# Start Functions Frame
frame_welcome_functions = tk.Frame(frame_welcome, bg=COLOR2)
frame_welcome_functions.place(width=500, height=50, relx=0.02, rely=0.92, anchor='nw')

button_welcome_overview = tk.Button(frame_welcome_functions,
                                    text='Overview Cards',
                                    font=FONT_BODY,
                                    bg=COLOR3,
                                    foreground=TEXT_COLOR,
                                    state='disabled',
                                    command=switch_overview)
button_welcome_overview.grid(column=0, row=0, padx=10)


button_welcome_search = tk.Button(frame_welcome_functions,
                                  text='Search Cards',
                                  font=FONT_BODY,
                                  bg=COLOR3,
                                  foreground=TEXT_COLOR,
                                  state='disabled',
                                  command=switch_search)
button_welcome_search.grid(column=1, row=0, padx=10)

button_welcome_add = tk.Button(frame_welcome_functions,
                               text='Add new Cards',
                               font=FONT_BODY,
                               bg=COLOR3,
                               foreground=TEXT_COLOR,
                               state='disabled',
                               command=switch_add)
button_welcome_add.grid(column=2, row=0, padx=10)


root.mainloop()
