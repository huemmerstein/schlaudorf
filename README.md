# Schlaudorf – Open Source Nachbarschaftshilfe

Schlaudorf ist eine offene Nachbarschaftshilfe-Web-App. Sie kombiniert ein 
leichtgewichtiges Frontend (HTML, Tailwind CSS, JavaScript + Leaflet) mit einem 
Python/Django-Backend und setzt auf PostgreSQL **oder** MariaDB. Das Ziel sind 
ca. 1.000 Benutzerinnen und Benutzer. Die Benutzerverwaltung erfolgt durch 
Admin-Konten, alle Komponenten sind Open Source.

Dieses README wird **nach jedem Entwicklungsschritt** erweitert und dient als 
fortlaufende Dokumentation.

---

## 1. Kernfunktionen

- Benutzerprofile mit Avatar, Fähigkeiten und Rollen (Helfer/Anfragende)
- Hilfegesuche und Angebote mit Geokoordinaten
- Echtzeit-Chat über WebSockets
- Terminabsprachen mit Kalenderfunktion
- Responsive Oberfläche mit Tailwind CSS
- Progressive Web App (Offline-Modus & Push-Notifications)

---

## 2. Technologie-Stack

| Ebene        | Komponente                                                  |
|--------------|-------------------------------------------------------------|
| Backend      | Python 3, Django, Django REST Framework, Channels, Celery   |
| Frontend     | HTML5, Tailwind CSS, Vanilla JS, Leaflet                    |
| Datenbank    | PostgreSQL **oder** MariaDB                                 |
| Caching/Queue| Redis (optional, für Sessions & Hintergrundjobs)            |
| Server       | Nginx + Gunicorn                                            |

---

## 3. Installationsanleitung (Ubuntu)

1. **System vorbereiten**

   ```bash
   sudo apt update && sudo apt upgrade -y
   sudo apt install -y python3-venv python3-dev build-essential \
       libpq-dev libmariadb-dev-compat libmariadb-dev git curl nginx
   ```

2. **Repository klonen und virtuelle Umgebung einrichten**

   ```bash
   git clone <REPO_URL> schlaudorf
   cd schlaudorf
   python3 -m venv venv
   source venv/bin/activate
   pip install --upgrade pip
   ```

3. **Python-Abhängigkeiten installieren**

   ```bash
   pip install django djangorestframework psycopg[binary] mysqlclient \
       django-cors-headers channels redis celery gunicorn whitenoise
   ```

4. **Tailwind CSS initialisieren**

   ```bash
   npm init -y
   npm install -D tailwindcss postcss autoprefixer
   npx tailwindcss init
   ```

5. **Datenbank vorbereiten**

   - PostgreSQL

     ```bash
     sudo apt install postgresql postgresql-contrib
     sudo -u postgres psql -c "CREATE DATABASE nachbarschaft;"
     sudo -u postgres psql -c "CREATE USER nb_user WITH PASSWORD 'STRONG_PASSWORD';"
     sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE nachbarschaft TO nb_user;"
     ```

   - MariaDB

     ```bash
     sudo apt install mariadb-server mariadb-client
     sudo mysql -e "CREATE DATABASE nachbarschaft;"
     sudo mysql -e "CREATE USER 'nb_user'@'localhost' IDENTIFIED BY 'STRONG_PASSWORD';"
     sudo mysql -e "GRANT ALL PRIVILEGES ON nachbarschaft.* TO 'nb_user'@'localhost';"
     ```

6. **Django-Projekt und Apps erstellen**

   ```bash
   django-admin startproject backend
   cd backend
   python manage.py startapp users
   python manage.py startapp help_requests
   python manage.py startapp chat
   python manage.py startapp appointments
   mkdir templates static
   ```

7. **Migrationen ausführen und Superuser anlegen**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```

8. **Entwicklungsserver starten**

   ```bash
   python manage.py runserver
   ```

---

## 4. Weiteres Vorgehen

- Chat-Consumer implementieren (Django Channels)
- Tailwind-Komponenten für moderne UI hinzufügen
- Terminverwaltung mit Kalenderbibliothek erweitern
- Service Worker und Web-Push für PWA-Funktionen integrieren
- Tests (pytest-django) und CI/CD-Pipeline einrichten

---

## 5. Lizenz

Dieses Projekt ist Open Source und steht unter der MIT-Lizenz. Ein Verkauf 
ist nicht vorgesehen.

