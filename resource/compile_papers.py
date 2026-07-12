import pandas as pd
import os
import sys
import pathlib
cur = pathlib.Path().resolve()

fn = getattr(sys.modules['__main__'], '__file__')
root_path = os.path.abspath(os.path.dirname(fn))
rst_file = os.path.join(root_path, "data_papers.xls")

df = pd.read_excel(rst_file, dtype=str).fillna("")


def _has_year(y):
    """True if row has a non-empty year (Excel uses strings; CSV may use NaN)."""
    if y is None:
        return False
    if isinstance(y, float) and pd.isna(y):
        return False
    return bool(str(y).strip())


def _cell_active(val):
    """Non-empty optional cell; '0' means omitted."""
    if isinstance(val, float) and pd.isna(val):
        return False
    s = str(val).strip()
    return bool(s) and s != "0"


item = ""
current_year = 0

cnt_total = sum(1 for _, row in df.iterrows() if _has_year(row["year"]))

body = ""
body += '''<hr>
<h3 style="color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 5px; display: inline-block;">Publications</h3>
<!--*denotes equal contribution.<br>-->
<style>
  ol.publications {{ counter-reset: item {}; list-style-type: none; }}
  ol.publications > li {{ counter-increment: item -1; }}
  ol.publications > li::before {{ content: "[" counter(item) "] "; font-weight: bold; margin-right: 5px; }}
</style>
<div style="max-height: 450px; overflow-y: auto; padding-right: 10px; border: 1px solid #e0e0e0; border-radius: 5px; background: #fafafa;">

<ol class="publications" style="line-height:1.4em">
  <font size="2">
'''.format(cnt_total + 1)

for index, row in df.iterrows():

    if not _has_year(row["year"]):
        continue

    if current_year != row["year"]:
        item += (
            "  <h4 style=\"color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 5px; margin-top: 20px; margin-left: -10px;\">"
            "<strong>[{}]</strong></h4>\n"
        ).format(row["year"])
        current_year = row["year"]

    item += "\t<li style=\"margin-left: 0px;\">\n"

    # add title
    item += "\t\t<strong>{}</strong>\n".format(row["title"])

    # add meta info
    if _cell_active(row["meta_1"]):
        item += "\t\t<a href=\"{}\">[{}]</a>\n".format(row["meta_1-url"], row["meta_1"])
        # print(row["meta_1"])
        
    if _cell_active(row["meta_2"]):
        item += "\t\t<a href=\"{}\">[{}]</a>\n".format(row["meta_2-url"], row["meta_2"])
        # print(row["meta_2"])
        
    if _cell_active(row["meta_3"]):
        item += "\t\t<a href=\"{}\">[{}]</a>\n".format(row["meta_3-url"], row["meta_3"])
        # print(row["meta_3"])
        
    if _cell_active(row["meta_4"]):
        item += "\t\t<a href=\"{}\">[{}]</a>\n".format(row["meta_4-url"], row["meta_4"])
        # print(row["meta_4"])

    # add comment (e.g., oral presentation)
    if _cell_active(row["comment"]):
        item += "\t\t<br><font color=red>({})</font>\n".format(row["comment"])

    # add authors
    item += "\t\t<br><i>{}</i>\n".format(row["authors"].replace("Seunghyun Yoon", "<u>Seunghyun Yoon</u>").replace("S Yoon", "<u>S Yoon</u>"))

    # add venue
    if _cell_active(row["conference"]):    
        item += "\t\t<br><a href=\"{}\" style=\"font-weight: bold;\">{}</a>\n".format(row["conference_url"], row["conference"])

    item += "\t\t<p>\n"
    item += "\t</li>\n"

body += item
body += "  </font>\n"
body += "</ol>\n"
body += "</div>\n"

# print(body)


output_file = os.path.join(root_path, "papers.txt")


with open(output_file, "w") as f:
    f.write(body)

print(f"Publications compiled! {cnt_total} papers written to papers.txt.")