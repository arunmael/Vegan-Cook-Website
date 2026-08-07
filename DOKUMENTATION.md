# Projektdokumentation – Vegan Cook Website

## 1. Idee des Projekts

In diesem Projekt entwickel ich eine Webseite für vegane Rezepte. Benutzer sollen später eigene Rezepte hochladen, Rezepte von anderen Personen anschauen und interessante Rezepte speichern können. Zusätzlich soll es eine Suchfunktion geben, bei der man Zutaten eingibt, die man noch zu Hause hat. Danach sollen passende Rezepte vorgeschlagen werden.

Das Ziel ist also, dass man neue vegane Gerichte entdecken kann und gleichzeitig weniger Lebensmittel verschwendet.

## 2. Was bis jetzt gemacht wurde

Das Projekt wurde am 7. Juli 2026 gestartet. Danach wurde zuerst die grundlegende Ordnerstruktur erstellt und die benötigten Python-Pakete wurden festgelegt.

Am 29. Juli 2026 wurde die Datenbank geplant und erstellt. Dazu gibt es ein ER-Diagramm als Draw.io-Datei und zusätzlich als PNG-Bild. Im ER-Diagramm sieht man die Tabellen und ihre Beziehungen.

Am 31. Juli 2026 wurde die SQL-Struktur verbessert und fertig geplant. Ausserdem wurde das Backend mit FastAPI gestartet, die Verbindung zur MySQL-Datenbank eingerichtet und mit den ersten Models und Schemas begonnen.

Am 7. August 2026 wurde die Benutzerregistrierung im Backend umgesetzt. Dazu wurden das `User`-Model, passende Pydantic-Schemas und der Endpunkt `POST /api/create-user` ergänzt. Passwörter werden vor dem Speichern mit PBKDF2 und einem zufälligen Salt gehasht. Zusätzlich wurde ein Startskript erstellt, das das Datenbankpasswort verdeckt im Terminal abfragt.

Danach wurde der E-Mail-Login begonnen. Der Endpunkt `POST /api/login-user-email` sucht einen Benutzer anhand seiner E-Mail-Adresse und prüft das eingegebene Passwort gegen den gespeicherten PBKDF2-Hash. Eine dauerhafte Anmeldung über eine Session oder ein signiertes Token ist noch nicht umgesetzt.

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
│           ├── create.py
│           └── select.py
├── db/
│   ├── Base Modell ERD.drawio
│   ├── Base Modell ERD.drawio.png
│   └── structure.sql
├── frontend/
│   └── app.js
├── .env.example
├── start_backend.sh
├── DOKUMENTATION.md
├── README.md
├── requirements.txt
└── LICENSE
```

## 4. Datenbank

Für die Datenbank wird MySQL verwendet. Die Datenbank heisst `vegan_cook_website`. In der Datei `db/structure.sql` stehen alle SQL-Befehle, mit denen die Datenbank und ihre Tabellen erstellt werden.

Aktuell gibt es folgende Tabellen:

### `user`

Hier werden die Benutzer gespeichert. Ein Benutzer besitzt eine automatisch erstellte ID, einen eindeutigen Benutzernamen, eine E-Mail-Adresse und einen Passwort-Hash. Das ursprüngliche Passwort wird nicht im Klartext gespeichert. Das SQLAlchemy-Model kennzeichnet auch die E-Mail-Adresse als eindeutig; in `structure.sql` fehlt dieser `UNIQUE`-Constraint momentan jedoch noch.

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

In dieser Datei befinden sich die Einstellungen für die Datenbank. Dazu gehören Host, Port, Datenbankname, Benutzername und Passwort. Nicht geheime Einstellungen können aus einer `.env`-Datei geladen werden. Das Datenbankpasswort besitzt keinen Standardwert und muss beim Start über die Umgebungsvariable `DB_PASSWORD` bereitgestellt werden. Dadurch wird kein echtes Passwort im Quellcode oder in einer Projektdatei gespeichert.

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

Ausserdem werden die beiden `APIRouter` aus `routes/create.py` und `routes/select.py` eingebunden. Dadurch gehören die Endpunkte zum Erstellen und zum Anmelden eines Benutzers zur Hauptanwendung.

### `model.py`

Ein Model ist wie ein Bauplan zwischen Python und einer Tabelle in der Datenbank. Die Klasse `Base` ist die gemeinsame Basisklasse für alle SQLAlchemy-Models.

`Mapped[int]` oder `Mapped[str]` gibt an, welchen Python-Datentyp eine zugeordnete Datenbankspalte besitzt. `mapped_column()` beschreibt die Spalte genauer, zum Beispiel ob sie ein Primary Key ist, automatisch hochgezählt wird oder nicht leer sein darf.

Das `User`-Model bildet die Tabelle `user` ab und enthält folgende Felder:

- `user_id`: automatisch hochgezählter Primary Key
- `user_name`: eindeutiger Benutzername
- `user_email`: eindeutige E-Mail-Adresse
- `user_password`: gespeicherter Passwort-Hash

Benutzername, E-Mail-Adresse und Passwort-Hash dürfen in der Datenbank nicht leer sein.

### `schema.py`

Schemas werden mit Pydantic erstellt. Sie bestimmen, welche Daten die API erwartet und welche Daten sie zurückgibt.

Aktuell gibt es:

- `UserBase` für die gemeinsamen Felder Benutzername und E-Mail-Adresse.
- `UserCreate` für das Erstellen eines Benutzers. Das Passwort muss zwischen 8 und 255 Zeichen lang sein.
- `UserResponse` für die API-Antwort mit Benutzer-ID, Benutzername und E-Mail-Adresse. Das Passwort wird nicht zurückgegeben.
- `UserLoginEmail` für eine Anmeldung mit E-Mail-Adresse und Passwort.
- `UserLoginName` für eine später mögliche Anmeldung mit Benutzername und Passwort. Ein eigener Endpunkt dafür ist noch nicht umgesetzt.
- `IngredientCreate` für das Erstellen einer Zutat.
- `IngredientResponse` für die Antwort der API mit `ingredient_id` und `ing_name`.

Mit `Field` werden Mindest- und Maximallängen geprüft. `ConfigDict(from_attributes=True)` ermöglicht es, die SQLAlchemy-Objekte in API-Antworten umzuwandeln.

### `routes/create.py`

In dieser Datei befindet sich der Endpunkt zum Erstellen eines Benutzers:

```text
POST /api/create-user
```

Der Endpunkt erwartet einen JSON-Body mit Benutzername, E-Mail-Adresse und Passwort:

```json
{
  "user_name": "beispielname",
  "user_email": "beispiel@example.com",
  "user_password": "sicheres-passwort"
}
```

Das Passwort wird mit PBKDF2-SHA256, 600.000 Iterationen und einem zufälligen Salt gehasht. Danach wird der neue Benutzer über eine SQLAlchemy-Session in der Datenbank gespeichert. Bei Erfolg antwortet die API mit dem HTTP-Status `201 Created`:

```json
{
  "user_name": "beispielname",
  "user_email": "beispiel@example.com",
  "user_id": 1
}
```

Wenn der Benutzername oder die E-Mail-Adresse bereits vergeben ist, wird die Transaktion zurückgesetzt und die API antwortet mit `409 Conflict`. Die Route wird über einen `APIRouter` in `main.py` eingebunden.

### `routes/select.py`

Diese Datei enthält die Prüfung der Anmeldedaten über folgenden Endpunkt:

```text
POST /api/login-user-email
```

Der Endpunkt erwartet die E-Mail-Adresse und das Passwort im JSON-Body:

```json
{
  "user_email": "beispiel@example.com",
  "user_password": "sicheres-passwort"
}
```

Zuerst wird der Benutzer anhand seiner E-Mail-Adresse aus der Datenbank gelesen. Die Funktion `verify_password()` zerlegt danach den gespeicherten Wert in Algorithmus, Anzahl der Iterationen, Salt und Hash. Aus dem eingegebenen Passwort wird mit denselben Einstellungen erneut ein PBKDF2-SHA256-Hash berechnet. `secrets.compare_digest()` vergleicht den berechneten und den gespeicherten Hash.

Bei falschen Zugangsdaten wird die Anmeldung abgelehnt, ohne in der Meldung zu verraten, ob die E-Mail-Adresse oder das Passwort falsch war. Bei korrekten Daten gibt der Endpunkt momentan eine Erfolgsmeldung und die `user_id` zurück:

```json
{
  "message": "Login successful",
  "user_id": 1
}
```

Diese Antwort bestätigt bisher nur, dass die Zugangsdaten stimmen. Sie hält den Benutzer noch nicht sicher eingeloggt. Dafür muss später eine serverseitige Session oder ein signiertes Token erstellt und bei geschützten Endpunkten geprüft werden.

### Vergessenes Benutzerpasswort zurücksetzen

Ein vergessenes Passwort kann nicht aus dem gespeicherten Hash zurückgewonnen werden. Stattdessen muss mit denselben Einstellungen wie bei der Registrierung ein neuer PBKDF2-SHA256-Hash erzeugt werden. In MariaDB darf anschliessend nur dieser neue Hash gespeichert werden:

```sql
UPDATE user
SET user_password = '<NEUER_PBKDF2_HASH>'
WHERE user_id = <USER_ID>;
```

Vor dem Update muss die richtige `user_id` geprüft werden. Danach zeigt `SELECT ROW_COUNT();`, wie viele Datensätze geändert wurden; erwartet wird genau ein Datensatz. Ein Klartext-Passwort oder ein mit MariaDB `SHA2()` erzeugter Wert darf nicht eingetragen werden, weil dies unsicher beziehungsweise nicht mit `verify_password()` kompatibel wäre. Echte Passwörter und Hashwerte gehören nicht in die Dokumentation oder andere Projektdateien.

### `start_backend.sh`

Das Startskript fragt das MariaDB-Passwort mit verdeckter Eingabe im Terminal ab, exportiert es nur für den gestarteten Prozess als `DB_PASSWORD` und startet anschliessend Uvicorn im Entwicklungsmodus:

```text
./start_backend.sh
```

Das Passwort wird dadurch nicht in `.env`, `.env.example` oder einer anderen Projektdatei gespeichert. In `.env.example` stehen nur die nicht geheimen Datenbankeinstellungen und ein Hinweis auf die Abfrage beim Start.

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

Bei der Benutzerregistrierung habe ich ausserdem gelernt, dass Passwörter nicht im Klartext gespeichert werden dürfen. Ein zufälliger Salt sorgt dafür, dass gleiche Passwörter unterschiedliche Hashes erhalten. Durch das Zurücksetzen einer Datenbanktransaktion mit `rollback()` kann die Anwendung nach einem Fehler weiterarbeiten.

Beim Login habe ich gelernt, dass ein Passwort-Hash nicht entschlüsselt wird. Stattdessen wird das eingegebene Passwort mit dem gespeicherten Salt und derselben Iterationszahl erneut gehasht. Erst ein sicherer Vergleich der beiden Hashes entscheidet, ob die Zugangsdaten stimmen. Eine zurückgegebene Benutzer-ID allein ersetzt noch keine Session und kein signiertes Token.

## 9. Aktueller Stand und nächste Schritte

Die Grundidee, die Ordnerstruktur und die Datenbankplanung sind vorhanden. Die Verbindung zwischen FastAPI und MySQL kann mit dem Health-Endpunkt geprüft werden. Das `User`-Model, die dazugehörigen Schemas und der Endpunkt zur Benutzerregistrierung sind umgesetzt. Der neue Login-Endpunkt kann E-Mail-Adresse und Passwort anhand des gespeicherten Hashs prüfen. Das Datenbankpasswort wird beim Backend-Start verdeckt abgefragt und Benutzerpasswörter werden nur als gesalzene Hashes gespeichert.

Als Nächstes müssen noch folgende Punkte gemacht werden:

1. Weitere Models für Rezepte, Zutaten, Kategorien und die anderen Tabellen erstellen.
2. Die benötigten Pydantic-Schemas für diese Bereiche ergänzen.
3. Benutzerregistrierung und Login mit gültigen, ungültigen und doppelten Eingaben testen.
4. Den fehlenden `UNIQUE`-Constraint für `user_email` in der SQL-Struktur ergänzen.
5. Eine sichere Session oder ein signiertes Token für dauerhaft angemeldete Benutzer ergänzen.
6. Routen für das Erstellen, Anzeigen, Bearbeiten und Löschen von Rezepten bauen.
7. Den Endpunkt `/api/recipes` umsetzen.
8. Eine HTML-Oberfläche erstellen und mit `app.js` verbinden.
9. Eingaben und Fehlermeldungen testen.
10. Später die intelligente Rezeptsuche nach vorhandenen Zutaten umsetzen.

## 10. Fazit

Das Projekt befindet sich noch am Anfang, aber die wichtigste Planung ist bereits gemacht. Vor allem die Datenbank hat schon eine gute Grundlage. Das Backend kann die Datenbankverbindung testen, neue Benutzer mit gehashten Passwörtern speichern und deren Zugangsdaten beim Login prüfen. Der nächste Schritt für die Anmeldung ist eine sichere Session- oder Token-Verwaltung. Danach müssen die restlichen Models und API-Routen umgesetzt und mit dem Frontend verbunden werden.
