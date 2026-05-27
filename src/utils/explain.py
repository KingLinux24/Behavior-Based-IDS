def explain(row):
    reasons = []
    if row["unique_ports"] > 5:
        reasons.append("High number of unique destination ports")
    if row["connections"] > 20:
        reasons.append("Unusually high connection rate")
    if row["bytes_mean"] < 200:
        reasons.append("Low byte transfers typical of scanning")

    if not reasons:
        reasons.append("Behavior deviates from learned baseline")

    return reasons
