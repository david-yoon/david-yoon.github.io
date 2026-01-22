import pandas as pd
import os
import sys
import pathlib
cur = pathlib.Path().resolve()

fn = getattr(sys.modules['__main__'], '__file__')
root_path = os.path.abspath(os.path.dirname(fn))
rst_file = os.path.join(root_path, "data_papers.csv")

df = pd.read_csv(rst_file)

item = ""
current_year = 0

cnt_conference = 0
cnt_workshop = 0
cnt_journal = 0
cnt_total = 0
for index, row in df.iterrows():
    if type(row["year"]) == float:
        continue
    cnt_total += 1
    if row["type"] == "conference":
        cnt_conference += 1
    elif row["type"] == "workshop":
        cnt_workshop += 1
    elif row["type"] == "journal":
        cnt_journal += 1

body = ""
body += '''<hr>
<h3 style="color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 5px; display: inline-block;">Publications</h3>
<!--*denotes equal contribution.<br>-->
<style>
  ol.publications {{ counter-reset: item {}; list-style-type: none; }}
  ol.publications > li {{ counter-increment: item -1; }}
  ol.publications > li::before {{ content: "[" counter(item) "] "; font-weight: bold; margin-right: 5px; }}
</style>
<div style="max-height: 500px; overflow-y: auto; padding-right: 10px; border: 1px solid #e0e0e0; border-radius: 5px; background: #fafafa;">

<ol class="publications" style="line-height:1.4em">
  <font size="2">
'''.format(cnt_total + 1)

for index, row in df.iterrows():

    if type(row["year"]) == float:
        continue
    
    # add year
    if current_year != row["year"]:
        item += "  <h4 style=\"color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 5px; margin-top: 20px; margin-left: -10px;\"><strong>[{}]</strong></h4>\n".format(row["year"])
        current_year = row["year"]

    item += "\t<li style=\"margin-left: 0px;\">\n"

    # add title
    item += "\t\t<strong>{}</strong>\n".format(row["title"])

    # add meta info
    if type(row["meta_1"]) != float and str(row["meta_1"]).strip() != "0":
        item += "\t\t<a href=\"{}\">[{}]</a>\n".format(row["meta_1-url"], row["meta_1"])
        print(row["meta_1"])
        
    if type(row["meta_2"]) != float and str(row["meta_2"]).strip() != "0":
        item += "\t\t<a href=\"{}\">[{}]</a>\n".format(row["meta_2-url"], row["meta_2"])
        print(row["meta_2"])
        
    if type(row["meta_3"]) != float and str(row["meta_3"]).strip() != "0":
        item += "\t\t<a href=\"{}\">[{}]</a>\n".format(row["meta_3-url"], row["meta_3"])
        print(row["meta_3"])
        
    if type(row["meta_4"]) != float and str(row["meta_4"]).strip() != "0":
        item += "\t\t<a href=\"{}\">[{}]</a>\n".format(row["meta_4-url"], row["meta_4"])
        print(row["meta_4"])

    # add comment (e.g., oral presentation)
    if type(row["comment"]) != float and str(row["comment"]).strip() != "0":
        item += "\t\t<br><font color=orange>({})</font>\n".format(row["comment"])

    # add authors
    item += "\t\t<br><i>{}</i>\n".format(row["authors"].replace("Seunghyun Yoon", "<u>Seunghyun Yoon</u>").replace("S Yoon", "<u>S Yoon</u>"))

    # add venue
    if type(row["conference"]) != float and str(row["conference"]).strip() != "0":    
        item += "\t\t<br><a href=\"{}\">{}</a>\n".format(row["conference_url"], row["conference"])

    item += "\t\t<p>\n"
    item += "\t</li>\n"


body += item
body += "  </font>\n"
body += "</ol>\n"
body += "</div>\n"

print(body)


output_file = os.path.join(root_path, "papers.txt")


with open(output_file, "w") as f:
    f.write(body)