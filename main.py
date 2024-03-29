import datetime
import random
import re

import pandas as pd


def random_with_n_digits(n):
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return random.randint(range_start, range_end)


# read location and
xls = pd.ExcelFile('data_model.xlsx')
location = pd.read_excel(xls, 'Dim_location')
date = pd.read_excel(xls, 'Dim_date')
services = pd.read_excel(xls, 'Dim_service')

names1 = pd.read_csv("uk-500.csv", usecols=['first_name', 'last_name'])
names2 = pd.read_csv("us-500.csv", usecols=['first_name', 'last_name'])
clinics = pd.read_csv("us-500.csv", usecols=['company_name'])

specialities = ['general', 'Endodontist', 'Orthodontist', 'Periodontist', 'Prosthodontist', 'Oral Medicine']

# define tables dataframes
dentist = pd.DataFrame(
    columns=['dentist_id', 'name', 'contact_number', 'speciality', 'capacity_in_month', 'location_id', 'clinic_name'])
patient = pd.DataFrame(columns=['patient_id', 'name', 'age', 'contact_number', 'location_id'])
fact = pd.DataFrame(
    columns=['fact_id', 'dentist_id', 'patient_id', 'assign_date_id', 'done_date', 'service_id', 'cost'],
    dtype="object")

# generate dentist table
offset1 = 10000
for i in range(1, 101):
    dentist_id = str(offset1 + i)
    contact_number = "09" + str(random_with_n_digits(9))
    first_name = names1['first_name'].loc[names1.index[random.randint(0, len(names1) - 1)]]
    last_name = names1['last_name'].loc[names1.index[random.randint(0, len(names1) - 1)]]
    name = first_name + " " + last_name
    speciality = specialities[random.randint(0, len(specialities) - 1)]
    capacity = random.randint(1, 10)
    location_id = location['Location_id'].loc[location.index[random.randint(0, len(location) - 1)]]
    clinic_name = clinics['company_name'].loc[clinics.index[random.randint(0, len(clinics) - 1)]]
    temp_df = pd.DataFrame(
        [{'dentist_id': dentist_id, 'name': name, 'contact_number': contact_number, 'speciality': speciality,
          'capacity_in_month': capacity,
          'location_id': location_id, 'clinic_name': clinic_name}])
    dentist = pd.concat([dentist, temp_df], ignore_index=True)

print(dentist.shape)
print(dentist.head())

# generate patient table
offset2 = 200000
for i in range(1, 1001):
    patient_id = str(offset2 + i)
    contact_number = "09" + str(random_with_n_digits(9))
    age = random.randint(4, 14)
    first_name = names1['first_name'].loc[names1.index[random.randint(0, len(names1) - 1)]]
    last_name = names1['last_name'].loc[names1.index[random.randint(0, len(names1) - 1)]]
    name = first_name + " " + last_name
    location_id = location['Location_id'].loc[location.index[random.randint(0, len(location) - 1)]]
    clinic_name = clinics['company_name'].loc[clinics.index[random.randint(0, len(clinics) - 1)]]
    temp_df = pd.DataFrame(
        [{'patient_id': patient_id, 'name': name, 'age': age, 'contact_number': contact_number,
          'location_id': location_id}])
    patient = pd.concat([patient, temp_df], ignore_index=True)

print(patient.shape)
print(patient.head())

# generate patient table
offset3 = 1000000
for i in range(1, 3001):
    fact_id = str(offset3 + i)
    dentist_id = str(random.randint(offset1 + 1, offset1 + 100))
    patient_id = str(random.randint(offset2 + 1, offset2 + 1000))
    # assign_date_key = date.index[random.randint(0, len(date) - 1)]
    assign_date_key = date.index[random.randint(0, len(date) - 1)]
    assign_date_id = date['Date_id'].loc[assign_date_key]
    assign_date = date['Date_M'].loc[assign_date_key]
    done_date = assign_date + datetime.timedelta(days=random.randint(3, 25))
    service_id = services['Service_id'].loc[services.index[random.randint(0, len(services) - 1)]]
    cost = str(services['ﻣﺑﻠﻎ ﻧﮭﺎﯾﯽ'].loc[services.index[random.randint(0, len(services) - 1)]])
    regex = r'(\d+)'
    matches = re.findall(regex, cost)
    cost_int = 0
    if matches:
        cost_int = int("".join(matches))
    else:
        pass
    temp_df = pd.DataFrame(
        [{'fact_id': fact_id, 'dentist_id': dentist_id, 'patient_id': patient_id, 'assign_date_id': assign_date_id,
          'done_date': done_date, 'service_id': service_id, 'cost': cost_int}], dtype="object")
    fact = pd.concat([fact, temp_df], ignore_index=True)

print(fact.shape)
print(fact.head())

# generate final file
with pd.ExcelWriter('output.xlsx') as writer:
    location.to_excel(writer, sheet_name='location')
    date.to_excel(writer, sheet_name='date')
    services.to_excel(writer, sheet_name='services')
    dentist.to_excel(writer, sheet_name='dentist')
    patient.to_excel(writer, sheet_name='patient')
    fact.to_excel(writer, sheet_name='fact')
