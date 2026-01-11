# Migracje Bazy Danych z Flask-Migrate

Flask-Migrate jest już skonfigurowany dla tego projektu! Oto jak go używać:

## Wymagania wstępne

Zawsze używaj środowiska wirtualnego z głównego folderu:
```bash
# Ustaw aplikację Flask
export FLASK_APP=index.py
```

Lub poprzedź komendy prefiksem `FLASK_APP=index.py`

## Popularne Komendy Migracji

### 1. Utwórz nową migrację (po zmianie modeli)

Gdy zmodyfikujesz swoje modele w `models.py`, utwórz migrację:

!!! Zmień /media/server/SQL_ALCHEMY_AND_FLUSK na swoją ścieżkę do pliku !!!

```bash
FLASK_APP=index.py /media/server/SQL_ALCHEMY_AND_FLUSK/.venv/bin/flask db migrate -m "Opis zmian"
```

Przykład:
```bash
FLASK_APP=index.py /media/server/SQL_ALCHEMY_AND_FLUSK/.venv/bin/flask db migrate -m "Dodaj pole bio do modelu User"
```

### 2. Zastosuj migracje do bazy danych

```bash
FLASK_APP=index.py /media/server/SQL_ALCHEMY_AND_FLUSK/.venv/bin/flask db upgrade
```

### 3. Cofnij ostatnią migrację

```bash
FLASK_APP=index.py /media/server/SQL_ALCHEMY_AND_FLUSK/.venv/bin/flask db downgrade
```

### 4. Wyświetl historię migracji

```bash
FLASK_APP=index.py /media/server/SQL_ALCHEMY_AND_FLUSK/.venv/bin/flask db history
```

### 5. Zobacz aktualną wersję migracji

```bash
FLASK_APP=index.py /media/server/SQL_ALCHEMY_AND_FLUSK/.venv/bin/flask db current
```

## Przepływ Pracy z Migracjami

1. **Zmodyfikuj swoje modele** w `models.py`
2. **Wygeneruj migrację**: `flask db migrate -m "opis"`
3. **Przejrzyj plik migracji** w `migrations/versions/`
4. **Zastosuj migrację**: `flask db upgrade`

## Przykład: Dodawanie nowego pola

Powiedzmy, że chcesz dodać pole `bio` do modelu User:

1. Edytuj `models.py`:
```python
class User(db.Model):
    # ... istniejące pola ...
    bio = db.Column(db.Text, nullable=True)
```

2. Utwórz migrację:
```bash
FLASK_APP=index.py /media/server/SQL_ALCHEMY_AND_FLUSK/.venv/bin/flask db migrate -m "Dodaj pole bio do User"
```

3. Przejrzyj wygenerowany plik w `migrations/versions/`

4. Zastosuj migrację:
```bash
FLASK_APP=index.py /media/server/SQL_ALCHEMY_AND_FLUSK/.venv/bin/flask db upgrade
```

## Uwagi

- Pliki migracji znajdują się w `migrations/versions/`
- Każda migracja jest śledzona w bazie danych
- Nigdy nie modyfikuj zastosowanych migracji - zamiast tego twórz nowe
- Commituj pliki migracji do kontroli wersji
- Początkowa migracja została już utworzona dla twojego aktualnego schematu
