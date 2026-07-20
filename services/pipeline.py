# services/pipeline.py

from pipeline.validator import validate_rows
from services.aggregator import aggregate
from services.loader import load_table
from services.reporter import create_report


def run_pipeline(files: list[str]) -> dict:
    """
    Полный ETL-пайплайн.
    """

    df = load_table(files).drop_duplicates(subset=["response_id"])

    valid_df, invalid_df = validate_rows(df)

    report, rejected_share = aggregate(
        valid_df,
        invalid_df,
    )

    create_report(
        report,
        valid_df,
        invalid_df,
    )

    return {
        "report": report,
        "valid": len(valid_df),
        "invalid": len(invalid_df),
        "rejected_share": rejected_share,
    }