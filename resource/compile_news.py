import os
import sys
from datetime import datetime
import pandas as pd

TARGET_NEW_BADGE_MONTHS = 4

# Get script directory
fn = getattr(sys.modules['__main__'], '__file__')
root_path = os.path.abspath(os.path.dirname(fn))

# Read the data file (columns: date, content — same as CSV)
data_file = os.path.join(root_path, "data_news.xls")
df = pd.read_excel(data_file, dtype=str).fillna("")
news_items = df.to_dict("records")


def normalize_news_date(val):
    """Excel dates often become strings like '2026-04-01 00:00:00'; show as '2026-04'."""
    if val is None or (isinstance(val, float) and pd.isna(val)):
        return ""
    s = str(val).strip()
    if not s:
        return ""
    try:
        return pd.to_datetime(s).strftime("%Y-%m")
    except (ValueError, TypeError, OSError):
        return s


for row in news_items:
    row["date"] = normalize_news_date(row.get("date", ""))

# print(news_items)


# Find the latest news entry date as the base date
def parse_date(date_str):
    """Parse 'YYYY-MM' (year-month, e.g. 2026-04)."""
    try:
        return datetime.strptime(date_str.strip(), "%Y-%m")
    except (ValueError, TypeError):
        return datetime.min


def months_before_latest(latest: datetime, target_months: int) -> datetime:
    """First day of the month `target_months` before `latest`'s month."""
    month = latest.month - target_months
    year = latest.year
    if month <= 0:
        month += 12
        year -= 1
    return datetime(year, month, 1)

_valid_dates = [d for d in (parse_date(item["date"]) for item in news_items) if d != datetime.min]
if _valid_dates:
    latest_date = max(_valid_dates)
    n_months_ago = months_before_latest(latest_date, TARGET_NEW_BADGE_MONTHS)
else:
    latest_date = datetime.today().replace(day=1)
    n_months_ago = datetime(9999, 12, 31)


# NEW badge HTML
NEW_BADGE = '<span style="background:rgb(246, 112, 97); color: white; padding: 2px 8px; border-radius: 10px; font-size: 11px; font-weight: bold;">NEW</span>'

def is_within_target_months(date_str, latest_date, target_months):
    """Check if the date has NOT passed target_months months (is recent)"""
    cutoff = months_before_latest(latest_date, target_months)
    entry_date = parse_date(date_str)
    if entry_date == datetime.min:
        return False
    return entry_date >= cutoff

# Generate HTML
body = '''<hr>

<h3 style="color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 5px; display: inline-block;">News</h3>

<style>
  .news-list a { font-weight: bold; }
</style>
<div style="max-height: 300px; overflow-y: auto; padding: 10px; border: 1px solid #e0e0e0; border-radius: 5px; background: #fafafa;">
<ul class="news-list" style="line-height:1.4em">
  <font size="2">
'''

for item in news_items:
    date = item["date"].strip()
    content = item["content"].strip()
    
    body += "  <li>\n"
    
    # Add NEW badge if within target_months months
    if is_within_target_months(date, latest_date, target_months=TARGET_NEW_BADGE_MONTHS):
        body += f"\t{NEW_BADGE}\n"
    
    body += f"\t[{date}]\n"
    body += f"\t{content}\n"
    body += "  </li>\n"

body += '''</ul>
</div>

<!-- <a href="{{ site.baseurl }}/news.html">history</a> -->'''

# Write output
output_file = os.path.join(root_path, "news.txt")
with open(output_file, "w", encoding="utf-8") as f:
    f.write(body)

if _valid_dates:
    print(
        f"News compiled! {len(news_items)} items. NEW badge for entries on/after "
        f"{n_months_ago.strftime('%m/%d/%Y')} (cutoff: {TARGET_NEW_BADGE_MONTHS} mo before month of latest; "
        f"latest: {latest_date.strftime('%Y-%m')})."
    )
else:
    print(f"News compiled! {len(news_items)} items. NEW badge off (no parseable YYYY-MM dates).")
