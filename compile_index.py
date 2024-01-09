

target_data = ["./resource/into.txt",
               "./resource/bio.txt",
               "./resource/news.txt",
               "./resource/academy.txt",
               "./resource/professional.txt",
               "./resource/papers.txt",
               "./resource/patents.txt",
               ]


main = ""

for file in target_data:

    with open(file, "r") as f:
        data = f.readlines()
    
    for item in data:
        main += item
    
    
with open("./index.html", "w") as f:
    f.write(main)

print(main)