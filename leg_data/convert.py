import json
import uuid

input_file_path = 'leg.txt' 
output_file_path = 'data.json'

# Read the data from the file
def read_data(file_path):
    with open(file_path, 'r') as file:
        data_blocks = file.read().strip().split('\n\n')  
        data_list = []
        for block in data_blocks:
            exercise_data = {'id': str(uuid.uuid4())}  
            for line in block.split('\n'):
                if line:
                    key, value = line.split(': ', 1)
                    exercise_data[key.strip()] = value.strip()
            data_list.append(exercise_data)
        return data_list


def save_to_json(data, output_path):
    with open(output_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

# Main execution
exercise_data = read_data(input_file_path)
save_to_json(exercise_data, output_file_path)
