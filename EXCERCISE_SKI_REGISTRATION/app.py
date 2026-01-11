from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'twoj-tajny-klucz-zmien-mnie'

# TODO: Skonfiguruj połączenie z bazą danych SQLite


# TODO: Zainicjalizuj SQLAlchemy


# TODO: Stwórz model Form (formularz rejestracji na wyjazd narciarski)


@app.route('/')
def index():
    """Strona główna - lista wszystkich formularzy"""
    # TODO: Pobierz wszystkie formularze z bazy danych

    # Tymczasowo - pusta lista
    forms = []

    return render_template('index.html', forms=forms)


@app.route('/formularz/<int:form_id>')
def formularz_detail(form_id):
    """Strona szczegółów pojedynczego formularza"""
    # TODO: Pobierz formularz o podanym ID

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

        # TODO: Stwórz nowy obiekt Form

        # TODO: Dodaj do bazy danych i zapisz

        flash('Formularz został pomyślnie utworzony!', 'success')
        return redirect(url_for('index'))

    return render_template('nowy.html')


@app.route('/usun/<int:form_id>', methods=['POST'])
def usun_formularz(form_id):
    """Usuwanie formularza"""
    # TODO: Znajdź formularz i usuń go

    flash('Formularz został usunięty!', 'success')
    return redirect(url_for('index'))


if __name__ == '__main__':
    # TODO: Utwórz tabele w bazie danych przy pierwszym uruchomieniu

    app.run(debug=True)
