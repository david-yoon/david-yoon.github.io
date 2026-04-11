import csv
import os
import sys
from datetime import datetime

# Get script directory
fn = getattr(sys.modules['__main__'], '__file__')
root_path = os.path.abspath(os.path.dirname(fn))

# Read the data file
data_file = os.path.join(root_path, "data_news.csv")
with open(data_file, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    news_items = list(reader)

# print(news_items)


# Find the latest news entry date as the base date
def parse_date(date_str):
    """Parse date format like 'Jan-26' (Month abbreviation + 2-digit year)"""
    # """Parse date format like '26-Jan' (Month abbreviation + 2-digit year)"""
    try:
        return datetime.strptime(date_str.strip(), "%b-%y")
    except:
        return datetime.min

latest_date = max(parse_date(item["date"]) for item in news_items)

# Calculate N months before the latest entry
month = latest_date.month - 3
year = latest_date.year
if month <= 0:
    month += 12
    year -= 1
n_months_ago = datetime(year, month, 1)

# NEW badge HTML
NEW_BADGE = '<span style="background:rgb(246, 112, 97); color: white; padding: 2px 8px; border-radius: 10px; font-size: 11px; font-weight: bold;">NEW</span>'

def is_within_6_months(date_str):
    """Check if the date has NOT passed 4 months (is recent)"""
    try:
        # Parse date format like "Jan-26" (Month abbreviation + 2-digit year)
        entry_date = datetime.strptime(date_str, "%b-%y")
        return entry_date >= n_months_ago
    except:
        return False

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
    
    # Add NEW badge if within 6 months
    if is_within_6_months(date):
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

print(f"News compiled! {len(news_items)} items. NEW badge for entries after {n_months_ago.strftime('%m/%Y')} (based on latest entry: {latest_date.strftime('%b-%y')}).")
