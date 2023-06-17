# Funx

Funx és un llenguatge de programació orientat a expressions i funcions. Amb Funx podem definir funcions i acabar, opcionalment, amb una expressió. Per poder programar en aquest llenguatge, es fa servir una web que conté les entrades i les sortides.


## Llenguatge

### Estructura
En Funx, primer es defineixen totes les funcions que es vulguin i finalment, es pot incloure o no una expressió final dins un bloc de codi. La sortida de l'intèrpret és el valor d'aquesta expressió final.

### Bloc de codi
El bloc de codi està format per condicionals, whiles, expressions i assignacions.
Els condicionals són `if`, `elseif` i `else`, amb la condició sense parèntesis i el bloc de codi entre `{` `}`. Els whiles funcionen de la mateixa manera.

Les expressions són combinacions de crides a funcions (que han de tenir el nombre de paràmetres amb el qual han estat declarades), operadors aritmètics (`+`, `-`, `*`, `/`, `%`, `^`), operadors relacionals (`=`, `!=`, `<`, `>`, `<=`, `>=`) que retornen 0 per fals i 1 per cert i operadors lògics (`and`, `or`, `not`), seguint sempre la mateixa prioritat que a C (s'ha seguit la taula que es troba en https://en.cppreference.com/w/c/language/operator_precedence).

Les assignacions avaluen primer l'expressió de la dreta del `<-` per poder després guardar el resultat a la variable local de la part esquerra.

### Funcions
L'estructura de les funcions és: `nom + paràmetres + { bloc de codi }`, on el nom de la funció ha de començar per una lletra majúscula, els paràmetres es passen per còpia i es separen entre ells per espais en blanc i el bloc de codi retorna el valor de la primera expressió que troba (en cas que no n'hi hagi, no retorna res).

A més, les funcions permeten recursivitat.

Si una funció té un nom amb un cert nombre de paràmetres, no es pot definir una funció amb el mateix nom i un nombre diferent de paràmetres.

### Variables
L'àmbit de les variables és local cada cop que s'invoca una funció i totes són de tipus enter. Comencen per una lletra minúscula.

### Comentaris
Funx permet fer comentaris i es troben després del símbol `#`.

### Extensions realitzades
L'intèrpret compta amb les següents extensions:
- Permet els operadors lògics `and, or i not`
- Permet utilitzar `True` i `False` (tenint en compte que True (booleà) s'equipara amb l'1 i False s'equipara amb el 0, per tant, si escrivim True per consola, l'output mostrarà 1), per tant, queda implícit que no es poden declarar funcions que es diguin True o False.
- Permet l'ús de potències `^` (amb exponent >= 0)
- S'ha millorat una mica la part estètica de l'entrada-sortida de l'intèrpret

S'inclouen dos fitxers de testos, un pels operadors lògics (testLogic.funx) i un per les potències (testPot.funx)

## Gestió d'errors
Funx compta amb un sistema de gestió d'errors, de moment, té implementats els següents errors:
```
Function + name + has been already defined
Function + name + hasn't been defined
The number of parameters of function + name + doesn't match
The same parameter appears repeated
Negative powers are not defined
Division by zero is illegal
Variable not defined
Unknown symbol
```

## Exemple de codi
```
# Factorial calcula n!

Factorial n {
  if n < 0 {
    0
  }
  elseif n > 1 {
    n*(Factorial n-1)
  }
  else {
    1
  }
}
Factorial 10
```
`Output: 3628800`


## L'intèrpret
Per poder utilitzar l'intèrpret, veure la secció `Ús`.

La part web compta amb una consola on es pot introduir el codi Funx, una part de funcions en la qual es mostra la definició de les funcions declarades fins al moment i una part de resultats en la qual es mostren els darrers 5 inputs amb els seus resultats corresponents, ja sigui un resultat correcte o amb error.

## Instal·lació
Per poder fer servir l'intèrpret en Linux, s'han d'instal·lar els següents paquets/programes en terminal:

1. Instal·lar python3
```bash
$ sudo apt install python3
```

2. Instal·lar python runtime
```bash
$ pip3 install antlr4-python3-runtime
```

3. Instal·lar ANTLR: descarregar el fitxer jar (https://www.antlr.org/download.html) i seguir les instruccions del Getting Started (https://github.com/antlr/antlr4/blob/master/doc/getting-started.md)

4. Instal·lar flask
```bash
$ pip install flask
```

5. Instal·lar jinja2
```bash
$ pip install Jinja2
```

## Compil·lació
S'ha d'executar la següent comanda per poder compil·lar la gràmtica amb antlr:
```bash
antlr4 -Dlanguage=Python3 -no-listener -visitor funx.g4
```

## Ús
L'intèrpret s'invoca amb les comandes:
```bash
$ export FLASK_APP=funx
$ flask run
```
