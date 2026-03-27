#!/usr/bin/env python3

import os
import re
import sys
import time

CACHE_DIR = "/tmp/fiberhome_cache"
CACHE_MAX_AGE = 600  # 10 minutos
INVALID_VALUES = {2147483647}

LINE_REGEX = re.compile(r".*\.(\d+)\s+=\s+\w+:\s+(-?\d+)$")

def fail(message: str, exit_code: int = 1) -> None:
    print(f"ZBX_NOTSUPPORTED: {message}")
    sys.exit(exit_code)

def parse_arguments():
    if len(sys.argv) != 3:
        fail("uso: mediaFiberhome.py <ip> <pon_index>")

    ip = sys.argv[1].strip()
    pon_index = sys.argv[2].strip()

    if not ip:
        fail("ip vazio")

    if not pon_index:
        fail("pon_index vazio")

    if not pon_index.isdigit():
        fail("pon_index invalido")

    return ip, int(pon_index)

def get_cache_file(ip: str) -> str:
    cache_file = os.path.join(CACHE_DIR, f"{ip}.cache")

    if not os.path.isfile(cache_file):
        fail(f"cache nao encontrado para {ip}")

    age = time.time() - os.path.getmtime(cache_file)
    if age > CACHE_MAX_AGE:
        fail(f"cache expirado para {ip} ({int(age)}s)")

    return cache_file

def same_pon(target_pon_index: int, composite_index: int) -> bool:
    return (composite_index & 0xFFFF0000) == target_pon_index

def collect_rx_values(target_pon_index: int, cache_file: str):
    values = []

    with open(cache_file, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            match = LINE_REGEX.search(line)

            if not match:
                continue

            composite_index = int(match.group(1))
            raw_value = int(match.group(2))

            if not same_pon(target_pon_index, composite_index):
                continue

            if raw_value in INVALID_VALUES:
                continue

            values.append(raw_value / 100.0)

    return values

def main():
    ip, pon_index = parse_arguments()
    cache_file = get_cache_file(ip)
    values = collect_rx_values(pon_index, cache_file)

    if not values:
        print("0")
        return

    average = sum(values) / len(values)
    print(f"{average:.2f}")

if __name__ == "__main__":
    main()
