import sqlite3 as sql

# https://www.tutorialspoint.com/sqlite/sqlite_python.htm


# db core functions -----------------------------------------------------------

def connect(dbname):
  """Connects to the database and returns the connection and cursor objects."""
  con = sql.connect(dbname)
  cur = con.cursor()
  print('Database connected...')
  return con, cur


def convert_to_dict(descriptions, records):
  """Returns a list of records as dicts using field names for keys."""
  field_names = [descriptions[i][0] for i in range(len(descriptions))]
  return [dict(zip(field_names, records[i])) for i in range(len(records))]


def populate(con, cur):
  """Creates the database tables and inserts some data for testing purposes."""

  # maybe convert to a single script call?? i.e. cur.executescript(script)

  cur.execute('''
    CREATE TABLE Logins(
      Email VARCHAR PRIMARY KEY NOT NULL,
      Password VARCHAR NOT NULL,
      ClientID INT,
      ProID INT
    )
  ''')

  cur.execute('''
    CREATE TABLE Bookings(
      ClientID INT NOT NULL,
      ProID INT NOT NULL,
      StartTime DATETIME NOT NULL
    )
  ''')

  cur.execute('''
    CREATE TABLE Pros(
      ProID INT NOT NULL,
      FirstName VARCHAR NOT NULL,
      Surname  VARCHAR NOT NULL,
      Phone VARCHAR NOT NULL,
      IsActive INT NOT NULL
    )
  ''')

  cur.execute('''
    CREATE TABLE Clients(
      ClientID INT NOT NULL,
      FirstName VARCHAR NOT NULL,
      Surname VARCHAR NOT NULL,
      AddressLine1 VARCHAR NOT NULL,
      AddressLine2 VARCHAR,
      City VARCHAR NOT NULL,
      County VARCHAR NOT NULL,
      PostCode VARCHAR NOT NULL,
      Phone VARCHAR NOT NULL,
      Handicap VARCHAR,
      DominantHand VARCHAR,
      Injuries VARCHAR,
      Restrictions VARCHAR,
      RegDate DATETIME NOT NULL,
      LastLogin DATETIME NOT NULL      
    )
  ''')

  # Insert test data ----------------------------------------------------------
  cur.execute('INSERT INTO Logins (Email, Password, ClientID, ProID) VALUES ("pro@user.com", "123", NULL, 1000)')
  cur.execute('INSERT INTO Logins (Email, Password, ClientID, ProID) VALUES ("client01@user.com", "123", 1000, NULL)')
  cur.execute('INSERT INTO Logins (Email, Password, ClientID, ProID) VALUES ("client02@user.com", "123", 1001, NULL)')
  cur.execute('INSERT INTO Logins (Email, Password, ClientID, ProID) VALUES ("client03@user.com", "123", 1002, NULL)')

  cur.execute('INSERT INTO Bookings (ClientID, ProID, StartTime) VALUES (1000, 1001, datetime("2021-01-01 15:00:00"))') # client01/matt king
  cur.execute('INSERT INTO Bookings (ClientID, ProID, StartTime) VALUES (1000, 1001, datetime("2021-12-15 09:00:00"))') # client01/matt king
  cur.execute('INSERT INTO Bookings (ClientID, ProID, StartTime) VALUES (1000, 1001, datetime("2021-10-01 09:00:00"))') # client01/matt king
  cur.execute('INSERT INTO Bookings (ClientID, ProID, StartTime) VALUES (1000, 1001, datetime("2021-10-01 10:00:00"))') # client01/matt king
  cur.execute('INSERT INTO Bookings (ClientID, ProID, StartTime) VALUES (1000, 1001, datetime("2021-10-05 11:00:00"))') # client01/matt king
  cur.execute('INSERT INTO Bookings (ClientID, ProID, StartTime) VALUES (1000, 1001, datetime("2021-11-01 09:00:00"))') # client01/matt king
  cur.execute('INSERT INTO Bookings (ClientID, ProID, StartTime) VALUES (1000, 1001, datetime("2021-11-10 09:00:00"))') # client01/matt king

  cur.execute('INSERT INTO Pros (ProID, FirstName, Surname, Phone, IsActive) VALUES (1000, "Pro", "Administrator", "07755 348752", 0)')
  cur.execute('INSERT INTO Pros (ProID, FirstName, Surname, Phone, IsActive) VALUES (1001, "Matt", "King", "07755 348752", 1)')
  cur.execute('INSERT INTO Pros (ProID, FirstName, Surname, Phone, IsActive) VALUES (1002, "Chris", "Lightfoot", "07755 348752", 1)')
  cur.execute('INSERT INTO Pros (ProID, FirstName, Surname, Phone, IsActive) VALUES (1003, "Lucy", "Clarke", "07755 348752", 1)')
  cur.execute('INSERT INTO Pros (ProID, FirstName, Surname, Phone, IsActive) VALUES (1004, "Steve", "Jackson", "07755 348752", 1)')
  cur.execute('INSERT INTO Pros (ProID, FirstName, Surname, Phone, IsActive) VALUES (1005, "Luke", "Gosling", "07755 348752", 1)')
  cur.execute('INSERT INTO Pros (ProID, FirstName, Surname, Phone, IsActive) VALUES (1006, "Paul", "Barham", "07755 348752", 1)')

  cur.execute('INSERT INTO Clients (ClientID, FirstName, Surname, AddressLine1, City, County, PostCode, Phone, RegDate, LastLogin) VALUES (1000, "Test", "Client 01", "1 Client Road", "Clientville", "Clientshire", "CL1 3NT", "01234 567891", datetime("now"), datetime("now"))')
  cur.execute('INSERT INTO Clients (ClientID, FirstName, Surname, AddressLine1, City, County, PostCode, Phone, RegDate, LastLogin) VALUES (1001, "Test", "Client 02", "2 Client Road", "Clientville", "Clientshire", "CL2 3NT", "01234 567892", datetime("now"), datetime("now"))')
  cur.execute('INSERT INTO Clients (ClientID, FirstName, Surname, AddressLine1, City, County, PostCode, Phone, RegDate, LastLogin) VALUES (1002, "Test", "Client 03", "3 Client Road", "Clientville", "Clientshire", "CL3 3NT", "01234 567893", datetime("now"), datetime("now"))')

  con.commit()
  print("Database populated...")


def close(con):
  """Closes the database."""
  con.close()
  print('Database closed.')


# db lookup functons ----------------------------------------------------------

def get_bookings_data_all(cur):
  """Returns all records from the bookings table."""
  cur.execute('SELECT * FROM Bookings')
  return cur.fetchall()


def get_bookings_data_client(cur, client_id):
  """Returns all records from the bookings table for a given client."""
  cur.execute('SELECT * FROM Bookings WHERE ClientID=?', (client_id, ))
  return cur.fetchall()


def get_bookings_data_pro(cur, pro_id):
  """Returns all records from the bookings table for a given pro."""
  cur.execute('SELECT * FROM Bookings WHERE ProID=?', (pro_id, ))
  return cur.fetchall()


def get_client_data(cur, client_id):
  """Returns the record from the clients table for a given client."""
  cur.execute('SELECT * FROM Clients WHERE ClientID=?', (client_id, ))
  return cur.fetchall()[0]


def get_client_data_all(cur):
  """Returns all records from the clients table."""
  cur.execute('SELECT * FROM Clients')
  return cur.fetchall()
  # return convert_to_dict(cur.description, cur.fetchall())


def get_client_email_from_logins_table(cur, client_id):
  """Returns the email address from the logins table for a given client."""
  cur.execute('SELECT * FROM Logins WHERE ClientID=?', (client_id, ))
  return cur.fetchall()[0][0]


def get_login_data(cur, email):
  """Returns the record from the logins table for a given email address."""
  cur.execute('SELECT * FROM Logins WHERE Email=?', (email, ))
  result = cur.fetchall()
  if result != []:
    return result[0]
  else:
    return result


def get_login_data_all(cur):
  """Returns all records from the logins table."""
  cur.execute('SELECT * FROM Logins')
  return cur.fetchall()


def get_max_client_id(cur):
  """Returns the max client id from the clients table."""
  cur.execute('SELECT MAX(ClientID) FROM Clients')
  return cur.fetchall()[0][0]


def get_pro_data(cur, pro_id):
  """Returns the record from the pros table for a given pro."""
  cur.execute('SELECT * FROM Pros WHERE ProID=?', (pro_id, ))
  return cur.fetchall()[0]


def get_pro_data_all(cur):
  """Returns all records from the pros table."""
  cur.execute('SELECT * FROM Pros')
  return cur.fetchall()


# db storage functions --------------------------------------------------------

def store_regdata_client(con, cur, userdata):
  """Inserts client registration data into the logins and clients tables."""
  cur.execute('INSERT INTO Logins (Email, Password, ClientID) VALUES (?, ?, ?)', (
    userdata[1],
    userdata[2],
    userdata[0]
  ))
  
  cur.execute('INSERT INTO Clients (ClientID, FirstName, Surname, AddressLine1, AddressLine2, City, County, PostCode, Phone, Handicap, DominantHand, Injuries, Restrictions, RegDate, LastLogin) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (
    userdata[0],
    userdata[3],
    userdata[4],
    userdata[5],
    userdata[6],
    userdata[7],
    userdata[8],
    userdata[9],
    userdata[10],
    userdata[11],
    userdata[12],
    userdata[13],
    userdata[14],
    sql.datetime.datetime.now(),
    sql.datetime.datetime.now()
  ))
  con.commit()


def store_regdata_pro(con, cur, userdata):
  """Inserts pro registration data into the logins and pros tables."""
  cur.execute('INSERT INTO Logins (Email, Password, ProID) VALUES (?, ?, ?)', (
    userdata[1],
    userdata[2],
    userdata[0]
  ))
  
  cur.execute('INSERT INTO Pros (ProID, FirstName, Surname, Phone, IsActive) VALUES (?, ?, ?, ?, ?)', (
    userdata[0],
    userdata[3],
    userdata[4],
    userdata[5],
    userdata[6]
  ))
  con.commit()


def store_booking_data(con, cur, booking_data):
  """Inserts booking data into the bookings table."""
  cur.execute('INSERT INTO Bookings (ClientID, ProID, StartTime) VALUES (?, ?, ?)', (
    booking_data[0],
    booking_data[1],
    booking_data[2]
  ))
  con.commit()


# db deletion functions -------------------------------------------------------

def delete_booking_data(con, cur, booking_data):
  """Deletes booking data from the bookings table."""
  cur.execute('DELETE FROM Bookings WHERE (ClientID=? AND ProID=? AND StartTime=?)', (
    booking_data[0],
    booking_data[1],
    booking_data[2]
  ))
  con.commit()


# db update functions ----------------------------------------------------------

def deactivate_pro(con, cur, pro_id):
  """Updates pro record field IsActive to 0 (False)."""
  cur.execute('UPDATE Pros SET IsActive=? WHERE ProID=?', (
    0,
    pro_id
  ))
  con.commit()

# testing - to be removed -----
if __name__ == "__main__":
  import main

