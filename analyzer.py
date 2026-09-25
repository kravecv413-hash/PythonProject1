import csv
from collections import defaultdict
from pathlib import Path


def load_leads(path: Path) -> list[dict]:
    leads = []
    seen_ids = set()

    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            lead_id = (row.get("id") or "").strip()
            channel = (row.get("channel") or "").strip()
            status = (row.get("status") or "").strip()
            amount_raw = (row.get("amount") or "").strip()

            if not channel or not status:
                continue
            if lead_id in seen_ids:
                continue
            seen_ids.add(lead_id)

            try:
                amount = float(amount_raw) if amount_raw else 0.0
            except ValueError:
                amount = 0.0

            leads.append({
                "id": lead_id,
                "channel": channel,
                "status": status,
                "amount": amount,
            })
    return leads


def build_report(leads: list[dict]) -> list[dict]:
    stats = defaultdict(lambda: {"leads": 0, "paid": 0, "revenue": 0.0})

    for lead in leads:
        ch = lead["channel"]
        stats[ch]["leads"] += 1
        if lead["status"] == "paid":
            stats[ch]["paid"] += 1
            stats[ch]["revenue"] += lead["amount"]

    report = []
    for channel, s in sorted(stats.items()):
        conversion = (s["paid"] / s["leads"] * 100) if s["leads"] else 0.0
        report.append({
            "channel": channel,
            "leads": s["leads"],
            "paid": s["paid"],
            "conversion": round(conversion, 2),
            "revenue": round(s["revenue"], 2),
        })
    return report


def save_report(report: list[dict], path: Path) -> None:
    fields = ["channel", "leads", "paid", "conversion", "revenue"]
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(report)