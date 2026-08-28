def monthly_rate(rj: float) -> float:
    """Convert an annual return rate into its equivalent monthly rate."""
    return (1 + rj) ** (1 / 12) - 1


def next_month_value(value: float, rm: float, contribution: float) -> float:
    """Grow the portfolio by one month, then add the monthly contribution.

    Contributions are applied at the end of the month (ordinary annuity),
    which matches the original closed-form formula.
    """
    return value * (1 + rm) + contribution


def build_monthly_history(rj: float, SK: float, EM: float, n: int) -> list[dict[str, float]]:
    """Portfolio development for every month from 0 until the end of the period.

    This is the single source of truth for the investment calculation: the
    final value and any yearly view are derived from this history.
    """
    rm = monthly_rate(rj)
    total_months = 12 * n

    value = SK
    invested = SK
    history = [{"month": 0, "invested": invested, "value": value}]

    for month in range(1, total_months + 1):
        value = next_month_value(value, rm, EM)
        invested += EM
        history.append({"month": month, "invested": invested, "value": value})

    return history


def yearly_history(monthly: list[dict[str, float]]) -> list[dict[str, float]]:
    """Derive the yearly view by selecting every 12th month (0, 12, 24, ...)."""
    return monthly[::12]


def calculate_future_value(rj: float, SK: float, EM: float, n: int) -> dict:
    history = build_monthly_history(rj, SK, EM, n)
    rm = monthly_rate(rj)

    total_future_value = history[-1]["value"]
    FVstart = SK * (1 + rm) ** (12 * n)

    return {
        "monthly_rate": rm,
        "future_value_start": FVstart,
        "future_value_payments": total_future_value - FVstart,
        "total_future_value": total_future_value,
        "history": history,
    }


if __name__ == "__main__":
    history = build_monthly_history(
        rj=0.08,
        SK=40_000,
        EM=1_000,
        n=40
    )

    print("Erste 5 Monate:")
    for entry in history[:5]:
        print(entry)

    print("\nErste 5 Jahre:")
    for entry in yearly_history(history)[:5]:
        print(entry)