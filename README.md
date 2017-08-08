# Zabbix IT Services
Configuração da árvore de serviços do Zabbix via API
- Cadastra automáticamente todo ambiente do Zabbix na árvore de serviços de TI
- Opção de incluir por grupo de hosts
- Opção de incluir apenas selecionando hosts

## Dependências

```sh
$ sudo apt-get figlet
```

<b>Obs.:</b> Verifique o nome do pacote em sua distribuição.

## Instalação

```sh
$ wget https://raw.githubusercontent.com/janssenlima/zabbix-it-services/master/it-services.py
$ sudo pip install -r requirements.txt
```
## Instalação

```sh
$ wget https://raw.githubusercontent.com/janssenlima/zabbix-it-services/master/it-services.py
$ chmod +x it-services.py
$ sudo pip install -r requirements.txt
```

## Configurar parâmetros de conexão do Zabbix

>Inserir URL, usuário e senha de acesso ao Zabbix

```sh
$ vim it-services.py
```

## Execução

```sh
$ ./it-services.py
```

## Quer ajudar no projeto?
Achou algum erro ou quer fazer uma sugestão para o projeto? <br>
Cadastre uma Issue aqui mesmo no GitHub
