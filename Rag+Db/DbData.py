

# from langchain_community.document_loaders import PyPDFLoader
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_community.vectorstores import FAISS
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_ollama import OllamaLLM



# loader = PyPDFLoader("data/PythonProgramming.pdf")
# docs = loader.load()

# splitter = RecursiveCharacterTextSplitter(
#     #separator="praveen kumar",splite spearate word
#     chunk_size=1000,
#     chunk_overlap=200,
#     add_start_index=True
# )

# chunks = splitter.split_documents(docs)

# embeddings = HuggingFaceEmbeddings(
#     model_name="sentence-transformers/all-MiniLM-L6-v2"
# )

# db = FAISS.from_documents(chunks, embeddings)

# llm = OllamaLLM(model="llama3", temperature=0.0)

# print(" Ready! Ask anything about the PDF")
# print("Type 'exit' to stop\n")


# def answer_question(question):

#     q_lower = question.lower()


#     is_summary = "summary" in q_lower or "summarize" in q_lower


#     results = db.similarity_search_with_score(question, k=6)
#              #db.max_marginal_relevance_search(query, k=6)

#     if not results:
#         return " Answer not found in document"

#     contexts = []
#     pages = set()

#     for doc, _ in results:
#         contexts.append(doc.page_content)
#         if "page" in doc.metadata:
#             pages.add(str(doc.metadata["page"] + 1))

#     context_text = "\n\n".join(contexts)
#     pages_text = ", ".join(pages)


#     if is_summary:
#         prompt = f"""
# You are summarizing content from a PDF textbook.

# Use ONLY the context below.
# Provide a clear summary.

# Context:
# {context_text}

# Summary:
# """
#     else:

#         prompt = f"""
# You are answering from a PDF textbook.

# Use ONLY the context below.
# If answer is not clearly present say EXACTLY:
# Answer not found in the document.

# Context:
# {context_text}

# Question:
# {question}

# Answer:
# """

#     response = llm.invoke(prompt)

#     if "not found" in response.lower() or len(response.strip()) < 5:
#         return " Answer not found in the document"

#     return f"{response}\n\n Source Page(s): {pages_text}"



# while True:

#     user_input = input(" Ask: ")

#     if user_input.lower() == "exit":
#         print("👋 Stopped")
#         break

#     print(" Searching PDF...")
#     reply = answer_question(user_input)
#     print("\n Answer:\n", reply)
#     print("-"*50)



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