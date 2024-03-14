import tkinter as tk  # Importuj bibliotekę tkinter do tworzenia interfejsu graficznego
import json  # Importuj bibliotekę json do obsługi formatu JSON
import os  # Importuj moduł os do operacji na plikach

class FlashcardsApp:
    def __init__(self, master):
        self.master = master  # Ustaw główny kontener interfejsu graficznego
        master.title("FISZING")  # Ustaw tytuł okna
        master.geometry("1200x600")  # Ustaw rozmiar okna

        # Inicjalizuj słownik przechowujący fiszki
        self.flashcards = {}
        # Zmienna przechowująca nazwę bieżącego pliku fiszek
        self.current_flashcards_filename = None

        # Tworzenie etykiety "Fiszing"
        self.label = tk.Label(master, text="FISZING", font=("Verdana", 18))
        self.label.pack(pady=20)  # Umieszczenie etykiety na ekranie

        # Tworzenie przycisku "Make a new set" do tworzenia nowego zestawu fiszek
        self.new_set_button = tk.Button(master, text="Make a new set", command=self.make_new_set, font=("Verdana", 14))
        self.new_set_button.pack()  # Umieszczenie przycisku na ekranie

        # Inicjalizacja zmiennych do przechowywania pól do wprowadzania tekstu i przycisków
        self.name_entry = None
        self.term_entry = None
        self.definition_entry = None
        self.confirm_button = None
        self.return_button = None

    # Metoda do tworzenia nowego zestawu fiszek
    def make_new_set(self):
        # Tworzenie pola do wprowadzenia nazwy zestawu
        self.name_entry = tk.Entry(self.master, font=("Verdana", 12))
        self.name_entry.pack(pady=10)  # Umieszczenie pola na ekranie

        # Tworzenie przycisku "Confirm" do potwierdzenia wprowadzonej nazwy
        self.confirm_button = tk.Button(self.master, text="Confirm", command=self.create_new_set, font=("Verdana", 12))
        self.confirm_button.pack(pady=10)  # Umieszczenie przycisku na ekranie

        # Tworzenie przycisku "Return" do powrotu do poprzedniego widoku
        self.return_button = tk.Button(self.master, text="Return", command=self.return_to_main_window, font=("Verdana", 12))
        self.return_button.pack(pady=10)  # Umieszczenie przycisku na ekranie

        # Ukrycie przycisku "Make a new set of cards"
        self.new_set_button.pack_forget()

    # Metoda do tworzenia nowego zestawu fiszek
    def create_new_set(self):
        name = self.name_entry.get()  # Pobranie wprowadzonej nazwy zestawu
        if name:
            self.current_flashcards_filename = f"{name}_flashcards.json"  # Utworzenie nazwy pliku na podstawie nazwy zestawu
            self.flashcards = self.load_flashcards()  # Wczytanie istniejących fiszek (jeśli istnieją)
            # Usunięcie pól do wprowadzania tekstu i przycisków
            self.name_entry.destroy()
            self.confirm_button.destroy()
            self.return_button.destroy()

            # Tworzenie pola do wprowadzenia pojęcia
            self.term_entry = tk.Entry(self.master, font=("Verdana", 12))
            self.term_entry.pack(pady=10)  # Umieszczenie pola na ekranie

            # Tworzenie pola do wprowadzenia definicji
            self.definition_entry = tk.Entry(self.master, font=("Verdana", 12))
            self.definition_entry.pack(pady=10)  # Umieszczenie pola na ekranie

            # Tworzenie przycisku "Confirm" do potwierdzenia wprowadzonej fiszki
            self.confirm_button = tk.Button(self.master, text="Confirm", command=self.add_flashcard, font=("Verdana", 12))
            self.confirm_button.pack(pady=10)  # Umieszczenie przycisku na ekranie

            # Tworzenie przycisku "Return" do powrotu do poprzedniego widoku
            self.return_button = tk.Button(self.master, text="Return", command=self.return_to_main_window, font=("Verdana", 12))
            self.return_button.pack(pady=10)  # Umieszczenie przycisku na ekranie

    # Metoda do dodawania nowej fiszki
    def add_flashcard(self):
        term = self.term_entry.get()  # Pobranie wprowadzonego pojęcia
        definition = self.definition_entry.get()  # Pobranie wprowadzonej definicji

        if term and definition:
            self.flashcards[term] = definition  # Dodanie nowej fiszki do słownika
            self.save_flashcards()  # Zapisanie fiszek do pliku
            self.show_flashcards()  # Wyświetlenie wszystkich fiszek

            # Wyczyszczenie pól do wprowadzania tekstu
            self.term_entry.delete(0, tk.END)
            self.definition_entry.delete(0, tk.END)

    # Metoda do wyświetlania wszystkich fiszek
    def show_flashcards(self):
        # Przygotowanie tekstu zawierającego wszystkie fiszki
        flashcard_text = "\n".join([f"{term}: {definition}" for term, definition in self.flashcards.items()])
        # Usunięcie poprzedniej etykiety
        if hasattr(self, "flashcards_label"):
            self.flashcards_label.destroy()
        # Utworzenie nowej etykiety z tekstem zawierającym fiszki
        self.flashcards_label = tk.Label(self.master, text=flashcard_text, font=("Verdana", 12), justify="left")
        self.flashcards_label.pack(pady=20)  # Umieszczenie etykiety na ekranie

    # Metoda do wczytywania fiszek z pliku
    def load_flashcards(self):
        # Sprawdzenie czy istnieje plik z fiszkami
        if self.current_flashcards_filename and os.path.exists(self.current_flashcards_filename):
            with open(self.current_flashcards_filename, "r") as file:
                return json.load(file)  # Wczytanie fiszek z pliku
        else:
            return {}  # Zwrócenie pustego słownika, jeśli plik nie istnieje

    # Metoda do zapisywania fiszek do pliku
    def save_flashcards(self):
        if self.current_flashcards_filename:  # Sprawdzenie czy nazwa pliku została ustalona
            with open(self.current_flashcards_filename, "w") as file:
                json.dump(self.flashcards, file)  # Zapisanie fiszek do pliku

    # Metoda do powrotu do głównego okna
    def return_to_main_window(self):
        if self.name_entry:  # Sprawdzenie czy pole do wprowadzenia nazwy zestawu istnieje
            # Usunięcie pól i przycisków oraz powrót do głównego okna
            self.name_entry.destroy()
            self.confirm_button.destroy()
            self.return_button.destroy()
            self.new_set_button.pack()
            self.term_entry.destroy()
            self.definition_entry.destroy()
            self.flashcards_label.destroy()
        elif self.term_entry:  # Sprawdzenie czy pole do wprowadzenia pojęcia istnieje
            # Usunięcie pól i przycisków oraz powrót do tworzenia nowego zestawu
            self.term_entry.destroy()
            self.definition_entry.destroy()
            self.confirm_button.destroy()
            self.return_button.destroy()
            self.flashcards_label.destroy()
            self.make_new_set()

    # Metoda wywoływana przy zamykaniu aplikacji
    def __del__(self):
        self.save_flashcards()  # Zapisanie fiszek przed zamknięciem aplikacji

# Funkcja główna
def main():
    root = tk.Tk()  # Utworzenie głównego okna
    app = FlashcardsApp(root)  # Utworzenie obiektu aplikacji
    root.mainloop()  # Uruchomienie pętli głównej aplikacji

# Wywołanie funkcji głównej
if __name__ == "__main__":
    main()
