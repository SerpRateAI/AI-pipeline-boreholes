import csv
import pandas as pd

def find_between(s, first, last):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

with open("/summarized.csv", 'r') as summarized:
    reader = csv.reader(summarized)
    sum=0
    L=[]
    for row in reader:
        keyline = row[6].split("content",1)[-1]
        print(row[0])
        if "Summary:\\n\\n" in keyline or "Keywords:\\n\\n" in keyline or "Keywords: \\n\\n" in keyline or "Summary: \\n\\n" in keyline:
            wordline=keyline.split(str('\\n\\n'), 2)[1]
            print(wordline)
            print('yep')
        else:
            wordline = keyline.split(str('\\n\\n'), 1)[0]
            print(wordline)

        if "\\n2" in wordline:

            if "Keywords" in wordline:
                keywords=[]
                if "\\n2)" in wordline:
                    for i in range(1,10):
                        keywords.append(find_between(wordline, "\\n"+str(i)+") ", "\\n"+str(i+1)))
                    keywords.append(wordline.split("\\n10) ")[-1])
                else:
                    for i in range(1,10):
                        keywords.append(find_between(wordline, "\\n"+str(i)+". ", "\\n"+str(i+1)))
                    keywords.append(wordline.split("\\n10. ")[-1])
                print(keywords)

            elif "1)" in wordline:
                keywords = []
                keywords.append(find_between(wordline, "1) ", "\\n2"))
                for i in range(2, 10):
                    keywords.append(find_between(wordline, "\\n" + str(i) + ") ", "\\n" + str(i + 1)))
                keywords.append(wordline.split("\\n10) ")[-1])
                print(keywords)

            else:
                keywords = []
                keywords.append(find_between(wordline, "1. ", "\\n2"))
                for i in range(2, 10):
                    keywords.append(find_between(wordline, "\\n" + str(i) + ". ", "\\n" + str(i + 1)))
                keywords.append(wordline.split("\\n10. ")[-1])
                print(keywords)

            if " - " in keywords[0]:
                #Key_pure=[]
                for i in range (10):
                    keywords[i]=keywords[i].split(" - ",1)[0]
                #print(Key_pure)
            if "- " in keywords[0]:
                # Key_pure=[]
                for i in range(10):
                    keywords[i] = keywords[i].split("- ", 1)[0]
                # print(Key_pure)
            if ": " in keywords[0]:
                # Key_pure=[]
                for i in range(10):
                    keywords[i] = keywords[i].split(": ", 1)[0]
                # print(Key_pure)

        else:
            if "2." in wordline:
                keywords = []
                for i in range(1, 10):
                    keywords.append(find_between(wordline, str(i) + ". ", str(i + 1) + ". "))
                keywords.append(wordline.split("10. ")[-1])
                print(keywords)
            elif "2)" in wordline:
                keywords = []
                for i in range(1, 10):
                    keywords.append(find_between(wordline, str(i) + ") ", str(i + 1) + ") "))
                keywords.append(wordline.split("10) ")[-1])
                print(keywords)
            else:
                soon = wordline.split("Keywords", 1)[-1]
                vsoon=soon[2:-1]
                keywords=vsoon.split(',')
                print(keywords)

        for i in range(len(keywords)):
            if keywords[i][0]==' ':
                keywords[i] = keywords[i][1:]
            if keywords[i][-1] == ' ':
                keywords[i] = keywords[i][:-1]

        while len(keywords)<10:
            keywords.append(0)
        print(keywords)

        keywords.append(row[0])

        L.append(keywords)

    print(L)



    name=[x[-1]for x in L]
    keywords_1 = [x[0] for x in L]
    keywords_2 = [x[1] for x in L]
    keywords_3 = [x[2] for x in L]
    keywords_4 = [x[3] for x in L]
    keywords_5 = [x[4] for x in L]
    keywords_6 = [x[5] for x in L]
    keywords_7 = [x[6] for x in L]
    keywords_8 = [x[7] for x in L]
    keywords_9 = [x[8] for x in L]
    keywords_10 = [x[9] for x in L]

    d = {'Line': name, 'Keyword_1': keywords_1, 'Keyword_2': keywords_2,
         'Keyword_3': keywords_3,'Keyword_4': keywords_4,'Keyword_5': keywords_5,
         'Keyword_6': keywords_6,'Keyword_7': keywords_7,'Keyword_8': keywords_8,
         'Keyword_9': keywords_9,'Keyword_10': keywords_10,
         }
    df = pd.DataFrame(data=d)
    df.to_excel("D:/SerpRateAI/Keywords cropped.xlsx")





