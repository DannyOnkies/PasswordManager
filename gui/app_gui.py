# Classe che crea la finestra di TKINTER della GUI
from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog

class PasswordManagerGUI:
    def __init__(self, titolo, manager):
        self.manager = manager
        self.titolo = titolo
        self.root = Tk()
        self.root.title(self.titolo)
        self.root.geometry('300x450')
        self.root.resizable(width=False, height=False)

        # creo il frame principale che conterrà gli altri
        self.frame_principale = Frame(self.root, padx=5, pady=5)
        self.frame_principale.pack(expand=True, fill="both")

        # aggiungo tre frame
        # 1 - alto - listbox con i nomi degli account
        # 2 - centro - input dati account
        # 3 - basso - area dei pulsanti

        # 1 - frame per listbox
        self.frame_alto = Frame(self.frame_principale, height=175)
        self.frame_alto.pack(fill="x", pady=1)

        # 2 - frame per input dati
        self.frame_centro = Frame(self.frame_principale, height=175)
        self.frame_centro.pack(fill="x", pady=1)

        # 3 - frame per pulsanti
        self.frame_basso = Frame(self.frame_principale, height=100)
        self.frame_basso.pack(fill="x", pady=1)

        # Creazione Scrollbar
        # con side="right" la barra viene posizionata a destra del frame.
        self.scrollbar = Scrollbar(self.frame_alto)
        self.scrollbar.pack(side="right", fill="y")

        # Creazione Listbox collegata alla scrollbar
        # yscrollcommand: Dice alla Listbox di aggiornare la
        # posizione della barra quando scorri (ad esempio con la rotella del mouse).
        # con side="left" posizioniamo la listbox alla sinistra del frame
        self.listbox = Listbox(self.frame_alto, yscrollcommand=self.scrollbar.set)
        self.listbox.pack(side="left", expand=True, fill="both")
        # Dice alla barra di muovere la vista della Listbox quando la trascini con il mouse.
        self.scrollbar.config(command=self.listbox.yview)

        # collego la listbox alla funzione on_select
        # <<binding>> - se seleziono un valore della listbox viene richiamata la funzione on_select
        self.listbox.bind('<<ListboxSelect>>', self.on_select)


        # Inserimento campi Label ed Entry per input dati
        # Per mettere una Entry a fianco di una Label in modo ordinato usando pack all'interno
        # dello stesso frame il segreto è usare dei "sotto-contenitori" (ovvero dei piccoli Frame
        # orizzontali).
        #
        #  ------------------------------
        #  |  ------------------------  |
        #  |  | label          entry |  |
        #  |  ------------------------  |
        #  |
        #  |  ------------------------  |
        #  |  | label          entry |  |
        #  |  ------------------------  |
        #  |                            |
        #  |  ------------------------  |
        #  |  | label          entry |  |
        #  |  ------------------------  |
        #  ------------------------------
        #
        # --- RIGA 1: SERVICE ---
        self.row1 = Frame(self.frame_centro)  # Creiamo il "cassetto" per la prima riga
        self.row1.pack(fill="x", pady=5)  # Lo mettiamo nell'armadio

        self.lbl_service = Label(self.row1, text="Service", width=10, anchor="w")
        self.lbl_service.pack(side="left", pady=(10, 0))  # Etichetta a sinistra
        self.ent_service = Entry(self.row1)
        self.ent_service.pack(side="left", expand=True, fill="x", padx=5, pady=(10, 0))  # Entry a fianco

        # --- RIGA 2: USERNAME ---
        self.row2 = Frame(self.frame_centro)
        self.row2.pack(fill="x", pady=5)

        self.lbl_username = Label(self.row2, text="Username", width=10, anchor="w")
        self.lbl_username.pack(side="left")
        self.ent_username = Entry(self.row2)
        self.ent_username.pack(side="left", expand=True, fill="x", padx=5)

        # --- RIGA 3: PASSWORD ---
        self.row3 = Frame(self.frame_centro)
        self.row3.pack(fill="x", pady=5)

        self.lbl_password = Label(self.row3, text="Password", width=10, anchor="w")
        self.lbl_password.pack(side="left")
        #self.ent_password = Entry(self.row3, show="*")
        self.ent_password = Entry(self.row3)
        self.ent_password.pack(side="left", expand=True, fill="x", padx=5)

        # --- RIGA 4: NOTES ---
        self.row4 = Frame(self.frame_centro)
        self.row4.pack(fill="x", pady=5)

        self.lbl_notes = Label(self.row4, text="Notes", width=10, anchor="w")
        self.lbl_notes.pack(side="left")
        self.ent_notes = Entry(self.row4)
        self.ent_notes.pack(side="left", expand=True, fill="x", padx=5)

        #        Area dei pulsanti
        #  ------------------------------
        #  |  ------------------------  |
        #  |  |  but1   but2   but3  |  | riga1
        #  |  ------------------------  |
        #  |
        #  |  ------------------------  |
        #  |  |  but1   but2   but3  |  | riga2
        #  |  ------------------------  |
        #  ------------------------------

        # ---- CREO LE RIGHE CHE CONTERRANNO I PULSANTI ----
        self.riga1 = Frame(self.frame_basso)
        self.riga1.pack(fill="x", pady=(20, 5)) # Aumentato lo spazio sopra i pulsanti
        self.riga2 = Frame(self.frame_basso)
        self.riga2.pack(fill="x", pady=5)

        # ---- CREO I PULSANTI ----
        # self.btn_password = Button(self.riga2, text="Password", width=10,command=lambda: self.test_pulsante('Hai premuto il pulsante PASSWORD'))
        # Per passare argomenti a una funzione tramite un pulsante,
        # si usa una funzione anonima chiamata lambda.
        # La parola chiave lambda crea una micro-funzione "usa e getta"
        # che viene definita sulla stessa riga. In pratica, si dice al pulsante:
        # "Quando vieni cliccato, esegui questa piccola lambda, la quale a
        # sua volta eseguirà la mia funzione vera e propria con i parametri".

        self.btn_rimuovi = Button(self.riga1, text="Rimuovi", width=10, command=self.on_rimuovi)
        self.btn_aggiungi = Button(self.riga1, text="Aggiungi", width=10, command=self.on_aggiungi)
        self.btn_modifica = Button(self.riga1, text="Modifica", width=10, command=self.on_modifica)
        self.btn_copia_pwd = Button(self.riga2, text="Copia_PWD", width=10,command=self.on_copia_password)
        self.btn_password = Button(self.riga2, text="Password", width=10,command=self.on_password)
        self.btn_pulisci_entry = Button(self.riga2, text="Pulisci Entry", width=10, command=self.on_svuota_entry)

        # Impacchetto i pulsanti della riga1 (Aggiungi, Modifica, Rimuovi)
        self.btn_aggiungi.pack(side="left", padx=10, pady=5)
        self.btn_modifica.pack(side="left", padx=10, pady=5)
        self.btn_rimuovi.pack(side="left", padx=10, pady=5)

        # Impacchetto i pulsanti della riga2 (Copia_PWD, Password, Pulisci Entry)
        self.btn_copia_pwd.pack(side="left", padx=10, pady=5)
        self.btn_password.pack(side="left", padx=10, pady=5)
        self.btn_pulisci_entry.pack(side="left", padx=10, pady=5)


        # Etichetta per segnalare lo stato del caricamento dei dati all'avvio
        self.lbl_status = Label(self.root, text="Pronto", bd=1, relief="sunken", anchor="w")
        self.lbl_status.pack(side='bottom', fill='x')


    # --- Funzione test per i pulsanti ---
    @staticmethod
    def test_pulsante(info):
        messagebox.showinfo("Test per il pulsante", info)

    def on_password(self):
        # Chiede all'utente la lunghezza della password
        lunghezza = simpledialog.askinteger(
            "Lunghezza password",
            "Inserisci il numero di caratteri:",
            minvalue=4,
            maxvalue=64
        )

        # Se l'utente preme ANNULLA → lunghezza sarà None
        if lunghezza is None:
            return

        # Genera la password
        nuova_password = self.manager.generate_password(lunghezza)

        # Inserisce la password nel campo
        self.ent_password.delete(0, END)
        self.ent_password.insert(0, nuova_password)


    def on_copia_password(self):
        """
        Copia la password selezionata negli appunti.
        """
        password = self.ent_password.get()
        if password:
            self.root.clipboard_clear()  # Pulisce gli appunti
            self.root.clipboard_append(password)  # Aggiunge la password agli appunti
            self.root.update()  # Aggiorna gli appunti
            messagebox.showinfo("Copia Password", "Password copiata negli appunti!")
        else:
            messagebox.showwarning("Copia Password", "Nessuna password da copiare.")

    def on_ordina(self):
        """
        - ordina gli account alfabeticamente
        - aggiorna la Listbox
        - salva il file JSON ordinato
        :return:
        """
        # Ordina la lista degli account
        # Usare la funzione LAMBDA è equivalente a questo:
        # ================================================
        # def estrai_servizio(account):
        #     return account['service'].lower()
        #
        # self.manager.accounts.sort(key=estrai_servizio)
        # ================================================
        #
        self.manager.accounts.sort(key=lambda x: x['service'].lower())

        # Salva i dati ordinati
        self.manager.save_data()

        # Aggiorna la Listbox
        self.aggiorna_listbox()

        # Conferma
        messagebox.showinfo("Ordina", "Elenco ordinato alfabeticamente.")

    def on_svuota_entry(self):
        """
        Pulisce i campi di Entry
        :return:
        """
        self.ent_service.delete(0, END)
        self.ent_username.delete(0, END)
        self.ent_password.delete(0, END)
        self.ent_notes.delete(0, END)

    def on_rimuovi(self ):
        """
        Rimuove l'account selezionato nella listbox
        :return:
        """
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            # prima di rimuovere l'account chiedo conferma con ASKYESNO
            risposta = messagebox.askyesno("Rimuovi", "Sei sicuro di voler rimuovere questo account?")
            if not risposta:
                return
            risultato = self.manager.remove_account(index)
            self.manager.save_data()
            if risultato == 'ok':
                self.aggiorna_listbox()
                self.on_svuota_entry() # elimina contenuto campi Entry
                messagebox.showinfo("Rimuovi", "Account rimosso correttamente.")
            else:
                messagebox.showerror("Errore", "Impossibile rimuovere l'account selezionato.")
        else:
            messagebox.showwarning("Rimuovi", "Devi selezionare un servizio per rimuoverlo!")

    def on_modifica(self):
        """
        Modifica l'account selezionato nella listbox
        """
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]

            service = self.ent_service.get().strip().lower()
            username = self.ent_username.get().strip()
            password = self.ent_password.get().strip()
            notes = self.ent_notes.get().strip()

            risultato = self.manager.update_account(index, service, username, password, notes)

            if risultato == 'ok':
                # Ordino A-Z
                self.manager.accounts.sort(key=lambda x: x['service'])

                # Salvo i dati
                self.manager.save_data()

                # Aggiorno la listbox
                self.aggiorna_listbox()

                # Pulisco i campi
                self.on_svuota_entry()

                messagebox.showinfo("Modifica", "Account modificato correttamente.")
            else:
                messagebox.showerror("Errore", "Impossibile modificare l'account selezionato.")
        else:
            messagebox.showwarning("Modifica", "Devi selezionare un servizio per modificarlo!")

    def on_select(self, event):
        """
        La funzione si attiva alla selezione di un elemento nella listbox.
        :param event:
        :return:
        """
        # curselection() restituisce una tupla di indici, non un numero singolo,
        # quindi bisogna estrarre il primo elemento
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            valore = self.listbox.get(index)
            # visualizzo in un messagebox i dati dell'account selezionato
            #messagebox.showinfo("Account selezionato", f"Hai selezionato l'indice: {index} - Valore: {valore}")
            account = self.manager.accounts[index]
            # print(account)

            # Linee guida per caricare un testo nella Entry:
            # 1. Cancella il contenuto attuale (da indice 0 alla fine)
            # 2. Inserisce la nuova stringa
            #
            # .delete(0, tk.END): Se non pulisci il campo prima di inserire, la nuova stringa
            # verrà aggiunta a quella già presente. Se nel campo c'era "Google" e vuoi mettere
            # "Facebook", otterresti "GoogleFacebook".
            #
            # 0 (lo zero): È l'indice che dice a Tkinter da dove iniziare a scrivere. Usando 0,
            # scrivi dall'inizio del campo.

            # visualizzo i dati dell'account selezionato in Entry
            self.ent_service.delete(0, END)
            self.ent_service.insert(0, account.get('service', 'Servizio senza nome'))
            self.ent_username.delete(0, END)
            self.ent_username.insert(0, account.get('username', 'Username inesistente'))
            self.ent_password.delete(0, END)
            self.ent_password.insert(0, account.get('password', 'Password inesistente'))
            self.ent_notes.delete(0, END)
            self.ent_notes.insert(0, account.get('notes', 'Nessuna nota'))


    def show_message(self,code_error):
        """
        Mostra un messaggio in base al codice di errore o di avviso
        :param code_error: codice di errore
        """
        if code_error == 0:
            self.aggiorna_stato("Dati caricati correttamente!","green")
        elif code_error == 1:
            self.aggiorna_stato("Il file non esiste","red")
        elif code_error == 2:
            self.aggiorna_stato("Errore nel caricamento del file JSON","red")
        elif code_error == 3:
            self.aggiorna_stato("Dati salvati correttamente!","green")
        elif code_error == 4:
            self.aggiorna_stato("Errore di I/O generico durante il salvataggio.","red")

    def aggiorna_listbox(self):
        """
        Aggiorna la listbox con i dati presenti nel manager
        prima svuoto la listbox poi l'aggiorno
        :return:
        """
        self.listbox.delete(0, END) # svuoto la listbox
        for entry in self.manager.accounts:
            self.listbox.insert(END, entry.get('service', 'Servizio senza nome'))
            #self.listbox.insert(END, entry['service'])

    def on_salva(self):
        risultato = self.manager.save_data()
        if risultato == 3:
            messagebox.showinfo("Salvataggio", "Dati salvati con successo!")
        elif risultato == 4:
            messagebox.showerror("Errore", "Errore di I/O generico durante il salvataggio.")


    def on_aggiungi(self):
        """
        Aggiunge un nuovo account al manager
        """
        service = self.ent_service.get().strip().lower()
        username = self.ent_username.get().strip()
        password = self.ent_password.get().strip()
        notes = self.ent_notes.get().strip()

        # Controllo se tutti i campi sono stati compilati
        if service and username and password and notes:
            # Aggiungo l'account
            self.manager.add_account(service, username, password, notes)
            # Ordino A-Z
            self.manager.accounts.sort(key=lambda x: x['service'])
            # Salvo i dati
            self.manager.save_data()
            # Aggiorno la listbox
            self.aggiorna_listbox()
            # Pulisco i campi
            self.on_svuota_entry()
        else:
            messagebox.showwarning('Campi vuoti', 'Compila tutti i campi')



    def aggiorna_stato(self,messaggio, colore="black"):
        """
        Aggiorna lo stato della finestra GUI
        :param messaggio:
        :param colore:
        :return:
        """
        self.lbl_status.config(text=messaggio, fg=colore)
        # Dopo 3000ms (3 secondi), cancella il testo
        self.root.after(3000, lambda: self.lbl_status.config(text=""))

    def start(self):
        """
        Avvia la finestra GUI
        :return:
        """
        # forza il focus sull'app
        self.root.focus_force()
        self.root.mainloop()


