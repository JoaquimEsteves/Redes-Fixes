RC 2016
Projecto "“Tradução RC"

Para testar:

TCS -> tejo.tecnico.ulisboa.pt : 58011
TRS -> 193.136.138.142 : 59100

if ctrl-c or exit plz remove from TCS server my friend!

signals:

SIGINT
SIGPIPE
SIGALARM

Nº 75966 - Frederico Moura

Nº 77020 - Joaquim Esteves

Nº 75455 - André Silva

Visto que o projecto está em Python, não é convencional criar uma makefile, então, de forma a correr o user.py, tsc.py e trs.py apenas tem de ser executado o seguinte comando para cada ficheiro:

```shell
$ python <nome_do_ficheiro>.py [commandos]
```

ou seja, testando cada ficheiro em separadores do terminal diferentes usariamos ou em maquinas diferentes:

[Terminal1] $ python user.py [-n TCSname] [-p TCSport]

[Terminal2] $ python tcs.py [-p TCSport]

[Terminal3] $ python trs.py language [-p TRSport] [-n TCSname] [-e TCSport]


## Possible words to be translated from Portuguese

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
