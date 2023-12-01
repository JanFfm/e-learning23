# e-learning23
 
1. Einrichtung
Virtuelle Umgebung erstellen:
    python3 -m venv ./venv

Virtuelle Umgebung aktivieren:
    windows:
    \venv\Scripts>activate

    linux:
    source /venv/bin/activate

packete installieren:
    pip install -r requirements.txt

superuser anlegen 
im ordner /project:
python3 manage.py createsuperuser

Dann die Datenbank aktualisieren. im gleichen verzeichnis 
python3 manage.py makemigrations 
python3 manage.py migrate 
// Dann noch ein paar wörter in die Datenbank laden: 
python3 manage.py loaddata exampe.json 
//(Tipp: Wenn python3 ... nicht geht, dann mit python probieren)//


2. starten: 
virtuelle Umgebung aktivieren, dann unter /project: 
python3 manage.py runserver //


A.)
die Seite ist dann im browser unter 127.0.0.1:8000

B=. admin oberfläche:
127.0.0.1:8000/admin
Hier können z.b auch weitere Vokabeln angelegt werden



Nach änderung im db-model (models.py) immer:
python3 manage.py makemigrations
python3 manage.py migrate

um die tabellen der db zu aktualisieren
