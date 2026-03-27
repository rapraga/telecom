#!/usr/bin/env python3

import re
import sys
import shutil
import subprocess

BASE_OID = "1.3.6.1.4.1.2011.6.128.1.1.2.51.1.4"
INVALID_VALUE = 2147483647

def fail(message: str, exit_code: int = 1) -> None:
    print(f"ZBX_NOTSUPPORTED: {message}")
    sys.exit(exit_code)

def parse_arguments():
    if len(sys.argv) != 4:
        fail("uso: mediaHuawei.py <ip> <community> <pon_id>")

    ip = sys.argv[1].strip()
    community = sys.argv[2].strip()
    pon_id = sys.argv[3].strip()

    if not ip:
        fail("ip vazio")

    if not community:
        fail("community vazia")

    if not pon_id:
        fail("pon_id vazio")

    return ip, community, pon_id

def get_snmpwalk_binary() -> str:
    binary = shutil.which("snmpwalk")
    if not binary:
        fail("binario snmpwalk nao encontrado no PATH")
    return binary

def collect_rx_values(ip: str, community: str, pon_id: str):
    oid = f"{BASE_OID}.{pon_id}"
    snmpwalk_bin = get_snmpwalk_binary()

    cmd = [
        snmpwalk_bin,
        "-v2c",
        "-c",
        community,
        ip,
        oid
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60
        )
    except subprocess.TimeoutExpired:
        fail("timeout ao executar snmpwalk")
    except Exception as exc:
        fail(f"erro ao executar snmpwalk: {exc}")

    if result.returncode != 0:
        stderr = (result.stderr or "").strip()
        stdout = (result.stdout or "").strip()
        error_text = stderr if stderr else stdout if stdout else "snmpwalk retornou erro"
        fail(error_text)

    values = []

    for line in result.stdout.splitlines():
        match = re.search(r"INTEGER:\s*(-?\d+)", line)
        if not match:
            continue

        raw_value = int(match.group(1))

        if raw_value == INVALID_VALUE:
            continue

        dbm_value = raw_value / 100.0
        values.append(dbm_value)

    return values

def main():
    ip, community, pon_id = parse_arguments()
    values = collect_rx_values(ip, community, pon_id)

    if not values:
        print("0")
        return

    average = sum(values) / len(values)
    print(f"{average:.2f}")

if __name__ == "__main__":
    main()
