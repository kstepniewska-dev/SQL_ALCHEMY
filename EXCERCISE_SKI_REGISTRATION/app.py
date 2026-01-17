from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'twoj-tajny-klucz-zmien-mnie'

# TODO: Skonfiguruj połączenie z bazą danych SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ski_registration.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# TODO: Zainicjalizuj SQLAlchemy
db = SQLAlchemy(app)

# TODO: Stwórz model Form (formularz rejestracji na wyjazd narciarski)
class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    imie = db.Column(db.String(100), nullable=False)
    nazwisko = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    telefon = db.Column(db.String(20), nullable=False)
    poziom_narciarski = db.Column(db.String(50), nullable=False)
    uwagi = db.Column(db.Text, nullable=True)
    data_rejestracji = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/')
def index():
    """Strona główna - lista wszystkich formularzy"""
    # TODO: Pobierz wszystkie formularze z bazy danych
    forms = Form.query.all()
    return render_template('index.html', forms=forms)


@app.route('/formularz/<int:form_id>')
def formularz_detail(form_id):
    """Strona szczegółów pojedynczego formularza"""
    # TODO: Pobierz formularz o podanym ID
    form = Form.query.get_or_404(form_id)
    
    # Tymczasowo - przykładowy obiekt
    form = {
        'id': form_id,
        'imie': 'Jan',
        'nazwisko': 'Kowalski',
        'email': 'jan@example.com',
        'telefon': '123456789',
        'poziom_narciarski': 'średniozaawansowany',
        'uwagi': 'Brak',
        'data_rejestracji': '2024-01-11'
    }

    return render_template('detail.html', form=form)


@app.route('/nowy', methods=['GET', 'POST'])
def nowy_formularz():
    """Tworzenie nowego formularza rejestracji"""
    if request.method == 'POST':
        # TODO: Pobierz dane z formularza
        imie = request.form['imie']
        nazwisko = request.form['nazwisko'] 
        email = request.form['email']
        telefon = request.form['telefon']
        poziom_narciarski = request.form['poziom_narciarski']
        # TODO: Stwórz nowy obiekt Form
        new_form = Form(
            imie=imie,
            nazwisko=nazwisko,
            email=email,
            telefon=telefon,
            poziom_narciarski=poziom_narciarski
        )
        # TODO: Dodaj do bazy danych i zapisz
        db.session.add(new_form)
        db.session.commit()

        flash('Formularz został pomyślnie utworzony!', 'success')
        return redirect(url_for('index'))

    return render_template('nowy.html')


@app.route('/usun/<int:form_id>', methods=['POST'])
def usun_formularz(form_id):
    """Usuwanie formularza"""
    # TODO: Znajdź formularz i usuń go
    form = Form.query.get_or_404(form_id)
    db.session.delete(form)
    db.session.commit() 
    flash('Formularz został usunięty!', 'success')
    return redirect(url_for('index'))


if __name__ == '__main__':
    # TODO: Utwórz tabele w bazie danych przy pierwszym uruchomieniu
    with app.app_context():
        db.create_all()
    app.run(debug=True)
