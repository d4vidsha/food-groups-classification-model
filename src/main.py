#   pip install pandas
#   pip install xlrd
#   pip install openpyxl
import pandas as pd
import re
import os

# depending on the OS the path to the data file is different
if os.name == 'nt':
    data = pd.read_excel(r'data\nutrient-file-release2-jan22.xlsx', sheet_name='All solids & liquids per 100g')
elif os.name == 'posix':
    data = pd.read_excel(r'data/nutrient-file-release2-jan22.xlsx', sheet_name='All solids & liquids per 100g')

#   list of nutrition column names
nutr_cols = list(data.columns[3:])



#   counts unique classifications
class_count = data["Classification"].nunique()
print(f"Number of Unique Food Classifications: {class_count}")

#   counts number of different nutrition types/columns
col_count = len(data.columns) - 3
print(f"Number of Different Nutrition Values: {col_count}\n")

#   counts the NaN values across columns - not used currently but can be used to discard columns if needed?
for column in data.columns[3:]:
    len(data[column].value_counts())



#   -------------------------------------------------------------------------------------------------
#   dataframe with food name and attributes separated and processed
sep_attrs = data

#   reg ex
useless_symbols = r'[^-a-z0-9%@\s\\]'
multiple_whitespace = r' +'
###   this can be changed to stopwords but i think words like 'no' are important to keep
conjunctions = ' and| or| with| from'

attrs = []
for i, row in sep_attrs.iterrows():
    food_name = row['Food Name']

    #   casefolds
    food_name = food_name.casefold()

    #   prepares food name for split
    food_name = food_name.replace(',', '@', 1)
    food_name = re.sub(useless_symbols, ' ', food_name)
    food_name = food_name.strip()

    #   split food name from attributes
    name_attr = food_name.split('@', 1)

    #   save name
    sep_attrs.at[i, 'Food Name'] = name_attr[0]

    #   clean attributes and save
    if len(name_attr) > 1:
        attr = name_attr[1]

        #   str to clean list
        attr = re.sub(conjunctions, '', attr)
        attr = re.sub(multiple_whitespace, ' ', attr)
        attr = attr.strip()
        attr = attr.split(' ')
        attr = [x.strip() for x in attr]

        attrs.append(attr)
    else:
        attrs.append('None')

#   adds attributes to df
sep_attrs.insert(3, 'Attribute', attrs)

###   saves to excel file for easier viewing (temp for convenience)
file_name = 'sep_attrs.xlsx'
sep_attrs.to_excel(file_name)




#   -------------------------------------------------------------------------------------------------
#   dataframe that averages nutrition values by classification
by_class = pd.DataFrame(columns = data.columns)
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

