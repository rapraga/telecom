#!/bin/bash

IP="$1"
COMMUNITY="$2"

CACHE_DIR="/tmp/fiberhome_cache"
BASE_OID="1.3.6.1.4.1.5875.800.3.9.3.3.1.6"

if [ -z "$IP" ] || [ -z "$COMMUNITY" ]; then
    echo "uso: coletaFiberHome.sh <ip> <community>"
    exit 1
fi

mkdir -p "$CACHE_DIR"

CACHE_FILE="${CACHE_DIR}/${IP}.cache"
TMP_FILE="${CACHE_FILE}.tmp"

/usr/bin/snmpwalk -v2c -c "$COMMUNITY" "$IP" "$BASE_OID" > "$TMP_FILE" 2>/dev/null

if [ $? -ne 0 ]; then
    rm -f "$TMP_FILE"
    echo "erro ao coletar dados SNMP de $IP"
    exit 1
fi

mv "$TMP_FILE" "$CACHE_FILE"
exit 0
