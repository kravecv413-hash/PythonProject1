from pathlib import Path

from analyzer import load_leads, build_report, save_report


def main() -> None:
    base = Path(__file__).parent
    input_path = base / "data" / "leads.csv"
    output_path = base / "report.csv"

    if not input_path.exists():
        print(f"Не найден входной файл: {input_path}")
        return

    leads = load_leads(input_path)
    report = build_report(leads)
    save_report(report, output_path)

    print(f"Обработано лидов: {len(leads)}")
    print(f"Отчёт сохранён: {output_path}")
    print()
    print(f"{'channel':<10}{'leads':>7}{'paid':>7}{'conv %':>9}{'revenue':>10}")
    for row in report:
        print(f"{row['channel']:<10}{row['leads']:>7}{row['paid']:>7}"
              f"{row['conversion']:>9}{row['revenue']:>10}")


if __name__ == "__main__":
    main()