from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from schema.pydantic import Students,UpdateStudent
from utils.data_operations import load_data,save_data
app=FastAPI()

PYDANTIC_VERSION='1.0.0'

# total marks will be calculated based on the marks obtained in each subject
@app.get('/')
def home():
    return {"message": "Welcome to the Student API"}

@app.get('/all_students')
def all_students():
    data=load_data()
    return data

@app.get('/health')
def health():
    return {'Status': 'OK','version':PYDANTIC_VERSION}

@app.get("/all_students/{student_id}")
def get_student(student_id:str):
    data=load_data()
    
    if student_id not in data:
        raise HTTPException(status_code=404, detail="Student not found")
    return Students(id=student_id, **data[student_id])

@app.post("/create_student")
def create_student(student:Students):
    data=load_data()

    if student.id in data:
        raise HTTPException(status_code=400, detail="Student already exists")
    
    data[student.id]=student.model_dump(exclude=['id'],)
    save_data(data)
    return JSONResponse(content={"message": "Student created successfully"}, status_code=201)

@app.put('/update_student/{student_id}')
def update_student(student_id:str,update_data:UpdateStudent):
    data=load_data()
    if student_id not in data:
        raise HTTPException(status_code=404, detail="Student not found")
    
    existing_student_info=data[student_id]
    updated_student_info=update_data.model_dump(exclude_unset=True) # takes pydantic object and converts into dict

    for key,value in updated_student_info.items():
        existing_student_info[key]=value

    # existing_student_info -> pydantic object -> updated total marks + grade -> dict -> save to json
    existing_student_info['id']=student_id
    student_pydantic_object = Students(**existing_student_info) # takes dict and converts in to a pydantic object

    # pydantic object -> dict (exclude id) -> save to json
    existing_student_info = student_pydantic_object.model_dump(exclude=['id'])

    # add this dict to data
    data[student_id]=existing_student_info

    #save data
    save_data(data)

    data[student_id]=existing_student_info    
    return JSONResponse(content={"message": "Student updated successfully"}, status_code=200)

@app.delete('/delete_student/{student_id}')
def delete_student(student_id:str):
    data=load_data()
    if student_id not in data:
        raise HTTPException(status_code=404, detail="Student not found")
    
    del data[student_id]
    save_data(data)
    return JSONResponse(content={"message": "Student deleted successfully"}, status_code=200)
