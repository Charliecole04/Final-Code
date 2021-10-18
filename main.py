import db
import os
import classes
import tkinter as tk


# global variables ------------------------------------------------------------

user_is_pro = bool()
userdata = list()
next_lesson = list()
lesson_pro = list()

# ----------------------------------------------------------------------------

class Tk(tk.Tk):
  """Custom Tk class which includes database connection and cursor objects,
     accessible as class attributes."""
  
  def __init__(self, con, cur):
    super().__init__()
    self.con = con
    self.cur = cur


# -----------------------------------------------------------------------------
# main program
# -----------------------------------------------------------------------------

# connect to database
con, cur = db.connect("data.db")

# populate database
if os.stat("data.db").st_size == 0: # if filesize is 0 bytes
  db.populate(con, cur)

# create GUI
root = Tk(con, cur)
root.title('Discount Golf Store Lesson Booking System')
root.geometry('450x275')

# starting frame
classes.Login(root)

# run mainloop
root.lift()
root.mainloop()

# close database
db.close(con)
