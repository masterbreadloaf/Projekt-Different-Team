# mKelner Aplikacja Webowa README (folder Interfejs)

## Opis
Aplikacja webowa mKelner to prosty system zarządzania restauracją, zaprojektowany do obsługi danych klientów, zamówień, zarządzania menu, statystyk i historii zamówień. Projekt obejmuje wiele stron HTML stylizowanych za pomocą jednego pliku CSS, z podstawową funkcjonalnością JavaScript do zarządzania klientami, obsługi formularzy i przechowywania danych za pomocą localStorage.

### Funkcjonalności
- **Logowanie i Rejestracja**: Bezpieczne strony logowania i rejestracji dla użytkowników.
- **Zarządzanie Klientami**: Wyświetlanie, dodawanie, edytowanie i usuwanie informacji o klientach (np. numer stolika, zdjęcie, imię i nazwisko, płeć, wiek, alergeny, status).
- **Zarządzanie Zamówieniami**: Składanie i zarządzanie zamówieniami z danymi klienta.
- **Zarządzanie Menu**: Przeglądanie i kategoryzowanie pozycji menu.
- **Statystyki**: Wyświetlanie podstawowych statystyk z wykresami.
- **Historia Zamówień**: Wyświetlanie przeszłych zamówień z opcjami filtrowania.
- **Responsywny Design**: Adaptacja do różnych rozmiarów ekranów.

### Pliki
- `css.css`: Centralny arkusz stylów dla wszystkich stron.
- `login.html`: Strona logowania.
- `register.html`: Strona rejestracji.
- `clients.html`: Lista klientów z opcjami dodawania, edytowania i usuwania.
- `add_clients.html`: Strona dodawania nowych klientów.
- `edit_clients.html`: Strona edytowania danych istniejących klientów.
- `order.html`: Strona zarządzania zamówieniami.
- `history.html`: Strona historii zamówień z opcjami filtrowania.
- `stats.html`: Strona statystyk z wykresami.
- `menu.html`: Strona przeglądania menu.

## Instalacja i Konfiguracja

### Wymagania
- Nowoczesna przeglądarka internetowa (np. Chrome, Firefox, Edge).
- Nie jest wymagana dodatkowa konfiguracja serwera dla tej statycznej wersji; działa lokalnie przy użyciu localStorage.

### Kroki do Pobrania i Uruchomienia
1. **Pobierz Repozytorium**:
   - Odwiedź stronę repozytorium GitHub tego projektu.
   - Kliknij zielony przycisk "Code" i wybierz:
     - Skopiuj URL i uruchom `git clone <adres-repozytorium>` w terminalu, jeśli masz zainstalowanego Gita.
     - Kliknij "Download ZIP", aby pobrać cały projekt jako plik ZIP.
   - Rozpakuj plik ZIP, jeśli został pobrany, lub przejdź do katalogu po klonowaniu.

2. **Otwórz Projekt**:
   - Upewnij się, że wszystkie pliki (`css.css`, `login.html`, `register.html` itp.) znajdują się w tym samym katalogu.
   - Otwórz `login.html` w przeglądarce, klikając dwukrotnie plik lub przeciągając go do przeglądarki.

3. **Użycie**:
   - Zaloguj się przy użyciu domyślnych danych: `email: admin@mkelner.com`, `hasło: admin`.
   - Przeglądaj sekcje za pomocą paska bocznego (np. Klienci, Zamówienia, Menu).
   - Użyj przycisku "Dodaj klienta" na `clients.html`, aby dodać nowych klientów, lub kliknij "Edytuj", aby edytować istniejących.
   - Dane klientów są zapisywane lokalnie i utrzymują się po odświeżeniu strony.

### Uwagi
- Jest to statyczna aplikacja HTML/CSS/JavaScript. W środowisku produkcyjnym należy skonfigurować serwer backendowy (np. Flask, Node.js) i bazę danych do obsługi przechowywania danych i bezpieczeństwa.
- Aplikacja używa `localStorage` do celów demonstracyjnych. Dane zostaną utracone po wyczyszczeniu pamięci podręcznej przeglądarki.
- Dostosuj ścieżki plików lub dodaj serwer, jeśli planujesz wdrożenie na hostingu.

## Dokumentacja Użycia
- **Logowanie**: Wprowadź email i hasło na `login.html`, aby uzyskać dostęp do systemu.
- **Rejestracja**: Użyj `register.html`, aby utworzyć nowe konto (obecnie symulowane z podstawową walidacją).
- **Klienci**: Na `clients.html` wyszukuj klientów, dodawaj nowych przez `add_clients.html` lub edytuj/usuwaj przez `edit_clients.html`.
- **Zamówienia**: Zarządzaj zamówieniami na `order.html` z wyborem klienta.
- **Menu**: Przeglądaj kategorie i pozycje na `menu.html`.
- **Statystyki**: Oglądaj analizy na `stats.html`.
- **Historia**: Filtrowanie i przeglądanie przeszłych zamówień na `history.html`.
---

### Ostatnia Aktualizacja
22:48 CEST, Czwartek, 22 Maja 2025
