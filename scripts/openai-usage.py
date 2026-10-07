"""Report organization-wide OpenAI costs without blocking content workflows."""
import calendar
import json
import os
import re
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


UTC = timezone.utc


def costs(start, end, key):
    total = Decimal(0)
    page = None
    seen = set()
    while True:
        params = {"start_time": int(start.timestamp()), "end_time": int(end.timestamp()),
                  "bucket_width": "1d", "limit": 180}
        if page:
            params["page"] = page
        request = Request("https://api.openai.com/v1/organization/costs?" + urlencode(params),
                          headers={"Authorization": "Bearer " + key})
        with urlopen(request, timeout=30) as response:
            data = json.load(response)
        for bucket in data["data"]:
            for result in bucket["results"]:
                amount = result.get("amount")
                if not amount or amount.get("currency") != "usd" or amount.get("value") is None:
                    raise ValueError("Costs response contains a missing or non-USD amount")
                value = Decimal(str(amount["value"]))
                if not value.is_finite():
                    raise ValueError("Costs response contains an invalid amount")
                total += value
        if not data["has_more"]:
            return total
        page = data.get("next_page")
        if not page or page in seen:
            raise ValueError("Invalid costs pagination")
        seen.add(page)


def reload_metadata(now):
    date = os.getenv("OPENAI_CREDIT_DATE", "").strip()
    amount = os.getenv("OPENAI_CREDIT_AMOUNT", "").strip()
    reload = expiry = credit = None
    notes = []
    if date:
        try:
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date):
                raise ValueError()
            reload = datetime.strptime(date, "%Y-%m-%d").replace(tzinfo=UTC)
            if reload > now:
                raise ValueError()
            year = reload.year + 1
            day = min(reload.day, calendar.monthrange(year, reload.month)[1])
            expiry = reload.replace(year=year, day=day)
        except ValueError:
            reload = None
            notes.append("Invalid OPENAI_CREDIT_DATE; use a non-future YYYY-MM-DD date.")
    if amount:
        try:
            credit = Decimal(amount)
            if not credit.is_finite() or credit <= 0:
                raise InvalidOperation()
        except InvalidOperation:
            credit = None
            notes.append("Invalid OPENAI_CREDIT_AMOUNT; use a positive USD amount.")
    return reload, expiry, credit, notes


def report(now, key):
    lines = ["## OpenAI API usage", "", "Organization-wide costs in USD (UTC).", ""]
    reload, expiry, credit, notes = reload_metadata(now)
    if not key:
        lines.append("⚠️ Usage unavailable: configure the OPENAI_ADMIN_KEY repository secret.")
    else:
        lines += ["| Period | Cost |", "| --- | ---: |"]
        for label, start in [("Today", now.replace(hour=0, minute=0, second=0, microsecond=0)),
                             ("Month to date", now.replace(day=1, hour=0, minute=0, second=0, microsecond=0))]:
            try:
                value = costs(start, now, key)
                lines.append(f"| {label} | ${value:.4f} |")
            except (HTTPError, URLError, TimeoutError, ValueError, KeyError, TypeError, InvalidOperation) as error:
                lines.append(f"| {label} | Unavailable |")
                notes.append(f"{label} costs unavailable ({safe_error(error)}).")
        if reload and credit is not None:
            try:
                spent = costs(reload, now, key)
                remaining = max(Decimal(0), credit - spent) if now < expiry else Decimal(0)
                lines += ["", f"Estimated remaining credit: **${remaining:.4f}**",
                          f"Costs since reload: ${spent:.4f}",
                          "Estimate covers only the latest reload; it excludes older credits and may lag recent usage."]
                if now >= expiry:
                    notes.append("The recorded credit purchase has expired.")
                elif remaining < max(Decimal("1"), credit * Decimal("0.2")):
                    notes.append("Estimated credit is low.")
            except (HTTPError, URLError, TimeoutError, ValueError, KeyError, TypeError, InvalidOperation) as error:
                notes.append(f"Credit estimate unavailable ({safe_error(error)}).")
    if expiry:
        lines += ["", f"Credit expires: **{expiry.date()}** (one calendar year after reload)."]
        if 0 <= (expiry - now).total_seconds() < 30 * 86400:
            notes.append("The recorded credit purchase expires within 30 days.")
    if not reload or credit is None:
        lines += ["", "Credit estimate omitted: configure both OPENAI_CREDIT_DATE and OPENAI_CREDIT_AMOUNT."]
    lines += ["", "Billing data may lag recent requests; today's costs are not the cost of this workflow run."]
    lines += ["", *[f"⚠️ {note}" for note in notes]]
    return "\n".join(lines) + "\n"


def safe_error(error):
    # Never print an API response body, request headers, or secrets.
    return f"HTTP {error.code}" if isinstance(error, HTTPError) else type(error).__name__


if __name__ == "__main__":
    try:
        summary = report(datetime.now(UTC), os.getenv("OPENAI_ADMIN_KEY", "").strip())
    except Exception as error:
        summary = f"## OpenAI API usage\n\n⚠️ Report unavailable ({safe_error(error)}).\n"
    print(summary)
    if os.getenv("GITHUB_STEP_SUMMARY"):
        with Path(os.environ["GITHUB_STEP_SUMMARY"]).open("a") as output:
            output.write(summary)
