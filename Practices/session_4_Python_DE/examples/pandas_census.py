import pandas as pd

# read the CSV file into a pandas DataFrame
df = pd.read_csv('./resources/census-data.csv')

# calculate the average hours-per-week
avg_hours = df['hours-per-week'].mean()
print('Average hours-per-week:', avg_hours)

# calculate the minimum and maximum age
min_age = df['age'].min()
max_age = df['age'].max()
print('Minimum age:', min_age)
print('Maximum age:', max_age)

# create a new DataFrame with the specified columns
new_df = df[['age', 'education', 'native-country', 'salary']]

# homework!
homework_df = df[['age', 'education', 'native-country', 'salary']].copy()

homework_df['age-is-above-21'] = homework_df.apply(lambda row: row['age'] > 21, axis=1)
homework_df['education-salary'] = homework_df.apply(lambda row: f"A person with {row['education']} is having {row['salary']}'education.", axis=1)

# save the new DataFrame to a CSV file
new_df.to_csv('./resources/census_demographics.csv', index=False)
homework_df.to_csv('./resources/homework.csv', index=False)
print('DataFrame saved to census_demographics.csv')