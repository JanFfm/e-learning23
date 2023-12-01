# e-learning23
 
1. Einrichtung
1.1 Virtuelle Umgebung erstellen:
    python3 -m venv ./venv

1.2 Virtuelle Umgebung aktivieren:
    windows:
    \venv\Scripts>activate
    linux:
    source venv/bin/activate

1.3 packete installieren:
    pip install -r requirements.txt



1.4 Dann die Datenbank aktualisieren. im gleichen verzeichnis 
python3 manage.py makemigrations 
python3 manage.py migrate 

1.5 Dann noch ein paar wörter in die Datenbank laden: 
python3 manage.py loaddata presentation_data.json 

1.6 user anlegen 
im ordner /project:
python3 manage.py createsuperuser

//(Tipp: Wenn python3 ... nicht geht, dann mit python probieren)//


2. starten:
virtuelle Umgebung aktivieren, dann unter /project: 
python3 manage.py runserver //
A.)
die Seite ist dann im browser unter 127.0.0.1:8000

B). admin oberfläche:
127.0.0.1:8000/admin
Hier können z.b auch weitere Vokabeln angelegt werden


Nach änderung im db-model (models.py) immer:
python3 manage.py makemigrations
python3 manage.py migrate

um die tabellen der db zu aktualisieren.
