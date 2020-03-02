import os
import reminder
import datetime
import file_io as fio
import string

string.ascii_uppercase

def main():
    app = MainWindow()

class MainWindow:
    def __init__(self):
        # self.print_header()
        self.remDict = {}
        self.populate_reminder_list()

    def populate_reminder_list(self):
        self.print_header()
        self.reminders = self.load_data()
        self.reminders = self.update_items_in_listview(self.reminders)
        self.reminders = reminder.sort_assignments(self.reminders)
        for i, item in enumerate(self.reminders):
            self.remDict[i + 1] = item
            print("* [{}] {} ".format(i + 1, self.format_list_string(item)))
        self.input_interface('ls')
        
    def clear_screen(self):
        if os.name == 'nt':
            _ = os.system('cls')
        else:
            _ = os.system('clear')

    def format_list_string(self, obj):
        titleLen = len(obj.title)
        dueLen = len(obj.time_till_due)
        totalLen = len(self.headerString) - 6
        spacer = ""
        if (titleLen + (dueLen+2)) <= totalLen:
            for i in range(totalLen - ((dueLen+2) + titleLen)):
                spacer += " "
            return "{}{}({})".format(obj.title, spacer, obj.time_till_due)
        elif (titleLen + (dueLen+2)) > totalLen:
            return "{}{}{}({})".format(obj.title[0:23], '...', spacer, obj.time_till_due)

    def print_header(self, name="Patrick Tumulty"):
        self.clear_screen()
        today = datetime.datetime.today().strftime("%m / %d / %Y")
        self.headerString = "*  {}  |  {}  |  {}  *".format("My Daily Q", name, today)
        self.line = ""
        c, r = os.get_terminal_size()
        # for i in range(len(self.headerString)-1):
        for i in range(c):
            self.line += "-"
        print(self.line)
        print(self.headerString)
        print(self.line)

    def input_interface(self, mode):
        print(self.line)
        if mode == 'ls':
            print("View Item [#] or [A]dd new Item")
            print("If your done you can E[X]it")
            while(True):
                uip = input(">>> ")
                if uip.upper() == "A":
                    self.print_add_window()
                    break
                elif uip.upper() == "X":
                    self.clear_screen()
                    print("** Goodbye! **")
                    self.save_data()
                    break
                elif uip.isdigit() == False and uip != "A" and uip != "X":
                    print("Input Not Recognized...")
                elif uip.isdigit() == True:
                    if int(uip) > len(self.reminders):
                        print("Input Out of Range...")
                    elif int(uip) in self.remDict.keys():
                        self.selected_item = self.remDict[int(uip)]
                        self.print_detail_window(self.selected_item)
                        break
        elif mode == 'dw':
            print("[R]eturn | [D]elete | [C]omplete")
            while(True):
                uip = input(">>> ")
                if uip.upper() == "R":
                    self.populate_reminder_list()
                    break
                elif uip.upper() == "D":
                    self.reminders.remove(self.selected_item)
                    self.save_data()
                    self.populate_reminder_list()
                    break
                elif uip.upper() == "C":
                    self.selected_item.completion_status = True
                    self.save_data()
                    self.populate_reminder_list()
                    break
                else:
                    print("Input Not Recognized...")

    def print_detail_window(self, obj):
        self.print_header()
        print("{}\n\n{}\n\nDue Date:    {}\nDateCreated: {}".format(self.wrap_text(obj.title, len(self.line)), self.wrap_text(obj.description,len(self.line)), obj.due_date.date(), obj.date_created.date()))
        self.input_interface('dw')

    def wrap_text(self, text, width):
        if len(text) <= width:
            return text
        else:
            ftext = ""
            linNum = int(len(text)/width)
            for i in range(linNum):
                if i == 0:
                    ftext = text[0:width] + "\n"
                else:
                    ftext += text[(i * width):(i * width)+width] + "\n"  
            ftext += text[(width*(linNum - 1)) + width:]
        return ftext  

    def print_add_window(self):
        self.clear_screen()
        self.print_header()
        title = input("Title : ")
        description = input("Description : ")
        print("* Enter Due Date *")
        while(True):
            #TODO: input a "c" command which stands for current month. Same 'C' command for year
            month = input("Month : ")
            #TODO: Add command for quickly adding a 1 week time interval (So I don't always have to look up date)
            day = input("Day : ")
            year = input("Year : ")
            if month.isdigit() == True and day.isdigit() == True and year.isdigit() is True:
                break
            else:
                print("Invalid Input")
                print("Please enter whole number integers for the month day and year")
                print("Example: September 18, 2019 >>> M = 9, D = 18, Y = 2019")
        rem = reminder.Assignment(title, description)
        rem.set_due_date(int(day), int(month), int(year))
        rem.update_time_till_due()
        self.print_obj(rem)
        print(self.line)
        print("[S]ave or [C]ancel")
        while(True):
            uip = input(">>> ")
            if uip.upper() == "S":
                self.reminders.append(rem)
                self.save_data()
                self.reminders = self.load_data()
                self.populate_reminder_list()
                break
            elif uip.upper() == "C":
                self.populate_reminder_list()
                break
            else:
                print("Input Not Recognized...")

    def print_obj(self, obj):
        self.clear_screen()
        self.print_header()
        print("{}\n\n{}\n\nDue Date:    {}\nDateCreated: {}".format(self.wrap_text(obj.title, len(self.line)), self.wrap_text(obj.description,len(self.line)), obj.due_date.date(), obj.date_created.date()))

    def update_items_in_listview(self, assignments):
        for obj in assignments:
            obj.update_time_till_due()
        return assignments

    def load_data(self):
        return fio.load("assignments")

    def save_data(self):
        fio.save('assignments', self.reminders)
 

if __name__ == "__main__":
    main()