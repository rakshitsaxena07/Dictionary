def __init__(self, root):
        self.root = root
        self.root.title("Dictionary App")
        self.root.geometry("700x500")
        self.root.configure(bg="#f0f0f0")

        # Load data from JSON file
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