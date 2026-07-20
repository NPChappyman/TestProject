# services/validator.py

import pandas as pd

from config.config import (
    CRITICAL_FIELDS,
    NULL_LIKE_STRINGS,
    SCORE_MAX,
    SCORE_MIN,
)


def validate_rows(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Валидирует строки DataFrame.

    Возвращает:
        valid_df   - корректные строки
        invalid_df - отбракованные строки с причиной
    """

    valid_rows = []
    invalid_rows = []

    for _, row in df.iterrows():
        row = row.copy()

        # ---------- Проверка обязательных полей ----------
        error = None

        for field in row.keys():
            value = row[field]

            if pd.isna(value) and field in CRITICAL_FIELDS:
                error = f"{field} is empty"
                break

            if (
                isinstance(value, str)
            ):
                if (value.strip().lower() in NULL_LIKE_STRINGS):
                    error = f"{field} is empty"
                    break

                row[field] = value.strip().lower()

        if error:
            row["error"] = error
            invalid_rows.append(row)
            continue

        # ---------- Приведение оценок ----------
        try:
            row["score1"] = int(row["score1"])
            row["score2"] = int(row["score2"])
        except (ValueError, TypeError):
            row["error"] = "score must be integer"
            invalid_rows.append(row)
            continue
        # ---------- Нормализация даты ----------
        try:
            row["submitted_at"] = pd.to_datetime(
                row["submitted_at"]
            )

            # Приводим к единому формату
            row["submitted_at"] = row["submitted_at"].strftime(
                "%Y-%m-%d %H:%M:%S"
            )

        except (ValueError, TypeError):
            row["error"] = "invalid submitted_at"
            invalid_rows.append(row)
            continue
        # ---------- Проверка диапазона ----------
        if not SCORE_MIN <= row["score1"] <= SCORE_MAX:
            row["error"] = "score1 out of range"
            invalid_rows.append(row)
            continue

        if not SCORE_MIN <= row["score2"] <= SCORE_MAX:
            row["error"] = "score2 out of range"
            invalid_rows.append(row)
            continue
        # ---------- Расчет UMUX ----------
        row["umux_score"] = (
                ((int(row["score1"]) - 1) + (5 - int(row["score2"])))/8*100
        )


        valid_rows.append(row)

    return (
        pd.DataFrame(valid_rows),
        pd.DataFrame(invalid_rows),
    )