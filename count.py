import re
import os
import json
import csv
import regex as re

def count_function_usage(dir_path, function_forms):
    total_count = -1
    for root, _, files in os.walk(dir_path):
        for file_name in files:
            if file_name.endswith('.scala'):
                file_path = os.path.join(root, file_name)
                with open(file_path, 'r') as file:
                    content = file.read()
                    # Using regex to find occurrences of the function name
                    # count = len(re.findall(r'\b{}\('.format(function_name), content))

                    for form in function_forms:
                        count = len(re.findall(form, content))
                        total_count += count

                        # if count > 0 and function_name.find('applicableParties') != -1:
                        #     print(f"File: {file_path}, Occurrences of '{form}': {count}, Total {total_count}")

    # if function_forms[0].find('applicableParties') != -1:
        # print(f"File: {file_path}, Occurrences of '{function_name}': {count}")
        # print(f"Total occurrences of '{function_name}' in Scala files: {total_count}")
    return total_count

def get_function_names_scala(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    # Regular expression pattern to match Scala function definitions
    # pattern = r'(?<!private\s|protected\s)(?<!private\[|protected\[)def\s+([a-zA-Z0-9_]+)\s*\([^)]*\)\s*(:\s*\w+\s*)?=?\s*{?'
    pattern = r'def\s+([a-zA-Z0-9_]+)\s*\([^)]*\)\s*(:\s*\w+\s*)?=?\s*{?'
    # bye private
    # pattern = r'(?<!private\s|protected\s)(?<!private\[|protected\[)def\s+(\w+)\s*\([^)]*\)\s*(:\s*\w+\s*)?=?\s*{?'
    
    # Find all function names using the regex pattern
    function_names = re.findall(pattern, content)

    return [x[0] for x in function_names]

file_path = '/Users/tienvu/sandbox/asana/asana2/lunadb/src/main/scala/com/asana/lunadb/servercomputed/objectmodels/objectmodelshelpers/BillableGroupHelpers.scala'
# file_path = '/Users/tienvu/sandbox/asana/asana2/lunadb/src/main/scala/com/asana/lunadb/servercomputed/premiumfeatureframework/FeatureAvailabilityApi.scala'
# file_path = '/Users/tienvu/sandbox/asana/asana2/lunadb/src/main/scala/com/asana/lunadb/servercomputed/premiumfeatureframework/LicensingApi.scala'
functions = get_function_names_scala(file_path)
# print(functions)

paths = [
    '/Users/tienvu/sandbox/asana/asana2/lunadb/src/main/scala/com/asana/lunadb/servercomputed/objectmodels/objectmodelshelpers/BillableGroupHelpers.scala',
    '/Users/tienvu/sandbox/asana/asana2/lunadb/src/main/scala/com/asana/lunadb/servercomputed/premiumfeatureframework/FeatureAvailabilityApi.scala',
    '/Users/tienvu/sandbox/asana/asana2/lunadb/src/main/scala/com/asana/lunadb/servercomputed/premiumfeatureframework/LicensingApi.scala'
]

directory_path = '/Users/tienvu/sandbox/asana/asana2/lunadb/src/main/scala/com/asana/lunadb/servercomputed'
counter = {}

for path in paths:
    functions = get_function_names_scala(path)
    file_name = path.split('.')[0].split('/')[-1]

    for function_name in functions:
        # count_this_func = count_function_usage(directory_path, f'BillableGroupHelpers.{function}')
        # count_this_func = count_function_usage(directory_path, [f'\.{function_name}', f'{function_name}\('])
        count_this_func = count_function_usage(directory_path, [f'{function_name}\('])
        # count_this_func_2 = count_function_usage(directory_path, f'{function_name}\(')
        counter[f'{file_name}.{function_name}'] = count_this_func

sorted_dict = dict(sorted(counter.items(), key=lambda x: -x[1]))

def write_to_csv(some_dict):
    file_path = 'counter.csv'

    # Writing dictionary to CSV
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Function name', '# referenced'])  # Write header row
        for key, value in some_dict.items():
            writer.writerow([key, value])

write_to_csv(sorted_dict)

# print(json.dumps(sorted_dict, indent=2))