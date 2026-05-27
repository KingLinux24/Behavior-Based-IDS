import random
import json
from datetime import datetime, timedelta
from pathlib import Path

OUT = Path("data/raw/flows.jsonl")
OUT.parent.mkdir(parents=True, exist_ok=True)

HOSTS = ["wkst-01", "wkst-02", "srv-web-01"]
NORMAL_PORTS = [80, 443, 53]
ATTACK_PORTS = [22, 3389, 445]
IPS_INTERNAL = ["10.0.1.10", "10.0.1.11"]
IPS_EXTERNAL = ["198.51.100.10", "203.0.113.55"]

def ts(base, sec):
    return (base + timedelta(seconds=sec)).isoformat() + "Z"

def main():
    base = datetime.utcnow() - timedelta(hours=1)
    rows = []

    # Normal behavior
    for i in range(1000):
        rows.append({
            "timestamp": ts(base, i * 3),
            "host": random.choice(HOSTS),
            "src_ip": random.choice(IPS_INTERNAL),
            "dst_ip": random.choice(IPS_EXTERNAL),
            "dst_port": random.choice(NORMAL_PORTS),
            "bytes": random.randint(200, 3000),
            "duration": random.uniform(0.1, 1.5),
            "protocol": "tcp"
        })

    # Anomalous scanning behavior
    attacker_ip = "198.51.100.10"
    for i in range(300):
        rows.append({
            "timestamp": ts(base, 4000 + i),
            "host": "srv-web-01",
            "src_ip": attacker_ip,
            "dst_ip": "10.0.1.10",
            "dst_port": random.choice(ATTACK_PORTS),
            "bytes": random.randint(40, 200),
            "duration": random.uniform(0.01, 0.2),
            "protocol": "tcp"
        })

    random.shuffle(rows)

    with OUT.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")

if __name__ == "__main__":
    main()
