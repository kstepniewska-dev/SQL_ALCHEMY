# Rozwiązanie - Kompletny kod app.py

**UWAGA: Nie patrz na to rozwiązanie zanim nie spróbujesz sam rozwiązać zadania!**

```python
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'twoj-tajny-klucz-zmien-mnie'

# Konfiguracja bazy danych SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wyjazd_narciarski.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicjalizacja SQLAlchemy
db = SQLAlchemy(app)


# Model formularza rejestracji
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


@app.route('/')
def index():
    """Strona główna - lista wszystkich formularzy"""
    forms = Form.query.all()
    return render_template('index.html', forms=forms)


@app.route('/formularz/<int:form_id>')
def formularz_detail(form_id):
    """Strona szczegółów pojedynczego formularza"""
    form = Form.query.get_or_404(form_id)
    return render_template('detail.html', form=form)


@app.route('/nowy', methods=['GET', 'POST'])
def nowy_formularz():
    """Tworzenie nowego formularza rejestracji"""
    if request.method == 'POST':
        # Pobierz dane z formularza
        imie = request.form.get('imie')
        nazwisko = request.form.get('nazwisko')
        email = request.form.get('email')
        telefon = request.form.get('telefon')
        poziom_narciarski = request.form.get('poziom_narciarski')
        uwagi = request.form.get('uwagi')

        # Stwórz nowy obiekt Form
        nowy_form = Form(
            imie=imie,
            nazwisko=nazwisko,
            email=email,
            telefon=telefon,
            poziom_narciarski=poziom_narciarski,
            uwagi=uwagi
        )

        # Dodaj do bazy danych i zapisz
        db.session.add(nowy_form)
        db.session.commit()

        flash('Formularz został pomyślnie utworzony!', 'success')
        return redirect(url_for('index'))

    return render_template('nowy.html')


@app.route('/usun/<int:form_id>', methods=['POST'])
def usun_formularz(form_id):
    """Usuwanie formularza"""
    form = Form.query.get_or_404(form_id)
    db.session.delete(form)
    db.session.commit()

    flash('Formularz został usunięty!', 'success')
    return redirect(url_for('index'))


if __name__ == '__main__':
    # Utwórz tabele w bazie danych przy pierwszym uruchomieniu
    with app.app_context():
        db.create_all()

    app.run(debug=True)
```

## Dodatkowe funkcje (bonusowe)

### Edycja formularza

```python
@app.route('/edytuj/<int:form_id>', methods=['GET', 'POST'])
def edytuj_formularz(form_id):
    """Edycja istniejącego formularza"""
    form = Form.query.get_or_404(form_id)

    if request.method == 'POST':
        form.imie = request.form.get('imie')
        form.nazwisko = request.form.get('nazwisko')
        form.email = request.form.get('email')
        form.telefon = request.form.get('telefon')
        form.poziom_narciarski = request.form.get('poziom_narciarski')
        form.uwagi = request.form.get('uwagi')

        db.session.commit()
        flash('Formularz został zaktualizowany!', 'success')
        return redirect(url_for('formularz_detail', form_id=form.id))

    return render_template('edytuj.html', form=form)
```

### Wyszukiwanie

```python
@app.route('/szukaj')
def szukaj():
    """Wyszukiwanie formularzy"""
    query = request.args.get('q', '')

    if query:
        forms = Form.query.filter(
            (Form.imie.contains(query)) |
            (Form.nazwisko.contains(query)) |
            (Form.email.contains(query))
        ).all()
    else:
        forms = Form.query.all()

    return render_template('index.html', forms=forms, search_query=query)
```
