file_name =  "C:\\Users\\Yunus\\Desktop\\GraphS\\temp.xls"




import pandas as pd

try:
    df = pd.read_excel(file_name)
except :
    print("Can not find")


a = list(df)

result = []
i = "Month"
j = "rainfall"

b = df[[i, j]].groupby([i]).agg(['count'])


for name in b.index:
    print (name)
    print (b.loc[name][0])
# for index, row in b.iterrows():
#     print(row[i], row['mean'])
     #result.append([row[i], row[j]])




#print(df[[a[0], a[2]]].groupby([a[0]]).agg(['mean', 'count']))

#print(df.groupby(a[0]).size()) #Count operation
