import sqlite3
from tqdm import tqdm
from random import choice, randint
import time

random_crap = [
'Removing boilerplate code', 'Connecting', 'Looking busy', 'Configuring...',
'Printing', 'Wrapping text', '<broadcasting>'
]

def look_busy():
    print(choice(random_crap))
    for i in tqdm(range(randint(15, 30))):
        time.sleep(0.01)

def wraptext(text):
    return """'""" + str(text) + """'"""


class SQLWORKER:
    LOGO = """
   __                             __   
  / /   ____  _____ _____ __      \ \  
 / /   |    \| __  |   __|  |      \ \ 
< <    |  |  | __ -|   __|  |__     > >
 \ \   |____/|_____|__|  |_____|   / / 
  \_\                             /_/  
     @github.com/dukeycamps/dbfill\n
"""
    text_values = []
    range_start = range_end = range_multi = None
    db_name = ''
    root_table_name = None
    conn = None
    c = None
    root_columns = None
    root_types = None
    # TODO: Incorporate it somehow

    def make_wordlist(self):
        print("Please craft your wordlist below, [for TEXT types] separated by [spaces]")
        stringz = input()
        self.text_values = stringz.split()

    def make_range(self):
        print("Declare your range [start end multiplier] [eg. 0 2000 25]")
        stringz = input().split()
        self.range_start = int(stringz[0])
        self.range_end = int(stringz[1])
        self.range_multi = int(stringz[2])

    def connect(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        self.conn = conn
        self.c = c

    def create_table_str(self):
        table_name = input("Table Name ->")
        self.root_table_name = table_name
        list_columns = []
        list_types = []
        columns = int(input("Number of columns ->"))
        
        for column in range(columns):
            list_columns.append(input("Column %s NAME ->" % (column+1)))
            list_types.append(input("Column %s TYPE ->" % (list_columns[column])))
        self.root_types = list_types
        print('\n')
        
        for lol in range(len(list_columns)):
            print("%s , %s" % (list_columns[lol], list_types[lol]))
        satisfied = input("Are you happy with this configuration? [yes]").lower()

        if satisfied == 'yes' or satisfied == '':
            tabstring = ''
            for lol in range(len(list_columns)):
                tabstring += "%s %s, " % (list_columns[lol], list_types[lol])
            return table_name, tabstring[:-2]
        else:
            self.create_table_str()

    def create_table(self):
        self.connect()
        self.c.execute('''CREATE TABLE IF NOT EXISTS %s(%s)''' %(self.create_table_str()))

    def __init__(self):

        print(self.LOGO)
        self.db_name = input("Please input your file name--------->filename.db\n")
        if(self.db_name[-3:] != '.db'):
            self.db_name += '.db'
        # TODO: MAKE THIS JUST A pass
        self.connect()
        self.conn.commit()
        self.conn.close()

    def get_columns(self, table_name):
        self.connect()
        self.c.execute('PRAGMA table_info(%s)' % (table_name))
        names = [tup[1] for tup in self.c.fetchall()]
        return names

    def data2str(self):
        random_data = ""
        for data_type in self.root_types:
            if(data_type.lower() == "real"):
                random_data += str(randint(self.range_start, self.range_end)*self.range_multi)
            elif(data_type.lower() == "text"):
                random_data += "'" + choice(self.text_values) + "'"
            random_data += ' ,'
        #TEXT, REAL
        #JOHN, 13
        return random_data[:-1]

    def insert_values(self, times=100):
        self.make_wordlist()
        self.make_range()
        # TODO: MAKE EVERYTHING CLASS BASED, NO PRE INPUT
        self.connect()
        for x in tqdm(range(times)):
            self.c.execute("INSERT INTO %s VALUES(%s)" %(self.root_table_name, self.data2str()))
        self.conn.commit()
        self.conn.close()

Boy_Cott = SQLWORKER();look_busy()
Boy_Cott.create_table();look_busy()
Boy_Cott.insert_values(int(input("How many random rows do you want to generate?")));look_busy()
input("\nPress Enter to exit.")