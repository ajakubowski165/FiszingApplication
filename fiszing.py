import tkinter as tk
from tkinter import messagebox
import json
import random
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
        
        self.lets_fiszing_button = tk.Button(master, text="Zacznij FISZING!", command=self.show_all_sets_to_learn, font=("Centaur", 30, "bold"), bg="lightgreen", width=25)
        self.lets_fiszing_button.pack(pady=(25, 0))

        self.solve_quiz_button = tk.Button(master, text="Rozwiaz quiz", command=self.solve_quiz, font=("Centaur", 30, "bold"), bg="lightgreen", width=25)
        self.solve_quiz_button.pack()  

        self.new_set_button = tk.Button(master, text="Utwórz nowy zestaw", command=self.make_new_set, font=("Centaur", 30, "bold"),bg="lightgreen", width=25)
        self.new_set_button.pack()

        self.see_all_sets_button = tk.Button(master, text="Dodaj fiszki do zestawu", command=self.see_all_sets, font=("Centaur", 30, "bold"),bg="lightgreen", width=25)
        self.see_all_sets_button.pack()

        self.delete_button = tk.Button(master, text="Usun...", command=self.delete_screen, font=("Centaur", 30, "bold"),bg="lightgreen", width=25)
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
        self.quiz_frame = None
        self.current_question_index = None
        self.current_question = None
        self.correct_answer = None
        self.selected_answer = None



    def solve_quiz(self):
        for widget in self.master.winfo_children():
            if widget != self.label:
                widget.pack_forget()

        # Pobranie listy plików fiszek w katalogu bieżącym za pomocą listdir z biblioteki os
        flashcard_files = [filename for filename in os.listdir() if filename.endswith("_flashcards.json")]

        # Tworzenie przycisków dla każdego zestawu fiszek
        for filename in flashcard_files:
            set_name = filename.replace("_flashcards.json", "")
            set_button = tk.Button(self.master, text=set_name, command=lambda name=set_name: self.start_quiz(name), font=("Centaur", 30), bg="lightgreen", width=25)
            set_button.pack()
            self.set_buttons.append(set_button)

        # Dodanie przycisku powrotu do ekranu głównego
        self.return_button = tk.Button(self.master, text="Powrót", command=self.return_to_main_window, font=("Centaur", 30), bg="#419745", width=15)
        self.return_button.pack(pady=25)


    def start_quiz(self, set_name):
        # Usunięcie przycisków zestawów
        self.remove_set_buttons()

        # Wyświetlenie nazwy zestawu
        set_label = tk.Label(self.master, text=set_name.upper(), font=("Jokerman", 30, "bold"), bg="#789c84")
        set_label.pack()

        # Ustawienie bieżącego pliku fiszek na wybrany zestaw
        self.current_flashcards_filename = f"{set_name}_flashcards.json"
        self.flashcards = self.load_flashcards()

        # Przygotowanie pytań do quizu
        self.prepare_questions()

        # Rozpoczęcie quizu od pierwszego pytania
        self.current_question_index = 0
        self.show_next_question()


    def prepare_questions(self):
        self.num_correct = 0
        # Przygotowanie listy pytań z zestawu fiszek
        self.questions = list(self.flashcards.items())
        random.shuffle(self.questions)  # Losowa kolejność pytań


    def show_next_question(self):
        if self.quiz_frame:
            self.quiz_frame.destroy()

        if self.current_question_index is None:
            self.current_question_index = 0

        if self.current_question_index < len(self.questions):
            self.current_question_index += 1
            self.current_question = self.questions[self.current_question_index - 1][0]
            self.correct_answer = self.flashcards[self.current_question]
            answers = [self.correct_answer] #Dodawanie poprawnej do listy

            # Wybieranie trzech losowych niepoprawne odpowiedzi
            all_definitions = list(self.flashcards.values()) #values - wartosci (definicje)
            all_definitions.remove(self.correct_answer)
            random.shuffle(all_definitions)
            answers.extend(all_definitions[:3]) #Dodawanie do listy 3 losowych niepoprawnych
            random.shuffle(answers)

            # Tworzenie  ramki dla pytan i odpowiedzi
            self.quiz_frame = tk.Frame(self.master, bg="#789c84")
            self.quiz_frame.pack(pady=20)

            # Wyświetlanie licznika pytan
            question_counter_label = tk.Label(self.quiz_frame, text=f"Pytanie {self.current_question_index}/{len(self.questions)}:", font=("Centaur", 20), bg="#789c84")
            question_counter_label.pack()

            # Wyświetlanie pytania
            question_label = tk.Label(self.quiz_frame, text=f"Pytanie: {self.current_question}", font=("Centaur", 20), bg="#789c84")
            question_label.pack(pady=10)

            # Wyświetlanie odpowiedzi jako przyciski
            answer_buttons = []
            for x, answer in enumerate(answers):
                button = tk.Button(self.quiz_frame, text=f"{chr(65+x)}. {answer}", font=("Centaur", 15), bg="lightgreen", width=45, command=lambda a=answer: self.check_answer(a))
                button.pack(pady=5)
                answer_buttons.append(button)

            # Zapisanie przycisków odpowiedzi, aby można się do nich odwołać i je usunąć po zmianie pytania
            self.answer_buttons = answer_buttons
        else:
            # Zakończenie quizu i wyświetlenie wyniku
            self.quiz_frame = tk.Frame(self.master, bg="#789c84")
            self.quiz_frame.pack(pady=20)

            result_label = tk.Label(self.quiz_frame, text="Koniec quizu!", font=("Jokerman", 30), bg="#789c84")
            result_label.pack()

            score_percentage = (self.num_correct / len(self.questions)) * 100

            score_label = tk.Label(self.quiz_frame, text=f"Twój wynik: {score_percentage:.1f}%", font=("Centaur", 20), bg="#789c84")
            score_label.pack(pady=10)

            # Usuwanie przyciski zestawów i przycisk powrotu
            self.remove_set_buttons()
            self.return_button.pack_forget()

            # Dodawanie przycisku powrotu do ekranu głównego
            self.return_button = tk.Button(self.master, text="Powrót", command=self.return_to_main_window, font=("Centaur", 30), bg="#419745", width=15)
            self.return_button.pack(pady=25)


    # Sprawdzanie odpowiedzi
    def check_answer(self, selected_answer):
        self.selected_answer = selected_answer
        if self.selected_answer == self.correct_answer:
            messagebox.showinfo("Wynik", "Odpowiedź poprawna!")
            self.num_correct += 1
        else:
            messagebox.showinfo("Wynik", f"Odpowiedź niepoprawna! Poprawna odpowiedź to: {self.correct_answer}")
        self.show_next_question()

    # Załadowanie fiszek z zestawu
    def load_flashcards(self):
        if self.current_flashcards_filename and os.path.exists(self.current_flashcards_filename):
            with open(self.current_flashcards_filename, "r") as file:
                return json.load(file)
        else:
            return {}


    def show_all_sets_to_learn(self):
        # Usuwanie wszystkich elementów z ekranu, z wyjątkiem tytułu
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
        self.return_button = tk.Button(self.master, text="Powrót", command=self.return_to_main_window, font=("Centaur", 30), bg="#419745", width=15)
        self.return_button.pack(pady=25)


    def show_learning_frame(self, set_name):
        # Usuwanie przycisków zestawów
        for button in self.set_buttons:
            button.pack_forget()

        # Inicjacja ramki do nauki
        self.learning_frame = tk.Frame(self.master, bg="#789c84")
        self.learning_frame.pack(fill=tk.BOTH, expand=True)

        # Ustawienia dotyczące pojęć do nauki
        self.current_set_name = set_name
        self.current_flashcards_filename = f"{set_name}_flashcards.json"
        self.flashcards = self.load_flashcards()
        self.num_flashcards = len(self.flashcards)
        self.current_flashcard_index = 0
        self.num_correct = 0
        self.num_incorrect = 0

        # Wyświetlanie nazwy zestawu
        set_name_label = tk.Label(self.learning_frame, text=f"{set_name.upper()}", font=("Jokerman", 30, "bold"), bg="#789c84")
        set_name_label.pack(pady=(20, 10))

        # Wyświetlanie licznika pytań
        self.flashcard_counter_label = tk.Label(self.learning_frame, text=f"1/{self.num_flashcards}", font=("Centaur", 20), bg="#789c84")
        self.flashcard_counter_label.pack()

        # Wyświetlanie licznika UMIEM/NIE UMIEM
        self.correct_counter_label = tk.Label(self.learning_frame, text=f"UMIEM {self.num_correct}/{self.num_incorrect} NIE UMIEM", font=("Centaur", 20), bg="#789c84")
        self.correct_counter_label.pack(pady=(10, 20))

        # Wyświetlanie aktualnego pojęcia lub definicji
        self.flashcard_button = tk.Button(self.learning_frame, text=list(self.flashcards.keys())[0], command=self.flip_flashcard, font=("Centaur", 40), bg="lightgreen", width=25)
        self.flashcard_button.pack(pady=20)

        # Przyciski UMIEM/NIE UMIEM
        self.know_button = tk.Button(self.learning_frame, text="UMIEM", command=self.on_know_click, font=("Centaur", 20), bg="lightgreen", width=10)
        self.know_button.pack(side="left", padx=40)
        self.dont_know_button = tk.Button(self.learning_frame, text="NIE UMIEM", command=self.on_dont_know_click, font=("Centaur", 20), bg="lightgreen", width=10)
        self.dont_know_button.pack(side="right", padx=40)


    def flip_flashcard(self):
        current_flashcard = list(self.flashcards.values())[self.current_flashcard_index]
        if self.flashcard_button.cget("text") == current_flashcard: #sczytanie tekstu z przycisku
            self.flashcard_button.config(text=list(self.flashcards.keys())[self.current_flashcard_index])
        else:
            self.flashcard_button.config(text=current_flashcard)

    
    def on_know_click(self):
        # Inkrementacja licznika UMIEM
        self.num_correct += 1
        # Przejście do następnej fiszki
        self.next_flashcard()

    
    def on_dont_know_click(self):
        # Inkrementacja licznika NIE UMIEM
        self.num_incorrect += 1
        # Przejście do następnej fiszki
        self.next_flashcard()


    def next_flashcard(self):
        # Aktualizacja licznika pytań
        self.current_flashcard_index += 1
        self.flashcard_counter_label.config(text=f"{self.current_flashcard_index + 1}/{self.num_flashcards}")

        # Aktualizacja licznika UMIEM/NIE UMIEM
        self.correct_counter_label.config(text=f"UMIEM {self.num_correct}/{self.num_incorrect} NIE UMIEM")

        # Sprawdzenie czy to już ostatnie pytanie
        if self.current_flashcard_index < self.num_flashcards:
            self.flip_flashcard()
        else:
           # Wyświetlenie wyniku w messageboxie
            result_message = f"Ukonczyles zestaw!\n" \
                            f"UMIEM: {self.num_correct}\n" \
                            f"NIE UMIEM: {self.num_incorrect}"
            messagebox.showinfo("Info", result_message)
            self.learning_frame.destroy()


    def make_new_set(self):
        self.name_entry = tk.Entry(self.master, font=("Centaur", 30), width=25)
        self.name_entry.insert(0, "Wprowadz nazwe zestawu...")
        self.name_entry.bind("<FocusIn>", self.clear_placeholder)
        self.name_entry.bind("<FocusOut>", self.restore_placeholder)
        self.name_entry.pack(pady=30)

        self.confirm_button = tk.Button(self.master, text="Zatwierdz", command=self.create_new_set, font=("Centaur", 30),bg="lightgreen", width=25)
        self.confirm_button.pack()

        self.return_button = tk.Button(self.master, text="Powrót", command=self.return_to_main_window, font=("Centaur", 30), bg="#419745", width=15)
        self.return_button.pack(pady=25)

        self.new_set_button.pack_forget() 
        self.see_all_sets_button.pack_forget()
        self.delete_button.pack_forget()
        self.lets_fiszing_button.pack_forget()
        self.solve_quiz_button.pack_forget()


    def delete_screen(self):
        self.new_set_button.pack_forget()
        self.see_all_sets_button.pack_forget()
        self.delete_button.pack_forget()
        self.lets_fiszing_button.pack_forget()
        self.solve_quiz_button.pack_forget()

        self.delete_set_button = tk.Button(self.master, text="Usun zestaw", command=self.show_delete_sets, font=("Centaur", 30),bg="lightgreen", width=25)
        self.delete_set_button.pack(pady=(25, 0))

        self.delete_cards_button = tk.Button(self.master, text="Usun konkretne fiszki z zestawu", command=self.delete_cards, font=("Centaur", 30),bg="lightgreen", width=25)
        self.delete_cards_button.pack()

        self.return_button = tk.Button(self.master, text="Powrót", command=self.return_to_main_window, font=("Centaur", 30), bg="#419745", width=15)
        self.return_button.pack(pady=25)

    
    def show_delete_sets(self):
        self.delete_cards_button.pack_forget()
        self.delete_set_button.pack_forget()
        self.return_button.pack_forget()
        self.lets_fiszing_button.pack_forget()
        self.solve_quiz_button.pack_forget()

        # Pobierz listę plików zestawów fiszek
        flashcard_files = [filename for filename in os.listdir() if filename.endswith("_flashcards.json")]

        for filename in flashcard_files:
            set_name = filename.replace("_flashcards.json", "")
            set_button = tk.Button(self.master, text=set_name, command=lambda name=set_name: self.confirm_delete_set(name), font=("Centaur", 30),bg="lightgreen", width=25)
            set_button.pack()
            self.set_buttons.append(set_button)

        self.return_button = tk.Button(self.master, text="Powrót", command=self.return_to_main_window, font=("Centaur", 30), bg="#419745", width=15)
        self.return_button.pack(pady=25)

    
    def confirm_delete_set(self, set_name):
        confirm_dialog = tk.messagebox.askquestion("Confirmation", f"Jestes pewny, ze chcesz usunac zestaw \"{set_name}\"?")
        if confirm_dialog == 'yes':
            self.delete_set(set_name)


    def delete_set(self, set_name):
        filename = f"{set_name}_flashcards.json"
        if os.path.exists(filename):
            os.remove(filename)
            messagebox.showinfo("Success", f"Zestaw '{set_name}' zostal usuniety pomyslnie.")
        else:
            messagebox.showerror("Error", f"Zestaw '{set_name}' nie istnieje.")
        
        # Usuwanie przycisków zestawu z listy przycisków
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

        # Pobieranie listy plików zestawów fiszek
        flashcard_files = [filename for filename in os.listdir() if filename.endswith("_flashcards.json")]

        for filename in flashcard_files:
            set_name = filename.replace("_flashcards.json", "")
            set_button = tk.Button(self.master, text=set_name, command=lambda name=set_name: self.show_set_flashcards_delete(name), font=("Centaur", 30),bg="lightgreen", width=25)
            set_button.pack()
            self.set_buttons.append(set_button)

        self.return_button = tk.Button(self.master, text="Powrót", command=self.return_to_main_window, font=("Centaur", 30), bg="#419745", width=15)
        self.return_button.pack(pady=25)

    def show_set_flashcards_delete(self, set_name):
        # Usunięcie przycisków zestawów
        for button in self.set_buttons:
            button.pack_forget()

        # Wyświetlenie nazwy zestawu
        self.set_label = tk.Label(self.master, text=set_name.upper(), font=("Jokerman", 30, "bold"), bg="#789c84")
        self.set_label.pack()

        # Ustawienie bieżącego pliku fiszek na wybrany zestaw
        self.current_flashcards_filename = f"{set_name}_flashcards.json"
        self.flashcards = self.load_flashcards()
        
        self.delete_flashcard_in_frame()
        
    
    def delete_flashcard_in_frame(self):
        self.scroll_frame = tk.Frame(self.master, bg="lightgreen", width=1200, height=400)
        self.scroll_frame.pack(pady=20)

        # Tworzenie ramki ze scrollbarem
        canvas = tk.Canvas(self.scroll_frame, bg="lightgreen")
        scrollbar = tk.Scrollbar(self.scroll_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        canvas.configure(yscrollcommand=scrollbar.set)
        flashcards_frame = tk.Frame(canvas, bg="lightgreen", width=1200, height=400)
        canvas.create_window((0, 0), window=flashcards_frame, anchor=tk.NW)
        flashcards_frame.bind("<Configure>", lambda event, canvas=canvas: canvas.configure(scrollregion=canvas.bbox("all")))

        # Wyświetlenie pojęć z wybranego zestawu w ramce
        for term, definition in self.flashcards.items():
            flashcard_button = tk.Button(flashcards_frame, text=f"{term}: {definition}", command=lambda t=term: self.delete_flashcard(t), font=("Centaur", 12), bg="lightgreen", width=42)
            flashcard_button.pack()
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
        if widget.get() == "Wprowadz nazwe zestawu..." or widget.get() == "Wprowadz pojecie..." or widget.get() == "Wprowadz definicje...":
            widget.delete(0, tk.END)
            widget.config(fg="black")


    def restore_placeholder(self, event):
        widget = event.widget
        if widget.get() == "":
            if widget == self.name_entry:
                widget.insert(0, "Wprowadz nazwe zestawu...")
            elif widget == self.term_entry:
                widget.insert(0, "Wprowadz pojecie...")
            elif widget == self.definition_entry:
                widget.insert(0, "Wprowadz definicje...")
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
            self.name_entry.pack_forget()
            self.confirm_button.pack_forget()
            self.return_button.pack_forget()
            self.solve_quiz_button.pack_forget()
            self.lets_fiszing_button.pack_forget()

            self.term_entry = tk.Entry(self.master, font=("Centaur", 20))
            self.term_entry.insert(0, "Wprowadz pojecie...")
            self.term_entry.bind("<FocusIn>", self.clear_placeholder)
            self.term_entry.bind("<FocusOut>", self.restore_placeholder)
            self.term_entry.pack(pady=10)

            self.definition_entry = tk.Entry(self.master, font=("Centaur", 20))
            self.definition_entry.insert(0, "Wprowadz definicje...")
            self.definition_entry.bind("<FocusIn>", self.clear_placeholder)
            self.definition_entry.bind("<FocusOut>", self.restore_placeholder)
            self.definition_entry.pack(pady=10)

            self.confirm_button = tk.Button(self.master, text="Zatwierdz", command=self.add_flashcard, font=("Centaur", 30),bg="lightgreen", width=25)
            self.confirm_button.pack()

            self.return_button = tk.Button(self.master, text="Powrót", command=self.return_to_main_window, font=("Centaur", 30), bg="#419745", width=15)
            self.return_button.pack(pady=25)


    def add_flashcard(self):
        term = self.term_entry.get()
        definition = self.definition_entry.get()

        if term and definition:
            self.flashcards[term] = definition
            self.save_flashcards()
            self.set_in_frame()

            # Czyszczenie wprowadzonych wartości
            self.term_entry.delete(0, tk.END)
            self.definition_entry.delete(0, tk.END)
        

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
        for widget in self.master.winfo_children():
            if widget not in [self.new_set_button, self.see_all_sets_button, self.label, self.lets_fiszing_button]:
                widget.pack_forget()

        if self.lets_fiszing_button.winfo_ismapped() == 0:
            self.lets_fiszing_button.pack()
        if self.solve_quiz_button.winfo_ismapped() == 0:
            self.solve_quiz_button.pack()
        if self.new_set_button.winfo_ismapped() == 0:
            self.new_set_button.pack()
        if self.see_all_sets_button.winfo_ismapped() == 0:
            self.see_all_sets_button.pack()
        if self.delete_button.winfo_ismapped() == 0:
            self.delete_button.pack()



    def set_in_frame(self):
        # Sprawdzenie, czy istnieje ramka scroll_frame
        if hasattr(self, 'scroll_frame'):
            # Jeśli ramka istnieje, usuń wszystkie elementy wewnątrz niej
            for widget in self.scroll_frame.winfo_children():
                widget.destroy()
            self.scroll_frame.pack(pady=20)
        else:
            # Jeśli ramka nie istnieje, utwórz nową
            self.scroll_frame = tk.Frame(self.master, bg="lightgreen", width=800, height=400)
            self.scroll_frame.pack(pady=20)

        # Tworzenie canvas i scrollbar jako dzieci ramki scroll_frame
        canvas = tk.Canvas(self.scroll_frame, bg="lightgreen")
        scrollbar = tk.Scrollbar(self.scroll_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Ustawienie canvas jako ramkę, którą będzie przewijać pasek przewijania
        canvas.configure(yscrollcommand=scrollbar.set)

        # Tworzenie ramki dla pojęć, która będzie umieszczona na canvasie
        flashcards_frame = tk.Frame(canvas, bg="lightgreen")

        # Ustawienie canvas tak, aby zawierał ramkę z pojęciami
        canvas.create_window((0, 0), window=flashcards_frame, anchor=tk.NW)

        # Powiązanie obszaru canvasa z jego zawartością
        flashcards_frame.bind("<Configure>", lambda event, canvas=canvas: canvas.configure(scrollregion=canvas.bbox("all")))

        # Wyświetlenie pojęć z wybranego zestawu w ramce
        for term, definition in self.flashcards.items():
            flashcard_text = f"{term}: {definition}"
            flashcard_label = tk.Label(flashcards_frame, text=flashcard_text, font=("Centaur", 15), bg="lightgreen", width=60, anchor=tk.W)
            flashcard_label.pack(fill=tk.X, padx=10, pady=5)

    def see_all_sets(self):
        # Usunięcie przycisku "See all sets" z ekranu głównego
        self.see_all_sets_button.pack_forget()
        self.new_set_button.pack_forget()
        self.delete_button.pack_forget()
        self.lets_fiszing_button.pack_forget()
        self.solve_quiz_button.pack_forget()
        
        # Pobieranie listy plików fiszek w katalogu bieżącym
        flashcard_files = [filename for filename in os.listdir() if filename.endswith("_flashcards.json")]

        # Tworzenie przycisków dla każdego zestawu fiszek
        for filename in flashcard_files:
            set_name = filename.replace("_flashcards.json", "")
            set_button = tk.Button(self.master, text=set_name, command=lambda name=set_name: self.show_set_flashcards(name), font=("Centaur", 30),bg="lightgreen", width=25)
            set_button.pack()
            self.set_buttons.append(set_button)
        
        # Dodawanie przycisku powrotu do ekranu głównego
        self.return_button = tk.Button(self.master, text="Powrót", command=self.return_to_main_window, font=("Centaur", 30), bg="#419745", width=15)
        self.return_button.pack(pady=25)


    def show_set_flashcards(self, set_name):
        # Usunięcie przycisków zestawów
        self.remove_set_buttons()
        self.return_button.pack_forget()

        # Wyświetlenie nazwy zestawu
        set_label = tk.Label(self.master, text=set_name.upper(), font=("Jokerman", 30, "bold"), bg="#789c84")
        set_label.pack()

        # Ustawienie bieżącego pliku fiszek na wybrany zestaw
        self.current_flashcards_filename = f"{set_name}_flashcards.json"
        self.flashcards = self.load_flashcards()

        self.term_entry = tk.Entry(self.master, font=("Centaur", 20))
        self.term_entry.insert(0, "Wprowadz pojecie...")
        self.term_entry.bind("<FocusIn>", self.clear_placeholder)
        self.term_entry.bind("<FocusOut>", self.restore_placeholder)
        self.term_entry.pack(pady=10)

        self.definition_entry = tk.Entry(self.master, font=("Centaur", 20))
        self.definition_entry.insert(0, "Wprowadz definicje...")
        self.definition_entry.bind("<FocusIn>", self.clear_placeholder)
        self.definition_entry.bind("<FocusOut>", self.restore_placeholder)
        self.definition_entry.pack(pady=10)

        self.confirm_button = tk.Button(self.master, text="Zatwierdz", command=self.add_flashcard, font=("Centaur", 30),bg="lightgreen", width=25)
        self.confirm_button.pack()

        self.return_button = tk.Button(self.master, text="Powrót", command=self.return_to_main_window, font=("Centaur", 30), bg="#419745", width=15)
        self.return_button.pack(pady=25)


def main():
    root = tk.Tk()
    app = FlashcardsApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()