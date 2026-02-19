#columns in a DataFrame are Series onjects, enabling various Operations such as arithmetic operations,filtering and sorting
#df["salary"]=[50000,60000,700000]

#data frames handling Nan (not consideres as the number)
# dropping the rows with the missing values
#df.dropna()
#print(df)
#filling the missing values with a specific value   
#df.fillna(0)
#print(df)
#import pandas as pd
#creating our dataset
#df = pd.DataFrame([[9,4,8,9],[8,10,7,6],[7,6,8,5]], columns=["maths", "english", "science", "social"])
#print(df)
import pandas as pd
df = pd.DataFrame({"maths" : [9,4,8,9],"science" : [8,10,7,6],"social" : [7,6,8,5]})
print(df)
a=df.sum()
b=df.agg(["sum","min","max"])
print(a)
print(b)
import numpy as np
df1 = pd.DataFrame({"maths" : [9,4,8],"science" : [8,10,7,6],"social" : [7,6,8]})
df2 = pd.DataFrame({"maths" : [9,4],"science" : [8,10],"social" : [7,6]})
#comparing the data frame one with data frame two so we are using the alignment
df1_aligned,df2_aligned = df1.align(df2,fill_value=np.nan)
print(df1_aligned)
print(df2_aligned)

import pandas as pd
data={"name": ["Alice", "Bob", "Charlie"], "age": [25, 30, 35]}
df=pd.DataFrame{data,index=["a","b","c"]}
print(df)

import pandas as pd
data={"name": ["Alice", "Bob", "Charlie"], "age": [25, 30, 35]}
df=pd.DataFrame(data,index=["a","b","c"])
#create a new index
new_index=["a","b","e","d"]
#reindex the DataFrame
df_reindexed=df.reindex(new_index)
print(df_reindexed)
data={"name": ["Alice", "Bob", "Charlie"], "age": [25, 30, 35]}
df=pd.DataFrame(data,index=["a","b","c"])
new_index=["a","b","e","d"]
df_reindexed=df.reindex(new_index)
print("..........")
print(df_reindexed)