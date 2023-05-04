#   pip install pandas
#   pip install xlrd
#   pip install openpyxl
import pandas as pd



data = pd.read_excel(r'data\nutrient-file-release2-jan22.xlsx', sheet_name='All solids & liquids per 100g')
#   filter out data that has NAN values 



#   counts unique classifications
class_count = data["Classification"].nunique()
print(f"Number of Unique Food Classifications: {class_count}\n")

#   counts number of different nutrition types/columns
col_count = len(data.columns) - 3
print(f"Number of Different Nutrition Values: {col_count}\n")

#   counts the NaN values across columns - not used currently but can be used to discard columns if needed?
for column in data.columns[3:]:
    len(data[column].value_counts())








#   list of nutrition column names
nutr_cols = list(data.columns[3:])



by_class = pd.DataFrame(columns = data.columns)

#   averages nutritional values for a classification and adds it to  the dataframe
for classification in data.groupby('Classification'):
    c_df = classification[1]

    #   get PFK
    pfk = list(c_df['Public Food Key'])

    #   get food name
    names = list(c_df['Food Name'])
    new_name = set()
    for name in names:
        get_first = name.split(',')[0]
        new_name.add(get_first)
    new_name = ' / '.join(list(new_name))
    
    #   average nutrition values
    c_df = c_df[nutr_cols]
    c_df = c_df.mean(axis=0)

    #   relabel new df, compress redundant info
    c_df['Public Food Key'] = pfk
    c_df['Classification'] = classification[0]
    c_df['Food Name'] = new_name


    by_class.loc[len(by_class)] = c_df
print(by_class)
