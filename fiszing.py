import tkinter as tk
import json
import os

class FlashcardsApp:
    def __init__(self, master):
        self.master = master
        master.title("Fiszing")

        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        master.geometry(f"{screen_width}x{screen_height}")

        self.flashcards = {}
        self.current_flashcards_filename = None

        self.label = tk.Label(master, text="Fiszing", font=("Verdana", 18))
        self.label.pack(pady=20)

        self.new_set_button = tk.Button(master, text="Make a new set of cards", command=self.make_new_set, font=("Verdana", 14))
        self.new_set_button.pack()

        self.name_entry = None
        self.term_entry = None
        self.definition_entry = None
        self.confirm_button = None
        self.return_button = None

    def make_new_set(self):
        self.name_entry = tk.Entry(self.master, font=("Verdana", 12))
        self.name_entry.pack(pady=10)

        self.confirm_button = tk.Button(self.master, text="Confirm", command=self.create_new_set, font=("Verdana", 12))
        self.confirm_button.pack(pady=10)

        self.return_button = tk.Button(self.master, text="Return", command=self.return_to_main_window, font=("Verdana", 12))
        self.return_button.pack(pady=10)

        self.new_set_button.pack_forget()  # Ukryj przycisk "Make a new set of cards"

    def create_new_set(self):
        name = self.name_entry.get()
        if name:
            self.current_flashcards_filename = f"{name}_flashcards.json"
            self.flashcards = self.load_flashcards()
            self.name_entry.destroy()
            self.confirm_button.destroy()
            self.return_button.destroy()

            self.term_entry = tk.Entry(self.master, font=("Verdana", 12))
            self.term_entry.pack(pady=10)

            self.definition_entry = tk.Entry(self.master, font=("Verdana", 12))
            self.definition_entry.pack(pady=10)

            self.confirm_button = tk.Button(self.master, text="Confirm", command=self.add_flashcard, font=("Verdana", 12))
            self.confirm_button.pack(pady=10)

            self.return_button = tk.Button(self.master, text="Return", command=self.return_to_main_window, font=("Verdana", 12))
            self.return_button.pack(pady=10)

    def add_flashcard(self):
        term = self.term_entry.get()
        definition = self.definition_entry.get()

        if term and definition:
            self.flashcards[term] = definition
            self.save_flashcards()
            self.show_flashcards()

            # Wyczyść wprowadzone wartości
            self.term_entry.delete(0, tk.END)
            self.definition_entry.delete(0, tk.END)

    def show_flashcards(self):
        flashcard_text = "\n".join([f"{term}: {definition}" for term, definition in self.flashcards.items()])
        if hasattr(self, "flashcards_label"):
            self.flashcards_label.destroy()

        self.flashcards_label = tk.Label(self.master, text=flashcard_text, font=("Verdana", 12), justify="left")
        self.flashcards_label.pack(pady=20)

    def load_flashcards(self):
        if self.current_flashcards_filename and os.path.exists(self.current_flashcards_filename):
            with open(self.current_flashcards_filename, "r") as file:
                return json.load(file)
        else:
            return {}

    def save_flashcards(self):
        if self.current_flashcards_filename:
            with open(self.current_flashcards_filename, "w") as file:
                json.dump(self.flashcards, file)

    def return_to_main_window(self):
        if self.name_entry:
            self.name_entry.destroy()
            self.flashcards_label.destroy()
            self.confirm_button.destroy()
            self.return_button.destroy()
            self.new_set_button.pack()
            self.term_entry.destroy()
            self.definition_entry.destroy()
        elif self.term_entry:
            self.term_entry.destroy()
            self.flashcards_label.destroy()
            self.definition_entry.destroy()
            self.confirm_button.destroy()
            self.return_button.destroy()
            self.make_new_set()

    def __del__(self):
        self.save_flashcards()


def main():
    root = tk.Tk()
    app = FlashcardsApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()