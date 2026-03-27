#!/bin/bash

IP="$1"
COMMUNITY="$2"
PON_ID="$3"

PYTHON="/mediaHuawei/venv/bin/python3"
SCRIPT="/mediaHuawei/mediaHuawei.py"

if [ -z "$IP" ] || [ -z "$COMMUNITY" ] || [ -z "$PON_ID" ]; then
    echo "ZBX_NOTSUPPORTED: uso: trigger.sh <ip> <community> <pon_id>"
    exit 1
fi

if [ ! -x "$PYTHON" ]; then
    echo "ZBX_NOTSUPPORTED: python do venv nao encontrado em $PYTHON"
    exit 1
fi

if [ ! -f "$SCRIPT" ]; then
    echo "ZBX_NOTSUPPORTED: script nao encontrado em $SCRIPT"
    exit 1
fi

"$PYTHON" "$SCRIPT" "$IP" "$COMMUNITY" "$PON_ID"
