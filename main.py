import random

import pandas as pd


def random_with_n_digits(n):
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return random.randint(range_start, range_end)


# read location and
xls = pd.ExcelFile('data_model.xlsx')
location = pd.read_excel(xls, 'Dim_location')
date = pd.read_excel(xls, 'Dim_date')

names1 = pd.read_csv("uk-500.csv", usecols=['first_name', 'last_name'])
names2 = pd.read_csv("us-500.csv", usecols=['first_name', 'last_name'])
clinics = pd.read_csv("us-500.csv", usecols=['company_name'])

specialities = ['general', 'Endodontist', 'Orthodontist', 'Periodontist', 'Prosthodontist', 'Oral Medicine']

# define tables dataframes
dentist = pd.DataFrame(columns=['dentist_id', 'name', 'speciality', 'capacity_in_month', 'location_id', 'clinic_name'])
patient = pd.DataFrame(columns=['patient_id', 'name', 'age', 'contact_number', 'location_id'])

# generate dentist table
offset = 10000
for i in range(1, 101):
    dentist_id = str(offset + i)
    contact_number = "09" + str(random_with_n_digits(9))
    age = random.randint(4, 14)
    first_name = names1['first_name'].loc[names1.index[random.randint(0, len(names1) - 1)]]
    last_name = names1['last_name'].loc[names1.index[random.randint(0, len(names1) - 1)]]
    name = first_name + " " + last_name
    speciality = specialities[random.randint(0, len(specialities) - 1)]
    capacity = random.randint(1, 10)
    location_id = location['Location_id'].loc[location.index[random.randint(0, len(location) - 1)]]
    clinic_name = clinics['company_name'].loc[clinics.index[random.randint(0, len(clinics) - 1)]]
    temp_df = pd.DataFrame(
        [{'dentist_id': dentist_id, 'name': name, 'speciality': dentist, 'capacity_in_month': capacity,
          'location_id': location_id, 'clinic_name': clinic_name}])
    dentist = pd.concat([dentist, temp_df], ignore_index=True)

print(dentist.head())

# generate final file
# with pd.ExcelWriter('output.xlsx') as writer:
#     location.to_excel(writer, sheet_name='location')
#     date.to_excel(writer, sheet_name='date')
