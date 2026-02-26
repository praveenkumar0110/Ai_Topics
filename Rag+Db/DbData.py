from pymongo import MongoClient
import random

client = MongoClient("mongodb://localhost:27017/")
db = client["RAGcompanyDB"]
collection = db["employees"]

# 100 unique names
names = [
"Aarav","Aditya","Akash","Amit","Anand","Arjun","Arun","Ashwin","Balaji","Bharath",
"Chandru","Deepak","Dinesh","Divakar","Eshwar","Gokul","Hari","Harish","Hemanth","Jagan",
"Jeeva","Karthik","Kiran","Kishore","Lokesh","Mahesh","Manoj","Mithun","Naveen","Nithin",
"Prabhu","Pradeep","Prakash","Pranav","Praveen","Rahul","Rajesh","Rakesh","Ravi","Rohit",
"Sachin","Sanjay","Sarath","Senthil","Shankar","Siddharth","Siva","Srikanth","Sriram","Suresh",
"Tarun","Uday","Varun","Vasanth","Venkatesh","Vignesh","Vijay","Vinod","Vishal","Yash",
"Ajay","Anil","Aravind","Bala","Chaitanya","Darshan","Dharani","Girish","Irfan","Jayant",
"Kamal","Kumar","Madhan","Naresh","Naren","Nikhil","Pavan","Raghu","Ranjith","Rishi",
"Ritesh","Rohan","Sathish","Selva","Shiva","Surya","Tejas","Vimal","Yogesh","Zubin",
"Abhinav","Anup","Bhaskar","Chirag","Dev","Eshan","Gautam","Harsha","Jithin","Kalyan"
]

levels = [
("Executive","CTO"),
("Leadership","Director"),
("Management","Project Manager"),
("Lead","Tech Lead"),
("Execution","Senior Engineer")
]

projects = ["SecurePay","HealthSync","TradeFlow","SmartCRM","AI Assist","BankCore"]

def generate_employee(i):

    level = random.choice(levels)

    return {
    "employee_id":f"EMP{i:03}",
    "name":names[i],
    "designation":level[1],
    "org_level":level[0],
    "experience_years":random.randint(4,15),
    "department":random.choice(["Engineering","AI","Cloud","Security","Data","Mobile"]),

    "reporting_to":
        names[random.randint(0,i-1)] if i > 0 else "Board",

    "project":{

    "project_name":random.choice(projects),

    "responsibility":
    f"{names[i]} contributes at the {level[0]} level ensuring smooth delivery and alignment of technical initiatives.",

    "team_structure":[
        {
        "member":random.choice(names),
        "role":"Support Engineer",
        "function":"Handles implementation tasks."
        },
        {
        "member":random.choice(names),
        "role":"QA Specialist",
        "function":"Ensures validation and release readiness."
        }
    ],

    "description":
    f"{names[i]}'s role focuses on improving system stability and supporting enterprise-scale delivery operations."
    }
    }

employees = [generate_employee(i) for i in range(100)]

collection.delete_many({})
collection.insert_many(employees)

print("✅ 100 Unique Hierarchical Employees Inserted")