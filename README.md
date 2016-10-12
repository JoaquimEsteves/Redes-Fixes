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
