def calculate_future_value(rj: float, SK: float, EM: float, n: int) -> dict[str, float]:
    rm = (1 + rj) ** (1 / 12) - 1

    FVstart = SK * (1 + rm) ** (12 * n)
    
    if rm == 0:
        FVeinzahlungen = EM * 12 * n
    else:
        FVeinzahlungen = EM * (((1 + rm) ** (12 * n) - 1) / rm)

    return {
        "monthly_rate": rm,
        "future_value_start": FVstart,
        "future_value_payments": FVeinzahlungen,
        "total_future_value": FVstart + FVeinzahlungen,
    }