import db
import re
import time
import tkinter as tk
from datetime import datetime, timedelta
from tkcalendar import Calendar, DateEntry
from tkinter import font


# # global variables ------------------------------------------------------------

# user_is_pro = bool()
# userdata = list()
# next_lesson = list()
# lesson_pro = list()

# custom Tk classes -----------------------------------------------------------

class Button(tk.Button):
  def __init__(self, cnf={}, **kw):
    super().__init__(cnf, **kw)
    self.config(bg="#0a1b40", fg="white")


class Entry(tk.Entry):
  def __init__(self, master=None, cnf={}, **kw):
    super().__init__(master, cnf, **kw)
    # Select/deselect entry text when widget gains/loses focus
    self.bind('<FocusIn>', lambda x: self.selection_range(0, tk.END))
    self.bind('<FocusOut>', lambda x: self.select_clear())


class Frame(tk.Frame):
  def __init__(self, master=None, display_logo=True): # this creates the logo to go in the corner of each page
    super().__init__(master)
    self.config(bg="#0a1b40")
    if display_logo:
      self.logo_image = tk.PhotoImage(file='images/cornerlogo.png')
      self.logo_label = tk.Label(self, image=self.logo_image, border=0)
      self.logo_label.image = self.logo_image
      self.logo_label.place(x=0, y=0)


class Label(tk.Label):
  def __init__(self, cnf={}, **kw):
    super().__init__(cnf, **kw)
    self.config(bg="#0a1b40", fg="white")


class Toplevel(tk.Toplevel):
  def __init__(self):
    super().__init__()
    self.config(bg="#0a1b40")
    self.grab_set()
  
  def destroy(self):
    self.grab_release()
    super().destroy()


# application classes ---------------------------------------------------------

class Login(tk.Frame):

  global user_is_pro
  global userdata

  def __init__(self, master):
    super().__init__()
    self.master = master
    self.master.title('Login') #This titles the window
    self.master.geometry('435x250') #This creates a window to the correct dimensions
    self.config(bg="#0a1b40") ##273747  #0a1b40
    self.pack(fill=tk.BOTH, expand=1)

    #self.email = tk.StringVar(self, 'pro@user.com')
    self.email = tk.StringVar(self, 'client01@user.com')
    self.password = tk.StringVar(self, '123')

    self.logo_image = tk.PhotoImage(file='images/logo.png') #loads the logo so it can be placed in the window
    self.logo_label = tk.Label(self, image=self.logo_image, border=0) #This puts the image into the label widget
    self.logo_label.image = self.logo_image
    self.logo_label.place(x=145, y=15) #places the logo in the centre of the page

    Entry(self, textvariable=self.email, width=22).place(x=150, y=85) #This creates a username entry box
    Entry(self, show='*', textvariable=self.password, width=22).place(x=150, y=105) #This creates a password entry box
    
    self.btn_login = tk.Button(self, text='Login', background = "#0a1b40", foreground = "white", command=self.authorise_user, width=6)
    self.btn_login.place(x=150 , y=145 ) #this creates a confirm button
    self.client_search_button_01 = tk.Button(self, text='Register', background = "#0a1b40", foreground = "white", command=self.register_user, width=6)
    self.client_search_button_01.place(x=235, y=145)

  def authorise_user(self): #This function will authorise the user
    authorised = False
    user = db.get_login_data(self.master.cur, self.email.get())
    if user != []: # username matches an entry in the db
      if self.password.get() == user[1]: # check the passwords match
        print('User authorised')
        if user[3] != None:  # ProID field not null, therefore user is a pro
          user_is_pro = True
          # set userdata to pro table lookup
          userdata = db.get_pro_data(self.master.cur, user[3]) # cursor and pro id
          Overview_Pro(self.master)
        else:
          user_is_pro = False
          # set userdata to cient table lookup
          userdata = db.get_client_data(self.master.cur, user[2]) # cursor and client id
          Overview_Client(self.master)
        self.destroy() # this closes the login window
        authorised = True
    if not authorised:
        print('User not authorised')
  
  def register_user(self):
    Register(self.master).grab_set()
    # self.client_search_button_01.config(state=tk.DISABLED)
    # self.btn_login.config(state=tk.DISABLED)
    # self.destroy()


class Register(Toplevel):

  def __init__(self, master): #, parent):
    super().__init__()
    self.master = master
    # self.parent = parent
    self.title('Registration')
    self.geometry('250x450')
    # self.configure(background = "#0a1b40")
    # self.pack(fill=tk.BOTH, expand=1)

    #These assign the text for the input boxes as a variable
    self.var_01 = tk.StringVar(self, 'client@client.com') 
    self.var_02 = tk.StringVar(self, 'Password')
    self.var_03 = tk.StringVar(self, 'Confirm Password')
    self.var_04 = tk.StringVar(self, 'First Name')
    self.var_05 = tk.StringVar(self, 'Surname')
    self.var_06 = tk.StringVar(self, 'Address Line 1')
    self.var_07 = tk.StringVar(self, 'Address Line 2')
    self.var_08 = tk.StringVar(self, 'City')
    self.var_09 = tk.StringVar(self, 'County')
    self.var_10 = tk.StringVar(self, 'Post Code')
    self.var_11 = tk.StringVar(self, 'Phone')
    self.var_12 = tk.StringVar(self, 'Handicap')
    self.var_13 = tk.StringVar(self, 'Dominant Hand')
    self.var_14 = tk.StringVar(self, 'Injuries')
    self.var_15 = tk.StringVar(self, 'Restrictions')

    #These create input boxes for the different information and place it in the correct positions
    Entry(self, textvariable=self.var_01).grid(row=1,  column=1, columnspan=2)
    Entry(self, textvariable=self.var_02).grid(row=2,  column=1, columnspan=2)
    Entry(self, textvariable=self.var_03).grid(row=3,  column=1, columnspan=2)
    Entry(self, textvariable=self.var_04).grid(row=4,  column=1, columnspan=2)
    Entry(self, textvariable=self.var_05).grid(row=5,  column=1, columnspan=2)
    Entry(self, textvariable=self.var_06).grid(row=6,  column=1, columnspan=2)
    Entry(self, textvariable=self.var_07).grid(row=7,  column=1, columnspan=2)
    Entry(self, textvariable=self.var_08).grid(row=8,  column=1, columnspan=2)
    Entry(self, textvariable=self.var_09).grid(row=9,  column=1, columnspan=2)
    Entry(self, textvariable=self.var_10).grid(row=10, column=1, columnspan=2)
    Entry(self, textvariable=self.var_11).grid(row=11, column=1, columnspan=2)
    Entry(self, textvariable=self.var_12).grid(row=12, column=1, columnspan=2)
    Entry(self, textvariable=self.var_13).grid(row=13, column=1, columnspan=2)
    Entry(self, textvariable=self.var_14).grid(row=14, column=1, columnspan=2)
    Entry(self, textvariable=self.var_15).grid(row=15, column=1, columnspan=2)

    tk.Button(self, text="Cancel", background="#0a1b40", foreground="white", command=self.cancel, width=7).grid(row=17, column=2, pady=20)
    tk.Button(self, text="Register", background="#0a1b40", foreground="white", command=self.register, width=7).grid(row=17, column=1, pady=20)
    
    self.grid_columnconfigure(0, minsize=25)
    self.grid_columnconfigure(1, minsize=100)
    self.grid_columnconfigure(2, minsize=100)
    self.grid_columnconfigure(3, minsize=25)
    self.grid_rowconfigure(0, minsize=20)

  # class methods ----------------------------------------------------------------

  def cancel(self):
    """ """
    self.destroy()


  def register(self): 
    """ """
    # validate email address
    if is_valid_email(self.var_01.get()):
      # check username doesn't exist
      if db.get_login_data(self.master.cur, self.var_01.get()) == []: # user doesn't exist
        # check password and confirm passwords matches
        if self.var_02.get() == self.var_03.get():
          # validate the other fields
          # - min no of chars
          # generate client id (auto-increment)
          client_id = db.get_max_client_id(self.master.cur)
          client_id += 1
          # update logins and clients tables
          db.store_regdata_client(self.master.con, self.master.cur, [
            client_id,
            self.var_01.get(),              # email
            self.var_02.get(),              # password
            self.var_04.get().title(),      # first name
            self.var_05.get().title(),      # surname
            self.var_06.get().title(),      # address line 1
            self.var_07.get().title(),      # address line 2
            self.var_08.get().title(),      # city
            self.var_09.get().title(),      # county
            self.var_10.get().upper(),      # post code
            self.var_11.get(),              # phone
            self.var_12.get(),              # handicap
            self.var_13.get().capitalize(), # dominant hand
            self.var_14.get().capitalize(), # injuries
            self.var_15.get().capitalize()  # restrictions
          ])
          self.destroy()
        else:
          print('Passwords don\'t match')
          # popup(self, "Passwords don't match")
      else:
        print('Username already exists')


  def destroy(self):
    self.grab_release()
    super().destroy()


class Overview_Client(Frame):
  
  global userdata

  def __init__(self, master):
    super().__init__()
    master.title("Overview")
    master.geometry("425x360")
    self.pack(fill=tk.BOTH, expand=1)

    self.booking_slots = list()
    self.booking_slot_details = list()
    self.client_id = userdata[0]
    self.master = master

    self.populate_booking_slots()

    self.welcome_message = tk.StringVar(self, "Welcome, " + userdata[1])

    Button(self, text="Book Now!", command=self.book_new_lesson).grid(row=8, column=3, sticky="E")
    Label(self, textvariable=self.welcome_message).grid(row=0, column=1, columnspan=2)
    Label(self, text="Here are your next 5 bookings:").grid(row=1, column=1, columnspan=2)
    Label(self, text="""Please note:
    cancellations within 24 hours 
    of the lesson are chargeable""", background = "#0a1b40", fg="White").grid(row=8 , column=0, columnspan=2)


    # configure grid
    self.grid_columnconfigure(0, minsize="100")
    self.grid_columnconfigure(1, minsize="100")
    self.grid_columnconfigure(2, minsize="100")
    self.grid_columnconfigure(3, minsize="100")
    self.grid_columnconfigure(4, minsize="100")
    self.grid_rowconfigure(0, minsize="50")
    self.grid_rowconfigure(1, minsize="50")
    self.grid_rowconfigure(2, minsize="30")
    self.grid_rowconfigure(3, minsize="30")
    self.grid_rowconfigure(4, minsize="30")
    self.grid_rowconfigure(5, minsize="30")
    self.grid_rowconfigure(6, minsize="30")
    self.grid_rowconfigure(7, minsize="50")
    self.grid_rowconfigure(8, minsize="50")


  # class methods
  def book_new_lesson(self):
    CalendarMonth(self.master)
    self.destroy()


  def populate_booking_slots(self):

    # clear booking slots
    for button in self.booking_slots:
      button.destroy()
    self.booking_slots = list()
    self.booking_slot_details = list()

    # get bookings from db
    bookings_data = db.get_bookings_data_client(self.master.cur, self.client_id)

    # sort bookings data by datetime (ascending)
    bookings_data.sort(key=lambda x: x[2])

    # get the next 5 bookings
    current_datetime = datetime.now()
    self.upcoming_lessons = []
    for booking in bookings_data:
      booking_datetime_obj = datetime.strptime(booking[2], '%Y-%m-%d %H:%M:%S')
      if booking_datetime_obj >= current_datetime:
        self.upcoming_lessons.append((booking[1], booking_datetime_obj))  # booking[1] -> pro_id
    self.upcoming_lessons = self.upcoming_lessons[:5]

    # create n buttons based on number of bookings
    for i in range(len(self.upcoming_lessons)):
      # populate booking slot details
      button_text = self.upcoming_lessons[i][1].strftime("%a, %e %b %Y @ %H:%M")
      self.booking_slot_details.append(
        [
          tk.StringVar(self, button_text),  # button text
          self.upcoming_lessons[i][0],      # pro id
          self.upcoming_lessons[i][1]       # booking date
        ]
      )
      # create button widgets
      self.booking_slots.append(
        Button(
          self, 
          textvariable=self.booking_slot_details[i][0],
          command=lambda i=i: self.select_booking_slot(i)
        )
      )
      self.booking_slots[i].grid(row=2 + i, column=1, columnspan=2, sticky="NEWS")


  def select_booking_slot(self, btn_index):
    """ """
    BookingEntry(
      self, 
      self.master,
      tk.StringVar(self, self.client_id),                           # client id
      tk.StringVar(self, self.booking_slot_details[btn_index][1]),  # pro id
      self.booking_slot_details[btn_index][2],                      # booking datetime obj
      False                                                         # slot is available
    )#.grab_set()


class Overview_Pro(Frame):

  def __init__(self, master):
    super().__init__()
    self.master = master
    self.master.title('Overview')
    self.master.geometry('440x250')
    self.configure(background = "#0a1b40")
    self.pack(fill=tk.BOTH, expand=1)

    self.welcome = tk.StringVar(self, "Welcome, " + userdata[1] + " " + userdata[2] + "!") # user's first name and surname
        
    tk.Label(self, textvariable=self.welcome, background = "#0a1b40", fg="white").grid(row=0, column=1, columnspan=3) #This label greets the pro
    Button(self, text="View Month", width=25, command=self.view_month).grid(row=2, column=1)    #place(x=25, y=125) #this button allows the pro to go to the main calendar
    Button(self, text="View Today", width=25, command=self.view_day).grid(row=2, column=3)    #place(x=300, y=125) #this button allows the pro to go and add a booking to their calendar
    Button(self, text="Add Pro User", width=25, command=self.add_pro).grid(row=4, column=1)   #place(x=150, y=175)
    Button(self, text="Remove Pro", width=25, command=self.remove_pro).grid(row=4, column=3)

    self.grid_rowconfigure(1, minsize=75)
    self.grid_rowconfigure(3, minsize=25)
    self.grid_columnconfigure(0, minsize=25)
    self.grid_columnconfigure(1, minsize=50)
    self.grid_columnconfigure(2, minsize=25) #spacer
    self.grid_columnconfigure(3, minsize=50)
    self.grid_columnconfigure(4, minsize=25)
  

  def add_pro(self):
    AddPro(self.master)


  def remove_pro(self):
    RemovePro(self.master)


  def view_month(self):
    CalendarMonth(self.master)
    self.destroy()


  def view_day(self):
    CalendarDay(self.master, datetime.today().date())
    self.destroy()

class CalendarMonth(Frame):

  def __init__(self, master):
    super().__init__()
    self.master = master
    self.master.title('Calendar')
    self.master.geometry('500x325')
    self.configure(background = "#0a1b40")
    self.pack(fill=tk.BOTH, expand=1)

    self.cal = Calendar(self,
                   font="Arial 14",
                   selectmode='day',
                   locale='en_US',
                  #These statements customise the look of the calendar
                   background="#0a1b40",
                   foreground="White",
                   selectbackground="Black",
                   selectforeground="White",
                   weekendbackground="White",
                   weekendforeground="Black",
                   disabledforeground='red',
                   othermonthbackground="light grey",
                   othermonthwebackground="light grey",
                   cursor="hand1",
                   year=datetime.today().year,
                   month=datetime.today().month,
                   day=datetime.today().day)
    self.cal.pack(fill=tk.BOTH, expand=1) 
  
    tk.Button(self, text="Select Date", bg="#0a1b40", fg="white", command=self.print_sel).pack()

  def print_sel(self):
    # self.cal.see(datetime.today())
    date_ = self.cal.selection_get()
    CalendarDay(self.master, date_)
    self.destroy()


class CalendarDay(Frame):

  global userdata
  global user_is_pro
  
  def __init__(self, master, date_obj):
    super().__init__()
    master.title('Day Calendar')
    master.geometry('575x700')
    self.configure(background="#0a1b40")
    self.pack(fill=tk.BOTH, expand=1)

    # class attributes --------------------------------------------------------
    self.available_pros = dict()
    self.booking_slots = list()
    self.booking_slot_details = list()
    self.date_obj = date_obj
    self.date_str = date_obj.strftime("%A, %d %B %Y")
    self.master = master
    self.selected_pro_id = tk.StringVar(self, "")
    self.selected_pro_name = tk.StringVar(self, "Please select a pro") # change initial value to specific pro?
    self.time_labels = list()

    # create widgets ----------------------------------------------------------
    main_label = tk.Label(self, background="#0a1b40", text=f"Bookings for {self.date_str}", fg="white") # Shows the day that the times displayed are for
    self.generate_available_pro_list()
    self.pro_selector = tk.OptionMenu(self, self.selected_pro_name, *self.available_pros.values(), command=self.select_pro)
    self.generate_time_labels_and_booking_slots()
    return_button = Button(self, text="Return to Welcome Page", command=self.return_to_overview)

    # configure widgets -------------------------------------------------------
    self.pro_selector.config(bg="#0a1b40", fg="White", width=16, anchor="w")
    # configure booking slot buttons to pass their index number to the booking slot selection method
    for i in range(len(self.booking_slots)):
      self.booking_slots[i].configure(command=lambda i=i: self.select_booking_slot(i))
      """The i=i trick causes your function to store the current value of i at 
         the time the lambda function is defined, instead of waiting to look up
         the value of i later. 
         Ref.: BrenBarn, Stack Overflow (https://stackoverflow.com/a/10865170)"""
    
    # place widgets -----------------------------------------------------------
    main_label.grid(row=0, rowspan=2, column=3, columnspan=5)
    self.pro_selector.grid(row=3, column=0, columnspan=1)
    for i in range(len(self.time_labels)):
      self.time_labels[i].grid(row=i + 3, column=1)
      self.booking_slots[i].grid(row=i + 3, column=3, columnspan=5, sticky="NEWS")
    return_button.grid(row=27, column=4, columnspan=3)

    # configure grid ----------------------------------------------------------
    self.grid_columnconfigure(0, minsize=225)
    self.grid_columnconfigure(1, minsize=50)
    self.grid_columnconfigure(2, minsize=10) # spacer
    self.grid_columnconfigure(3, minsize=50)
    self.grid_columnconfigure(4, minsize=50)
    self.grid_columnconfigure(5, minsize=50)
    self.grid_columnconfigure(6, minsize=50)
    self.grid_columnconfigure(7, minsize=50)
    self.grid_columnconfigure(8, minsize=200)
    self.grid_rowconfigure(0, minsize=20)
    self.grid_rowconfigure(1, minsize=20)    


  # class methods -------------------------------------------------------------
  
  def generate_available_pro_list(self):
    """ """
    # get list of all pro records from database
    pro_data = db.get_pro_data_all(self.master.cur)
    # compile list of available pros for option menu
    for i in range(0, len(pro_data)):
      if pro_data[i][4] == 1: # if pro is active
        pro_id = pro_data[i][0]
        pro_name = pro_data[i][1] + " " + pro_data[i][2] # concatenate first name and surname fields
        self.available_pros[pro_id] = pro_name # map name to ID
  

  def generate_time_labels_and_booking_slots(self):
    """ """
    time_ = datetime.strptime("09:00", "%H:%M") # earliest booking time is 9:00am
    for i in range(24): # 24 half hour slots over 12 hours
      self.booking_slot_details.append([tk.StringVar(self, "")])  # placeholder for client's id
      self.booking_slot_details[i].append(tk.StringVar(self, "")) # placeholder for client's name
      self.booking_slot_details[i].append(None)                   # placeholder for booking_datetime_obj
      self.booking_slots.append(tk.Button(self, textvariable=self.booking_slot_details[i][1]))
      self.time_labels.append(tk.Label(self, text=datetime.strftime(time_, "%H:%M"), bg="#0a1b40", fg="white"))
      time_ += timedelta(minutes=30) # increment time by half an hour

  
  def populate_booking_slots(self):
    """ """
    # restore booking slots to default state
    for i in range(len(self.booking_slots)):
      # create booking slot datetime object
      time_str = self.time_labels[i].cget("text")
      datetime_obj = datetime.strptime(self.date_str + time_str, "%A, %d %B %Y%H:%M")
      # initialise booking slot details
      self.booking_slot_details[i][0].set("") # clear client id
      self.booking_slot_details[i][1].set("") # clear client name
      self.booking_slot_details[i][2] = datetime_obj  # assign datetime object

    # get all bookings data for selected pro
    bookings_for_selected_pro = db.get_bookings_data_pro(self.master.cur, self.selected_pro_id.get())
    # use only bookings for current day
    for booking in bookings_for_selected_pro:
      # get booking details
      booking_datetime_obj = datetime.strptime(booking[2], "%Y-%m-%d %H:%M:%S")
      booking_date_obj = booking_datetime_obj.date()
      booking_time_obj = booking_datetime_obj.time()
      if booking_date_obj == self.date_obj: # if booking is for current day...
        # get client details
        client_id = booking[0]
        client_record = db.get_client_data(self.master.cur, client_id)
        client_name = client_record[1] + " " + client_record[2]
        # find the booking slot which matches the booking time
        for i in range(len(self.booking_slots)):
          if self.time_labels[i].cget("text") == booking_time_obj.strftime("%H:%M"):
            # update the booking slot details
            if user_is_pro or not user_is_pro and client_id == userdata[0]: # allow user to see their own bookings
              self.booking_slot_details[i][0].set(client_id)
              self.booking_slot_details[i][1].set(client_name)
            else: # user is a client and booking is for a different client
              self.booking_slot_details[i][1].set("~ UNAVAILABLE ~") # client id and booking datetime are not updated
              self.booking_slots[i].configure(state=tk.DISABLED) # slots for other clients are disabled

        # need to add datetime_object to booking slot details for available slots!!

  def return_to_overview(self):
    """ """
    if user_is_pro:
      Overview_Pro(self.master)
    else:
      Overview_Client(self.master)
    self.destroy()


  def select_booking_slot(self, btn_index):
    """ """
    # only proceed if a pro has been selected...
    if self.selected_pro_id.get() != "":

      # then if there's a booking in the selected slot... 
      if self.booking_slot_details[btn_index][0].get() != "":
        # ... flag the slot as available
        slot_is_available = False
      else: 
        # ... otherwise, flag the slot as unavailable
        slot_is_available = True

      # open booking entry window
      self.booking_entry_window = BookingEntry(
        self, 
        self.master, 
        self.booking_slot_details[btn_index][0],  # client id
        self.selected_pro_id,                     # pro id
        self.booking_slot_details[btn_index][2],  # datetime_obj
        slot_is_available
      ).grab_set()

      # disable pro_selector and booking_slots while booking entry window open
      # self.pro_selector.configure(state=tk.DISABLED)
      # for button in self.booking_slots:
      #   button.configure(state=tk.DISABLED)


  def select_pro(self, selected_pro_name):
    """ """
    for id, name in self.available_pros.items():
      if name == selected_pro_name:
        self.selected_pro_id.set(id)
    self.populate_booking_slots()


class BookingEntry(Toplevel):

  global userdata
  global user_is_pro

  def __init__(self, parent, master, client_id, pro_id, datetime_obj, slot_is_available): 
    super().__init__()
    self.title("Booking Entry")
    self.geometry('500x290')
    self.configure(background="#0a1b40")

    # class attributes --------------------------------------------------------
    self.date_str = datetime.strftime(datetime_obj, "%Y-%m-%d")
    self.time_str = datetime.strftime(datetime_obj, "%H:%M")

    self.booking_date_obj = tk.StringVar(self, self.date_str)
    self.booking_time_obj = tk.StringVar(self, self.time_str)
    self.client_id = tk.StringVar(self, client_id.get())
    self.client_name = tk.StringVar(self, "")
    self.client_email = tk.StringVar(self, "")
    self.client_phone = tk.StringVar(self, "")
    self.date_obj = datetime_obj.date()
    self.datetime_obj = datetime_obj
    self.master = master
    self.parent = parent
    self.pro_id = tk.StringVar(self, pro_id.get())
    self.pro_name = tk.StringVar(self, "")
    self.slot_is_available = slot_is_available
    self.time_obj = datetime_obj.time()

    # create widgets ----------------------------------------------------------
    self.client_search_frame = Frame(self, False)
    self.client_search_label_01 = Label(self.client_search_frame, text="Client ID: ")
    self.client_search_entry_01 = Entry(self.client_search_frame, textvariable=self.client_id)
    self.client_search_button_01 = Button(self.client_search_frame, text="New Client")
    self.client_search_button_02 = Button(self.client_search_frame, text="Search")

    self.booking_details_frame = Frame(self, False)
    self.booking_details_label_01 = Label(self.booking_details_frame, text="Booking Details:")
    if user_is_pro:
      self.booking_details_label_02a = Label(self.booking_details_frame, text="Client Name:")
      self.booking_details_label_02b = Label(self.booking_details_frame, textvariable=self.client_name)
      self.booking_details_label_03a = Label(self.booking_details_frame, text="Client Email:")
      self.booking_details_label_03b = Label(self.booking_details_frame, textvariable=self.client_email)
      self.booking_details_label_04a = Label(self.booking_details_frame, text="Client Phone:")
      self.booking_details_label_04b = Label(self.booking_details_frame, textvariable=self.client_phone)
  
      self.booking_details_button_00 = Button(self.booking_details_frame, text="Client Details")

    else: # user is a client
      self.booking_details_label_02a = Label(self.booking_details_frame, text="Pro Name:")
      self.booking_details_label_02b = Label(self.booking_details_frame, textvariable=self.pro_name)
      # should we also include email & phone fields for pros? would need to update pro table on db!
    self.booking_details_label_05a = Label(self.booking_details_frame, text="Time:")
    self.booking_details_label_05b = Label(self.booking_details_frame, textvariable=self.booking_time_obj)
    self.booking_details_label_06a = Label(self.booking_details_frame, text="Date:")
    self.booking_details_label_06b = Label(self.booking_details_frame, textvariable=self.booking_date_obj)
    if self.slot_is_available:
      self.booking_details_button_01 = Button(self.booking_details_frame, text="Create Booking")
    else:
      self.booking_details_button_01 = Button(self.booking_details_frame, text="Delete Booking")

    self.button_01 = Button(self, text="Close")

    # configure widgets -------------------------------------------------------
    self.client_search_frame.configure(highlightthickness=1, highlightcolor="white")
    self.client_search_label_01.configure()
    self.client_search_entry_01.configure()
    self.client_search_button_01.configure(command=self.create_new_client)
    self.client_search_button_02.configure(command=self.search_clients)

    self.booking_details_frame.configure(highlightthickness=1, highlightcolor="white")
    self.booking_details_label_01.configure()
    self.booking_details_label_02a.configure(width=20, anchor="e")
    self.booking_details_label_02b.configure(width=20, anchor="w")
    if user_is_pro:
      self.booking_details_label_03a.configure(width=20, anchor="e")
      self.booking_details_label_03b.configure(width=20, anchor="w")
      self.booking_details_label_04a.configure(width=20, anchor="e")
      self.booking_details_label_04b.configure(width=20, anchor="w")
      self.booking_details_button_00.configure(command=self.view_client_details, width=12)
    self.booking_details_label_05a.configure(width=20, anchor="e")
    self.booking_details_label_05b.configure(width=20, anchor="w")
    self.booking_details_label_06a.configure(width=20, anchor="e")
    self.booking_details_label_06b.configure(width=20, anchor="w")
    if self.slot_is_available:
      self.booking_details_button_01.configure(command=self.create_booking)
    else:
      self.booking_details_button_01.configure(command=self.delete_booking, width=12)

    self.button_01.configure(command=self.destroy)

    # place widgets -----------------------------------------------------------
    self.client_search_label_01.grid(row=0, column=1)
    self.client_search_entry_01.grid(row=0, column=2, columnspan=2)
    self.client_search_button_01.grid(row=1, column=1)
    self.client_search_button_02.grid(row=1, column=3)

    self.booking_details_label_01.grid(row=0, column=0, columnspan=2) # booking details
    self.booking_details_label_02a.grid(row=1, column=0) # client/pro name label
    self.booking_details_label_02b.grid(row=1, column=1) # client/pro name
  
    if user_is_pro:
      self.booking_details_label_03a.grid(row=2, column=0) # client email label
      self.booking_details_label_03b.grid(row=2, column=1) # client email
      self.booking_details_label_04a.grid(row=3, column=0) # client phone label
      self.booking_details_label_04b.grid(row=3, column=1) # client phone
      self.booking_details_button_00.grid(row=6, column=0, pady=10) # view client details button
      self.booking_details_button_01.grid(row=6, column=1, pady=10) # create/delete booking
    else:
      self.booking_details_button_01.grid(row=6, column=0, columnspan=2, pady=10) # create/delete booking
  
    self.booking_details_label_05a.grid(row=4, column=0) # booking time label
    self.booking_details_label_05b.grid(row=4, column=1) # booking time
    self.booking_details_label_06a.grid(row=5, column=0) # booking date label
    self.booking_details_label_06b.grid(row=5, column=1) # booking date

    self.button_01.grid(row=2, column=1, pady=10) # close button

    # configure grid ----------------------------------------------------------
    self.grid_columnconfigure(0, minsize=100)
    self.grid_columnconfigure(3, minsize=100)
    self.grid_rowconfigure(0, minsize=50)

    self.client_search_frame.grid_columnconfigure(0, minsize=100)
    self.client_search_frame.grid_columnconfigure(1, minsize=100)

    self.booking_details_frame.grid_columnconfigure(0, minsize=100)
    self.booking_details_frame.grid_columnconfigure(1, minsize=100)

    # determine which frame to show initially ---
    if self.slot_is_available and user_is_pro:
      self.show_client_search_frame()
    else: # slot is either booked or user is a client
      # set client/pro details
      if user_is_pro:
        client_record = db.get_client_data(self.master.cur, int(self.client_id.get()))
        client_email_ = db.get_client_email_from_logins_table(self.master.cur, int(self.client_id.get()))
        self.client_name.set(client_record[1] + " " + client_record[2])
        self.client_email.set(client_email_)
        self.client_phone.set(client_record[8])
      else:
        pro_record = db.get_pro_data(self.master.cur, int(self.pro_id.get()))
        self.pro_name.set(pro_record[1] + " " + pro_record[2])
      self.show_booking_details_frame()
    
    
  # class methods -------------------------------------------------------------

  def create_booking(self):
    """Add booking details to the database."""
    if self.client_id.get() == "":  # user is a client
      self.client_id.set(userdata[0]) # set to user's id
    try:
      db.store_booking_data(self.master.con, self.master.cur, 
        [
          int(self.client_id.get()),
          int(self.pro_id.get()),
          self.datetime_obj
        ]
      )
    except: # generic error message
      print("Error: booking could not be created!")
    else:
      print("Booking created!")
    finally:
      self.destroy()
    
    
  def create_new_client(self):
    """Open the registration form to add a new client to the database."""
    Register(self.master, self)
    self.client_search_button_01.config(state="disabled")   # how is this re-enabled?


  def delete_booking(self):
    """Delete booking record from database."""
    try:
      db.delete_booking_data(self.master.con, self.master.cur,
        [
          int(self.client_id.get()),
          int(self.pro_id.get()),
          self.datetime_obj
        ]          
      )
    except: # generic error message
      print("Error: booking could not be deleted!")
    else:
      print("Booking deleted!")
    finally:
      self.destroy()


  def search_clients(self):
    # ensure client_id is an integer
    try:
      client_id = int(self.client_id.get())
    except:
      client_id = 0
    finally:
      # attempt to get client details from db
      try:
        client_record = db.get_client_data(self.master.cur, client_id)
        client_email = db.get_client_email_from_logins_table(self.master.cur, client_id)
      except IndexError:
        print("Client ID not found")
      else:
        self.client_name.set(client_record[1] + " " + client_record[2])
        self.client_email.set(client_email)
        self.client_phone.set(client_record[8])
        self.show_booking_details_frame()


  def show_client_search_frame(self):   # change states instead ?
    """ """
    self.client_search_frame.grid(row=0, column=1)


  def show_booking_details_frame(self):
    """ """
    self.booking_details_frame.grid(row=1, column=1)


  def view_client_details(self):
    """ """
    ClientDetails(self.master, self.client_id)


  def destroy(self):
    """ """
    # # re-enable Day Calendar buttons/dropdown
    # try:
    #   # if coming from CalendarDay()...
    #   self.parent.pro_selector.configure(state=tk.NORMAL)
    # except AttributeError:
    #   pass
    # else:
    #   # repopulate Day Calendar booking slots
    #   self.parent.populate_booking_slots()
    # finally:
    #   for button in self.parent.booking_slots:
    #     button.configure(state=tk.NORMAL)
    #   super().destroy()
    
    # self.parent.destroy()
    # Overview_Client(self.master)

    self.parent.populate_booking_slots()
    # self.grab_release()
    super().destroy()


class AllPros(Frame):
  
  def __init__(self, master, date_):
    super().__init__()
    self.master = master
    self.master.title('Available Pros')
    self.master.geometry('800x780')
    self.configure(background = "#0a1b40")
    self.date = date_
    self.pack(fill=tk.BOTH, expand=1)

    all_pros = db.get_pro_data_all(self.master.cur)
    
    # create custom 2D dictionary from all_pros data
    pro_data = {}
    for i in range(1, len(all_pros)):  # all pros except admin (record 1)
      pro_id = all_pros[i][0]
      pro_data[pro_id] = {}
      for j in range(len(all_pros[i])):
        pro_data[pro_id]["ProID"] = pro_id
        pro_data[pro_id]["FirstName"] = all_pros[i][1]
        pro_data[pro_id]["Surname"] = all_pros[i][2]
        pro_data[pro_id]["Phone"] = all_pros[i][3]
    
    tk.Label(self, text=f"Available pros and times on {datetime.strftime(self.date, '%A, %d %B %Y')}:", background = "#0a1b40", fg="white").grid(row=0, rowspan=2, column=3, columnspan=7, sticky="NEWS")

    # make conditional!
    time_font = font.Font(overstrike=1) # this creates the overstrike font 
    time_font0 = font.Font(overstrike=0) # this is to make all of the times the same size as the overstriked times

    # create labels and buttons
    labels = []
    buttons = []
    for pro in pro_data.values():
      labels.append(tk.Label(self, text=pro["FirstName"] + "\n" + pro["Surname"], bd=1, fg='black', bg='light grey', relief='solid', wraplength=70, padx=10, pady=10, height=2, width=8))
      times_ = []
      time_ = datetime.strptime("09:00", "%H:%M")
      for i in range(24):
        times_.append(tk.Button(self, text=datetime.strftime(time_, "%H:%M"), font=time_font0))
        time_ += timedelta(minutes=30)
      buttons.append(times_)
      
    # arrange labels and buttons in grid
    row = 2
    for i in range(2):  # label rows
      column = 1
      for j in range(3):  # label columns
        labels[j+(i*3)].grid(row=row, column=column, columnspan=3, sticky="NEWS")
        for k in range(3):  # button columns
          for l in range(8):  # button rows
            row += 1
            buttons[j+(i*3)][l+(k*8)].grid(row=row, column=column)
          row -= 8
          column += 1
        column += 1
      column -= 3
      row += 10

    tk.Button(self, text="View Your\nPros", fg="White", bg="#0a1b40", command=self.view_yourpro).grid(row=21, column=1, columnspan=2, pady=10, sticky="NEWS")
    
    tk.Button(self, text="Return to\nOverview", fg="White", bg="#0a1b40", command=self.back_to_overview).grid(row=21, column=10, columnspan=2, pady=10, sticky="NEWS")

    self.grid_columnconfigure(0, minsize=20)
    self.grid_columnconfigure(4, minsize=17)
    self.grid_columnconfigure(8, minsize=17)
    self.grid_rowconfigure(0, minsize=20)
    self.grid_rowconfigure(1, minsize=20)
    self.grid_rowconfigure(11, minsize=15)

  def back_to_overview(self):
    """ """
    Overview_Client(self.master)
    self.destroy()

  def view_yourpro(self):
    """ """
    YourPro(self.master, self.date)
    self.destroy() 


class YourPro(Frame):

  def __init__(self, master, date_):
    super().__init__()
    self.master = master
    self.master.title("Your Pro's Availability")
    self.master.geometry("440x460")
    self.configure(background = "#0a1b40")
    self.date = date_
    self.pack(fill=tk.BOTH, expand=1)

    pro_id = lesson_pro[0]
    pro_firstname = lesson_pro[1]
    pro_surname = lesson_pro[2]

    tk.Label(self, text=f"Available Times on {datetime.strftime(self.date, '%A, %d %B %Y')}", background="#0a1b40", fg="white", pady=5, wraplength=160).grid(row=0, column=1, columnspan=4, sticky="NEWS")

    # make conditional!!!
    time_font = font.Font(overstrike=1) # this creates the overstrike font 
    time_font0 = font.Font(overstrike=0)

    # create label and buttons
    tk.Label(self, text=pro_firstname + " " + pro_surname, bd=1, fg='black', bg='light grey', relief='solid', wraplength=110, padx=10, pady=10, height=2, width=8).grid(row=2, column=2, columnspan=3, sticky="NEWS")
    
    buttons = []
    time_ = datetime.strptime("09:00", "%H:%M")
    for i in range(24):
      buttons.append(tk.Button(self, text=datetime.strftime(time_, "%H:%M"), font=time_font0))
      time_ += timedelta(minutes=30)
      
    # arrange buttons in grid
    row = 3
    column = 2
    for k in range(3):  # button columns
      for l in range(8):  # button rows
        row += 1
        buttons[l+(k*8)].grid(row=row, column=column)
      row -= 8
      column += 1

    tk.Button(self, text="View All\nPros", fg="White", bg="#0a1b40", command=self.view_allpros).grid(row=12, column=0, padx=10, pady=10)

    tk.Button(self, text="Return to\nOverview", fg="White", bg="#0a1b40", command=self.back_to_overview).grid(row=12, column=5, padx=10, pady=10)


  def back_to_overview(self):
    """ """
    Overview_Client(self.master)
    self.destroy()
  
  def view_allpros(self):
    """ """
    AllPros(self.master, self.date)
    self.destroy()  


class ClientDetails(Toplevel):

  ##
  ## Expand client details to include ALL fields from the clients table!!
  ##

  # def __init__(self, parent, client_id, pro_id, booking_time_obj):
  def __init__(self, master, client_id):
    super().__init__()
    # self.parent = parent
    self.master = master
    self.title("Client Details")
    # self.configure(background = "#0a1b40")

    client_id = int(client_id.get())
    # self.pro_id = pro_id
    # self.booking_time_obj = booking_time_obj

    client_record = db.get_client_data(self.master.cur, client_id)
    client_data = []
    for i in range(len(client_record)):
      client_data.append(tk.StringVar(self, client_record[i]))
    client_data.append(tk.StringVar(self, db.get_client_email_from_logins_table(self.master.cur, client_id)))

    tk.Label(self, background = "#0a1b40", text=f"{client_data[1].get() + ' ' + client_data[2].get()}'s Details", fg="white").grid(row=0, column=1, columnspan=3)

    #These create the labels that show what information is being stored
    tk.Label(self, background="White", text="First Name", width=15, anchor="e").grid(row=1, column=1)
    tk.Label(self, background="White", text="Surname", width=15, anchor="e").grid(row=2, column=1)
    tk.Label(self, background="White", text="Telephone", width=15, anchor="e").grid(row=3, column=1)
    tk.Label(self, background="White", text="Email", width=15, anchor="e").grid(row=4, column=1)
    tk.Label(self, background="White", text="Address", width=15, anchor="e").grid(row=5, column=1)
    tk.Label(self, background="White", text="Handicap", width=15, anchor="e").grid(row=6, column=1)
    tk.Label(self, background="White", text="Dominant Hand", width=15, anchor="e").grid(row=7, column=1)
    tk.Label(self, background="White", text="Injuries", width=15, anchor="e").grid(row=8, column=1)
    tk.Label(self, background="White", text="Restrictions", width=15, anchor="e").grid(row=9, column=1)
    
    #These create data entries for the user to input data to be stored
    tk.Label(self, textvariable=client_data[1], width=15, bg="White", anchor="w").grid(row=1, column=3)
    tk.Label(self, textvariable=client_data[2], width=15, bg="White", anchor="w").grid(row=2, column=3)
    
    tk.Label(self, textvariable=client_data[8], width=15, bg="White", anchor="w").grid(row=3, column=3)
    tk.Label(self, textvariable=client_data[15], width=15, bg="White", anchor="w").grid(row=4, column=3)

    tk.Label(self, textvariable=client_data[3], width=15, bg="White", anchor="w").grid(row=5, column=3)
    tk.Label(self, textvariable=client_data[9], width=15, bg="White", anchor="w").grid(row=6, column=3)
    tk.Label(self, textvariable=client_data[10], width=15, bg="White", anchor="w").grid(row=7, column=3)
    tk.Label(self, textvariable=client_data[11], width=15, bg="White", anchor="w").grid(row=8, column=3)
    tk.Label(self, textvariable=client_data[12], width=15, bg="White", anchor="w").grid(row=9, column=3)

    self.grid_columnconfigure(0, minsize=75)
    self.grid_columnconfigure(1, minsize=20)
    self.grid_columnconfigure(2, minsize=10) # spacer
    self.grid_columnconfigure(3, minsize=50)
    self.grid_columnconfigure(4, minsize=75)
    self.grid_rowconfigure(0, minsize=50)

    # tk.Button(self, text="Delete Booking", fg="White", bg="#0a1b40", command=self.delete_booking).grid(row=10, column=1, columnspan=1)#creates a button to change the data

    tk.Button(self, text="Back", fg="White", bg="#0a1b40", command=self.back, width=12).grid(row=10, column=3, columnspan=1)#creates a button to change the data
 
    self.grid_rowconfigure(10, minsize=50)

  def back(self):
    """ """
    self.destroy()

  # def delete_booking(self):
  #   """ """
  #   db.delete_booking_data(self.master.con, self.master.cur, 
  #     [
  #       self.client_id,
  #       self.pro_id.get(),
  #       self.booking_time_obj
  #     ]
  #   )
  #   self.parent.destroy()
  #   CalendarDay(self.master, datetime.today().date())
  #   self.destroy()


class AddPro(Toplevel):
  def __init__(self, master):
    super().__init__()
    self.master = master
    self.title("Add A Pro")
    #self.geometry("250x450")
    self.configure(background = "#0a1b40")

    self.var_01 = tk.StringVar(self, "First Name") 
    self.var_02 = tk.StringVar(self, "Surname")
    self.var_03 = tk.StringVar(self, "Telephone")
    self.var_04 = tk.StringVar(self, "Email")
    self.var_05 = tk.StringVar(self, "Password")
    self.var_06 = tk.StringVar(self, "Confirm Password")

    Entry(self, textvariable=self.var_01).grid(row=1,  column=1, columnspan=2)
    Entry(self, textvariable=self.var_02).grid(row=2,  column=1, columnspan=2)
    Entry(self, textvariable=self.var_03).grid(row=3,  column=1, columnspan=2)
    Entry(self, textvariable=self.var_04).grid(row=4,  column=1, columnspan=2)
    Entry(self, textvariable=self.var_05).grid(row=5,  column=1, columnspan=2)
    Entry(self, textvariable=self.var_06).grid(row=6,  column=1, columnspan=2)

    self.grid_columnconfigure(0, minsize=25)
    self.grid_columnconfigure(1, minsize=100)
    self.grid_columnconfigure(2, minsize=100)
    self.grid_columnconfigure(3, minsize=25)
    self.grid_rowconfigure(0, minsize=20)

    tk.Button(self, text="Cancel", background="#0a1b40", foreground="white", width=7, command=self.cancel).grid(row=7, column=2, pady=20)
    tk.Button(self, text="Register", background="#0a1b40", foreground="white", width=7, command=self.new_pro).grid(row=7, column=1, pady=20)

  def cancel(self):
    self.destroy()

  def new_pro(self):
    # presence check (all fields)
    if self.var_01.get() != "" and self.var_01.get() != "First Name" and \
       self.var_02.get() != "" and self.var_02.get() != "Surname" and \
       self.var_03.get() != "" and self.var_03.get() != "Telephone" and \
       self.var_04.get() != "" and self.var_04.get() != "Email" and \
       self.var_05.get() != "" and self.var_05.get() != "Password" and \
       self.var_06.get() != "" and self.var_06.get() != "Confirm Password":
      # check password and confirm password matches
      if self.var_05.get() == self.var_06.get():
        # validate email address
        if is_valid_email(self.var_04.get()):
          # check email doesn't exist on logins table
          login_data = db.get_login_data(self.master.cur, self.var_04.get())
          if login_data != []:
            print("Email already exists on the database")
          else:
            # email isn't on the database (new user)
            # get next available pro id
            pro_data = db.get_pro_data_all(self.master.cur)
            pro_id = max(pro_data, key=lambda x: x[0])[0] + 1 # increment max id by 1
            # add user to database
            db.store_regdata_pro(
              self.master.con,
              self.master.cur,
              [
                pro_id,
                self.var_04.get(),          # Email
                self.var_05.get(),          # Password
                self.var_01.get().title(),  # First name
                self.var_02.get().title(),  # Surname
                self.var_03.get(),          # Phone
                1                           # IsActive = True
              ]
            )
            print("Pro record created successfully!")
        else:
          # invalid email address
          print("Invalid email address format.")
      else:
        # passwords don't match
        print("Passwords don't match")
    else:
      print("Please fill in all fields")
    self.destroy()


class RemovePro(Toplevel):
  
  def __init__(self, master):
    super().__init__()
    self.title("Remove A Pro")
    #self.geometry("300x400")

    self.available_pros = dict()
    self.master = master
    self.selected_pro_id = tk.StringVar(self, "")
    self.selected_pro_name = tk.StringVar(self, "Please select a pro")

    self.generate_available_pro_list()

    self.pro_selector = tk.OptionMenu(self, self.selected_pro_name, *self.available_pros.values(), command=self.select_pro)
    self.pro_selector.config(bg="#0a1b40", fg="White", width=16, anchor="w")
    self.pro_selector.grid(row=1, column=2, columnspan=2)
        
    tk.Button(self, text="Cancel", background="#0a1b40", foreground="white", width=8, command=self.cancel).grid(row=3, column=1)
    tk.Button(self, text="Remove", background="#0a1b40", foreground="white", width=8, command=self.Confirm).grid(row=3, column=4)

    self.columnconfigure(0, minsize=25)
    self.columnconfigure(1, minsize=75)
    self.columnconfigure(2, minsize=75)
    self.columnconfigure(3, minsize=75)
    self.columnconfigure(4, minsize=75)
    self.columnconfigure(5, minsize=25)
    self.rowconfigure(0, minsize=25)
    self.rowconfigure(1, minsize=25)
    self.rowconfigure(2, minsize=25)
    self.rowconfigure(3, minsize=25)

  def cancel(self):
    """ """
    self.destroy()


  def generate_available_pro_list(self):
    """ """
    # get list of all pro records from database
    pro_data = db.get_pro_data_all(self.master.cur)
    # compile list of available pros for option menu
    for i in range(0, len(pro_data)):
      if pro_data[i][4] == 1: # if pro is active
        pro_id = pro_data[i][0]
        pro_name = pro_data[i][1] + " " + pro_data[i][2] # concatenate first name and surname fields
        self.available_pros[pro_id] = pro_name # map name to ID


  def remove_pro(self):
    """ """
    if self.selected_pro_id.get() != "":
      # confirmed = popup(self, "Are you sure you want to remove this pro?")
      # if confirmed:
        db.deactivate_pro(self.master.con, self.master.cur, int(self.selected_pro_id.get()))
        print("Pro successfully removed from the database.")
        self.destroy()
    else:
      print("Please select a pro")
    self.destroy()


  def select_pro(self, selected_pro_name):
    """ """
    for id, name in self.available_pros.items():
      if name == selected_pro_name:
        self.selected_pro_id.set(id)

  def Confirm(self):

    window = Toplevel()

    def confirm():
      window.destroy()
      self.remove_pro()
    
    def cancel():
      window.destroy()
    
      
    Label(window, text="Are you sure you want to remove this pro?").pack()
    Button(window, text="Confirm", command=confirm).pack()
    Button(window, text="Cancel", command=cancel).pack()
    

    
    

# global subroutines ----------------------------------------------------------

def is_valid_email(email_address):
  """Returns True if email address syntax is valid."""
  pattern = r"^(\S+)(@)(\S+)([.])(\S+)$"
  match = re.fullmatch(pattern, email_address)
  if not match:
    return False
  else: # email is valid....
    return True

# testing ---------------------------------------------------------------------

# if __name__ == '__main__':
#   import main

# # ---
# testing_as_pro_user = False  # <--adjust---
# testing_as_client = 1      # <--adjust---
# # ---

# if testing_as_pro_user:
#   user_is_pro = True
#   userdata = [1000, "Pro", "Administrator", "00000 000000"]
# else:
#   user_is_pro = False
#   if testing_as_client == 1:
#     userdata = [1000, "Test", "Client 01", "1 Client Road", "Clientville", "Clientshire", "CL1 3NT", "01234 567891"]
#   elif testing_as_client == 2:
#     userdata = [1001, "Test", "Client 02", "2 Client Road", "Clientville", "Clientshire", "CL2 3NT", "01234 567892"]
#   elif testing_as_client == 3:
#     userdata = [1002, "Test", "Client 03", "3 Client Road", "Clientville", "Clientshire", "CL3 3NT", "01234 567893"]

# -----------------------------------------------------------------------------


""" Notes: --------------------------------------------------------------------

• ADD DATA TYPE INDICATORS TO ALL TIME/DATE VARIABLES (STR/OBJ)
• Register client - if default fields not changed (e.g. Injuries), add blank entries
• what do we do when a client has a booking with a removed (deactivated) pro coming up?

fix code without testing info?

• fix grab_release to not also release 3rd tier widgets (i.e. login -> register -> toplevel)

# Last Tweaks: search client by name instead of id,menu widget to navigate windows, use scrollwheel fot common window size """  