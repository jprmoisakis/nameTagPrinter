# Sistema de Impressão de Crachás

Sistema faz a impressão de crachás de acordo com as informações repassadas de uma planilha excel

### Pre-requisitos

```
python3
```

```
pip
```

```
virtualenv
```

## Configuração do ambiente

Para configurar o projeto é necessário seguir os seguintes passos:
```console

$ sudo apt install virtualenv
$ virtualenv -p python3 venv
$ source venv/bin/activate
$ pip install -r requirements.txt

```

### Execução

```console

$ cd Eventos
$ python manage.py runserver

```
Após a execução desses passos o sistema deve estar disponivel na url http://127.0.0.1:8000/geradorCrachas/


### Dificuldades

Inicialmente, a idéia era manipular os arquivos psd, a fim de criar layers de texto e fazer todo o
layout do cracha dessa forma, porém o suporte para esse tipo de arquivo propietário é bem precario 
em Python, dessa maneira optei por ter um Background fixo dos crachas com o logo do evento personalizável.

Com as bibliotecas que utilizei não seria dificil personalizar o texto com diferentes fontes, tamanhos e adicionar as opções de negrito e itálico, assim como um layout mais bonito para o frontend porém não fiz a tempo da entrega.


Exemplo a ser colocado no campo layout do crachá:

Nome: {{Nome}}
País: {{País}}
