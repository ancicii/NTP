# NTP

Rešavanje problema transporta paketa: ovde bi se rešavao problem transporta svih m - paketa sa početne na krajnju destinaciju (imamo nekih p - gradova) ukoliko imamo n - vozova koji sluze za transport. Koristile bi se breadth first search, depth first search, uniform cost search i A* search, svaka pretraga bi bila implementirana u Go(lang).
Primer: imamo 4 paketa: P1 (Novi Sad - Beograd), P2 (Beograd - Novi Sad), P3 (Subotica - Beograd), P4 (Čačak - Novi Sad) i 2 voza: V1 i V2
rešenje bi bilo: Utovariti(P2, V2, Beograd), Utovariti (P1, V1, Novi Sad), Otputovati(V2, Beograd, Čačak), Utovariti(P4, V2, Čačak), Otputovati(V1, Novi Sad, Subotica), Utovariti(P3, V1, Subotica), Otputovati(V1, Subotica, Beograd), Istovariti(P1, V1, Beograd), Istovariti(P3, V1, Beograd), Otputovati(V2, Čačak, Novi Sad), Istovariti(P2, V2, Novi Sad), Istovariti(P4, V2, Novi Sad).
