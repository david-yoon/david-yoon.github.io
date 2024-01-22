import pandas as pd
import pathlib
cur = pathlib.Path().resolve()

df = pd.read_csv(str(cur) + "/data_papers.csv")

body = ""
body += '''<hr>
<h3>Publications</h3>
<!--*denotes equal contribution.<br>-->
<ol style="line-height:1.4em" reversed>
  <font size="2">
'''

item = ""

current_year = 0

for index, row in df.iterrows():

    if type(row["year"]) == float:
        continue
    
    # add year
    if current_year != row["year"]:
        item += "  <h4><strong>[{}]</strong></h4>\n".format(row["year"])
        current_year = row["year"]

    item += "\t<li>\n"

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

print(body)


with open("papers.txt", "w") as f:
    f.write(body)