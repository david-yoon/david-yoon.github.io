import pandas as pd
import pathlib
cur = pathlib.Path().resolve()

df = pd.read_excel(str(cur) + "/data_patents.xls", dtype=str).fillna("")

type_patent = ""
item = ""
body = ""
body += '''<hr>
<h3 style="color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 5px; display: inline-block;">Patents</h3>
<div style="max-height: 300px; overflow-y: auto; padding-right: 10px; border: 1px solid #e0e0e0; border-radius: 5px; background: #fafafa;">
'''

for index, row in df.iterrows():
    try:
        if type_patent != row["Type"]:
            
            # first case
            if type_patent != "":
                item += "  </font>\n"
                item += "</ol>\n"
            
            type_patent = row["Type"]
                    
            item += "<font color=lightblue>\n"
            
            item += "  <h4 style=\"color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 5px; margin-top: 20px; margin-left: 15px;\"><strong>[{}]</strong></h4>\n".format(row["Type"])
            
            # item += "  <h4>[ {} ]</h4>\n".format(row["Type"])
            item += "</font>\n"
            item += "<ol reversed style=\"line-height:1.4em\">\n"
            item += "<font size=\"2\">"
    
        item += "\t<li style=\"margin-left: 15px;\">\n"
    
        # add issue
        if str(row["issued"]) == "1":
            item += "\t<span style=\"background: linear-gradient(135deg, #3498db, #2980b9); color: white; padding: 2px 10px; border-radius: 12px; font-size: 11px; font-weight: bold; margin-right: 8px;\">ISSUED</span>"
    
        # add title
        item += "<strong>{}</strong>\n".format(row["title"])
        # print(row["title"])
    
        # add meta info
        if type(row["meta_1"]) != float and str(row["meta_1"]).strip() != "0":
            item += "\t\t<a href=\"{}\">[{}]</a>\n".format(row["meta_1-url"], row["meta_1"])        
    
        # add authors    
        item += "\t\t<br><i>{}</i>\n".format(row["authors"].replace("Seunghyun Yoon", "<u>Seunghyun Yoon</u>").replace("S Yoon", "<u>S Yoon</u>"))
        
        # add number and date
        item += "\t\t<br>{}, {}\n".format(row["number"].strip(), row["date"].strip())
    
        item += "\t\t<p>\n"
        item += "\t</li>\n"
        
    except:
        continue;


body += item
body += "  </font>\n"
body += "</ol>\n"
body += "</div>\n"


# print(body)


with open("patents.txt", "w") as f:
    f.write(body)

print(f"Patents compiled! {len(df)} rows written to patents.txt.")