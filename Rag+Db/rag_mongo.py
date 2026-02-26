from pymongo import MongoClient
from langchain_core.documents import Document

def load_mongo_docs():

    client = MongoClient("mongodb://localhost:27017/")
    db = client["RAGcompanyDB"]
    collection = db["employees"]

    docs = []

    for emp in collection.find():

        team_text = ""

        if "project" in emp and "team_structure" in emp["project"]:
            for member in emp["project"]["team_structure"]:
                team_text += f"""
                Team Member Name: {member.get('member','')}
                Role: {member.get('role','')}
                Responsibility: {member.get('function','')}
                """

        text = f"""
        Employee ID: {emp.get('employee_id','')}
        Name: {emp.get('name','')}
        Designation: {emp.get('designation','')}
        Org Level: {emp.get('org_level','')}
        Experience: {emp.get('experience_years','')} years
        Department: {emp.get('department','')}
        Reporting To: {emp.get('reporting_to','')}

        Project Name: {emp.get('project',{}).get('project_name','')}

        Role in Project:
        {emp.get('project',{}).get('responsibility','')}

        Team Structure:
        {team_text}

        Project Description:
        {emp.get('project',{}).get('description','')}
        """

        docs.append(Document(page_content=text))

    return docs