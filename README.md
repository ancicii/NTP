# NTP - Rešavanje problema transporta paketa


### Zadatak: 
Rešavao bi se problem transporta svih m - paketa sa početne na krajnju destinaciju (imamo nekih p - gradova) ukoliko imamo n - vozova koji sluze za transport. Koristile bi se breadth first search, depth first search, uniform cost search i A* search, svaka pretraga bi bila implementirana u Go(lang).

### Funkcionalnosti: 
- Registracija
- Login
- Logout
- Dodavanje voza (admin)
- Slanje novog paketa sa pocetne na krajnju destinaciju (admin)
- Slanje novog paketa sa svoje na odredjenu destinaciju (korisnik)
- Slanje novog paketa drugom korisniku (korisnik)
- Pregled poslatih paketa (korisnik)
- Pregled paketa koje treba da primi (korisnik)
- Pregled paketa koji nisu poslati, izbor paketa i izbor pretrage za slanje (admin)
- Pregled izracunatih ruta (admin)
  
  
### Primer: 
imamo 4 paketa: P1 (Novi Sad - Beograd), P2 (Beograd - Novi Sad), P3 (Subotica - Beograd), P4 (Čačak - Novi Sad) i 2 voza: V1(Novi Sad) i V2(Beograd)
rešenje bi bilo: Utovariti(P2, V2, Beograd), Utovariti (P1, V1, Novi Sad), Otputovati(V2, Beograd, Čačak), Utovariti(P4, V2, Čačak), Otputovati(V1, Novi Sad, Subotica), Utovariti(P3, V1, Subotica), Otputovati(V1, Subotica, Beograd), Istovariti(P1, V1, Beograd), Istovariti(P3, V1, Beograd), Otputovati(V2, Čačak, Novi Sad), Istovariti(P2, V2, Novi Sad), Istovariti(P4, V2, Novi Sad).
