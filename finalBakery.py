#!/usr/bin/env python
import curses
import psycopg2
import string

##NOTE: All python ncurses code adapted from https://docs.python.org/3.4/library/curses.html and https://docs.python.org/dev/howto/curses.html

conn = psycopg2.connect(database="myapp", user="postgres", password="dbpass",
                        host="localhost", port="5432")
##Main function
def main():
    ##curses initialization
    stdscr = curses.initscr()
    curses.start_color()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    stdscr.nodelay(True)

    ##color sets
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLUE)

    #create main menu window
    max_y, max_x = stdscr.getmaxyx()
    stdscr.border('|','|','-','-','*','*','*','*')
    stdscr.addstr(0,34,"Cake Database", curses.color_pair(2))
    stdscr.bkgd(' ', curses.color_pair(2))
    win = stdscr.subwin(20, 75, 2, 2)
    win.bkgd(' ', curses.color_pair(3))
    win.addstr(2,8,"SELECT MENU OPTION WITH ARROWS:",curses.A_UNDERLINE)
    win.refresh()
    stdscr.refresh()

    c = stdscr.getch()##user input
    cursor = 1; ##cursor location
    end = 1;##menu loop condition
    
    ##get user menu input
    while end != 0:
        
        ##highlisht cursor location
        if cursor == 1:
            win.addstr(4,8,"Ingredients",curses.color_pair(1))
        else:
            win.addstr(4,8,"Ingredients",curses.color_pair(3))
        if cursor == 2:
            win.addstr(6,8,"Cakes",curses.color_pair(1))
        else:
            win.addstr(6,8,"Cakes",curses.color_pair(3))
        if cursor == 3:
            win.addstr(8,8,"Exit",curses.color_pair(1))
        else:
            win.addstr(8,8,"Exit",curses.color_pair(3))
        win.refresh()
        c = stdscr.getch()
        
        ##down arrow conditions
        if c == curses.KEY_DOWN: 
            if cursor < 3:
                cursor = cursor + 1
            else:
                cursor = 1
        ##up arrow conditions
        elif c == curses.KEY_UP: 
            if cursor > 1:
                cursor = cursor - 1
            else:
                cursor = 3
        
        ##ENTER key conditions
        elif c == 10: ##ASCII value for enter key.  Taken from http://stackoverflow.com/questions/11067800/ncurses-key-enter-is-fail
            if cursor == 3:
                end = 0
            if cursor == 2:
                 cake_menu()
                 win.addstr(2,8,"SELECT MENU OPTION WITH ARROWS:",curses.A_UNDERLINE)
            if cursor == 1:
                ingredient_menu()
                win.addstr(2,8,"SELECT MENU OPTION WITH ARROWS:",curses.A_UNDERLINE)
            
         
    ##remove window    
    c = stdscr.getch()
    curses.echo()
    curses.nocbreak()
    stdscr.keypad(False)
    stdscr.nodelay(False)
    curses.endwin()

#ingredient sub menu    
def ingredient_menu():
    ##initialize ingredient menu window
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLUE)
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
    win = curses.newwin(20, 75, 2, 2)
    win.bkgd(' ', curses.color_pair(3))
    win.addstr(2,8,"INGREDIENTS",curses.A_UNDERLINE)
    win.keypad(True)
    win.refresh()
    
    cursor = 1;##cursor location
    end = 1;##menu loop condition
    
    ##get user menu input
    while end != 0:
        
        ##highlight cursor location
        if cursor == 1:
            win.addstr(4,8,"List Ingredients",curses.color_pair(1))
        else:
            win.addstr(4,8,"List Ingredients",curses.color_pair(3))
        if cursor == 2:
            win.addstr(6,8,"Add Ingredient",curses.color_pair(1))
        else:
            win.addstr(6,8,"Add Ingredient",curses.color_pair(3))
        if cursor == 3:
            win.addstr(8,8,"Main Menu",curses.color_pair(1))
        else:
            win.addstr(8,8,"Main Menu",curses.color_pair(3))
        win.refresh()
        c = win.getch()
        
        ##DOWN arrow input condition
        if c == curses.KEY_DOWN: 
            if cursor < 3: 
                cursor = cursor + 1
            else:
                cursor = 1
        
        ##UP arrow input condition
        elif c == curses.KEY_UP:
            if cursor > 1:
                cursor = cursor - 1
            else:
                cursor = 3
        
        ##ENTER key input condition
        elif c == 10: ##ASCII value for enter key.  Taken from http://stackoverflow.com/questions/11067800/ncurses-key-enter-is-fail
            if cursor == 1:
                ingredient_list()
            if cursor == 2:
                ingredient_add()
            if cursor == 3:
                end = 0
    
    ##remove ingredient menu window
    win.clear()
    win.refresh()
    win.keypad(False)
    del win

##Ingredient list
def ingredient_list():
    ## set up screen
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLUE)
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
    win = curses.newwin(17, 35, 2, 35)
    win.bkgd(' ', curses.color_pair(3))
    win.addstr(2,10,"     LIST     ",curses.A_UNDERLINE)
    win.border('|','|','-','-','*','*','*','*')
    win.keypad(True)
    win.refresh()
    cursor = 1;
    end = 1;
    
    index = 0 ##cursor index
    while end != 0:
        
        ##Get ingredient list from the database
        db_call = conn.cursor()
        db_call.execute("SELECT ingrname FROM bakery.ingr;") # execute your query
        object_list = []
        object_list = db_call.fetchall() # and store the results in a list
        new_object_list = [str(i)[2:-3] for i in object_list] ##string slicing from http://pythoncentral.io/cutting-and-slicing-strings-in-python/

        ## set cursor location data for each list output and menu option
        
        ##if cursor is on the first list object
        if cursor == 1:
            if index < len(object_list):
                win.addstr(4,10,"-                    ",curses.color_pair(3))
                win.addstr(4,10,str(new_object_list[index]),curses.color_pair(1))
            else:
                win.addstr(4,10,"-                    ",curses.color_pair(1))
        else:
            if index < len(object_list):
                win.addstr(4,10,"-                    ",curses.color_pair(3))
                win.addstr(4,10,str(new_object_list[index]),curses.color_pair(3))
            else:
                win.addstr(4,10,"-                    ",curses.color_pair(3))
            
        ##if cursor is on the second list object
        if cursor == 2:
            if index+1 < len(object_list):
                win.addstr(6,10,"-                    ",curses.color_pair(3))
                win.addstr(6,10,str(new_object_list[index+1]),curses.color_pair(1))
            else:
                win.addstr(6,10,"-                    ",curses.color_pair(1))
        else:
            if index+1 < len(object_list):
                win.addstr(6,10,"-                    ",curses.color_pair(3))
                win.addstr(6,10,str(new_object_list[index+1]),curses.color_pair(3))
            else:
                win.addstr(6,10,"-                    ",curses.color_pair(3))
            
            
        ##if cursor is on the third list object    
        if cursor == 3:
            if index+2 < len(object_list):
                win.addstr(8,10,"-                    ",curses.color_pair(3))
                win.addstr(8,10,str(new_object_list[index+2]),curses.color_pair(1))
            else:
                win.addstr(8,10,"-                    ",curses.color_pair(1))
        else:
            if index+2 < len(object_list):
                win.addstr(8,10,"-                    ",curses.color_pair(3))
                win.addstr(8,10,str(new_object_list[index+2]),curses.color_pair(3))
            else:
                win.addstr(8,10,"-                    ",curses.color_pair(3))
            
            
        ##if cursor is on the fourth list object    
        if cursor == 4:
            if index+3 < len(object_list):
                win.addstr(10,10,"-                    ",curses.color_pair(3))
                win.addstr(10,10,str(new_object_list[index+3]),curses.color_pair(1))
            else:
                win.addstr(10,10,"-                    ",curses.color_pair(1))
        else:
            if index+3 < len(object_list):
                win.addstr(10,10,"-                    ",curses.color_pair(3))
                win.addstr(10,10,str(new_object_list[index+3]),curses.color_pair(3))
            else:
                win.addstr(10,10,"-                    ",curses.color_pair(3))
            
            
        ##if cursor is on the fifth list object    
        if cursor == 5:
            if index+4 < len(object_list):
                win.addstr(12,10,"-                    ",curses.color_pair(3))
                win.addstr(12,10,str(new_object_list[index+4]),curses.color_pair(1))
            else:
                win.addstr(12,10,"-                    ",curses.color_pair(1))
        else:
            if index+4 < len(object_list):
                win.addstr(12,10,"-                    ",curses.color_pair(3))
                win.addstr(12,10,str(new_object_list[index+4]),curses.color_pair(3))
            else:
                win.addstr(12,10,"-                    ",curses.color_pair(3))
            
            
        ##if cursor is on the 'back to menu' option  
        if cursor == 6:
            win.addstr(14,1,"Ingredient Menu",curses.color_pair(1))
        else:
            win.addstr(14,1,"Ingredient Menu",curses.color_pair(3))
            
        ##if cursor is on the 'print out next list objects' option     
        if cursor == 7:
            win.addstr(14,18,"Next",curses.color_pair(1))
        else:
            win.addstr(14,18,"Next",curses.color_pair(3))
            
        ##if cursor is on the 'go to previous list objects' option         
        if cursor == 8:
            win.addstr(14,24,"Back",curses.color_pair(1))
        else:
            win.addstr(14,24,"Back",curses.color_pair(3))
            
            
        win.refresh()
        c = win.getch()
        
        ##if user presses DOWN
        if c == curses.KEY_DOWN:
            if cursor < 6:
                cursor = cursor + 1
            else:
                cursor = 1
                
        ##if user presses UP        
        elif c == curses.KEY_UP:
            if cursor > 1 and cursor < 6:
                cursor = cursor - 1
            elif cursor > 5:
                cursor = 5
            else: 
                cursor = 6
                
        ##if user presses LEFT        
        elif c == curses.KEY_LEFT:
            if cursor == 7 or cursor == 8:
                cursor = cursor - 1
            elif cursor == 6:
                cursor = 8
                
        ##if user presses RIGHT        
        elif c == curses.KEY_RIGHT:
            if cursor == 6 or cursor == 7:
                cursor = cursor + 1
            elif cursor == 8:
                cursor = 6
        
        ##if uses presses ENTER
        elif c == 10: ##ASCII value for enter key.  Taken from http://stackoverflow.com/questions/11067800/ncurses-key-enter-is-fail
           ##ENTER on return to prior menu 
           if cursor == 6:
                end = 0
           ##ENTER on print out more list objects     
           elif cursor == 7:
                if index +5 < len(object_list):
                    index = index + 5
                else:
                    curses.beep()
           ##ENTER on print out previous list objects         
           elif cursor == 8:
                if index  > 0:
                    index = index - 5
                else:
                    curses.beep()

    ##close window
    win.clear()
    win.refresh()
    win.keypad(False)
    del win    

##Check if a name is already in use in the ingredient table
def check_ingr(ingr_name):
    ##Call database and see if ingredient exists
    db_call = conn.cursor()
    db_call.execute("SELECT ingrname FROM bakery.ingr WHERE ingrname ='"+ingr_name+"';") # execute your query
    ##return TRUE if target ingredient name is found in the DB, otherwise return FALSE
    return bool(db_call.rowcount) ##syntax from http://stackoverflow.com/questions/1874113/checking-if-a-postgresql-table-exists-under-python-and-probably-psycopg2
    
##add a new ingredient profile
def ingredient_add():
    
    ##Set up new sub window
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLUE)
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
    input_win = curses.newwin(8, 20, 10, 30)
    input_win.bkgd(' ', curses.color_pair(3))
    input_win.addstr(2,2,"ENTER NAME",curses.A_UNDERLINE)
    input_win.border('|','|','-','-','*','*','*','*')
    curses.noecho()
    input_win.keypad(True)
    input_win.refresh()
    user_input = ''
    finish = 0
    x = 1
    
    ##get user keyboard input
    ##code for limiting keyboard input from http://stackoverflow.com/questions/22646951/input-limit-on-python-curses-getstr
    while finish == 0:
        input_win.border('|','|','-','-','*','*','*','*')
        input_win.refresh()
        char_input = input_win.getch(5,x)
        
        if char_input == 10:
            if len(user_input) > 0:
                finish = 1 
            else:
                finish = 0
        
        elif char_input == 263 :
            if len(user_input) > 0:
                input_win.addstr(5,x-1," ")
                x = x -1
                user_input = user_input[:-1] ##syntax from http://stackoverflow.com/questions/15478127/remove-final-character-from-string-python
            else:
                user_input = user_input ##do nothing

        elif len(user_input) > 15:
            curses.beep()
            
        elif (char_input >= 48 and char_input <= 57) or (char_input >= 65 and char_input <= 90) or (char_input >= 97 and char_input <= 122):
            input_win.addstr(5,x, chr(char_input))
            user_input = user_input + chr(char_input)
            x = x + 1  
    
        else:
            user_input = user_input 
            
    ##marks if user input already exists in DB with '1'        
    already_exists = 0;
    ##assign new ingredient to user input
    new_ingredient_name = user_input ##save name of new ingredient
    
    ##check to see if ingredient already exists
    if check_ingr(new_ingredient_name) == True:
        already_exists = 1
        
    
    ##Call database and add new ingredient profile if already_exists = 0
    if already_exists == 0:
        db_call = conn.cursor()
        db_call.execute("INSERT INTO bakery.ingr VALUES (DEFAULT, '"+user_input+"');") # execute your query  
        db_call.connection.commit() ##commit function from http://twigstechtips.blogspot.com/2010/09/python-psycopg-doesn-insert-or-delete.html
    
    
    ##Print out confirmation message and close sub window
    input_win.clear()
    input_win.refresh()
   
    if already_exists == 0:
        input_win.addstr(2,1,"INGREDIENT ENTERED",curses.A_UNDERLINE)
    else:
        input_win.addstr(2,1,"ERR:ALREADY EXISTS",curses.A_UNDERLINE)
    input_win.border('|','|','-','-','*','*','*','*')
    input_win.addstr(4,2,"-Press Any Key-")
    c = input_win.getch()
    
    input_win.clear()
    input_win.refresh()
    del input_win
    already_exists = 0
    curses.noecho() 
    
##cake sub menu
def cake_menu():
    ##create cake menu window
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLUE)
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
    win = curses.newwin(20, 75, 2, 2)
    win.bkgd(' ', curses.color_pair(3))
    win.addstr(2,8,"CAKES",curses.A_UNDERLINE)
    win.keypad(True)
    win.refresh()
    cursor = 1;##cursor location
    end = 1;##menu loop condition
    
    ##get user menu input
    while end != 0:
        
        ##show cursor location
        if cursor == 1:
            win.addstr(4,8,"List Cakes",curses.color_pair(1))
        else:
            win.addstr(4,8,"List Cakes",curses.color_pair(3))
        if cursor == 2:
            win.addstr(6,8,"Search by Ingredient",curses.color_pair(1))
        else:
            win.addstr(6,8,"Search by Ingredient",curses.color_pair(3))
        if cursor == 3:
            win.addstr(8,8,"Add Cake",curses.color_pair(1))
        else:
            win.addstr(8,8,"Add Cake",curses.color_pair(3))
        if cursor == 4:
            win.addstr(10,8,"Main Menu",curses.color_pair(1))
        else:
            win.addstr(10,8,"Main Menu",curses.color_pair(3))
        
        win.refresh()
        c = win.getch()
        
        ##DOWN button input
        if c == curses.KEY_DOWN: 
            if cursor < 4:
                cursor = cursor + 1
            else:
                cursor = 1
        
        ##UP button input
        elif c == curses.KEY_UP: ##up arrow condition
            if cursor > 1:
                cursor = cursor - 1
            else:
                cursor = 4
        
        ##ENTER key input
        elif c == 10: ##ASCII value for enter key.  Taken from http://stackoverflow.com/questions/11067800/ncurses-key-enter-is-fail
            if cursor == 1:## SELECT Cake list
                cake_list()
            if cursor == 2:## SELECT ingredient filter
                cake_search()
            if cursor == 3:## SELECT cake creation
                cake_add()
            if cursor == 4:## SELECT return to menu
                end = 0
                
    ##remove cake sub menu window
    win.delch(2,8)
    win.delch(4,8)
    win.delch(6,8)
    win.delch(8,8)
    win.delch(10,8)
    win.clear()
    win.refresh()
    win.keypad(False)
    del win

##filter cake list by ingredient
def cake_search():
   
    ##create sub menu window
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLUE)
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
    input_win = curses.newwin(8, 20, 10, 30)
    input_win.bkgd(' ', curses.color_pair(3))
    input_win.addstr(2,2,"ENTER INGREDIENT",curses.A_UNDERLINE)
    input_win.border('|','|','-','-','*','*','*','*')
    curses.noecho()
    input_win.keypad(True)
    input_win.refresh()
    
    ##search filter
    search_term = '' 
    finish = 0 
    x = 1##print location

    ##get user keyboard input for search filter
    ##code outline for limited ncurses string input from http://stackoverflow.com/questions/22646951/input-limit-on-python-curses-getstr
    while finish == 0:
        input_win.border('|','|','-','-','*','*','*','*')
        input_win.refresh()
        char_input = input_win.getch(5,x) ##get next char in filter term
        
        if char_input == 10: ##if ENTER pressed, use entered term if not blank
            if len(search_term) > 0:
                finish = 1 
            else:
                finish = 0
        
        elif char_input == 263 : ##BACKSPACE
            if len(search_term) > 0:
                input_win.addstr(5,x-1," ")
                x = x -1
                search_term = search_term[:-1] ##syntax from http://stackoverflow.com/questions/15478127/remove-final-character-from-string-python
            else:
                search_term = search_term ##do nothing

        elif len(search_term) > 15: ##Search term longer than 15 chars is rejected
            curses.beep()
            
        ##only alphanumeric charaters are printed to the screen
        elif (char_input >= 48 and char_input <= 57) or (char_input >= 65 and char_input <= 90) or (char_input >= 97 and char_input <= 122):
            input_win.addstr(5,x, chr(char_input))
            search_term = search_term + chr(char_input)
            x = x + 1  
    
        else:
            search_term = search_term ##do nothing
    
    ##remove filter input window
    input_win.clear()
    input_win.refresh()
    del input_win
    curses.noecho()
    
    ##print out filtered cake list window 
    win = curses.newwin(17, 35, 2, 35)
    win.bkgd(' ', curses.color_pair(3))
    win.addstr(2,10,"     LIST     ",curses.A_UNDERLINE)
    win.border('|','|','-','-','*','*','*','*')
    win.keypad(True)
    win.refresh()
    
    
    cursor = 1;##cursor location
    end = 1;##menu loop condition
    index = 0##cake profile array index
    
    ##Get list menu input from user
    while end != 0:
        
        ##Get database cake profiles with target ingredient contained in 'search_term'
        db_call = conn.cursor()
        db_call.execute("SELECT cakename FROM bakery.cake INNER JOIN bakery.recipe ON CakeID = Cid INNER JOIN bakery.ingr ON Iid = IngrID WHERE IngrName ='"+search_term+"';") # execute your query, JOIN syntax from http://stackoverflow.com/questions/8779918/postgres-multiple-joins
        object_list = []
        object_list = db_call.fetchall() # and store the results in a list
        new_object_list = [str(i)[2:-3] for i in object_list] ##string slicing from http://pythoncentral.io/cutting-and-slicing-strings-in-python/
        i = 0

        
        ##if cursor is on the first list object
        if cursor == 1:
            if index < len(object_list):
                win.addstr(4,10,"-                    ",curses.color_pair(3))
                win.addstr(4,10,str(new_object_list[index]),curses.color_pair(1))
            else:
                win.addstr(4,10,"-                    ",curses.color_pair(1))
        else:
            if index < len(object_list):
                win.addstr(4,10,"-                    ",curses.color_pair(3))
                win.addstr(4,10,str(new_object_list[index]),curses.color_pair(3))
            else:
                win.addstr(4,10,"-                    ",curses.color_pair(3))
        
        ##if cursor is on the second list object    
        if cursor == 2:
            if index+1 < len(object_list):
                win.addstr(6,10,"-                    ",curses.color_pair(3))
                win.addstr(6,10,str(new_object_list[index+1]),curses.color_pair(1))
            else:
                win.addstr(6,10,"-                    ",curses.color_pair(1))
        else:
            if index+1 < len(object_list):
                win.addstr(6,10,"-                    ",curses.color_pair(3))
                win.addstr(6,10,str(new_object_list[index+1]),curses.color_pair(3))
            else:
                win.addstr(6,10,"-                    ",curses.color_pair(3))
            
        ##if cursor is on the third list object      
        if cursor == 3:
            if index+2 < len(object_list):
                win.addstr(8,10,"-                    ",curses.color_pair(3))
                win.addstr(8,10,str(new_object_list[index+2]),curses.color_pair(1))
            else:
                win.addstr(8,10,"-                    ",curses.color_pair(1))
        else:
            if index+2 < len(object_list):
                win.addstr(8,10,"-                    ",curses.color_pair(3))
                win.addstr(8,10,str(new_object_list[index+2]),curses.color_pair(3))
            else:
                win.addstr(8,10,"-                    ",curses.color_pair(3))
            
            
        ##if cursor is on the fourth list object      
        if cursor == 4:
            if index+3 < len(object_list):
                win.addstr(10,10,"-                    ",curses.color_pair(3))
                win.addstr(10,10,str(new_object_list[index+3]),curses.color_pair(1))
            else:
                win.addstr(10,10,"-                    ",curses.color_pair(1))
        else:
            if index+3 < len(object_list):
                win.addstr(10,10,"-                    ",curses.color_pair(3))
                win.addstr(10,10,str(new_object_list[index+3]),curses.color_pair(3))
            else:
                win.addstr(10,10,"-                    ",curses.color_pair(3))
            
            
        ##if cursor is on the fifth list object      
        if cursor == 5:
            if index+4 < len(object_list):
                win.addstr(12,10,"-                    ",curses.color_pair(3))
                win.addstr(12,10,str(new_object_list[index+4]),curses.color_pair(1))
            else:
                win.addstr(12,10,"-                    ",curses.color_pair(1))
        else:
            if index+4 < len(object_list):
                win.addstr(12,10,"-                    ",curses.color_pair(3))
                win.addstr(12,10,str(new_object_list[index+4]),curses.color_pair(3))
            else:
                win.addstr(12,10,"-                    ",curses.color_pair(3))
            
            
        ##if cursor is on the 'return to prior menu' option      
        if cursor == 6:
            win.addstr(14,4,"Cake Menu",curses.color_pair(1))
        else:
            win.addstr(14,4,"Cake Menu",curses.color_pair(3))
            
        ##if cursor is on the 'print next list objects' option     
        if cursor == 7:
            win.addstr(14,16,"Next",curses.color_pair(1))
        else:
            win.addstr(14,16,"Next",curses.color_pair(3))
            
        ##if cursor is on the 'print prior list objects' option     
        if cursor == 8:
            win.addstr(14,22,"Back",curses.color_pair(1))
        else:
            win.addstr(14,22,"Back",curses.color_pair(3))
            
            
        win.refresh()
        c = win.getch()
        
        ##if user presses DOWN key
        if c == curses.KEY_DOWN:
            if cursor < 6:
                cursor = cursor + 1
            else:
                cursor = 1
                
        ##if user presses UP key        
        elif c == curses.KEY_UP:
            if cursor > 1 and cursor < 6:
                cursor = cursor - 1
            elif cursor > 5:
                cursor = 5
            else: 
                cursor = 6
                
        ##if user presses LEFT key        
        elif c == curses.KEY_LEFT:
            if cursor == 7 or cursor == 8:
                cursor = cursor - 1
            elif cursor == 6:
                cursor = 8
                
        ##if user presses RIGHT key        
        elif c == curses.KEY_RIGHT:
            if cursor == 6 or cursor == 7:
                cursor = cursor + 1
            elif cursor == 8:
                cursor = 6
        
        ##if user presses ENTER key
        elif c == 10: ##ASCII value for enter key.  Taken from http://stackoverflow.com/questions/11067800/ncurses-key-enter-is-fail
           
           ##first list object
           if cursor == 1 and index < len(object_list):
               ##create a cake_entry object to hold the cake profile and display in open_profile() function
               cake_profile = create_cake_obj(str(new_object_list[index]))
               open_profile(cake_profile)
               win.addstr(2,10,"     LIST     ",curses.A_UNDERLINE)
               win.border('|','|','-','-','*','*','*','*')
               win.refresh()
           ##second list object
           elif cursor == 2 and index+1 < len(object_list):
               ##create a cake_entry object to hold the cake profile and display in open_profile() function
               cake_profile = create_cake_obj(str(new_object_list[index+1]))
               open_profile(cake_profile)
               win.addstr(2,10,"     LIST     ",curses.A_UNDERLINE)
               win.border('|','|','-','-','*','*','*','*')
               win.refresh()
           ##third list object
           elif cursor == 3 and index+2 < len(object_list):
               ##create a cake_entry object to hold the cake profile and display in open_profile() function
               cake_profile = create_cake_obj(str(new_object_list[index+2]))
               open_profile(cake_profile)
               win.addstr(2,10,"     LIST     ",curses.A_UNDERLINE)
               win.border('|','|','-','-','*','*','*','*')
               win.refresh()
           ##fourth list object
           elif cursor == 4 and index+3 < len(object_list):
               ##create a cake_entry object to hold the cake profile and display in open_profile() function
               cake_profile = create_cake_obj(str(new_object_list[index+3]))
               open_profile(cake_profile)
               win.addstr(2,10,"     LIST     ",curses.A_UNDERLINE)
               win.border('|','|','-','-','*','*','*','*')
               win.refresh()
           ##fifth list object
           elif cursor == 5 and index+4 < len(object_list):
               ##create a cake_entry object to hold the cake profile and display in open_profile() function
               cake_profile = create_cake_obj(str(new_object_list[index+4]))
               open_profile(cake_profile)
               win.addstr(2,10,"     LIST     ",curses.A_UNDERLINE)
               win.border('|','|','-','-','*','*','*','*')
               win.refresh()
           ##return to prior menu   
           elif cursor == 6:
                end = 0
           ##print next list objects     
           elif cursor == 7:
                if index +5 < len(object_list):
                    index = index + 5
                else:
                    curses.beep()
           ##first prior list object         
           elif cursor == 8:
                if index  > 0:
                    index = index - 5
                else:
                    curses.beep()

    ##remove this sub menu screen
    win.clear()
    win.refresh()
    win.keypad(False)
    del win
 
##Check if a name is already in use in the cake table
def check_cake(cake_name):
    ##Call database and see if cake exists
    db_call = conn.cursor()
    db_call.execute("SELECT CakeName FROM bakery.cake WHERE CakeName ='"+cake_name+"';") # execute your query
    ##return TRUE if target cake name is found in the DB, otherwise return FALSE
    return bool(db_call.rowcount) ##syntax from http://stackoverflow.com/questions/1874113/checking-if-a-postgresql-table-exists-under-python-and-probably-psycopg2 

##add a new cake profile
def cake_add():
    ##set up new sub window
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLUE)
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
    
    input_win = curses.newwin(8, 20, 10, 30)
    input_win.bkgd(' ', curses.color_pair(3))
    input_win.addstr(2,2,"ENTER NAME",curses.A_UNDERLINE)
    input_win.border('|','|','-','-','*','*','*','*')
    curses.noecho()
    input_win.keypad(True)
    input_win.refresh()
    user_input = '' 
    finish = 0
    x = 1
    
    ##get user keyboard input for cake name.
    ##code for limiting input from http://stackoverflow.com/questions/22646951/input-limit-on-python-curses-getstr
    while finish == 0:
        input_win.border('|','|','-','-','*','*','*','*')
        input_win.refresh()
        char_input = input_win.getch(5,x)
        
        if char_input == 10:
            if len(user_input) > 0:
                
                ##marks if user input already exists in DB with '1'        
                already_exists = 0;
                ##check to see if cake name already exists
                if check_cake(user_input) == True:
                    already_exists = 1
                ##complete creation of new cake if user selected name is not in database
                if already_exists == 0:
                    finish = 1 
                ##error message if user selected name already exists in the database
                else:
                    finish = 0
                    input_win2 = curses.newwin(8, 20, 10, 30)
                    input_win2.bkgd(' ', curses.color_pair(3))
                    input_win2.addstr(2,1,"ERR:ALREADY EXISTS",curses.A_UNDERLINE)
                    input_win2.border('|','|','-','-','*','*','*','*')
                    input_win2.addstr(4,2,"-Press Any Key-")
                    c = input_win2.getch()
                    
                    input_win2.clear()
                    input_win2.refresh()
                    del input_win2
                
            else:
                finish = 0
        
        elif char_input == 263 :
            if len(user_input) > 0:
                input_win.addstr(5,x-1," ")
                x = x -1
                user_input = user_input[:-1] ##syntax from http://stackoverflow.com/questions/15478127/remove-final-character-from-string-python
            else:
                user_input = user_input ##do nothing

        elif len(user_input) > 16:
            curses.beep()
            
        elif (char_input >= 48 and char_input <= 57) or (char_input >= 65 and char_input <= 90) or (char_input >= 97 and char_input <= 122) or (char_input == 32):
            input_win.addstr(5,x, chr(char_input))
            user_input = user_input + chr(char_input)
            x = x + 1  
    
        else:
            user_input = user_input ##do nothing
    
    ##save name of new cake
    new_cake_name = user_input 
    
         
    ##Enter the number of ingredients used
    finish = 0
    cursor = 1
    ingredient_count = 0
    

    ##have the user select how many ingredients to use (limit of 10)
    while finish == 0:
        input_win.addstr(2,2,"INGREDIENT COUNT",curses.A_UNDERLINE)
        input_win.addstr(4,4,"  ") ##clear prior text
        input_win.addstr(4,4,str(ingredient_count))
        input_win.addstr(4,6," Ingredients")
        input_win.addstr(5,1,"                ",curses.color_pair(3)) ##clear prior text
        input_win.refresh()
        ##cursor location on <- arrow
        if cursor == 1:
            input_win.addstr(6,1,"  <- ",curses.color_pair(1))
        else:
            input_win.addstr(6,1,"  <- ",curses.color_pair(3))
        ##cursor location on Input option    
        if cursor == 2:
            input_win.addstr(6,7,"Input ",curses.color_pair(1))
        else:
            input_win.addstr(6,7,"Input ",curses.color_pair(3))
        ##cursor location on -> arrow
        if cursor == 3:
            input_win.addstr(6,13," ->  ",curses.color_pair(1))
        else:
            input_win.addstr(6,13," ->  ",curses.color_pair(3))
        
        input_win.refresh()
        c = input_win.getch()
        
        ##if user presses LEFT
        if c == curses.KEY_LEFT:
            if cursor == 1:
                cursor = 3
            else:
                cursor = cursor - 1
        ##if user presses RIGHT
        elif c == curses.KEY_RIGHT:
            if cursor == 3:
                cursor = 1
            else:
                cursor = cursor + 1
        
        ##if user presses ENTER
        elif c == 10:
            ## if on <- option, decrease ingredient count
            if cursor == 1:
                if ingredient_count > 0:
                    ingredient_count = ingredient_count - 1
                else:
                    ingredient_count = ingredient_count ##do nothing
            ## if on 'INPUT' option, proceed to the next menu step
            elif cursor == 2:
                finish = 1
            ## if on -> option, increase ingredient count
            else:
                if ingredient_count < 10:
                    ingredient_count = ingredient_count + 1
                else:
                    ingredient_count = ingredient_count ##do nothing
        else:
            ingredient_count = ingredient_count ##do nothing
    
    ##array of ingredient objects to hold user ingredient input
    ingredient_arr = []     
    
   ##Enter ingredient in new cake recipe 'x' times, where 'x' is the previously chosen ingredient count 
    count_down = 1 ##counts the ingredient number
    x = 1
    
    input_win.addstr(4,1,"                 ",curses.color_pair(3)) ##clear prior text
    input_win.addstr(5,1,"                 ",curses.color_pair(3)) ##clear prior text
    input_win.addstr(6,1,"                 ",curses.color_pair(3)) ##clear prior text
    
    ##get keyboard input for ingredient name
    ##code for limiting input from http://stackoverflow.com/questions/22646951/input-limit-on-python-curses-getstr
    while ingredient_count > 0:
        finish = 0
        x = 1
        input_win.border('|','|','-','-','*','*','*','*')
        input_win.addstr(5,1,"                 ",curses.color_pair(3)) ##clear prior text
        user_input = ""
        input_win.refresh()
        while finish == 0:
            input_win.addstr(2,1,"ENTER INGREDIENT ",curses.A_UNDERLINE)
            input_win.addstr(2,18,str(count_down),curses.A_UNDERLINE)
            input_win.refresh()
            char_input = input_win.getch(5,x)
            
            if char_input == 10:
                if len(user_input) > 0:
                    finish = 1 
                else:
                    finish = 0
            
            elif char_input == 263 :
                if len(user_input) > 0:
                    input_win.addstr(5,x-1," ")
                    x = x -1
                    user_input = user_input[:-1] ##syntax from http://stackoverflow.com/questions/15478127/remove-final-character-from-string-python
                else:
                    user_input = user_input ##do nothing

            elif len(user_input) > 15:
                curses.beep()
                
            elif (char_input >= 48 and char_input <= 57) or (char_input >= 65 and char_input <= 90) or (char_input >= 97 and char_input <= 122):
                input_win.addstr(5,x, chr(char_input))
                user_input = user_input + chr(char_input)
                x = x + 1  
        
            else:
                user_input = user_input ##do nothing
        
        ##save new ingredient name
        new_ingredient_name = user_input
        ##get the unit of measurement
        unit = get_unit()
        ##get ingredient quantity used
        count = get_count()
        
        ##create new ingredient object with name, count, and unit
        ingredient_arr.append(ingredient_entry(new_ingredient_name,count,unit))
        
        ##APPEND NEW INGREDIENT OBJECT TO RECIPIE LIST
   
        count_down = count_down + 1
        ingredient_count = ingredient_count - 1

    ##Create  cake profile object 
    new_cake_entry = cake_entry(new_cake_name,ingredient_arr,0) 

    ##add cake name to cake DB
    db_call = conn.cursor()
    db_call.execute("INSERT INTO bakery.cake VALUES (DEFAULT, '"+new_cake_entry.name+"');") # execute your query  
    db_call.connection.commit() ##commit function from http://twigstechtips.blogspot.com/2010/09/python-psycopg-doesn-insert-or-delete.html
    
    ##get ID of newly created cake
    db_call = conn.cursor()
    db_call.execute("SELECT CakeID FROM bakery.cake WHERE CakeName ='"+new_cake_name+"';") # execute your query
    id_call = []
    id_call = db_call.fetchall() # and store the results in a list
    ID_cake = str(id_call[0])[1:-2]
    
    ##check each ingredient in the new cake   
    for ingr in ingredient_arr:
        ingredient_name = ingr.name
        ##check to see if ingredient in the cake already exists, add to DB if it does not
        if check_ingr(ingredient_name) == False:
            db_call = conn.cursor()
            db_call.execute("INSERT INTO bakery.ingr VALUES (DEFAULT, '"+ingredient_name+"');") # execute your query  
            db_call.connection.commit() ##commit function from http://twigstechtips.blogspot.com/2010/09/python-psycopg-doesn-insert-or-delete.html
        ##Get ingredient ID number:
        db_call = conn.cursor()
        db_call.execute("SELECT IngrID FROM bakery.ingr WHERE IngrName ='"+ingredient_name+"';") # execute your query
        id_call = []
        id_call = db_call.fetchall() 
        ID_ingr = str(id_call[0])[1:-2]
        
        ##add cake and its recipe ingredient to the recipe table
        db_call = conn.cursor()
        db_call.execute("INSERT INTO bakery.recipe VALUES (DEFAULT, "+ingr.count+", '"+ingr.unit+"', "+ID_cake+", "+ID_ingr+");") # execute your query  
        db_call.connection.commit()##commit function from http://twigstechtips.blogspot.com/2010/09/python-psycopg-doesn-insert-or-delete.html
    
    ##remove sub menu window
    input_win.clear()
    input_win.refresh()
    
    input_win.addstr(2,2,"NEW CAKE ENTERED",curses.A_UNDERLINE)
    input_win.border('|','|','-','-','*','*','*','*')
    input_win.addstr(4,2,"-Press Any Key-")
    c = input_win.getch()
    
    input_win.clear()
    input_win.refresh()
    del input_win
  
    curses.noecho() 

 ##get the ingredient count for a cake profile
def get_count():
    
    ##create new window
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLUE)
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
    
    input_win = curses.newwin(8, 20, 10, 30)
    input_win.bkgd(' ', curses.color_pair(3))
    input_win.addstr(2,3,"ENTER QUANTITY",curses.A_UNDERLINE)
    input_win.border('|','|','-','-','*','*','*','*')
    curses.noecho()
    input_win.keypad(True)
    input_win.refresh()
    user_input = '' 
    finish = 0
    x = 1
    
    ##get an integer input from the user
    ##code for limiting input from http://stackoverflow.com/questions/22646951/input-limit-on-python-curses-getstr
    while finish == 0:
        input_win.border('|','|','-','-','*','*','*','*')
        input_win.refresh()
        char_input = input_win.getch(5,x)
        
        if char_input == 10:
            if len(user_input) > 0:
                finish = 1 
            else:
                finish = 0
        
        elif char_input == 263 :
            if len(user_input) > 0:
                input_win.addstr(5,x-1," ")
                x = x -1
                user_input = user_input[:-1] ##syntax from http://stackoverflow.com/questions/15478127/remove-final-character-from-string-python
            else:
                user_input = user_input ##do nothing

        elif len(user_input) > 2:
            curses.beep()
            
        elif (char_input >= 48 and char_input <= 57):
            input_win.addstr(5,x, chr(char_input))
            user_input = user_input + chr(char_input)
            x = x + 1  
    
        else:
            user_input = user_input ##do nothing
    
    ##remove sub menu window
    input_win.clear()
    input_win.refresh()
    del input_win
    
    return user_input 

##get the ingredient unit of measure for a cake profile
def get_unit():
    ##set up new submenu window
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLUE)
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
    
    input_win = curses.newwin(8, 20, 10, 30)
    input_win.bkgd(' ', curses.color_pair(3))
    input_win.addstr(2,1," ENTER MEASUREMENT ",curses.A_UNDERLINE)
    input_win.border('|','|','-','-','*','*','*','*')
    curses.noecho()
    input_win.keypad(True)
    input_win.refresh()
    user_input = '' 
    finish = 0
    x = 1

    ##get keyboard input for ingredient measurment name
    ##code for limiting input from http://stackoverflow.com/questions/22646951/input-limit-on-python-curses-getstr
    while finish == 0:
        input_win.border('|','|','-','-','*','*','*','*')
        input_win.refresh()
        char_input = input_win.getch(5,x)
        
        if char_input == 10:
            if len(user_input) > 0:
                finish = 1 
            else:
                finish = 0
        
        elif char_input == 263 :
            if len(user_input) > 0:
                input_win.addstr(5,x-1," ")
                x = x -1
                user_input = user_input[:-1] ##syntax from http://stackoverflow.com/questions/15478127/remove-final-character-from-string-python
            else:
                user_input = user_input ##do nothing

        elif len(user_input) > 10:
            curses.beep()
            
        elif (char_input >= 48 and char_input <= 57) or (char_input >= 65 and char_input <= 90) or (char_input >= 97 and char_input <= 122):
            input_win.addstr(5,x, chr(char_input))
            user_input = user_input + chr(char_input)
            x = x + 1  
    
        else:
            user_input = user_input ##do nothing
    
    ##save name of new measurement    
    input_win.clear()
    input_win.refresh()
    del input_win
    return user_input;

##list out cakes in database    
def cake_list():

    ##Set up sub menu screen
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLUE)
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
    win = curses.newwin(17, 35, 2, 35)
    win.bkgd(' ', curses.color_pair(3))
    win.addstr(2,10,"     LIST     ",curses.A_UNDERLINE)
    win.border('|','|','-','-','*','*','*','*')
    win.keypad(True)
    win.refresh()
    
    cursor = 1;##cursor location
    end = 1;##menu loop condition
    index = 0##cake profile array index
    
    ##Get list menu input from user
    while end != 0:
        
        ##Get database cake profile names
        db_call = conn.cursor()
        db_call.execute("SELECT cakename FROM bakery.cake;") # execute your query
        object_list = []
        object_list = db_call.fetchall() # and store the results in a list
        new_object_list = [str(i)[2:-3] for i in object_list] ##string slicing from http://pythoncentral.io/cutting-and-slicing-strings-in-python/
        i = 0

        
        ##if cursor is on the first list object
        if cursor == 1:
            win.addstr(4,10,"-                    ",curses.color_pair(3))
            win.addstr(4,10,str(new_object_list[index]),curses.color_pair(1))
        else:
            win.addstr(4,10,"-                    ",curses.color_pair(3))
            win.addstr(4,10,str(new_object_list[index]),curses.color_pair(3))
        
        
        ##if cursor is on the second list object    
        if cursor == 2:
            if index+1 < len(object_list):
                win.addstr(6,10,"-                    ",curses.color_pair(3))
                win.addstr(6,10,str(new_object_list[index+1]),curses.color_pair(1))
            else:
                win.addstr(6,10,"-                    ",curses.color_pair(1))
        else:
            if index+1 < len(object_list):
                win.addstr(6,10,"-                    ",curses.color_pair(3))
                win.addstr(6,10,str(new_object_list[index+1]),curses.color_pair(3))
            else:
                win.addstr(6,10,"-                    ",curses.color_pair(3))
            
        ##if cursor is on the third list object      
        if cursor == 3:
            if index+2 < len(object_list):
                win.addstr(8,10,"-                    ",curses.color_pair(3))
                win.addstr(8,10,str(new_object_list[index+2]),curses.color_pair(1))
            else:
                win.addstr(8,10,"-                    ",curses.color_pair(1))
        else:
            if index+2 < len(object_list):
                win.addstr(8,10,"-                    ",curses.color_pair(3))
                win.addstr(8,10,str(new_object_list[index+2]),curses.color_pair(3))
            else:
                win.addstr(8,10,"-                    ",curses.color_pair(3))
            
            
        ##if cursor is on the fourth list object      
        if cursor == 4:
            if index+3 < len(object_list):
                win.addstr(10,10,"-                    ",curses.color_pair(3))
                win.addstr(10,10,str(new_object_list[index+3]),curses.color_pair(1))
            else:
                win.addstr(10,10,"-                    ",curses.color_pair(1))
        else:
            if index+3 < len(object_list):
                win.addstr(10,10,"-                    ",curses.color_pair(3))
                win.addstr(10,10,str(new_object_list[index+3]),curses.color_pair(3))
            else:
                win.addstr(10,10,"-                    ",curses.color_pair(3))
            
            
        ##if cursor is on the fifth list object      
        if cursor == 5:
            if index+4 < len(object_list):
                win.addstr(12,10,"-                    ",curses.color_pair(3))
                win.addstr(12,10,str(new_object_list[index+4]),curses.color_pair(1))
            else:
                win.addstr(12,10,"-                    ",curses.color_pair(1))
        else:
            if index+4 < len(object_list):
                win.addstr(12,10,"-                    ",curses.color_pair(3))
                win.addstr(12,10,str(new_object_list[index+4]),curses.color_pair(3))
            else:
                win.addstr(12,10,"-                    ",curses.color_pair(3))
            
            
        ##if cursor is on the 'return to prior menu' option      
        if cursor == 6:
            win.addstr(14,4,"Cake Menu",curses.color_pair(1))
        else:
            win.addstr(14,4,"Cake Menu",curses.color_pair(3))
            
        ##if cursor is on the 'print next list objects' option     
        if cursor == 7:
            win.addstr(14,16,"Next",curses.color_pair(1))
        else:
            win.addstr(14,16,"Next",curses.color_pair(3))
            
        ##if cursor is on the 'print prior list objects' option     
        if cursor == 8:
            win.addstr(14,22,"Back",curses.color_pair(1))
        else:
            win.addstr(14,22,"Back",curses.color_pair(3))
            
            
        win.refresh()
        c = win.getch()
        
        ##if user presses DOWN key
        if c == curses.KEY_DOWN:
            if cursor < 6:
                cursor = cursor + 1
            else:
                cursor = 1
                
        ##if user presses UP key        
        elif c == curses.KEY_UP:
            if cursor > 1 and cursor < 6:
                cursor = cursor - 1
            elif cursor > 5:
                cursor = 5
            else: 
                cursor = 6
                
        ##if user presses LEFT key        
        elif c == curses.KEY_LEFT:
            if cursor == 7 or cursor == 8:
                cursor = cursor - 1
            elif cursor == 6:
                cursor = 8
                
        ##if user presses RIGHT key        
        elif c == curses.KEY_RIGHT:
            if cursor == 6 or cursor == 7:
                cursor = cursor + 1
            elif cursor == 8:
                cursor = 6
        
        ##if user presses ENTER key
        elif c == 10: ##ASCII value for enter key.  Taken from http://stackoverflow.com/questions/11067800/ncurses-key-enter-is-fail
           
           ##first list object
           if cursor == 1:
               ##create a cake_entry object to hold the cake profile and display in open_profile() function
               cake_profile = create_cake_obj(str(new_object_list[index]))
               open_profile(cake_profile)
               win.addstr(2,10,"     LIST     ",curses.A_UNDERLINE)
               win.border('|','|','-','-','*','*','*','*')
               win.refresh()
           ##second list object
           elif cursor == 2 and index+1 < len(object_list):
               ##create a cake_entry object to hold the cake profile and display in open_profile() function
               cake_profile = create_cake_obj(str(new_object_list[index+1]))
               open_profile(cake_profile)
               win.addstr(2,10,"     LIST     ",curses.A_UNDERLINE)
               win.border('|','|','-','-','*','*','*','*')
               win.refresh()
           ##third list object
           elif cursor == 3 and index+2 < len(object_list):
               ##create a cake_entry object to hold the cake profile and display in open_profile() function
               cake_profile = create_cake_obj(str(new_object_list[index+2]))
               open_profile(cake_profile)
               win.addstr(2,10,"     LIST     ",curses.A_UNDERLINE)
               win.border('|','|','-','-','*','*','*','*')
               win.refresh()
           ##fourth list object
           elif cursor == 4 and index+3 < len(object_list):
               ##create a cake_entry object to hold the cake profile and display in open_profile() function
               cake_profile = create_cake_obj(str(new_object_list[index+3]))
               open_profile(cake_profile)
               win.addstr(2,10,"     LIST     ",curses.A_UNDERLINE)
               win.border('|','|','-','-','*','*','*','*')
               win.refresh()
           ##fifth list object
           elif cursor == 5 and index+4 < len(object_list):
               ##create a cake_entry object to hold the cake profile and display in open_profile() function
               cake_profile = create_cake_obj(str(new_object_list[index+4]))
               open_profile(cake_profile)
               win.addstr(2,10,"     LIST     ",curses.A_UNDERLINE)
               win.border('|','|','-','-','*','*','*','*')
               win.refresh()
           ##return to prior menu   
           elif cursor == 6:
                end = 0
           ##print next list objects     
           elif cursor == 7:
                if index +5 < len(object_list):
                    index = index + 5
                else:
                    curses.beep()
           ##first prior list object         
           elif cursor == 8:
                if index  > 0:
                    index = index - 5
                else:
                    curses.beep()

    ##remove this sub menu screen
    win.clear()
    win.refresh()
    win.keypad(False)
    del win

##create an object from the class cake_entry
def create_cake_obj(name):
    
    ##get the cake name
    input_name = name
    
    ##get the cake ID
    db_call = conn.cursor()
    db_call.execute("SELECT CakeID FROM bakery.cake WHERE CakeName ='"+name+"';") # execute your query
    id_call = []
    id_call = db_call.fetchall() # and store the results in a list
    ID_string = str(id_call[0])[1:-2]
    
    ##get the cake ingredients and store the results in a list of ingredient_entry objects
    db_call = conn.cursor()
    db_call.execute("SELECT Quantity, Unit, IngrName FROM bakery.recipe, bakery.ingr WHERE Cid='"+ID_string+"' AND IngrID = Iid;") # execute your query
    object_list = []
    object_list = db_call.fetchall() # 
    
    ##list of ingredient_entry objects
    ingredient_list = []
    for i in object_list:
        ingr_data = i
        ingredient_list.append(ingredient_entry(str(ingr_data[2]),str(ingr_data[0]),str(ingr_data[1]))) ##tuple extraction method from http://stackoverflow.com/questions/21662532/python-list-indices-must-be-integers-not-tuple
    
    ##create cake entry object using new ingredient entry list, input cake name, and input cake ID number
    cake_object = cake_entry(input_name,ingredient_list,ID_string)
    
    return cake_object
       
##Open a cake profile    
def open_profile(input_profile):
    
    ##set up menu window
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLUE)
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
    win = curses.newwin(17, 35, 2, 35)
    win.bkgd(' ', curses.color_pair(3))
    win.addstr(2,10,input_profile.name,curses.A_UNDERLINE)
    win.border('|','|','-','-','*','*','*','*')
    win.keypad(True)
    win.refresh()
    cursor = 1;
    end = 1;
 
    y = 3
    x = 3
    
    ##print out ingredients
    for i in range (len(input_profile.ingredients)):

        x = 3
        y = y + 1
        ingredient_name = input_profile.ingredients[i].name
        ingredient_count = input_profile.ingredients[i].count
        ingredient_unit = input_profile.ingredients[i].unit
        ingredient_ouput = "-" +ingredient_count + " " + ingredient_unit + " " + ingredient_name
        win.addstr(y,x,ingredient_ouput,curses.color_pair(3))
        
    
    win.refresh()
    
    finish = 0
    cursor = 2
    

    ##print out menu options
    while finish == 0:
        win.refresh()
        if cursor == 1:
            win.addstr(14,2,"Delete Cake",curses.color_pair(1))
        else:
            win.addstr(14,2,"Delete Cake",curses.color_pair(3))
            
        if cursor == 2:
            win.addstr(14,14,"Return to List ",curses.color_pair(1))
        else:
            win.addstr(14,14,"Return to List ",curses.color_pair(3))
        
        
        win.refresh()
        c = win.getch()
        
        ##if user presses LEFT key
        if c == curses.KEY_LEFT:
            if cursor == 1:
                cursor = 2
            else:
                cursor = 1
        ##if user presses RIGHT key
        elif c == curses.KEY_RIGHT:
            if cursor == 2:
                cursor = 1
            else:
                cursor = 2
        ##if user presses ENTER key
        elif c == 10:
            ##select DELETe option
            if cursor == 1:
                delete_cake(input_profile)
                win.border('|','|','-','-','*','*','*','*')
                win.refresh()
                finish = 1
            ##exit this sub menu
            else:
                finish = 1
        else:
            cursor = cursor ##do nothing
            
    ##clear this sub menu        
    win.clear()
    win.refresh()
    win.keypad(False)
    del win

##remove a cake profile    
def delete_cake(target):
    
    ##set up sub menu window
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLUE)
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
    
    input_win = curses.newwin(8, 20, 10, 30)
    input_win.bkgd(' ', curses.color_pair(3))
    input_win.addstr(2,2," ARE YOU SURE? ",curses.A_UNDERLINE)
    input_win.border('|','|','-','-','*','*','*','*')
    curses.noecho()
    input_win.keypad(True)
    input_win.refresh()
   
    finish = 0
    cursor = 2
    

    
    while finish == 0:
        input_win.refresh()
        ##if cursor is on the 'YES' option
        if cursor == 1:
            input_win.addstr(5,4,"YES",curses.color_pair(1))
        else:
            input_win.addstr(5,4,"YES",curses.color_pair(3))
        ##if cursor is on the 'NO' option    
        if cursor == 2:
            input_win.addstr(5,9,"NO",curses.color_pair(1))
        else:
            input_win.addstr(5,9,"NO",curses.color_pair(3))
        
        
        input_win.refresh()
        c = input_win.getch()
        
        ##if user presses LEFT key
        if c == curses.KEY_LEFT:
            if cursor == 1:
                cursor = 2
            else:
                cursor = 1
        ##if user presses RIGHT key
        elif c == curses.KEY_RIGHT:
            if cursor == 2:
                cursor = 1
            else:
                cursor = 2
        ##if user presses ENTER key
        elif c == 10:
            ##'YES' (to delete) selected
            if cursor == 1:
                 input_win.addstr(4,2,"  CAKE DELETED  ",curses.color_pair(3))
                 input_win.addstr(5,2,"-Press Any Key-")
                 input_win.refresh()
                 c = input_win.getch()
                 ##NEED TO REMOVE CAKE FROM DATABASE HERE
                 db_call = conn.cursor()
                 # delete foreign key from Recipe table first due to constraints
                 db_call.execute("DELETE FROM bakery.recipe WHERE Cid=%s;", (target.id))
                 db_call.connection.commit() ##commit function from http://twigstechtips.blogspot.com/2010/09/python-psycopg-doesn-insert-or-delete.html
                 db_call.execute("DELETE FROM bakery.cake WHERE CakeID=%s;", (target.id)) # execute your query
                 db_call.connection.commit() ##commit function from http://twigstechtips.blogspot.com/2010/09/python-psycopg-doesn-insert-or-delete.html
                 finish = 1
                 
            ##'NO' (to delete) selected
            else:
               finish = 1
        else:
            cursor = cursor ##do nothing
            
    ##clear this sub menu window
    input_win.clear()
    input_win.refresh()
    del input_win
    cake_list()
 
##cake profile object 
class cake_entry:
    def __init__(self,input_name, input_ingredients, input_id):
        self.name = input_name
        self.ingredients = input_ingredients
        self.id = input_id
 
 ##ingredient object for cake profile
class ingredient_entry:
    def __init__(self,input_name, count, unit):
        self.name = input_name
        self.count = count
        self.unit = unit
 
if __name__ == "__main__":
    main()
    
