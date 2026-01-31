# PRD – Aplikacja webowa „Dzisiejsze Smaki Lodów”

## 1. Cel produktu

Celem aplikacji jest prezentowanie **aktualnie dostępnych smaków lodów** w lodziarni w formie atrakcyjnej, mobilnej strony promocyjnej, która:
- zachęca klientów do fizycznej wizyty w lodziarni,
- pozwala właścicielowi szybko (1–2 min dziennie) aktualizować ofertę,
- bazuje na zdjęciach i prostym przekazie (bez stanów magazynowych).

Aplikacja nie służy do sprzedaży online ani do zarządzania magazynem.

---

## 2. Grupy użytkowników

### 2.1 Klient końcowy (frontend – publiczny)
- osoba szukająca informacji „jakie smaki są dziś dostępne”
- użytkownik mobilny (smartfon)

### 2.2 Właściciel / obsługa lodziarni (backend – panel admina)
- codziennie aktualizuje listę smaków
- czasami dodaje nowe smaki i zdjęcia
- często korzysta z telefonu

---

## 3. Zakres funkcjonalny – frontend (strona publiczna)

### 3.1 Sekcja „Dzisiejsze smaki”

Lista smaków w formie kart:
- zdjęcie smaku (kluczowe)
- nazwa smaku
- opcjonalny krótki opis
- tagi/ikonki:
  - wegański
  - bez laktozy
  - nowość
  - hit dnia

Układ:
- grid 2–3 kolumny
- mobile-first

---

### 3.2 Informacja o zmienności oferty

Stała informacja widoczna dla klienta:

> ⚠️ Smaki mogą się różnić w ciągu dnia – zapytaj obsługę o aktualną dostępność

Dodatkowo:
- „Ostatnia aktualizacja: [data + godzina]”

---

### 3.3 Sekcja promocyjna

Krótki content sprzedażowy:
- rzemieślnicza produkcja
- świeże składniki
- sezonowość smaków

---

### 3.4 Lokalizacja i CTA

- mapa Google
- godziny otwarcia
- CTA: „Wpadnij zanim znikną”

---

## 4. Zakres funkcjonalny – backend (panel admina)

### 4.1 Baza smaków

Centralna baza wszystkich smaków, tworzona i rozwijana w czasie.

Dane smaku:
- nazwa
- slug (automatyczny)
- opis (opcjonalny)
- typ: mleczny / sorbet
- tagi:
  - wegański
  - bez laktozy
  - nowość
  - hit
- sezonowy (bool)
- zdjęcie
- status: aktywny / zarchiwizowany
- data utworzenia

Smak dodany do bazy **nie jest automatycznie widoczny dla klientów**.

---

### 4.2 Dodawanie nowego smaku

Formularz „Dodaj nowy smak”:

Pola obowiązkowe:
- nazwa smaku
- zdjęcie

Pola opcjonalne:
- opis
- typ
- tagi
- sezonowy

Zachowanie systemu:
- walidacja obecności zdjęcia
- automatyczna kompresja i przycięcie obrazu
- zapis jako smak nieaktywny (tylko w bazie)

---

### 4.3 Edycja i archiwizacja smaków

Możliwości:
- edycja danych smaku
- zmiana zdjęcia
- archiwizacja (zamiast usuwania)
- ponowne przywrócenie w przyszłości

---

### 4.4 Zarządzanie „Dzisiejszymi smakami”

Oddzielny widok operacyjny:
- lista smaków z bazy
- wybór smaków dostępnych dziś
- zmiana kolejności (drag & drop)
- oznaczenie „hit dnia”

Szybkie akcje:
- skopiuj wczorajsze smaki
- ukryj smak (sprzedany w ciągu dnia)
- wyczyść listę

---

## 5. Model danych (logiczny)

### 5.1 Smak
- id
- nazwa
- slug
- opis
- typ
- tagi[]
- sezonowy
- zdjęcie_url
- aktywny
- data_utworzenia

### 5.2 Dzisiejsze smaki
- data
- smak_id
- kolejność
- hit_dnia

---

## 6. Workflow użytkownika (realny scenariusz)

### Rano:
- otwarcie panelu
- zaznaczenie dzisiejszych smaków
- zapis

### W ciągu dnia:
- ukrycie sprzedanego smaku
- dodanie nowego smaku + zdjęcia
- natychmiastowe opublikowanie

Czas obsługi: 30–60 sekund

---

## 7. Wymagania niefunkcjonalne

- pełna responsywność
- bardzo szybkie ładowanie (zdjęcia!)
- backend dostosowany do obsługi mobilnej
- SEO (indeksowalna strona)

---

## 8. Elementy opcjonalne (po MVP)

- QR kod do strony
- historia smaków z poprzednich dni
- elementy social proof
- przygotowanie pod SaaS (wiele lodziarni)

---

## 9. Zakres MVP

W MVP MUSI się znaleźć:
- frontend z listą dzisiejszych smaków
- backend: CRUD smaków + upload zdjęć
- zarządzanie „dzisiejszymi smakami”
- informacja o zmienności oferty

Poza MVP:
- stany magazynowe
- sprzedaż online
- integracje POS

