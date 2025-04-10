Tutaj będą się pojawiały elementy dotyczące bazy danych. Aktualny postęp prac: Wdrażanie CRUD w bazie MS SQL

Baza tworzona na:
-Microsoft SQL Server 2022 Express
-Windows 10 Pro x64

Baza do zaimportowania do SMSS za pomocą pliku restauracjadb_export.bacpac.

Ścieżka importu:
1) Do zainstalowania Microsoft SQL Server 2022 Express
2) Do zainstalowania Microsoft SQL Managment Studio, najlepiej 19 lub 20
3) Przy pierwszej konfiguracji pakietu komputer uruchamiamy ponownie
4) Uruchamiamy SQL Server jeśli jeszcze nie został uruchomiony (domyślnie włączone w autostarcie)
5) Wchodzimy do SMSS, aktualnie Encryption: Optional, klikamy connect
6) Po załadowaniu zawartości serwera bazę importujemy ścieżką:
	-prawy przycisk myszy na Databases
	-Import Data-tier Application
	-Next
	-Wybieramy plik bacpac z dysku, next
	-Nazwa bazy najlepiej żeby została domyślna
	-Lokalizacja bazy może być domyślna, może być customowa. Testowane na niezależnym środowisku i nie robi to różnicy
	-Finish

Po wykonaniu powyższych kroków baza zostanie zaimportowana w całości. Aby usunąć bazę rozwijamy Databases, PPM na naszą bazę i Delete.