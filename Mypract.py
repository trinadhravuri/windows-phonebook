from tkinter import *
from tkinter import ttk
import sqlite3

class MyContacts:


    def __init__(self, root):
        self.root = root
        #self.Connection()
        #self.Add_Contact()
        #self.display()
        self.Label_Frame()
        self.Create_logo()
        self.Create_tree_view()
        self.Create_scrollbar()
        self.Create_bottom_buttons()
        self.Create_message_display()
        ttk_style = ttk.Style()
        ttk_style.configure("Treeview", font=('helvetica', 10))
        ttk_style.configure("Treeview.Heading", font=('helvetica', 12, 'bold'))

    def Connection(self,query, parameters = ()):
        with sqlite3.connect('C:\sqlite\contacts.db') as con:
            print("successfully connected to database")
            cur = con.cursor()
            res = cur.execute(query, parameters)
            con.commit()
        return res
            #for i in res:
                #print(i)

    def Create_logo(self):
        photo = PhotoImage(file='contacts1.png')
        label =Label(image= photo)
        label.image = photo
        label.grid(row=0, column=0)

    def Label_Frame(self):
        labelframe = LabelFrame(self.root, text='Create New Contact', bg='sky blue')
        labelframe.grid(row=0, column=1, sticky='ew')
        Label(labelframe, text='Name',bg='green', fg='white').grid(row=2, column=1, sticky=W, padx=5, pady=5)
        self.namefield = Entry(labelframe)
        self.namefield.grid(row=2, column=2, sticky=W, padx=5, pady=5)
        Label(labelframe, text='Email', bg='pink', fg='white').grid(row=3, column=1, sticky=W, padx=5, pady=5)
        self.emailfield = Entry(labelframe)
        self.emailfield.grid(row=3, column=2, sticky=W, padx=5, pady=5)
        Label(labelframe, text='Number', bg='yellow', fg='white').grid(row=4, column=1, sticky=W, padx=5, pady=5)
        self.numfield = Entry(labelframe)
        self.numfield.grid(row=4, column=2, sticky=W, padx=5, pady=5)
        Button(labelframe, text='Add Contact', command=self.Add_Contact, bg='black', fg='White').grid(row=5, column=2, sticky=E, pady=10, padx=10)

    def Create_message_display(self):
        self.message_label = Label(text='', fg='red')
        self.message_label.grid(row=3, column=1, sticky=W)

    def Create_tree_view(self):
        self.tree = ttk.Treeview(height=10, columns=('email', 'number'), style="Treeview")
        self.tree.grid(row=6, column=0, columnspan=3)
        self.tree.heading('#0', text='Name', anchor=CENTER)
        self.tree.heading('#1', text='Email', anchor=CENTER)
        self.tree.heading('#2', text='Number', anchor=CENTER)

    def Create_scrollbar(self):
        self.scrollbar = Scrollbar(orient='vertical', command=self.tree.yview)
        self.scrollbar.grid(row=6, column=3, rowspan=10, sticky='sn')

    def labes_display(self):
        print(self.namefield.get())
        print(self.emailfield.get())
        print(self.numfield.get())

    def OnAddContactButtonClicked(self):
        self.Add_Contact()

    def Add_Contact(self):
        if self.NewContactsValidated():
            query = "INSERT INTO contacts_list VALUES(NULL,?,?,?)"
            parameters = (self.namefield.get(), self.emailfield.get(), self.numfield.get())
            #name = input('enter name : ')
            #email = input('enter email :')
            #number = input('enter number : ')
            #query = "INSERT INTO contacts_list(name, email, number) VALUES('sree','vyshu@gmail.com',9553417757)"
            self.Connection(query, parameters)
            self.message_label['text'] = 'New contact {} added '.format(self.namefield.get())
            self.namefield.delete(0,END)
            self.emailfield.delete(0, END)
            self.numfield.delete(0, END)
            self.display()
        else:
            self.message_label['text'] = 'name,email,number cannot be blank'
            self.display()

    def NewContactsValidated(self):
        return len(self.namefield.get()) != 0 and len(self.emailfield.get()) !=0 and len(self.numfield.get()) != 0

    def display(self):
        items = self.tree.get_children()
        for item in items:
            self.tree.delete(item)
        query = "SELECT * FROM contacts_list ORDER BY name desc"
        contact_entries = self.Connection(query)
        for row in contact_entries:
            self.tree.insert('',0,text=row[1], values=(row[2],row[3]))

    def Create_bottom_buttons(self):
        Button(text='Delete Selected', command=self.No_item_delete, bg='pink', fg='black').grid(row=8, column=0, sticky=E, padx=10, pady=10)
        Button(text='Edit Selected', command=self.No_edit_contact, bg='sky blue', fg='black').grid(row=8, column=2, sticky=W)

    def Delete_contact(self):
        self.message_label['text'] = ''
        name = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM contacts_list WHERE name = ?'
        self.Connection(query,(name,))
        self.message_label['text'] = "{} contact deleted".format(name)
        self.display()

    def No_item_delete(self):
        self.message_label['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message_label['text'] = 'No Item Selected to delete'
            return
        self.Delete_contact()

    def Edit_contact(self):
        name = self.tree.item(self.tree.selection())['text']
        old_number = self.tree.item(self.tree.selection())['values'][1]
        self.transient = Toplevel()
        self.transient.title('update contact')
        Label(self.transient, text='Name').grid(row=0, column=1)
        Entry(self.transient, textvariable=StringVar(self.transient, value=name),state='readonly').grid(row=0, column=2)

        Label(self.transient, text='Old contact number').grid(row=1, column=1)
        Entry(self.transient, textvariable=StringVar(self.transient, value=old_number), state='readonly').grid(row=1,
                                                                                                         column=2)
        Label(self.transient, text='New Phone number:').grid(row=2, column=1)
        new_phone_number_entry_widget = Entry(self.transient)
        new_phone_number_entry_widget.grid(row=2, column=2)

        Button(self.transient, text='update contact', command=lambda : self.Update_contact(
            new_phone_number_entry_widget.get(), old_number,name)).grid(row=3, column=1)
        self.transient.mainloop()

    def Update_contact(self, new_phone, old_phone, name):
        query = 'UPDATE contacts_list SET number = ? WHERE number =? and name = ?'
        parameters = (new_phone, old_phone, name)
        self.Connection(query,parameters)
        self.transient.destroy()
        self.message_label['text'] = 'Phone number of {} modified'.format(name)
        self.display()

    def No_edit_contact(self):
        self.message_label['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message_label['text'] = 'No item selected to EDIT'
            return
        self.Edit_contact()
if __name__ == '__main__':
    root = Tk()
    root.title('My Contacts')
    app = MyContacts(root)
    root.mainloop()