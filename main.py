import random
import pandas as pd


def random_with_n_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return random.randint(range_start, range_end)


# read location and
xls = pd.ExcelFile('data_model.xlsx')
location = pd.read_excel(xls, 'Dim_location')
date = pd.read_excel(xls, 'Dim_date')

speciality = ['general', 'Endodontist', 'Orthodontist', 'Periodontist', 'Prosthodontist', 'Oral Medicine']

# define tables dataframes
dentist = pd.DataFrame(columns=['dentist_id', 'name', 'speciality', 'capacity_in_month', 'location_id', 'clinic_name'])
patient = pd.DataFrame(columns=['patient_id', 'name', 'age', 'contact_number', 'location_id'])

# generate dentist table
offset = 10000
for i in range(1, 101):
    dentist_id = str(offset + i)
    contact_number = "09" + str(random_with_n_digits(9))
    age = random.randint(4, 14)
    dentist.add()

# generate final file
with pd.ExcelWriter('output.xlsx') as writer:
    location.to_excel(writer, sheet_name='location')
    date.to_excel(writer, sheet_name='date')
