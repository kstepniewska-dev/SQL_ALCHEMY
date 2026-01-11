# Ćwiczenie: Flask + SQLAlchemy - Formularz Rejestracji na Wyjazd Narciarski

## Cel ćwiczenia

Nauczysz się jak:
- Połączyć aplikację Flask z bazą danych SQLite przy użyciu SQLAlchemy
- Tworzyć modele danych
- Wykonywać operacje CRUD (Create, Read, Update, Delete)
- Obsługiwać formularze HTML

## Zadanie

Dokończ aplikację Flask do zarządzania rejestracją uczestników wyjazdu narciarskiego.

### Co już jest zrobione:

✅ Struktura routów Flask
✅ Szablony HTML z Bootstrap
✅ Podstawowe przekierowania i flash messages

### Co musisz zrobić:

## Krok 1: Połączenie z bazą danych (app.py)

Odkomentuj i uzupełnij kod w pliku `app.py`:

```python
# Dodaj import na początku pliku
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Skonfiguruj połączenie z SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wyjazd_narciarski.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Zainicjalizuj SQLAlchemy
db = SQLAlchemy(app)
```

## Krok 2: Stwórz model Form

Utwórz model reprezentujący formularz rejestracji:

```python
class Form(db.Model):
    __tablename__ = 'forms'

    id = db.Column(db.Integer, primary_key=True)
    imie = db.Column(db.String(100), nullable=False)
    nazwisko = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    telefon = db.Column(db.String(20), nullable=False)
    poziom_narciarski = db.Column(db.String(50))
    uwagi = db.Column(db.Text)
    data_rejestracji = db.Column(db.DateTime, default=datetime.utcnow)
```

## Krok 3: Zaimplementuj operacje CRUD

### 3.1 READ - Lista wszystkich formularzy (route '/')

```python
@app.route('/')
def index():
    forms = Form.query.all()
    return render_template('index.html', forms=forms)
```

### 3.2 READ - Szczegóły pojedynczego formularza (route '/formularz/<id>')

```python
@app.route('/formularz/<int:form_id>')
def formularz_detail(form_id):
    form = Form.query.get_or_404(form_id)
    return render_template('detail.html', form=form)
```

### 3.3 CREATE - Tworzenie nowego formularza (route '/nowy')

```python
@app.route('/nowy', methods=['GET', 'POST'])
def nowy_formularz():
    if request.method == 'POST':
        # Pobierz dane z formularza
        imie = request.form.get('imie')
        nazwisko = request.form.get('nazwisko')
        email = request.form.get('email')
        telefon = request.form.get('telefon')
        poziom_narciarski = request.form.get('poziom_narciarski')
        uwagi = request.form.get('uwagi')

        # Stwórz nowy obiekt
        nowy_form = Form(
            imie=imie,
            nazwisko=nazwisko,
            email=email,
            telefon=telefon,
            poziom_narciarski=poziom_narciarski,
            uwagi=uwagi
        )

        # Zapisz do bazy danych
        db.session.add(nowy_form)
        db.session.commit()

        flash('Formularz został pomyślnie utworzony!', 'success')
        return redirect(url_for('index'))

    return render_template('nowy.html')
```

### 3.4 DELETE - Usuwanie formularza (route '/usun/<id>')

```python
@app.route('/usun/<int:form_id>', methods=['POST'])
def usun_formularz(form_id):
    form = Form.query.get_or_404(form_id)
    db.session.delete(form)
    db.session.commit()

    flash('Formularz został usunięty!', 'success')
    return redirect(url_for('index'))
```

## Krok 4: Inicjalizacja bazy danych

Odkomentuj kod w `if __name__ == '__main__':`:

```python
if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)
```

## Jak uruchomić aplikację

1. Zainstaluj wymagane pakiety:
```bash
pip install flask flask-sqlalchemy
```

2. Uruchom aplikację:
```bash
python app.py
```

3. Otwórz przeglądarkę: `http://localhost:5000`

## Testowanie

1. Dodaj kilka zgłoszeń przez formularz
2. Sprawdź listę zgłoszeń
3. Kliknij "Szczegóły" aby zobaczyć pełne informacje
4. Usuń zgłoszenie

## Dodatkowe wyzwania (opcjonalne)

Jeśli skończysz wcześniej, spróbuj dodać:

1. **Edycję formularza** - route `/edytuj/<id>`
2. **Walidację danych** - sprawdzaj czy email jest poprawny
3. **Filtrowanie** - możliwość filtrowania po poziomie narciarskim
4. **Sortowanie** - sortowanie listy po dacie rejestracji
5. **Wyszukiwanie** - wyszukiwanie po imieniu/nazwisku

## Przydatne komendy SQLAlchemy

```python
# Pobierz wszystkie rekordy
Form.query.all()

# Pobierz jeden rekord po ID
Form.query.get(1)
Form.query.get_or_404(1)  # zwróci 404 jeśli nie znajdzie

# Filtrowanie
Form.query.filter_by(poziom_narciarski='zaawansowany').all()

# Sortowanie
Form.query.order_by(Form.data_rejestracji.desc()).all()

# Dodanie do bazy
db.session.add(obiekt)
db.session.commit()

# Usunięcie z bazy
db.session.delete(obiekt)
db.session.commit()
```

## Struktura projektu

```
cwiczenie_studenci/
├── app.py                 # Główny plik aplikacji (tutaj pracujesz)
├── templates/
│   ├── base.html         # Szablon bazowy
│   ├── index.html        # Lista formularzy
│   ├── detail.html       # Szczegóły formularza
│   └── nowy.html         # Formularz dodawania
└── README.md             # Ten plik
```

## Pomoc

Jeśli masz problem, sprawdź:
- Czy wszystkie importy są na górze pliku
- Czy odkomentowałeś wszystkie potrzebne linie
- Czy tabele zostały utworzone (sprawdź czy pojawił się plik `wyjazd_narciarski.db`)
- Komunikaty błędów w terminalu

Powodzenia! 🎿
