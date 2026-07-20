from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)


def create_report(
    report: pd.DataFrame,
    valid_df: pd.DataFrame,
    invalid_df: pd.DataFrame,
) -> None:
    """
    Сохраняет результаты ETL и формирует отчет.
    """

    total = len(valid_df) + len(invalid_df)
    rejected = len(invalid_df)
    rejected_share = rejected / total * 100 if total else 0

    # ---------------- CSV ----------------

    csv_path = OUTPUT_DIR / "report.csv"

    report.to_csv(
        csv_path,
        index=False,
    )

    # ---------------- Консоль ----------------

    print("\n" + "=" * 50)
    print("                UMUX REPORT")
    print("=" * 50)

    print(f"Всего анкет:        {total}")
    print(f"Валидных:           {len(valid_df)}")
    print(f"Отбракованных:      {rejected}")
    print(f"Доля брака:         {rejected_share:.2f}%")

    print("\nОтчет сохранен:")
    print(csv_path)


    print("\nСоздание графиков...\n")

    # ---------------- Графики по продуктам ----------------

    for product, product_df in report.groupby("product"):

        # Средний UMUX по версии
        chart = (
            product_df
            .groupby("product_version", as_index=False)
            .agg(
                average_umux=("average_umux", "mean")
            )
            .sort_values("average_umux")
        )

        plt.figure(figsize=(8, 5))

        plt.bar(
            chart["product_version"].astype(str),
            chart["average_umux"],
        )

        plt.title(f"{product}")
        plt.xlabel("Version")
        plt.ylabel("Average UMUX")

        # Показываем значения над столбцами
        for x, y in zip(chart["product_version"], chart["average_umux"]):
            plt.text(
                x,
                y + 1,
                f"{y:.1f}",
                ha="center",
            )

        # Линии порогов
        plt.axhline(
            60,
            linestyle="--",
            linewidth=1,
            label="Risk",
        )

        plt.axhline(
            80,
            linestyle="--",
            linewidth=1,
            label="Good",
        )

        plt.ylim(0, 100)

        plt.legend()

        file_name = (
            str(product)
            .replace(" ", "_")
            .replace("/", "_")
            .replace("\\", "_")
        )

        graph_path = OUTPUT_DIR / f"{file_name}.png"

        plt.tight_layout()
        plt.savefig(graph_path)
        plt.close()

        print(f"✓ {graph_path}")