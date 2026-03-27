#!/bin/bash

IP="$1"
PON_INDEX="$2"

PYTHON="/mediaFiberhome/venv/bin/python3"
SCRIPT="/mediaFiberhome/mediaFiberhome.py"

if [ -z "$IP" ] || [ -z "$PON_INDEX" ]; then
    echo "ZBX_NOTSUPPORTED: uso: triggerFiberHome.sh <ip> <pon_index>"
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

"$PYTHON" "$SCRIPT" "$IP" "$PON_INDEX"
