# main.py

import argparse

from services.pipeline import run_pipeline


def main():
    parser = argparse.ArgumentParser(
        description="UMUX ETL Pipeline"
    )

    parser.add_argument(
        "--input",
        nargs="+",
        required=True,
        metavar="FILE",
        help="Один или несколько файлов",
    )

    args = parser.parse_args()

    run_pipeline(args.input)


if __name__ == "__main__":
    main()