import os
import pandas as pd
import datetime, curses, requests, os
import requests
import numpy as np
import pandas as pd
#from io import StringIO
#from rtlsdr import RtlSdr

def draw_menu(stdscr, title, options, selected_idx):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    stdscr.addstr(1, 2, title, curses.A_BOLD | curses.A_UNDERLINE)
    for idx, option in enumerate(options):
        x = 4
        y = 3 + idx
        if idx == selected_idx:
            stdscr.attron(curses.A_REVERSE)
            stdscr.addstr(y, x, option)
            stdscr.attroff(curses.A_REVERSE)
        else:
            stdscr.addstr(y, x, option)
    stdscr.refresh()

def menu(stdscr, title, options):
    current_idx = 0
    while True:
        draw_menu(stdscr, title, options, current_idx)
        key = stdscr.getch()
        if key == curses.KEY_UP:
            current_idx = (current_idx - 1) % len(options)
        elif key == curses.KEY_DOWN:
            current_idx = (current_idx + 1) % len(options)
        elif key in (curses.KEY_ENTER, 10, 13):
            return current_idx

def get_input(stdscr, prompt):
    stdscr.clear()
    stdscr.addstr(2, 2, prompt)
    stdscr.refresh()
    curses.echo()
    input_bytes = stdscr.getstr(4, 2, 60)  # get up to 60 characters
    curses.noecho()
    return input_bytes.decode('utf-8').strip()


class Attribute(object):
    attribute_columns = ["Name", "Description"]

    def __init__(self, name):
        self.name = name
        self.filename = f"{name}.csv"
        if os.path.exists(self.filename):
            self.df = pd.read_csv(self.filename)
        else:
            self.df = pd.DataFrame(columns=self.attribute_columns)
        
    def make_new(self, stdscr):
        name        = get_input(stdscr, f"Enter {self.name} name:")
        description = get_input(stdscr, f"Enter {self.name} description:")
        new_row = {"Name": name, "Description": description}
        self.df = pd.concat([self.df, pd.DataFrame([new_row])], ignore_index=True)
        self.df.to_csv(self.filename, index=False)
        self.selected = name
        return name

    def select(self, stdscr):
        selection_list = list(self.df["Name"]) if not self.df.empty else []
        selection_list.append(f"Create new {self.name}")
        selected_idx = menu(stdscr, f"Select a {self.name}", selection_list)
        if selected_idx == len(selection_list) - 1:
            selected = self.make_new(stdscr)
        else:
            selected = selection_list[selected_idx]
        self.selected = selected
        return selected
        

class Antenna(Attribute):

    attribute_columns = ["Name", "Type", "Feed_Diameter"]

    def __init__(self):
        super().__init__("antenna")

    def make_new(self, stdscr):
        name     = get_input(stdscr, "Enter antenna name:")
        ant_type = get_input(stdscr, "Enter antenna type:")
        diameter = get_input(stdscr, "Enter feed line diameter:")
        new_row = {"Name": name, "Type": ant_type, "Feed_Diameter": diameter}
        self.df = pd.concat([self.df, pd.DataFrame([new_row])], ignore_index=True)
        self.df.to_csv(self.filename, index=False)
        self.selected = name
        return name

class Location(Attribute):

    def __init__(self):
        super().__init__("location")

class Orientation(Attribute):

    def __init__(self):
        super().__init__("orientation")
