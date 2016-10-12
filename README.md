# RC 2016 Projecto "“Tradução RC"

Nº 75455 - André Silva

Nº 75966 - Frederico Moura

Nº 77020 - Joaquim Esteves

Visto que o projecto está em Python, não é convencional criar uma makefile, então, de forma a correr o **user.py**, **tsc.py** e **trs.py** apenas tem de ser executado o seguinte comando para cada ficheiro:

```shell
$ python <nome_do_ficheiro>.py [commandos]
```

ou seja, testando cada ficheiro em separadores do terminal diferentes usariamos ou em maquinas diferentes:

```shell
// Separador #1
$ python user.py [-n TCSname] [-p TCSport]

// Separador #2
$ python tcs.py [-p TCSport]

// Separador #3
$ python trs.py language [-p TRSport] [-n TCSname] [-e TCSport]
```

## Available Languages
Nesta versão do projecto disponibilizamos a prossibilidade de existir 5 TRS a correr em paralelo, cada um a servir traduções para apenas uma lingua. Notar que todas as traduções são de **Português** para *target_language*.

#### Lista de Linguas
- Alemão
- Inglês
- Françês
- Italiano
- Espanhol

Portanto, apenas substituindo a lingua quando se corre o TRS server irá disponibilizar todas as traduções para a mesma lingua

```shell
// Exemplo
$ python trs.py Inglês -p 59001
```

### Lista de Possiveis Palavras

Para cada par de lingua acima referido (*Português* para *Lista de Linguas*), existe a tradução para as respectivas palavras:

```text
navegador
domínio
endereço de e-mail
extensão
funcionalidade
seguir
seguidor
centro de ajuda
olá
ocultar
caixa de entrada
idioma
iniciar sessão
terminar sessão
terminar sessão
início de sessão
fim de sessão
encerrar
histórias
história
tópico
tópicos
guardar
```
