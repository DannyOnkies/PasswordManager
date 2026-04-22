# Password Manager
# Progetto di una applicazione per gestire
# le password di account web , di sim , di accesso al pc ecc.

import json
import os
import secrets
import string

# Importo la classe PasswordManagerGUI dal modulo app_gui presente nel package gui
from gui.app_gui import PasswordManagerGUI


# Classe principale
class PasswordManager:

    def __init__(self):
        self.accounts = []  # attributo interno, lista vuota all'inizio
        # Usa un percorso assoluto basato sulla posizione di questo file
        # Serve a individuare la cartella che contiene lo script attualmente in esecuzione.
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.file_path = os.path.join(base_dir, 'data', 'passwords.json')
        # Assicurati che la cartella data esista
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    def load_data(self):
        """Carica il file JSON all'avvio dell'applicazione"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                self.accounts = json.load(f)
                return 0  # il file esiste e viene caricato senza errori
        except FileNotFoundError:
            # File non trovato, verrà creato al salvataggio
            self.accounts = []
            return 1  # il file non esiste
        except json.JSONDecodeError:
            # Errore nel formato del file JSON. Inizializzazione con lista vuota
            self.accounts = []
            return 2  # ci sono errori nel caricamento del file JSON

    def save_data(self):
        """Salva i dati nel file JSON"""
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(self.accounts, f, indent=4,
                          ensure_ascii=False)  # ensure_ascii garantisce il salvataggio di caratteri speciali
                return 3  # dati salvati con successo
        except OSError as e:
            return 4

    def add_account(self, service, username, password, notes):
        """Aggiunge un nuovo account al manager """
        # creo un dizionario temporaneo
        entry_temp = {'service': service, 'username': username, 'password': password, 'notes': notes}
        self.accounts.append(entry_temp)

    def update_account(self, index, service, username, password, notes):
        """
        Aggiorna un account esistente nella lista in base alla posizione (indice).
        :param index: Posizione dell'account nella lista
        :param service: Nuovo nome del servizio
        :param username: Nuovo nome utente
        :param password: Nuova password
        :param notes: Nuove note
        :return: 'ok' se l'aggiornamento è andato a buon fine, 'errore' altrimenti
        """
        if 0 <= index < len(self.accounts):
            # Creiamo il dizionario con i nuovi dati
            nuovi_dati = {
                'service': service,
                'username': username,
                'password': password,
                'notes': notes
            }
            # Sostituiamo i vecchi dati con quelli nuovi all'indice indicato
            self.accounts[index] = nuovi_dati
            return 'ok'
        else:
            return 'errore'

    def dati_archivio(self):
        """
        Carica i dati dal file JSON e stampa i nomi dei servizi disponibili
        da cui selezionare quello da modificare con la funzione modifica_account()
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for entr in data:
                    print(entr.get('service', 'Servizio senza nome'))
                return data
        except FileNotFoundError:
            print('Il file non esiste')
            return []  # Restituiamo lista vuota se il file non esiste

    def modifica_account(self, service, username, password, notes):
        """
        Modifica un account esistente nel dataset dati.
        Aggiorna i dati e li salva nel file JSON.
        """
        for entry in self.accounts:  # scorro l'archivio
            if entry.get('service') == service:  # se trovo il servizio modifico i dati
                entry['username'] = username
                entry['password'] = password
                entry['notes'] = notes
                print('Account modificato')
                self.save_data()
                return True
        return False

    def remove_account(self, index):
        """
        Rimuove l'account in base all'indice.
        Ritorna 'ok' se rimosso, 'errore' altrimenti.
        """
        if 0 <= index < len(self.accounts):
            del self.accounts[index]
            return 'ok'
        else:
            return 'errore'

    @staticmethod  # converte la funzione in un metodo statico
    # quando un metodo di una classe non ha bisogno di accedere allo stato dell'istanza
    # si usa il decoratore @staticmethod che indica chiaramente che la funzione appartiene
    # alla classe ma è indipendente dalle singole istanze.
    def generate_password(lunghezza):
        """
        Genera una password di lunghezza definita
        :param lunghezza:
        :return password:
        """
        if lunghezza < 4:
            raise ValueError("La lunghezza deve essere almeno 4 per includere tutti i tipi di caratteri")

        # Definizione dei set di caratteri
        lettere_maiuscole = string.ascii_uppercase
        lettere_minuscole = string.ascii_lowercase
        numeri = string.digits
        simboli = string.punctuation

        # Assicurare almeno un carattere per categoria
        password = [
            secrets.choice(lettere_maiuscole),
            secrets.choice(lettere_minuscole),
            secrets.choice(numeri),
            secrets.choice(simboli)
        ]

        # Combinare tutti i caratteri possibili
        tutti_caratteri = lettere_maiuscole + lettere_minuscole + numeri + simboli

        # Aggiungere caratteri casuali fino alla lunghezza desiderata usando ciclo for
        # si usa "_" per dire che la variabile non verrà utilizzata nel ciclo.
        # E una convenzione
        for _ in range(lunghezza - 4):
            carattere_casuale = secrets.choice(tutti_caratteri)
            password.append(carattere_casuale)

        # Mescolare la lista per non avere i primi 4 caratteri sempre in ordine
        secrets.SystemRandom().shuffle(password)

        # Convertire la lista in stringa
        return ''.join(password)


# creo un'istanza della classe PasswordManager dove risiede la logica del programma
manager = PasswordManager()

# leggo i dati dal file ; viene restituito un valore
# 0 se il file esiste e viene caricato senza errori
# 1 se il file non esiste
# 2 se ci sono errori nel caricamento del file JSON
code_error = manager.load_data()

# creo un'istanza della classe PasswordManagerGUI dove risiede la GUI del programma
gui = PasswordManagerGUI('Password Manager v1.0', manager)

# aggiorno la listbox con i dati
gui.aggiorna_listbox()

# mostro un messaggio nella parte bassa della GUI
# con il risultato del caricamento del file JSON
# con i contatti
gui.show_message(code_error)

# avvio la finestra GUI
gui.start()