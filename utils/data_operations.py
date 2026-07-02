import json

def load_data():
    with open('data/students.json') as f:
        data=json.load(f)
        return data
    
def save_data(data):
    with open('data/students.json', 'w') as f:
        json.dump(data, f)
        return {"message": "Data saved successfully"}


