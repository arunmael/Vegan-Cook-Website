# Projektdokumentation – Vegan Cook Website

## 1. Idee des Projekts

In diesem Projekt entwickel ich eine Webseite für vegane Rezepte. Benutzer sollen später eigene Rezepte hochladen, Rezepte von anderen Personen anschauen und interessante Rezepte speichern können. Zusätzlich soll es eine Suchfunktion geben, bei der man Zutaten eingibt, die man noch zu Hause hat. Danach sollen passende Rezepte vorgeschlagen werden.

Das Ziel ist also, dass man neue vegane Gerichte entdecken kann und gleichzeitig weniger Lebensmittel verschwendet.

## 2. Was bis jetzt gemacht wurde

Das Projekt wurde am 7. Juli 2026 gestartet. Danach wurde zuerst die grundlegende Ordnerstruktur erstellt und die benötigten Python-Pakete wurden festgelegt.

Am 29. Juli 2026 wurde die Datenbank geplant und erstellt. Dazu gibt es ein ER-Diagramm als Draw.io-Datei und zusätzlich als PNG-Bild. Im ER-Diagramm sieht man die Tabellen und ihre Beziehungen.

Am 31. Juli 2026 wurde die SQL-Struktur verbessert und fertig geplant. Ausserdem wurde das Backend mit FastAPI gestartet, die Verbindung zur MySQL-Datenbank eingerichtet und mit den ersten Models und Schemas begonnen.

Momentan besteht das Projekt aus drei wichtigen Teilen:

- `frontend`: Der Teil, den Benutzer später im Browser sehen und bedienen.
- `backend`: Die API und die Logik des Projekts.
- `db`: Die Struktur und Planung der MySQL-Datenbank.

## 3. Aufbau des Projekts

```text
vegan-cook-website/
├── backend/
│   └── app/
│       ├── config.py
│       ├── db.py
│       ├── main.py
│       ├── model.py
│       ├── schema.py
│       └── routes/
│           └── create.py
├── db/
│   ├── Base Modell ERD.drawio
│   ├── Base Modell ERD.drawio.png
│   └── structure.sql
├── frontend/
│   └── app.js
├── README.md
├── requirements.txt
└── LICENSE
```

## 4. Datenbank

Für die Datenbank wird MySQL verwendet. Die Datenbank heisst `vegan_cook_website`. In der Datei `db/structure.sql` stehen alle SQL-Befehle, mit denen die Datenbank und ihre Tabellen erstellt werden.

Aktuell gibt es folgende Tabellen:

### `user`

Hier werden die Benutzer gespeichert. Ein Benutzer besitzt eine automatisch erstellte ID, einen eindeutigen Benutzernamen, eine E-Mail-Adresse und ein Passwort.

### `recipe`

Diese Tabelle speichert die Rezepte. Zu einem Rezept gehören der Name, eine Beschreibung, die Anleitung, ein Bild, die Zubereitungszeit, der Autor und die Herkunft.

### `ingredient`

Hier werden alle Zutaten gespeichert. Jede Zutat besitzt eine ID und einen eindeutigen Namen.

### `category`

Die Kategorien helfen dabei, Rezepte zu sortieren. Eine Kategorie könnte zum Beispiel „Frühstück“, „Dessert“ oder „Hauptgericht“ sein.

### `origin`

Hier wird die Herkunft eines Rezeptes gespeichert, zum Beispiel Italien, Indien oder Schweiz.

### Verbindungstabellen

Ein Rezept kann mehrere Zutaten und mehrere Kategorien haben. Gleichzeitig können Zutaten und Kategorien bei mehreren Rezepten vorkommen. Deshalb gibt es dafür eigene Verbindungstabellen:

- `recipe_ingredient` verbindet Rezepte mit Zutaten und speichert zusätzlich die Menge und Einheit.
- `recipe_category` verbindet Rezepte mit Kategorien.
- `saved_recipe` speichert, welcher Benutzer welches Rezept gespeichert hat.
- `rating` speichert die Bewertung eines Benutzers für ein Rezept.

Die Primary Keys sorgen dafür, dass jeder Datensatz eindeutig erkannt werden kann. Die Foreign Keys verbinden die Tabellen miteinander. Zum Beispiel verweist `author_id` in der Tabelle `recipe` auf den Benutzer, der das Rezept erstellt hat.

## 5. Backend

Das Backend wird mit Python und FastAPI entwickelt. FastAPI nimmt Anfragen vom Frontend entgegen und gibt Antworten zurück. SQLAlchemy wird verwendet, damit man mit Python auf die Datenbank zugreifen kann.

### `config.py`

In dieser Datei befinden sich die Einstellungen für die Datenbank. Dazu gehören Host, Port, Datenbankname, Benutzername und Passwort. Diese Werte können aus einer `.env`-Datei geladen werden. Dadurch muss man echte Zugangsdaten nicht direkt in den Python-Code schreiben.

Die Eigenschaft `database_url` baut aus den Einstellungen eine vollständige Verbindungsadresse für MySQL und PyMySQL zusammen.

### `db.py`

Diese Datei erstellt die Verbindung zur Datenbank. Der `engine` ist dabei die grundlegende Verbindung von SQLAlchemy zu MySQL.

Mit `SessionLocal` kann für eine Anfrage eine Datenbank-Session erstellt werden. Die Funktion `get_db()` stellt so eine Session bereit und schliesst sie nach der Benutzung wieder. Das ist wichtig, damit nicht unnötig viele offene Verbindungen entstehen.

Die Funktion `check_database_connection()` führt den einfachen SQL-Befehl `SELECT 1` aus. Damit wird getestet, ob die Datenbank erreichbar ist.

### `main.py`

Hier wird die FastAPI-Anwendung erstellt. Momentan gibt es den Endpunkt:

```text
GET /api/health
```

Dieser Endpunkt prüft die Verbindung zur Datenbank. Wenn alles funktioniert, kommt folgende Antwort zurück:

```json
{
  "status": "ok",
  "database": "reachable"
}
```

### `model.py`

Ein Model ist wie ein Bauplan zwischen Python und einer Tabelle in der Datenbank. Die Klasse `Base` ist die gemeinsame Basisklasse für alle SQLAlchemy-Models.

`Mapped[int]` oder `Mapped[str]` gibt an, welchen Python-Datentyp eine zugeordnete Datenbankspalte besitzt. `mapped_column()` beschreibt die Spalte genauer, zum Beispiel ob sie ein Primary Key ist, automatisch hochgezählt wird oder nicht leer sein darf.

Momentan wird das Model von `Ingredient` zu `User` umgebaut. `user_id` ist bereits vorhanden. Das zweite Feld heisst aber noch `ing_name` und passt deshalb nicht zur Tabelle `user`. Später müssen dort wahrscheinlich `user_name`, `user_email` und `user_password` eingetragen werden.

### `schema.py`

Schemas werden mit Pydantic erstellt. Sie bestimmen, welche Daten die API erwartet und welche Daten sie zurückgibt.

Aktuell gibt es:

- `IngredientCreate` für das Erstellen einer Zutat.
- `IngredientResponse` für die Antwort der API mit `ingredient_id` und `ing_name`.

Mit `Field(min_length=1, max_length=255)` wird geprüft, dass ein Zutatenname nicht leer und nicht länger als 255 Zeichen ist.

### `routes/create.py`

In dieser Datei wurde mit einem Endpunkt zum Erstellen eines Benutzers begonnen:

```text
POST /api/create-user
```

Der Endpunkt nimmt momentan Benutzername, E-Mail und Passwort entgegen und erhält mit `Depends(get_db)` eine Datenbank-Session. Die eigentliche Logik zum Speichern des Benutzers fehlt aber noch. Ausserdem ist hier aktuell eine zweite FastAPI-Anwendung erstellt. Später sollte die Route wahrscheinlich über einen `APIRouter` in `main.py` eingebunden werden.

## 6. Frontend

Im Frontend gibt es bis jetzt die JavaScript-Datei `frontend/app.js`.

Die Funktion `loadHealth()` ruft `/api/health` auf. Danach wird im HTML angezeigt, ob die API und die Datenbank funktionieren.

Die Funktion `loadRecipes()` ruft `/api/recipes` auf und möchte die erhaltenen Rezepte als Liste anzeigen. Der passende Backend-Endpunkt existiert momentan aber noch nicht. Auch eine HTML-Datei mit den Elementen `status` und `recipes` ist im Projekt noch nicht vorhanden.

Das Frontend ist deshalb aktuell eher eine Vorbereitung und noch nicht komplett benutzbar.

## 7. Verwendete Technologien

- Python für das Backend
- FastAPI für die API
- Uvicorn als Webserver für FastAPI
- SQLAlchemy für die Arbeit mit der Datenbank
- PyMySQL als Verbindung zwischen Python und MySQL
- Pydantic für das Prüfen von API-Daten
- python-dotenv und pydantic-settings für Einstellungen aus der `.env`-Datei
- MySQL für die Datenbank
- JavaScript für das Frontend
- Draw.io für das ER-Diagramm
- Git für die Versionsverwaltung

Die genauen Python-Pakete und Versionen stehen in `requirements.txt`.

## 8. Was ich dabei gelernt habe

Bis jetzt habe ich gelernt, wie man eine relationale Datenbank plant und Tabellen mit Primary Keys und Foreign Keys verbindet. Ich habe auch besser verstanden, warum man bei Beziehungen mit mehreren Einträgen Verbindungstabellen braucht.

Beim Backend habe ich gelernt, wie FastAPI grundsätzlich aufgebaut ist und wie ein API-Endpunkt funktioniert. Ausserdem weiss ich jetzt besser, wofür Models, Schemas und Datenbank-Sessions gebraucht werden. Ein Model stellt die Verbindung zwischen einer Python-Klasse und einer Datenbanktabelle her. Ein Schema prüft dagegen die Daten, die über die API gesendet oder empfangen werden.

## 9. Aktueller Stand und nächste Schritte

Die Grundidee, die Ordnerstruktur und die Datenbankplanung sind vorhanden. Die Verbindung zwischen FastAPI und MySQL ist ebenfalls vorbereitet und kann mit dem Health-Endpunkt geprüft werden.

Als Nächstes müssen noch folgende Punkte gemacht werden:

1. Das `User`-Model passend zur SQL-Tabelle fertigstellen.
2. Weitere Models für Rezepte, Zutaten, Kategorien und die anderen Tabellen erstellen.
3. Die benötigten Pydantic-Schemas ergänzen.
4. Den Endpunkt zum Erstellen eines Benutzers fertig programmieren.
5. Passwörter vor dem Speichern sicher hashen und niemals als normalen Text speichern.
6. Routen für das Erstellen, Anzeigen, Bearbeiten und Löschen von Rezepten bauen.
7. Den Endpunkt `/api/recipes` umsetzen.
8. Eine HTML-Oberfläche erstellen und mit `app.js` verbinden.
9. Eingaben und Fehlermeldungen testen.
10. Später die intelligente Rezeptsuche nach vorhandenen Zutaten umsetzen.

## 10. Fazit

Das Projekt befindet sich noch am Anfang, aber die wichtigste Planung ist bereits gemacht. Vor allem die Datenbank hat schon eine gute Grundlage. Das Backend kann die Datenbankverbindung testen und erste Models, Schemas und Routen wurden angefangen. Der nächste grosse Schritt ist, diese Teile richtig miteinander zu verbinden, damit Benutzer und Rezepte wirklich gespeichert und angezeigt werden können.
