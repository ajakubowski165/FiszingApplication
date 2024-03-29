import tkinter as tk
import json
import os

class FlashcardsApp:
    def __init__(self, master):
        self.master = master
        master.title("Fiszing")
        master.configure(bg="#789c84")

        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        master.geometry(f"{screen_width}x{screen_height}")

        self.flashcards = {}
        self.current_flashcards_filename = None

        self.label = tk.Label(master, text="FISZING", font=("Jokerman", 100), bg="#789c84")
        self.label.pack(pady=20)

        self.new_set_button = tk.Button(master, text="Make a new set of cards", command=self.make_new_set, font=("Centaur", 30, "bold"),bg="lightgreen", width=25)
        self.new_set_button.pack(pady=10)

        self.see_all_sets_button = tk.Button(master, text="See all sets", command=self.see_all_sets, font=("Centaur", 30, "bold"),bg="lightgreen", width=25)
        self.see_all_sets_button.pack()

        self.name_entry = None
        self.term_entry = None
        self.definition_entry = None
        self.confirm_button = None
        self.return_button = None
        self.set_buttons = []

    def make_new_set(self):
        self.name_entry = tk.Entry(self.master, font=("Centaur", 30), width=25)
        self.name_entry.insert(0, "Enter set name...")
        self.name_entry.bind("<FocusIn>", self.clear_placeholder)
        self.name_entry.bind("<FocusOut>", self.restore_placeholder)
        self.name_entry.pack(pady=30)

        self.confirm_button = tk.Button(self.master, text="Confirm", command=self.create_new_set, font=("Centaur", 30),bg="lightgreen", width=25)
        self.confirm_button.pack()

        self.return_button = tk.Button(self.master, text="Return", command=self.return_to_main_window, font=("Centaur", 30),bg="lightgreen", width=25)
        self.return_button.pack(pady=(0, 25))

        self.new_set_button.pack_forget()  # Ukryj przycisk "Make a new set of cards"
        self.see_all_sets_button.pack_forget()

    def clear_placeholder(self, event):
        widget = event.widget
        if widget.get() == "Enter set name..." or widget.get() == "Enter term..." or widget.get() == "Enter definition...":
            widget.delete(0, tk.END)
            widget.config(fg="black")

    def restore_placeholder(self, event):
        widget = event.widget
        if widget.get() == "":
            if widget == self.name_entry:
                widget.insert(0, "Enter set name...")
            elif widget == self.term_entry:
                widget.insert(0, "Enter term...")
            elif widget == self.definition_entry:
                widget.insert(0, "Enter definition...")
            else:
                widget.config(fg="black")
                widget.insert(0, "Enter...")
        elif widget == self.definition_entry:
            widget.config(fg="black")

    def create_new_set(self):
        name = self.name_entry.get()
        if name:
            self.current_flashcards_filename = f"{name}_flashcards.json"
            self.flashcards = self.load_flashcards()
            self.name_entry.destroy()
            self.confirm_button.destroy()
            self.return_button.destroy()

            self.term_entry = tk.Entry(self.master, font=("Centaur", 20))
            self.term_entry.insert(0, "Enter term...")
            self.term_entry.bind("<FocusIn>", self.clear_placeholder)
            self.term_entry.bind("<FocusOut>", self.restore_placeholder)
            self.term_entry.pack(pady=10)

            self.definition_entry = tk.Entry(self.master, font=("Centaur", 20))
            self.definition_entry.insert(0, "Enter definition...")
            self.definition_entry.bind("<FocusIn>", self.clear_placeholder)
            self.definition_entry.bind("<FocusOut>", self.restore_placeholder)
            self.definition_entry.pack(pady=10)

            self.confirm_button = tk.Button(self.master, text="Confirm", command=self.add_flashcard, font=("Centaur", 30),bg="lightgreen", width=25)
            self.confirm_button.pack()

            self.return_button = tk.Button(self.master, text="Return", command=self.return_to_main_window, font=("Centaur", 30),bg="lightgreen", width=25)
            self.return_button.pack(pady=(0, 25))

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

        self.flashcards_label = tk.Label(self.master, text=flashcard_text, font=("Centaur", 12), bg="lightgreen", width=25)
        self.flashcards_label.pack(pady=(0, 25))

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
        # Usuń wszystkie elementy z ekranu, z wyjątkiem przycisków "Make a new set of cards" i "See all sets"
        for widget in self.master.winfo_children():
            if widget not in [self.new_set_button, self.see_all_sets_button, self.label]:
                widget.pack_forget()

        # Wyświetl przyciski "Make a new set of cards" i "See all sets", jeśli nie są już na ekranie
        if self.new_set_button.winfo_ismapped() == 0:
            self.new_set_button.pack()
        if self.see_all_sets_button.winfo_ismapped() == 0:
            self.see_all_sets_button.pack()


    def see_all_sets(self):
        # Usunięcie przycisku "See all sets" z ekranu głównego
        self.see_all_sets_button.pack_forget()
        self.new_set_button.pack_forget()
        
        # Pobranie listy plików fiszek w katalogu bieżącym
        flashcard_files = [filename for filename in os.listdir() if filename.endswith("_flashcards.json")]

        # Tworzenie przycisków dla każdego zestawu fiszek
        for filename in flashcard_files:
            set_name = filename.replace("_flashcards.json", "")
            set_button = tk.Button(self.master, text=set_name, command=lambda name=set_name: self.show_set_flashcards(name), font=("Centaur", 30),bg="lightgreen", width=25)
            set_button.pack()
            self.set_buttons.append(set_button)
        
        # Dodanie przycisku powrotu do ekranu głównego
        self.return_button = tk.Button(self.master, text="Return", command=self.return_to_main_window, font=("Centaur", 30), bg="lightgreen", width=25)
        self.return_button.pack(pady=(0, 25))


    def show_set_flashcards(self, set_name):
         # Wyświetlenie nazwy zestawu
        set_label = tk.Label(self.master, text=set_name.upper(), font=("Jokerman", 30, "bold"), bg="#789c84")
        set_label.pack()

        # Ustawienie bieżącego pliku fiszek na wybrany zestaw
        self.current_flashcards_filename = f"{set_name}_flashcards.json"
        self.flashcards = self.load_flashcards()

        # Wyświetlenie pojęć z wybranego zestawu
        self.show_flashcards()


    def clear_screen(self):
        # Usunięcie wszystkich elementów z ekranu
        for widget in self.master.winfo_children():
            widget.pack_forget()

def main():
    root = tk.Tk()
    app = FlashcardsApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
