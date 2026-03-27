Necessário instalar o VENV

Colocar "triggerFiberHome.sh" em "/usr/lib/zabbix/externalscripts"

Não esquecer de dar permissões para os arquivos

Ajustar o path das variaveis PYTHON e SCRIPT para o que se adequar ao seu cenário


key do zabbix
Type: External Check
triggerFiberHome.sh["{HOST.IP}","{#SNMPINDEX}"]
