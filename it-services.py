# -*- coding: utf-8 -*-

#@author: Janssen dos reis lima
#@email : janssenreislima@gmail.com / janssen@conectsys.com.br
#@web   : https://www.conectsys.com.br

# Update: 08/08/2017

from zabbix_api import ZabbixAPI
import os

# add the IP of your Zabbix Server
zapi = ZabbixAPI(server="http://localhost/zabbix")
# add your access credentials
zapi.login("Admin", "zabbix")

def get_hostgroups():
    hostgroups = zapi.hostgroup.get({"output": "extend"})
    listaGrupos = []
    for x in hostgroups:
        print x['name']
        listaGrupos += [x['name']]
    return listaGrupos

def get_hostgroups_id(grupo):
    groupId = zapi.hostgroup.get({"output": "extend","filter":{"name":grupo}})[0                                                                                                                     ]['groupid']
    return groupId

def get_hosts(grupo):
    hosts_grupo = zapi.host.get({"groupids":get_hostgroups_id(grupo),"output":["                                                                                                                     host"]})
    listaHosts = []
    for x in hosts_grupo:
        print x['host']
        listaHosts += [x['host']]
    return listaHosts

def get_hostid(host):
    hostId = zapi.host.get({"output":"hostid","filter":{"host":host}})[0]['hosti                                                                                                                     d']
    return hostId

def get_triggers_hosts(host):
    triggers = zapi.trigger.get({"hostids":get_hostid(host),"expandDescription":                                                                                                                     "true","expandComment":"true","expandExpression":"true"})
    for x in triggers:
        print x['description']

def get_items_hosts(host):
    items = zapi.item.get({"hostids":get_hostid(host),"with_triggers":True,"sele                                                                                                                     ctTriggers":"extend"})
    listaItems = []
    for x in items:
        print x['name']
        listaItems += [x['name']]
    return listaItems

def get_item_triggerid(host,item):
    triggerId = zapi.item.get({"output":"triggers","hostids":get_hostid(host),"w                                                                                                                     ith_triggers":True,"selectTriggers":"triggers","filter":{"name":item}})[0]['trig                                                                                                                     gers'][0]['triggerid']
    return triggerId

def mk_father_itservices(grupo):
    zapi.service.create({"name":grupo,"algorithm":"1","showsla":"1","goodsla":"9                                                                                                                     9.99","sortorder":"1"})

def get_itservice_pid(grupo):
    parentId = zapi.service.get({"selectParent":"extend","selectTrigger":"extend                                                                                                                     ","expandExpression":"true","filter":{"name":grupo}})[0]['serviceid']
    return parentId

def mk_child_itservices(host,grupo):
    zapi.service.create({"name":host,"algorithm":"1","showsla":"1","goodsla":"99                                                                                                                     .99","sortorder":"1","parentid":get_itservice_pid(grupo)})

def get_itservice_pid_child(host):
    parentIdChild = zapi.service.get({"selectParent":"extend","selectTrigger":"e                                                                                                                     xtend","expandExpression":"true","filter":{"name":host}})[0]['serviceid']
    return parentIdChild

def mk_child_itservices_trigger(host,item):
    zapi.service.create({"name":item,"algorithm":"1","showsla":"1","goodsla":"99                                                                                                                     .99","sortorder":"1","parentid":get_itservice_pid_child(host),"triggerid":get_it                                                                                                                     em_triggerid(host,item)})

def get_itservices():
    itServices = zapi.service.get({"selectParent":"extend","selectTrigger":"exte                                                                                                                     nd"})
    listaServicos = []
    for x in itServices:
        listaServicos += [x['serviceid']]
    return listaServicos

def delete_tree_itservices():
    for x in get_itservices():
        zapi.service.deletedependencies([x])
        zapi.service.delete([x])

def mk_populate():
    delete_tree_itservices()
    for nomeGrupo in get_hostgroups():
        mk_father_itservices(nomeGrupo)
        for nomeHost in get_hosts(nomeGrupo):
            mk_child_itservices(nomeHost, nomeGrupo)
            for nomeItem in get_items_hosts(nomeHost):
                mk_child_itservices_trigger(nomeHost, nomeItem)

def mk_populate_grupo_host(nomeGrupo):
        mk_father_itservices(nomeGrupo)
        for nomeHost in get_hosts(nomeGrupo):
                mk_child_itservices(nomeHost, nomeGrupo)
                for nomeItem in get_items_hosts(nomeHost):
                        mk_child_itservices_trigger(nomeHost, nomeItem)

def mk_populate_host(host,grupo):
        mk_father_itservices(grupo)
        mk_child_itservices(host, grupo)
        for nomeItem in get_items_hosts(host):
                mk_child_itservices_trigger(host, nomeItem)

def limparTela():
    os.system("clear")
    os.system("figlet Servicos de TI")
    print "===================================================="
    print "Escrito por Janssen Lima"
    print "janssen@conectsys.com.br / janssenreislima@gmail.com"
    print "https://www.conectsys.com.br"
    print "===================================================="

# Inicio da execucao
limparTela()

resposta=True
while resposta:
    print ("""
    1.  Listar grupos de hosts
    2.  Listar hosts de um grupo
    3.  Listar itens com triggers de um host
    4.  Listar triggers de um host
    5.  Criar IT Services de um host
    6.  Criar IT Services de um grupo de hosts
    7.  Criar IT Services de todo ambiente automaticamente
    8.  Apagar todos os IT Services
    9.  Sair
    """)
    resposta=raw_input("Escolha uma opcao: ")
    if resposta=="1":
      limparTela()
      print "GRUPOS CADASTRADOS"
      print "----------------------------------------------------"
      get_hostgroups()
      print "===================================================="
    elif resposta=="2":
      grupo=raw_input("Digite o nome do grupo de hosts: ")
      limparTela()
      print "HOSTS CADASTRADOS NO GRUPO", grupo
      print "----------------------------------------------------"
      get_hosts(grupo)
      print "===================================================="
    elif resposta=="3":
      host=raw_input("Digite o nome do host: ")
      limparTela()
      print "ITENS CADASTRADOS NO HOST", host, "QUE POSSUEM TRIGGERS."
      print "----------------------------------------------------"
      get_items_hosts(host)
      print "===================================================="
    elif resposta=="4":
      host=raw_input("Digite o nome do host: ")
      limparTela()
      print "TRIGGERS CADASTRADAS NO HOST", host
      print "----------------------------------------------------"
      get_triggers_hosts(host)
      print "===================================================="
    elif resposta=="5":
      grupo=raw_input("Digite o nome do grupo de hosts: ")
      get_hosts(grupo)
      host=raw_input("Digite o nome do host: ")
      limparTela()
      mk_populate_host(host,grupo)
      print "===================================================="
    elif resposta=="6":
      grupo=raw_input("Digite o nome do grupo de hosts: ")
      limparTela()
      mk_populate_grupo_host(grupo)
      print "===================================================="
    elif resposta=="7":
      limparTela()
      print "Recriando ambiente IT Services. Aguarde ..."
      mk_populate()
      print "===================================================="
      print "IT Services criados com sucesso. Acesse http://<ip_servidor>/zabbix                                                                                                                     /srv_status.php"
      print ""
      print "===================================================="
    elif resposta=="8":
      limparTela()
      print "Removendo ambiente IT Services. Aguarde ..."
      delete_tree_itservices()
      print "===================================================="
      print "IT Services removidos com sucesso."
    elif resposta=="9":
      print("\nObrigado por usar a API do Zabbix! Acesse: https://www.conectsys.                                                                                                                     com.br")
      resposta=False
    elif resposta !="":
      print("\n Opcao invalida!")
