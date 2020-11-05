# NTP - Rešavanje problema transporta paketa


### Zadatak: 
Rešavao bi se problem transporta svih m - paketa sa početne na krajnju destinaciju (imamo nekih p - gradova) ukoliko imamo n - vozova koji sluze za transport. Koristile bi se breadth first search, depth first search, uniform cost search i A* search, svaka pretraga bi bila implementirana u Go(lang).

### Funkcionalnosti: 
- ##### Registracija
![register](https://user-images.githubusercontent.com/41138106/98263223-dab05500-1f86-11eb-8755-151269e6e955.JPG)

- ##### Login
![login](https://user-images.githubusercontent.com/41138106/98262973-84431680-1f86-11eb-80c0-8a80ec7797f1.JPG)

- ##### Logout

- ##### Dodavanje voza (admin)
![addTrain](https://user-images.githubusercontent.com/41138106/98263339-fca9d780-1f86-11eb-8643-0924305d14ff.JPG)

- ##### Slanje novog paketa sa pocetne na krajnju destinaciju (admin)
![addAdmin](https://user-images.githubusercontent.com/41138106/98263388-0cc1b700-1f87-11eb-913e-d3880e7e6255.JPG)

- ##### Slanje novog paketa sa svoje na odredjenu destinaciju (korisnik)
![addKorisnik](https://user-images.githubusercontent.com/41138106/98263414-1814e280-1f87-11eb-883a-2041ba65f7d7.JPG)

- ##### Slanje novog paketa drugom korisniku (korisnik)
![addKorisnikKorisnik](https://user-images.githubusercontent.com/41138106/98263441-206d1d80-1f87-11eb-9517-92e98641e462.JPG)
![addKorisnikKorisnik2](https://user-images.githubusercontent.com/41138106/98263444-22cf7780-1f87-11eb-882f-b0099f72c33e.JPG)

- ##### Pregled poslatih paketa (korisnik)
![sentKorisnik](https://user-images.githubusercontent.com/41138106/98263666-61653200-1f87-11eb-9fbf-235b2509bd78.JPG)

- ##### Pregled paketa koje treba da primi (korisnik)
![received](https://user-images.githubusercontent.com/41138106/98263709-6a560380-1f87-11eb-9ae0-f93b0f99f2fc.JPG)

- ##### Pregled paketa koji nisu poslati, izbor paketa i izbor pretrage za slanje (admin)
![sendP](https://user-images.githubusercontent.com/41138106/98263740-72ae3e80-1f87-11eb-82f8-eaafb0065fc5.JPG)

- ##### Pregled izracunatih ruta (admin)
![rezultattt](https://user-images.githubusercontent.com/41138106/98263813-86f23b80-1f87-11eb-998a-37abf957ef54.JPG)

- ##### Prihvatanje i odbjanje poslatih posiljki (admin)
![approve](https://user-images.githubusercontent.com/41138106/98263872-95d8ee00-1f87-11eb-9ad9-dc3d4641c198.JPG)
  
  
### Primer: 
imamo 4 paketa: P1 (Novi Sad - Beograd), P2 (Beograd - Novi Sad), P3 (Subotica - Beograd), P4 (Čačak - Novi Sad) i 2 voza: V1(Novi Sad) i V2(Beograd)
rešenje bi bilo: Utovariti(P2, V2, Beograd), Utovariti (P1, V1, Novi Sad), Otputovati(V2, Beograd, Čačak), Utovariti(P4, V2, Čačak), Otputovati(V1, Novi Sad, Subotica), Utovariti(P3, V1, Subotica), Otputovati(V1, Subotica, Beograd), Istovariti(P1, V1, Beograd), Istovariti(P3, V1, Beograd), Otputovati(V2, Čačak, Novi Sad), Istovariti(P2, V2, Novi Sad), Istovariti(P4, V2, Novi Sad).
