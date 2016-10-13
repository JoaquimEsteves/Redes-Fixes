# RC 2016 Projecto "“Tradução RC"

Nº 75455 - André Silva

Nº 75966 - Frederico Moura

Nº 77020 - Joaquim Esteves

Visto que o projecto está na linguagem **Python**, não é convencional criar uma makefile, então, de forma a correr o **user**, **tcs** e **trs** apenas tem de ser executado o seguinte comando para cada ficheiro:

```shell
$ python <nome_do_ficheiro>.py [commandos]
```

ou seja, executando cada aplicação em separadores do terminal ou em maquinas diferentes:

```shell
# Separador nº1
$ python user.py [-n TCSname] [-p TCSport]

# Separador nº2
$ python tcs.py [-p TCSport]

# Separador nº3
$ python trs.py language [-p TRSport] [-n TCSname] [-e TCSport]
```

## Linguas Disponivels
Nesta versão do projecto existem traduções que suportam **até 5 TRS** a correr em paralelo (cada um a servir traduções para apenas uma lingua). Notar que todas as traduções são de **Português** para **target_language**.

## Lista de Linguas
- Alemão
- Inglês
- Françês
- Italiano
- Espanhol

Portanto, apenas substituindo a lingua ao correr o **TRS server**, irá disponibilizar todas as traduções para a mesma lingua.

```shell
# Exemplo
$ python trs.py Inglês -p 59001
```
## Ficheiro para Tradução

Disponibilizamos apenas um ficheiro para tradução que se dá pelo nome **pyrion.png**.
Existe tradução desta imagem para cada uma das linguas anteriormente mencionadas. Para chamar a tradução da imagem apenas tem de correr o mesmo que está no exemplo abaixo. Note que cada tradução tem uma imagem diferente. Para simplificação, as traduções da imagem são apenas a mesma imagem com diferentes *hues*, *saturações* e *luminosidades* e o nome, para o qual o ficheiro recebido, é **pyrion.pngDOWNLOADED.png**.

```shell
# exemplo
$ python user.py 
[INFO]: Starting client...
[INFO]: Welcome :).
$ list
[DEBUG]: [UDP] Sending request to localhost:58001 > "ULQ".
[DEBUG]: [UDP] Got back > "ULR 2 Inglês Alemão".
Got 2 languages:
1. Inglês
2. Alemão
$ request 1 f pyrion.png
[DEBUG]: [UDP] Sending request to localhost:58001 > "UNQ Inglês".
[DEBUG]: [UDP] Got back > "UNR 127.0.0.1 59001".
[DEBUG]: [TCP] Sending request to 127.0.0.1:59001 > "TRQ f pyrion.png 35520 ?PNGIHDR?EV*sRGB.."
[DEBUG]: [TCP] Got back > "TRQ f pyrion.png 35520 ?PNGIHDR?EV*sRGB...".
[INFO]: How lovely, the TRS has sent us a file!
Got back translated file from 127.0.0.1:
pyrion.png (35520 bytes)
```


## Lista de Possiveis Palavras para Tradução

Para cada par de lingua acima referido (**Português** para **Lista de Linguas**), existe a tradução para as respectivas palavras:

```text
navegador
domínio
extensão
funcionalidade
seguir
seguidor
olá
ocultar
idioma
encerrar
histórias
história
tópico
tópicos
guardar
```


```shell
# exemplo
$ python user.py 
[INFO]: Starting client...
[INFO]: Welcome :).
$ list
[DEBUG]: [UDP] Sending request to localhost:58001 > "ULQ".
[DEBUG]: [UDP] Got back > "ULR 2 Inglês Alemão".
Got 2 languages:
1. Inglês
2. Alemão
$ request 1 t olá
[DEBUG]: [UDP] Sending request to localhost:58001 > "UNQ Inglês".
[DEBUG]: [UDP] Got back > "UNR 127.0.0.1 59001".
[DEBUG]: [TCP] Sending request to 127.0.0.1:59001 > "TRQ t 1 olá"
[DEBUG]: [TCP] Got back > "TRR t 1 hi".
Got back translated file from 127.0.0.1:
"hi"
```


