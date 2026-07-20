import pandas as pd


def aggregate(
    valid_df: pd.DataFrame,
    invalid_df: pd.DataFrame,
) -> tuple[pd.DataFrame, float]:
    """
    Строит агрегированную статистику.

    Returns:
        report - средний UMUX по месяцам, продуктам и версиям.
        rejected_share - доля отбракованных анкет.
    """

    report = valid_df.copy()
    report["submitted_at"] = pd.to_datetime(
        report["submitted_at"],
        errors="coerce"
    )

    # Получаем месяц
    report["month"] = report["submitted_at"].dt.to_period("M").astype(str)

    # Агрегация
    report = (
        report
        .groupby(
            ["month", "product", "product_version"],
            as_index=False
        )
        .agg(
            average_umux=("umux_score", "mean"),
            responses=("response_id", "count"),
        )
    )
    report["average_umux"] = report["average_umux"].round(2)

    total = len(valid_df) + len(invalid_df)

    rejected_share = (
        (len(invalid_df) / total)
        if total > 0
        else 0
    )

    return report, rejected_share