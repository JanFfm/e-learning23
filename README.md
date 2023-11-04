# e-learning23
 
1. Schritte
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


zum starten:
virtuelle Umgebung aktivieren, dann unter /project:
python3 manage.py runserver

dann im browser über 127.0.0.1:8000

admin oberfläche:
127.0.0.1:8000/admin


Nach änderung im db-model (models.py) immer:
python3 manage.py makemigrations
python3 manage.py migrate

um die tabellen der db zu aktualisieren