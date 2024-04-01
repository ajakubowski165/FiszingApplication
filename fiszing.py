import tkinter as tk
from tkinter import messagebox
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
        
        self.lets_fiszing_button = tk.Button(master, text="Let's Fiszing", command=self.show_all_sets_to_learn, font=("Centaur", 30, "bold"), bg="lightgreen", width=25)
        self.lets_fiszing_button.pack(pady=(25, 0))  

        self.new_set_button = tk.Button(master, text="Make a new set of cards", command=self.make_new_set, font=("Centaur", 30, "bold"),bg="lightgreen", width=25)
        self.new_set_button.pack()

        self.see_all_sets_button = tk.Button(master, text="See all sets", command=self.see_all_sets, font=("Centaur", 30, "bold"),bg="lightgreen", width=25)
        self.see_all_sets_button.pack()

        self.delete_button = tk.Button(master, text="Delete...", command=self.delete_screen, font=("Centaur", 30, "bold"),bg="lightgreen", width=25)
        self.delete_button.pack()

        self.name_entry = None
        self.term_entry = None
        self.definition_entry = None
        self.confirm_button = None
        self.return_button = None
        self.set_buttons = []
        self.learning_window = None
        self.current_set_name = None
        self.current_flashcard_index = 0
        self.num_flashcards = 0
        self.num_correct = 0


    def show_all_sets_to_learn(self):
        # Usuń wszystkie elementy z ekranu, z wyjątkiem przycisku "Let's Fiszing"
        for widget in self.master.winfo_children():
            if widget != self.label:
                widget.pack_forget()

        # Pobranie listy plików fiszek w katalogu bieżącym
        flashcard_files = [filename for filename in os.listdir() if filename.endswith("_flashcards.json")]

        # Tworzenie przycisków dla każdego zestawu fiszek
        for filename in flashcard_files:
            set_name = filename.replace("_flashcards.json", "")
            set_button = tk.Button(self.master, text=set_name, command=lambda name=set_name: self.show_learning_frame(name), font=("Centaur", 30),bg="lightgreen", width=25)
            set_button.pack()
            self.set_buttons.append(set_button)
        
        # Dodanie przycisku powrotu do ekranu głównego
        self.return_button = tk.Button(self.master, text="Return", command=self.return_to_main_window, font=("Centaur", 30), bg="lightgreen", width=25)
        self.return_button.pack(pady=(0, 25))

    def show_learning_frame(self, set_name):
        # Usuń przyciski zestawów
        for button in self.set_buttons:
            button.pack_forget()

        # Zainicjuj ramkę do nauki
        self.learning_frame = tk.Frame(self.master, bg="#789c84")
        self.learning_frame.pack(fill=tk.BOTH, expand=True)

        # Ustawienia dotyczące pojęć do nauki
        self.current_set_name = set_name
        self.current_flashcards_filename = f"{set_name}_flashcards.json"
        self.flashcards = self.load_flashcards()
        self.num_flashcards = len(self.flashcards)
        self.current_flashcard_index = 0
        self.num_correct = 0

        # Wyświetlanie nazwy zestawu
        set_name_label = tk.Label(self.learning_frame, text=f"{set_name.upper()}", font=("Jokerman", 30, "bold"), bg="#789c84")
        set_name_label.pack(pady=(20, 10))

        # Wyświetlanie licznika pytań
        self.flashcard_counter_label = tk.Label(self.learning_frame, text=f"1/{self.num_flashcards}", font=("Centaur", 20), bg="#789c84")
        self.flashcard_counter_label.pack()

        # Wyświetlanie licznika UMIEM/NIE UMIEM
        self.correct_counter_label = tk.Label(self.learning_frame, text=f"UMIEM {self.num_correct}/{self.num_flashcards} NIE UMIEM", font=("Centaur", 20), bg="#789c84")
        self.correct_counter_label.pack(pady=(10, 20))

        # Wyświetlanie aktualnego pojęcia lub definicji
        self.flashcard_button = tk.Button(self.learning_frame, text=list(self.flashcards.keys())[0], command=self.flip_flashcard, font=("Centaur", 40), bg="lightgreen", width=25)
        self.flashcard_button.pack(pady=20)

        # Przyciski UMIEM/NIE UMIEM
        self.know_button = tk.Button(self.learning_frame, text="UMIEM", command=self.next_flashcard, font=("Centaur", 20), bg="lightgreen", width=10)
        self.know_button.pack(side="left", padx=20)
        self.dont_know_button = tk.Button(self.learning_frame, text="NIE UMIEM", command=self.next_flashcard, font=("Centaur", 20), bg="lightgreen", width=10)
        self.dont_know_button.pack(side="right", padx=20)

    def flip_flashcard(self):
        current_flashcard = list(self.flashcards.values())[self.current_flashcard_index]
        if self.flashcard_button.cget("text") == current_flashcard:
            self.flashcard_button.config(text=list(self.flashcards.keys())[self.current_flashcard_index])
        else:
            self.flashcard_button.config(text=current_flashcard)

    def next_flashcard(self):
        # Inkrementacja licznika UMIEM/NIE UMIEM
        if self.know_button['state'] != 'disabled':
            self.num_correct += 1

        # Aktualizacja licznika pytań
        self.current_flashcard_index += 1
        self.flashcard_counter_label.config(text=f"{self.current_flashcard_index + 1}/{self.num_flashcards}")

        # Aktualizacja licznika UMIEM/NIE UMIEM
        self.correct_counter_label.config(text=f"UMIEM {self.num_correct}/{self.num_flashcards} NIE UMIEM")

        # Sprawdzenie, czy to już ostatnie pytanie
        if self.current_flashcard_index < self.num_flashcards:
            self.flip_flashcard()
        else:
            messagebox.showinfo("Info", "You have completed learning this set!")
            self.learning_frame.destroy()



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
        self.delete_button.pack_forget()
        self.lets_fiszing_button.pack_forget()

    def delete_screen(self):
        self.new_set_button.pack_forget()
        self.see_all_sets_button.pack_forget()
        self.delete_button.pack_forget()
        self.lets_fiszing_button.pack_forget()

        self.delete_set_button = tk.Button(self.master, text="Delete set", command=self.show_delete_sets, font=("Centaur", 30),bg="lightgreen", width=25)
        self.delete_set_button.pack(pady=(25, 0))

        self.delete_cards_button = tk.Button(self.master, text="Delete cards from specific set", command=self.delete_cards, font=("Centaur", 30),bg="lightgreen", width=25)
        self.delete_cards_button.pack()

        self.return_button = tk.Button(self.master, text="Return", command=self.return_to_main_window, font=("Centaur", 30),bg="lightgreen", width=25)
        self.return_button.pack()

    
    def show_delete_sets(self):
        self.delete_cards_button.pack_forget()
        self.delete_set_button.pack_forget()
        self.return_button.pack_forget()
        self.lets_fiszing_button.pack_forget()

        # Pobierz listę plików zestawów fiszek
        flashcard_files = [filename for filename in os.listdir() if filename.endswith("_flashcards.json")]

        for filename in flashcard_files:
            set_name = filename.replace("_flashcards.json", "")
            set_button = tk.Button(self.master, text=set_name, command=lambda name=set_name: self.confirm_delete_set(name), font=("Centaur", 30),bg="lightgreen", width=25)
            set_button.pack()
            self.set_buttons.append(set_button)

        self.return_button = tk.Button(self.master, text="Return", command=self.return_to_main_window, font=("Centaur", 30),bg="lightgreen", width=25)
        self.return_button.pack(pady=(0,25))

    
    def confirm_delete_set(self, set_name):
        confirm_dialog = tk.messagebox.askquestion("Confirmation", f"Are you sure you want to delete set \"{set_name}\"?")
        if confirm_dialog == 'yes':
            self.delete_set(set_name)


    def delete_set(self, set_name):
        filename = f"{set_name}_flashcards.json"
        if os.path.exists(filename):
            os.remove(filename)
            messagebox.showinfo("Success", f"Set '{set_name}' has been deleted successfully.")
        else:
            messagebox.showerror("Error", f"Set '{set_name}' does not exist.")
        
        # Usuń przycisk zestawu z listy przycisków
        for button in self.set_buttons:
            if button.cget("text") == set_name:
                button.destroy()
                self.set_buttons.remove(button)

    def delete_cards(self):
        self.new_set_button.pack_forget()
        self.see_all_sets_button.pack_forget()
        self.delete_button.pack_forget()
        self.delete_set_button.pack_forget()
        self.delete_cards_button.pack_forget()
        self.return_button.pack_forget()
        self.lets_fiszing_button.pack_forget()

        # Pobierz listę plików zestawów fiszek
        flashcard_files = [filename for filename in os.listdir() if filename.endswith("_flashcards.json")]

        for filename in flashcard_files:
            set_name = filename.replace("_flashcards.json", "")
            set_button = tk.Button(self.master, text=set_name, command=lambda name=set_name: self.show_set_flashcards_delete(name), font=("Centaur", 30),bg="lightgreen", width=25)
            set_button.pack()
            self.set_buttons.append(set_button)

        self.return_button = tk.Button(self.master, text="Return", command=self.return_to_main_window, font=("Centaur", 30),bg="lightgreen", width=25)
        self.return_button.pack(pady=(0,25))

    def show_set_flashcards_delete(self, set_name):
        # Usunięcie przycisków zestawów
        for button in self.set_buttons:
            button.pack_forget()

        # Usunięcie etykiety z nazwą zestawu, jeśli istnieje
        if hasattr(self, "set_label"):
            self.set_label.pack_forget()

        # Wyświetlenie nazwy zestawu
        self.set_label = tk.Label(self.master, text=set_name.upper(), font=("Jokerman", 30, "bold"), bg="#789c84")
        self.set_label.pack()

        # Ustawienie bieżącego pliku fiszek na wybrany zestaw
        self.current_flashcards_filename = f"{set_name}_flashcards.json"
        self.flashcards = self.load_flashcards()

        # Wyświetlenie pojęć z wybranego zestawu jako przycisków
        for term, definition in self.flashcards.items():
            flashcard_button = tk.Button(self.master, text=f"{term}: {definition}", command=lambda t=term: self.delete_flashcard(t), font=("Centaur", 15), bg="lightgreen", width=20)
            flashcard_button.pack(pady=5)
            self.set_buttons.append(flashcard_button)


    def delete_flashcard(self, term):
        # Usunięcie pojęcia z aktualnego zestawu
        if term in self.flashcards:
            del self.flashcards[term]
            self.save_flashcards()

        # Usunięcie przycisku pojęcia
        for button in self.set_buttons:
            if term in button["text"]:
                button.destroy()
                self.set_buttons.remove(button)
    
    def remove_set_buttons(self):
        # Usunięcie przycisków dla poprzedniego zestawu (jeśli istnieją)
        for button in self.set_buttons:
            button.destroy()
        self.set_buttons.clear()


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
            if widget not in [self.new_set_button, self.see_all_sets_button, self.label, self.lets_fiszing_button]:
                widget.pack_forget()

        # Wyświetl przyciski "Make a new set of cards" i "See all sets", jeśli nie są już na ekranie
        if self.lets_fiszing_button.winfo_ismapped() == 0:
            self.lets_fiszing_button.pack()
        if self.new_set_button.winfo_ismapped() == 0:
            self.new_set_button.pack()
        if self.see_all_sets_button.winfo_ismapped() == 0:
            self.see_all_sets_button.pack()
        if self.delete_button.winfo_ismapped() == 0:
            self.delete_button.pack()



    def see_all_sets(self):
        # Usunięcie przycisku "See all sets" z ekranu głównego
        self.see_all_sets_button.pack_forget()
        self.new_set_button.pack_forget()
        self.delete_button.pack_forget()
        self.lets_fiszing_button.pack_forget()
        
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
