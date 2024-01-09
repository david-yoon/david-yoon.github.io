import pandas as pd
import pathlib
cur = pathlib.Path().resolve()

# df = pd.read_csv(str(cur) + "/resource/data_patents.csv")
df = pd.read_csv(str(cur) + "/data_patents.csv")

type_patent = ""
item = ""
body = ""
body += '''<hr>
<h3>Patents</h3>
'''

for index, row in df.iterrows():
    
    if type_patent != row["Type"]:
        
        # first case
        if type_patent != "":
            item += "  </font>\n"
            item += "</ol>\n"
        
        type_patent = row["Type"]
                
        item += "<font color=lightblue>\n"
        item += "  <h4>[ {} ]</h4>\n".format(row["Type"])
        item += "</font>\n"
        item += "<ol reversed style=\"line-height:1.4em\">"
        item += "<font size=\"2\">"

    item += "\t<li>\n"

    # add issue
    if str(row["issued"]) == "1":
        item += "\t\t[<font color=magenta>issued</font>]"

    # add title
    item += "\t\t<strong>{}</strong>\n".format(row["title"])
    print(row["title"])

    # add meta info
    if type(row["meta_1"]) != float and str(row["meta_1"]).strip() != "0":
        item += "\t\t<a href=\"{}\">[{}]</a>\n".format(row["meta_1-url"], row["meta_1"])        

    # add authors
    item += "\t\t<br><i>{}</i>\n".format(row["authors"].replace("Seunghyun Yoon", "<u>Seunghyun Yoon</u>").replace("S Yoon", "<u>S Yoon</u>"))
    
    # add number and date
    item += "\t\t<br>{}, {}\n".format(row["number"].strip(), row["date"].strip())

    item += "\t\t<p>\n"
    item += "\t</li>\n"


body += item
body += "  </font>\n"
body += "</ol>\n"

# print(body)


with open("patents.txt", "w") as f:
    f.write(body)