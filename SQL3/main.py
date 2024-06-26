import tkinter as tk #Importerer tkinter som tk
import customtkinter as ctk #Importerer ctk
import sqlite3 #Importerer sqlite3
import csv #Importerer csv

with sqlite3.connect("Database.db") as DB: #Lager en database som heter Database.db
         Cursor = DB.cursor()#Lager en Cursor som heter DB.cursor
 
def OpprettDatabase():#Lager en funksjon som heter OpprettDatabase
    with sqlite3.connect("TomDatabase.db") as TDB: #Lager en database som heter Database.db
         Cursor = TDB.cursor()#Lager en Cursor som heter TDB.cursor

def LagPostnummerTabell():#Lager en funksjon som heter LagPostnummerTabell
    with sqlite3.connect("Database.db") as DB: #Lager en database som heter Database.db om den ikke eksisterer.
         Cursor = DB.cursor()#Lager en Cursor som heter DB.cursor

    Cursor.execute('''
    CREATE TABLE IF NOT EXISTS postnummer(
                   Postnummer NOT NULL,
                   Poststed NOT NULL,
                   Kommunenummer NOT NULL,
                   Kommunenavn NOT NULL,
                   Kategori NOT NULL);
    ''')#Lager en tabell som heter postnummer med kolonnene Postnummer, Poststed, Kommunenummer, Kommunenavn og Kategori     
 
    with open('Postnummerregister.csv', 'r') as file:#Åpner en csv fil som heter Postnummerregister.csv
        reader = csv.reader(file)#Leser fra csv filen
        next(reader)#Hopper over første rad i csv filen
        for row in reader:#Går igjennom hver rad i csv filen
        
            #Legger til radene i databasen
            Cursor.execute('''
            INSERT INTO postnummer(Postnummer, 
                           Poststed, 
                           Kommunenummer, 
                           Kommunenavn, 
                           Kategori)
            VALUES(?, ?, ?, ?, ?)''', row)
            DB.commit()#Lagrer endringene i databasen

    
def LagBrukerTabell():#Lager en funksjon som heter LagBrukerTabell
    try:
        Cursor.execute('''CREATE TABLE IF NOT EXISTS Brukerdatabase(id INTEGER PRIMARY KEY, 
                       fname VARCHAR(25) NOT NULL, 
                       ename VARCHAR(30) NOT NULL, 
                       epost VARCHAR (50) UNIQUE, 
                       tlf INTEGER UNIQUE, 
                       postnummer INTEGER)
    ''')#Lager en tabell som heter Brukerdatabase med kolonnene id, fname, ename, epost, tlf og postnummer
        
        with open('Brukerdatabase.csv', 'r') as file:#Åpner en csv fil som heter Brukerdatabase.csv
            reader = csv.reader(file)#Leser fra csv filen
            next(reader)#Hopper over første rad i csv filen
            for row in reader:#Går igjennom hver rad i csv filen
                Cursor.execute('''
                INSERT INTO Brukerdatabase(fname, ename, epost, tlf, postnummer)
                VALUES(?, ?, ?, ?, ?)''', row)#Legger til radene i databasen
        DB.commit() #Lagrer endringene i databasen

        Cursor.execute('''
    SELECT Brukerdatabase.id, 
       Brukerdatabase.fname, 
       Brukerdatabase.ename, 
       Brukerdatabase.epost, 
       Brukerdatabase.tlf, 
       Brukerdatabase.postnummer, 
       postnummer.Poststed, 
       postnummer.Kommunenummer, 
       postnummer.Kommunenavn, 
       postnummer.Kategori 
    FROM Brukerdatabase 
    JOIN postnummer ON postnummer.postnummer = Brukerdatabase.postnummer
    ORDER BY Brukerdatabase.id ASC
    ''') #sammenspleiser tabellene brukerdatabase og postnummer og sorterer etter id sånn at man ser det enklere det er også denne koden her som spleiser postnummer sammen med brukerdatabase

        Resultat = Cursor.fetchall()#Henter ut alle resultatene fra databasen

    except Exception as e:
        print(f"En feil har oppstått: {e}")#Printer ut en feilmelding hvis det oppstår en feil

def SlettPostnummerTabell():#Lager en funksjon som heter SlettPostnummerTabell
    Cursor.execute('''DROP TABLE IF EXISTS postnummer''')#Sletter tabellen postnummer
    DB.commit()#Lagrer endringene i databasen

def SlettBrukerTabell():#Lager en funksjon som heter SlettBrukerTabell
    Cursor.execute('''DROP TABLE IF EXISTS Brukerdatabase''')#Sletter tabellen postnummer
    DB.commit()#Lagrer endringene i databasen


def main():#Lager en funksjon som heter main
    Root = tk.Tk()#Lager et vindu som heter Root
    Root.title("Endre i Systemet")#Setter tittelen på vinduet til Endre i systemet"
    Root.eval('tk::PlaceWindow . center')#Setter vinduet i midten av skjermen
    Root.geometry("400x500",)#Setter størrelsen på vinduet til 300x300
    Root.configure(bg='#001B3A')#Endrer bakgrunnsfargen til grå

    LagTomDataBaseLabel = ctk.CTkLabel(Root,#Lager en label som heter lag tom database label
                              text_color="white", #Endrer fargen på teksten til svart
                              font=("TkHeadingFont", 20),#Endrer fonten til 20
                              text="Legg til Tom Database Her:").pack()#Pakker inn brukernavnlabelo og brukernavnentry feltet
    
    LagTomDataBaseButton = ctk.CTkButton(Root,#Lager en knapp som heter lagtomdatabasebutton
                                text="Lag Tom Databasen",#Endrer teksten på det som står i knappen
                                fg_color="#00FF00",#Endrer fargen på på selve knappen
                                text_color="white",#Endrer fargen på teksten til knappen
                                hover_color="#32CD32",#Endrer fargen til knappen når du holder over den
                                font=("TkMenuFont", 15),#Endrer fonten skriften til knappen
                                cursor="hand2",#Endrer cursor til en hånd når du holder over knappen
                                command=OpprettDatabase,).pack(pady=20)
    
    LeggIHovedDataBaseLabel = ctk.CTkLabel(Root,#Lager en label som heter legg inn i hoveddatabasen label
                              text_color="white", #Endrer fargen på teksten til svart
                              font=("TkHeadingFont", 20),#Endrer fonten til 20
                              text="Legg til i Hoveddatabasen Her:").pack()#Pakker inn brukernavnlabelo og brukernavnentry feltet
        
    LagPostnummerButton = ctk.CTkButton(Root,#Lager en knapp som heter lagpostnummerbutton
                                text="Lag Postnummertabell",#Endrer teksten på det som står i knappen
                                fg_color="#00FF00",#Endrer fargen på på selve knappen
                                text_color="white",#Endrer fargen på teksten til knappen
                                hover_color="#32CD32",#Endrer fargen til knappen når du holder over den
                                font=("TkMenuFont", 15),#Endrer fonten skriften til knappen
                                cursor="hand2",#Endrer cursor til en hånd når du holder over knappen
                                command=LagPostnummerTabell,).pack(pady=5)
    
    LagBrukerButton = ctk.CTkButton(Root,#Lager en knapp som heter lagbrukerbutton
                                text="Lag BrukerTabell",#Endrer teksten på det som står i knappen
                                fg_color="#00FF00",#Endrer fargen på på selve knappen
                                text_color="white",#Endrer fargen på teksten til knappen
                                hover_color="#32CD32",#Endrer fargen til knappen når du holder over den
                                font=("TkMenuFont", 15),#Endrer fonten skriften til knappen
                                cursor="hand2",#Endrer cursor til en hånd når du holder over knappen
                                command=LagBrukerTabell,).pack(pady=15)
    
    

    SlettTingHoveddataBaseLabel = ctk.CTkLabel(Root,#label for sletting av ting i hoveddatabasen
                        text_color="white",#Endrer fargen på teksten til svart
                        font=("TkHeadingFont", 20),#Endrer fonten til 20
                        text="Fjern i Hoveddatabasen Her:"#lager en tekst som står skriv inn ditt passord
                        ).pack()#Pakker inn passordlabel
    
    SlettPostnummerButton = ctk.CTkButton(Root,#Lager en knapp som heter slettpostnummerbutton
                                text="Slett Postnummertabell",#Endrer teksten på det som står i knappen
                                fg_color="red",#Endrer fargen på på selve knappen
                                text_color="white",#Endrer fargen på teksten til knappen
                                hover_color="#B22222",#Endrer fargen til knappen når du holder over den
                                font=("TkMenuFont", 15),#Endrer fonten skriften til knappen
                                cursor="hand2",#Endrer cursor til en hånd når du holder over knappen
                                command=SlettPostnummerTabell,).pack(pady=5)
    
    SlettBrukerButton = ctk.CTkButton(Root,#Lager en knapp som heter slettbrukerbutton
                                text="Slett Brukertabell",#Endrer teksten på det som står i knappen
                                fg_color="red",#Endrer fargen på på selve knappen
                                text_color="white",#Endrer fargen på teksten til knappen
                                hover_color="#B22222",#Endrer fargen til knappen når du holder over den
                                font=("TkMenuFont", 15),#Endrer fonten skriften til knappen
                                cursor="hand2",#Endrer cursor til en hånd når du holder over knappen
                                command=SlettBrukerTabell,).pack(pady=15)
    
    LagerCTKVinduetlabel = ctk.CTkLabel(Root,#label for sletting av ting i hoveddatabasen
                        text_color="white",#Endrer fargen på teksten til svart
                        font=("TkHeadingFont", 20),#Endrer fonten til 20
                        text="Hent Opplysninger på brukere:"#lager en tekst som står skriv inn ditt passord
                        ).pack()#Pakker inn passordlabel
    
    LagerCTKVinduetButton = ctk.CTkButton(Root,#Lager en knapp som heter slettbrukerbutton
                                text="Hent Opplysninger",#Endrer teksten på det som står i knappen
                                fg_color="blue",#Endrer fargen på på selve knappen
                                text_color="white",#Endrer fargen på teksten til knappen
                                hover_color="#151B54",#Endrer fargen til knappen når du holder over den
                                font=("TkMenuFont", 15),#Endrer fonten skriften til knappen
                                cursor="hand2",#Endrer cursor til en hånd når du holder over knappen
                                command=LagerCTKVinduet).pack(pady=15) 

    Root.mainloop()#Kjører programmet



def HentBrukerInfo(BrukerID):#Lager en funksjon som heter HentBrukerInfo og tar inn brukerID.
    Cursor.execute('''
        SELECT Brukerdatabase.id, 
           Brukerdatabase.fname, 
           Brukerdatabase.ename, 
           Brukerdatabase.epost, 
           Brukerdatabase.tlf, 
           Brukerdatabase.postnummer, 
           postnummer.Poststed, 
           postnummer.Kommunenummer, 
           postnummer.Kommunenavn, 
           postnummer.Kategori 
        FROM Brukerdatabase 
        JOIN postnummer ON postnummer.postnummer = Brukerdatabase.postnummer
        WHERE Brukerdatabase.id = ?
        ORDER BY Brukerdatabase.id ASC
    ''', (BrukerID,))#Henter ut brukerinfoen fra databasen og bruker join for å spleise sammen tabellene brukerdatabase og postnummer.
    return Cursor.fetchone()#Henter ut brukerinfoen fra databasen


def HenterOGPrinterDataen():#Lager en funksjon som heter HenterOGPrinterDataen
    BrukerID = IDEntry.get()#Henter brukerID fra brukerinputen
    if not BrukerID.isdigit():#Sjekker om brukerID er et tall
        print("Error: BrukerID må være et tall ikke bokstaver.")#Printer feilmelding om noen bruker bokstaver istedenfor tall
        return#Returnerer tilbake til starten av funksjonen
    
    BrukerInfo = HentBrukerInfo(BrukerID)#Henter brukerinfoen fra databasen
    if BrukerInfo is None:#Hvis brukeren ikke finnes i databasen så vil det komme en feilmelding
        print("Error: Brukeren ligger ikke i databasen prøv en annen ID.")#Printer ut en feilmelding hvis det oppstår en feil
    else:#Hvis brukeren finnes i databasen så vil det ikke komme en feilmelding
        print(BrukerInfo)#Printer ut brukerinfoen


def LagerCTKVinduet():#Lager en funksjon som heter main
    VinduCTK = ctk.CTk()#Lager et vindu som heter Root
    VinduCTK.title("Opplysninger om Brukere")#Setter tittelen på vinduet til Endre i systemet"
    VinduCTK.eval('tk::PlaceWindow . center')#Setter vinduet i midten av skjermen
    VinduCTK.geometry("400x500",)#Setter størrelsen på vinduet til 300x300
    VinduCTK.configure(fg='#001B3A')#Endrer bakgrunnsfargen til grå
    
    global IDEntry#Gjør IDEntry global sånn at vi kan bruke den i andre funksjoner som ikke ligger i en funkjson, eksempel så ligger den i HenterOGPrinterDataen funksjonen som er en annen funksjon enn main funksjonen
    IDLabel = ctk.CTkLabel(VinduCTK, text="Skriv inn Bruker ID:", bg_color="#333333", font=("TkMenuFont", 15))
    IDLabel.pack(pady=15) 

    IDEntry = tk.Entry(VinduCTK)#Lager en entry som heter IDEntry som er en input boks for brukerID
    IDEntry.pack()#Pakker inn IDEntry boksen
    # SjekkerBrukerinformasjonID er knappen for å hente brukerinformasjonen
    SjekkBrukerinformasjonID = ctk.CTkButton(VinduCTK,
                                text="Hent Brukerinformasjonen",
                                fg_color="blue",
                                text_color="white",
                                hover_color="#151B54",
                                font=("TkMenuFont", 15),
                                cursor="hand2",
                                command=HenterOGPrinterDataen)
    SjekkBrukerinformasjonID.pack(pady=15)



if __name__ == '__main__':#Hvis filen blir kjørt direkte
    main()#Kjører main()