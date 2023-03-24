import sys
import os
import getpass
import tkinter as tk
from tkinter import ttk
import tkinter.font as font
import textwrap
import time

#import functions for searching
import search_functions

###############
##### Main tkinter class used to switch between two tabs
###############
class SearchConverter(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        #title of gui
        self.title("Search Engine")
        self.columnconfigure(0, weight=1)
        self.frames = dict()
        
        #main container to put sub frames in
        container = ttk.Frame(self)
        container.grid(padx=60, pady=15, sticky="NSEW", columnspan=1)
        container.columnconfigure(0, weight=1)
        container.rowconfigure(0, weight=1)
        
        #configure set up of both frames we are making a class for
        for FrameClass in (ContextualSearch, LiteralSearch):
            frame = FrameClass(container, self)
            self.frames[FrameClass] = frame
            frame.grid(row=0, column=0, sticky="NSEW", columnspan=1, rowspan=1)
            frame.columnconfigure(0, weight=1)
            frame.rowconfigure(0, weight=1)
        
        #start on the contextual question-answer pipeline
        self.show_frame(ContextualSearch)
        
    def show_frame(self, container):
        """
        Bind return key to the calculate function and raise the new frame to the top after switching.
        """
        frame = self.frames[container]
        self.bind('<Return>', frame.submit)
        #self.bind('<KP_Enter', frame.submit)
        frame.tkraise()
        
###############
##### Tab for contextual question-answer pipeline
###############
class ContextualSearch(ttk.Frame):
    def __init__(self, container, controller, **kwargs):
        super().__init__(container, **kwargs)
        
        #set up a label and entry box for the user to input their question
        self.question = tk.StringVar()
        question_label = ttk.Label(self, text="Question: ")
        question_input = ttk.Entry(self, width=20, textvariable=self.question, font=("Segoe UI", 11))
        question_label.grid(row=0, column=0, sticky="W")
        question_input.grid(row=1, column=0, sticky="NSEW")
        question_input.columnconfigure(0, weight=1)
        
        #set up a large text box for the pipeline to output question answers and context
        output_box_label = ttk.Label(self, text="Output: ")
        output_box_label.grid(row=2, column=0, sticky="W")
        self.output_box = tk.Text(self, height=25, wrap=tk.WORD,
                                  background="white", font=("Segoe UI", 10))
        self.output_box.grid(row=3, column=0, sticky="EW")
        self.output_box.columnconfigure(0, weight=1)
        
        #create another frame to put our buttons
        buttons = tk.Frame(self)
        buttons.grid(row=4, column=0, sticky="E")
        
        #submit button
        sub_button = ttk.Button(buttons, text="Enter", command=self.submit)
        sub_button.grid(row=0, column=0, sticky="E")
        
        #switch page button
        switch_button = ttk.Button(buttons, text="Change Tab",
                                    command=lambda:controller.show_frame(LiteralSearch))
        switch_button.grid(row=0, column=1, sticky="E")
        
        #add padding to all parts of main tk frame
        for child in self.winfo_children():
            child.grid_configure(padx=2, pady=0.5)
            
    def submit(self, *args):
        #delete text from entry box every time the submit button is clicked
        self.output_box.delete('1.0', tk.END)
        #retrieve input question
        contextual_question = self.question.get()
        #send question to QA pipeline
        results = search_functions.query_faiss_index('C:/Users/dylan/OneDrive/Documents/search_engine/LoTR_Faiss_Index', contextual_question)
        
        if contextual_question != '':
            self.output_box.insert(tk.END, f"Question: {contextual_question}\n\n")
            if len(results) != 0:
                for result in results:
                    self.output_box.insert(tk.END, "-"*200)
                    self.output_box.insert(tk.END, f"\nAnswer: {result[0]}\n")
                    self.output_box.insert(tk.END, f"Score: {result[2]}\n")
                    self.output_box.insert(tk.END, f"Context: {result[1]}\n")
                    self.output_box.insert(tk.END, "-"*200 + "\n\n")
            else:
                self.output_box.insert(tk.END, "No answers found.")
                
###############
##### Tab for whoosh search engine pipeline
###############
class LiteralSearch(ttk.Frame):
    def __init__(self, container, controller, **kwargs):
        super().__init__(container, **kwargs)
        
        #set up a label and entry box for the user to input their question
        self.search = tk.StringVar()
        search_label = ttk.Label(self, text="Search: ")
        search_input = ttk.Entry(self, width=20, textvariable=self.search, font=("Segoe UI", 11))
        search_label.grid(row=0, column=0, sticky="W")
        search_input.grid(row=1, column=0, sticky="NSEW")
        search_input.columnconfigure(0, weight=1)
        
        #set up a large text box for the pipeline to output question answers and context
        search_output_box_label = ttk.Label(self, text="Output: ")
        search_output_box_label.grid(row=2, column=0, sticky="W")
        self.search_output_box = tk.Text(self, height=25, wrap=tk.WORD,
                                  background="white", font=("Segoe UI", 10))
        self.search_output_box.grid(row=3, column=0, sticky="EW")
        self.search_output_box.columnconfigure(0, weight=1)
        
        #create another frame to put our buttons
        buttons = tk.Frame(self)
        buttons.grid(row=4, column=0, sticky="E")
        
        #submit button
        sub_button = ttk.Button(buttons, text="Enter", command=self.submit)
        sub_button.grid(row=0, column=0, sticky="E")
        
        #switch page button
        switch_button = ttk.Button(buttons, text="Change Tab",
                                    command=lambda:controller.show_frame(ContextualSearch))
        switch_button.grid(row=0, column=1, sticky="E")
        
        #add padding to all parts of main tk frame
        for child in self.winfo_children():
            child.grid_configure(padx=2, pady=0.5)
            
    def submit(self, *args):
        #delete text from entry box every time the submit button is clicked
        self.search_output_box.delete('1.0', tk.END)
        #retrieve input question
        literal_search = self.search.get()
        #search whoosh index
        query, results = search_functions.query_index('C:/Users/dylan/OneDrive/Documents/search_engine/LordOfTheRingsWhooshIndex', literal_search)
        
        if literal_search != '':
            self.search_output_box.insert(tk.END, f"Query: {query}\n\n")
            if len(results) != 0:
                for hit in results:
                    self.search_output_box.insert(tk.END, "-"*200)
                    self.search_output_box.insert(tk.END, f"\nPage: {hit[0]}\n")
                    self.search_output_box.insert(tk.END, f"Content:\n{hit[2]}\n")
                    self.search_output_box.insert(tk.END, "-"*200 + "\n\n")
            else:
                self.search_output_box.insert(tk.END, "-"*200)
                
root = SearchConverter()
root.geometry("1175x640")
root.eval("tk::PlaceWindow . center")
font.nametofont("TkDefaultFont").configure(size=11)
root.columnconfigure(0, weight=1)
root.mainloop()