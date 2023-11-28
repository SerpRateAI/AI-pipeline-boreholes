import pandas as pd
import csv

with open("D:\SerpRateAI\Keywords mod.csv", 'r') as summarized:
    L=[]
    reader = csv.reader(summarized)
    for row in reader:
        print(row[3:])
        L.append(row[3:])

    print(L)

    Count=[]

    for i in range(len(L)):
        for l in range(len(L[i])):
            L[i][l]=L[i][l].capitalize()
            if 'Carb' in L[i][l]:
                L[i][l]='Carbonate veins'

            elif 'Black' in L[i][l]:
                L[i][l] = 'Black serpentinization'

            elif 'Irregular' in L[i][l]:
                L[i][l] = 'Irregular'

            elif 'Blue' in L[i][l]:
                L[i][l] = 'Blue patches'

            elif 'Green' in L[i][l]:
                L[i][l] = 'Green veins'

            elif 'White' in L[i][l]:
                L[i][l] = 'White veins'

            elif 'Lineation' in L[i][l]:
                L[i][l] = 'Lineation'

            elif 'Striation' in L[i][l]:
                L[i][l] = 'Striations'

            elif 'Px' in L[i][l]:
                L[i][l]='Pxenites'

            elif 'Plag' in L[i][l]:
                L[i][l]='Plagioclase'

            elif 'Ox' in L[i][l] or 'Oxidation' in L[i][l]:
                L[i][l] = 'Oxidation'

            elif 'Hydrothermal' in L[i][l]:
                L[i][l]='Hydrothermal'

            elif 'Gabbro' in L[i][l] or 'gabbroic' in L[i][l]:
                L[i][l]='Gabbro'

            elif 'Harzburgite' in L[i][l] or 'Harz' in L[i][l] or 'Harzb' in L[i][l]:
                L[i][l]='Harzburgite'

            elif 'Harzburgite' in L[i][l] or 'Harz' in L[i][l] or 'Harzb' in L[i][l]:
                L[i][l]='Harzburgite'

            elif 'Crosscutting' in L[i][l] or 'Crosscut' in L[i][l] or 'Cross-cutting' in L[i][l]:
                L[i][l] = 'Veins'

            elif 'Subvertical' in L[i][l] or 'Sub-vertical' in L[i][l]:
                L[i][l] = 'Subvertical'

            elif 'Subhorizontal' in L[i][l] or 'Sub-horizontal' in L[i][l]:
                L[i][l] = 'Subhorizontal'

            elif 'Fine' in L[i][l]:
                L[i][l]='Fine grained'


            elif 'dyke' in L[i][l] or 'Dyke' in L[i][l]:
                L[i][l]='Dyke'

            elif 'Serp' in L[i][l]:
                L[i][l]='Serpentine vein'


            elif 'Vein' in L[i][l] or 'Veins' in L[i][l]:
                L[i][l] = 'Veins'

            elif '0' in L[i][l] or L[i][l]==0:
                L[i][l] = None


    for i in range(len(L)):
        for l in range(len(L[i])):
            count=0
            for j in range(len(L)):
                for k in range(len(L[j])):
                    if L[i][l]==L[j][k]:
                        count+=1
            if count<=10:
                L[i][l]=0

    for i in range(len(L)):
        for l in range(len(L[i])):
            if L[i][l] not in Count:
                Count.append(L[i][l])

    print(Count)
    print(len(Count))

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

    d = {'Keyword_1': keywords_1, 'Keyword_2': keywords_2,
         'Keyword_3': keywords_3, 'Keyword_4': keywords_4, 'Keyword_5': keywords_5,
         'Keyword_6': keywords_6, 'Keyword_7': keywords_7, 'Keyword_8': keywords_8,
         'Keyword_9': keywords_9, 'Keyword_10': keywords_10,
         }

    df = pd.DataFrame(data=d)
    df = pd.get_dummies(data=df, columns=['Keyword_1', 'Keyword_2', 'Keyword_3', 'Keyword_4', 'Keyword_5', 'Keyword_6', 'Keyword_7', 'Keyword_8', 'Keyword_9', 'Keyword_10'])

    df.drop(columns=['Keyword_1_0', 'Keyword_2_0', 'Keyword_3_0', 'Keyword_4_0', 'Keyword_5_0', 'Keyword_6_0', 'Keyword_7_0',
                         'Keyword_8_0', 'Keyword_9_0', 'Keyword_10_0'],
                inplace=True)

    for keyword in Count[2:]:
        print(keyword)
        cols=[]
        #print(df.columns)
        for i in range(1,11):
            if 'Keyword_'+str(i)+'_'+keyword in df.columns:
                cols.append('Keyword_'+str(i)+'_'+keyword)
        print(cols)
        df[keyword] = df[cols].max(1)
        df = df.drop(cols, 1)

    df = df.iloc[1:]

    df.to_excel("D:/SerpRateAI/Keywords cropped.xlsx")