# Tema-LC


Tema1:
Formule propoziţionale bine formate

-Propoziții atomice se consideră toate literele mari
-Se considera datele intrare fiind foarmate doar din paranteze, litere, conectori logici, spatii

Codul evalueaza recursiv secventa introdusă:
    1)dacă secvența este formată dintr-o singură literă returnează adevărat
    2)dacă secvența este formată dintr-o propozitie negata de forma (¬Q) returnează adevărat
    3)dacă secvența este formată dintr-o propozitie negata de forma (¬(X)) returnează valoarea de adevăr pentu X
    4)parcurge secvența până găsește primul conector logic pentru care numărele de paranteze închise și deschise până la momentul curect sunt egale și returneaza adevăr atunci când secventa de pană la conector si secventa de după conector sunt ambele formule propoziționale
    
În cazul în care expresia este adevarată codul va returna și reprezentarea grafică a arborelui de relații drept demonstrație
 
Compilarea programului:
  Puteți descărca fișierul cpp atașat și să îl deschideți în orice IDE disponibil care are o extensie pentru C++
  Drept date de intrare se introduce secvența care urmează să fie evaluată
