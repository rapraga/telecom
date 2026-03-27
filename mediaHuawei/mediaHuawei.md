Necessário instalar o VENV

Colocar "triggerHuawei.sh" em "/usr/lib/zabbix/externalscripts"

Não esquecer de dar permissões para os arquivos

Ajustar o path das variaveis PYTHON e SCRIPT para o que se adequar ao seu cenário


key do zabbix
Type: External Check
triggerHuawei.sh["{HOST.IP}","{$SNMP_COMMUNITY}","{#SNMPINDEX}"]
