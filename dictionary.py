import json
import tkinter as tk
from tkinter import messagebox
from difflib import get_close_matches

class DictionaryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ai Dictionary App")
        self.root.geometry("700x500")
        self.root.configure(bg="#f0f0f0")

        # Loads data from JSON file
        self.data = json.load(open("data.json"))

        # Create widgets
        self.label = tk.Label(root, text="Enter a word:", font=("Arial", 14), bg="#f0f0f0", fg="#333333")
        self.entry = AutocompleteEntry(root, self.data.keys(), font=("Arial", 14), bg="white", fg="#333333")
        self.result_text = tk.Text(root, height=15, width=60, font=("Arial", 12), bg="white", fg="#333333")
        self.search_button = tk.Button(root, text="Search", command=self.search_word, font=("Arial", 12), bg="#4CAF50", fg="white")
        self.clear_button = tk.Button(root, text="Clear", command=self.clear_fields, font=("Arial", 12), bg="#f44336", fg="white")
        self.status_label = tk.Label(root, text="", font=("Arial", 12), fg="red", bg="#f0f0f0")

        # Grid layout
        self.label.grid(row=0, column=0, padx=10, pady=(20, 5), sticky="e")
        self.entry.grid(row=0, column=1, padx=(0, 10), pady=(20, 5), sticky="ew")
        self.result_text.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        self.search_button.grid(row=2, column=0, padx=10, pady=(5, 10), sticky="ew")
        self.clear_button.grid(row=2, column=1, padx=10, pady=(5, 10), sticky="ew")
        self.status_label.grid(row=3, column=0, columnspan=2, padx=10, pady=(0, 20))

        # Configure grid weights
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

    def search_word(self):
        word = self.entry.get().lower()
        output = self.translate(word)

        self.result_text.delete(1.0, tk.END)  # Clear previous results
        self.status_label.config(text="")  # Clear previous status

        if type(output) == list:
            for idx, item in enumerate(output, start=1):
                self.result_text.insert(tk.END, f"{idx}. {item}\n")
        else:
            self.result_text.insert(tk.END, output)

    def translate(self, word):
        if word in self.data:
            return self.data[word]
        elif len(get_close_matches(word, self.data.keys())) > 0:
            suggested_word = get_close_matches(word, self.data.keys())[0]
            yn = messagebox.askquestion("Did you mean?", f"Did you mean {suggested_word} instead?")  # Use messagebox from imported module
            if yn == "yes":
                return self.data[suggested_word]
            else:
                return "The word doesn't exist. Please double-check it."
        else:
            return "The word is not in this dictionary."

    def clear_fields(self):
        self.entry.delete(0, tk.END)
        self.result_text.delete(1.0, tk.END)
        self.status_label.config(text="")

class AutocompleteEntry(tk.Entry):
    def __init__(self, master, word_list, **kwargs):
        self.word_list = word_list
        self.var = tk.StringVar()
        tk.Entry.__init__(self, master, textvariable=self.var, **kwargs)
        self.var.trace('w', self.autocomplete)

    def autocomplete(self, *args):
        entered_text = self.var.get()
        if len(entered_text) == 0:
            self.autocomplete_listbox_update([])
        else:
            matches = self.get_matches(entered_text)
            self.autocomplete_listbox_update(matches)

    def get_matches(self, entered_text):
        matches = []
        for word in self.word_list:
            if word.startswith(entered_text):
                matches.append(word)
        return matches

    def autocomplete_listbox_update(self, matches):
        if matches:
            if hasattr(self, 'listbox'):
                self.listbox.destroy()
            self.listbox = tk.Listbox(self)
            self.listbox.bind('<<ListboxSelect>>', self.selection)
            self.listbox.grid(row=1, column=1, sticky="ew")
            for item in matches:
                self.listbox.insert(tk.END, item)
        else:
            if hasattr(self, 'listbox'):
                self.listbox.destroy()

    def selection(self, event):
        if self.listbox.curselection():
            index = self.listbox.curselection()[0]
            value = self.listbox.get(index)
            self.var.set(value)

if __name__ == "__main__":
    root = tk.Tk()
    app = DictionaryApp(root)
    root.mainloop()
