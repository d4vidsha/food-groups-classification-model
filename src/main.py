import pandas as pd
import re
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import PCA
from sklearn.preprocessing import Normalizer
from sklearn.preprocessing import StandardScaler
import seaborn as sns
import matplotlib.pyplot as plt

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
sep_attrs = data.copy()

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
        # attr = attr.split(' ')
        # attr = [x.strip() for x in attr]

        attrs.append(attr)
    else:
        attrs.append('None')

#   adds attributes to df
sep_attrs.insert(3, 'Attribute', attrs)

# ###   saves to excel file for easier viewing (temp for convenience)
# file_name = 'sep_attrs.xlsx'
# sep_attrs.to_excel(file_name)



#   -------------------------------------------------------------------------------------------------
#   dataframe that averages nutrition values by classification
by_class = pd.DataFrame(columns = data.columns)
bows = []
for classification in data.groupby('Classification'):
    c_df = classification[1]

    #   get PFK
    pfk = list(c_df['Public Food Key'])

    #   get food name   - info not in use, can be depreciated if not used by end 
    names = list(c_df['Food Name'])
    new_name = set()
    for name in names:
        get_first = name.split(',')[0]
        new_name.add(get_first)
    new_name = ' / '.join(list(new_name))
    
    #   get cleaned bow
    bow = ' '.join([x for x in names])
    bow = bow.casefold()
    bow = re.sub(useless_symbols, ' ', bow)
    bow = bow.strip()
    bow = re.sub(multiple_whitespace, ' ', bow)
    bows.append(bow)

    #   average nutrition values
    c_df = c_df[nutr_cols]
    c_df = c_df.mean(axis=0)

    #   relabel new df, compress redundant info
    c_df['Public Food Key'] = pfk
    c_df['Classification'] = classification[0]
    c_df['Food Name'] = new_name


    by_class.loc[len(by_class)] = c_df


#   concats dataframes (adds bow to by_class)
bow_df = pd.DataFrame(bows, columns=['Bag of Words'])


#   -------------------------------------------------------------------------------------------------
#   performs pca on bow by classification



#   count vectorizer intialise
vectoriser = CountVectorizer()
attr_vector = vectoriser.fit_transform(bow_df['Bag of Words'])

#   normaliser
norm = Normalizer('max')
norm.fit(attr_vector)
norm_attr_vector = norm.transform(attr_vector)


#   pca
pca = PCA(n_components=6)
bow_pca = pca.fit_transform(norm_attr_vector.toarray())

#   save pca values of bow
# bow_pca['Group 0']  = [x[0] for x in bow_pca.tolist()]
# bow_pca['Group 1']  = [x[1] for x in bow_pca.tolist()]
# bow_pca['Group 2']  = [x[2] for x in bow_pca.tolist()]
# bow_pca['Group 3']  = [x[3] for x in bow_pca.tolist()]
# bow_pca['Group 4']  = [x[4] for x in bow_pca.tolist()]
# bow_pca['Group 5']  = [x[5] for x in bow_pca.tolist()]


#   get some cols of nutr vals
columns = ['Energy with dietary fibre, equated \n(kJ)', 'Energy, without dietary fibre, equated \n(kJ)', 'Moisture (water) \n(g)', 'Protein \n(g)', 'Nitrogen \n(g)', 'Fat, total \n(g)']
nutr_df = by_class[columns].copy()

#   scale data
scaler = StandardScaler()
scaled_num = scaler.fit_transform(nutr_df[columns])

#   pca
pca = PCA(n_components=6)
nutr_pca = pca.fit_transform(scaled_num)

#   concat nutr and bow data
pca_df = pd.concat([pd.DataFrame(bow_pca).add_suffix('b'), pd.DataFrame(nutr_pca).add_suffix('n')], axis=1)

pca_df['Group 0'] = pca_df[['0b', '0n']].mean(axis=1)
pca_df['Group 1'] = pca_df[['1b', '1n']].mean(axis=1)
pca_df['Group 2'] = pca_df[['2b', '2n']].mean(axis=1)
pca_df['Group 3'] = pca_df[['3b', '3n']].mean(axis=1)
pca_df['Group 4'] = pca_df[['4b', '4n']].mean(axis=1)
pca_df['Group 5'] = pca_df[['5b', '5n']].mean(axis=1)

pca_df['Food Name'] = by_class['Food Name'].copy()

file = 'pca.xlsx'
pca_df.to_excel(file)


# 6x6 subplots (temp and messy)
fig, axes = plt.subplots(nrows=5, ncols=5, figsize=(20, 20,))
sns.scatterplot(x=pca_df['Group 0'], y=pca_df['Group 1'], hue=pca_df['Food Name'], ax=axes[0, 0], legend=False)
sns.scatterplot(x=pca_df['Group 0'], y=pca_df['Group 2'], hue=pca_df['Food Name'], ax=axes[0, 1], legend=False)
sns.scatterplot(x=pca_df['Group 0'], y=pca_df['Group 3'], hue=pca_df['Food Name'], ax=axes[0, 2], legend=False)
sns.scatterplot(x=pca_df['Group 0'], y=pca_df['Group 4'], hue=pca_df['Food Name'], ax=axes[0, 3], legend=False)
sns.scatterplot(x=pca_df['Group 0'], y=pca_df['Group 5'], hue=pca_df['Food Name'], ax=axes[0, 4], legend=False)

sns.scatterplot(x=pca_df['Group 1'], y=pca_df['Group 0'], hue=pca_df['Food Name'], ax=axes[1, 0], legend=False)
sns.scatterplot(x=pca_df['Group 1'], y=pca_df['Group 2'], hue=pca_df['Food Name'], ax=axes[1, 1], legend=False)
sns.scatterplot(x=pca_df['Group 1'], y=pca_df['Group 3'], hue=pca_df['Food Name'], ax=axes[1, 2], legend=False)
sns.scatterplot(x=pca_df['Group 1'], y=pca_df['Group 4'], hue=pca_df['Food Name'], ax=axes[1, 3], legend=False)
sns.scatterplot(x=pca_df['Group 1'], y=pca_df['Group 5'], hue=pca_df['Food Name'], ax=axes[1, 4], legend=False)

sns.scatterplot(x=pca_df['Group 2'], y=pca_df['Group 0'], hue=pca_df['Food Name'], ax=axes[2, 0], legend=False)
sns.scatterplot(x=pca_df['Group 2'], y=pca_df['Group 1'], hue=pca_df['Food Name'], ax=axes[2, 1], legend=False)
sns.scatterplot(x=pca_df['Group 2'], y=pca_df['Group 3'], hue=pca_df['Food Name'], ax=axes[2, 2], legend=False)
sns.scatterplot(x=pca_df['Group 2'], y=pca_df['Group 4'], hue=pca_df['Food Name'], ax=axes[2, 3], legend=False)
sns.scatterplot(x=pca_df['Group 2'], y=pca_df['Group 5'], hue=pca_df['Food Name'], ax=axes[2, 4], legend=False)

sns.scatterplot(x=pca_df['Group 3'], y=pca_df['Group 0'], hue=pca_df['Food Name'], ax=axes[3, 0], legend=False)
sns.scatterplot(x=pca_df['Group 3'], y=pca_df['Group 1'], hue=pca_df['Food Name'], ax=axes[3, 1], legend=False)
sns.scatterplot(x=pca_df['Group 3'], y=pca_df['Group 2'], hue=pca_df['Food Name'], ax=axes[3, 2], legend=False)
sns.scatterplot(x=pca_df['Group 3'], y=pca_df['Group 4'], hue=pca_df['Food Name'], ax=axes[3, 3], legend=False)
sns.scatterplot(x=pca_df['Group 3'], y=pca_df['Group 5'], hue=pca_df['Food Name'], ax=axes[3, 4], legend=False)

sns.scatterplot(x=pca_df['Group 4'], y=pca_df['Group 0'], hue=pca_df['Food Name'], ax=axes[4, 0], legend=False)
sns.scatterplot(x=pca_df['Group 4'], y=pca_df['Group 1'], hue=pca_df['Food Name'], ax=axes[4, 1], legend=False)
sns.scatterplot(x=pca_df['Group 4'], y=pca_df['Group 2'], hue=pca_df['Food Name'], ax=axes[4, 2], legend=False)
sns.scatterplot(x=pca_df['Group 4'], y=pca_df['Group 3'], hue=pca_df['Food Name'], ax=axes[4, 3], legend=False)
sns.scatterplot(x=pca_df['Group 4'], y=pca_df['Group 5'], hue=pca_df['Food Name'], ax=axes[4, 4], legend=False)

# adjust spacing between subplots
plt.subplots_adjust(wspace=0.4, hspace=0.4)

# show plot
plt.show()

