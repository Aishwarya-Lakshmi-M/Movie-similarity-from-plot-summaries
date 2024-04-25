from connect import cursor,mydb
class Project:
    def __init__(self,projecttitle, description, start_date, end_date, empmanagerid):
        self.__projecttitle = projecttitle
        self.__description = description
        self.__end_date = end_date
        self.__start_date = start_date
        self.__empmanagerid = empmanagerid
    def get_projecttitle(self):
        return self.__projecttitle
    def get_description(self):
        return self.__description
    def get_start_date(self):
        return self.__start_date
    def get_end_date(self):
        return self.__end_date
    def get_empmanagerid(self):
        return self.__empmanagerid

class projectdba:
    def __init__(self):
        self.mydb = mydb
        self.cursor = cursor

    def add_project(self,project):
        self.cursor.execute("INSERT INTO project (projectname, description, startdate, enddate, projectmanagerId) VALUES(%s,%s,%s,%s,%s)",(project.get_projecttitle(),project.get_description(),project.get_start_date(),project.get_end_date(),project.get_empmanagerid()))
        self.mydb.commit()

    def add_to_projectemp(self,emp_id,project_id):
        self.cursor.execute("INSERT INTO projectemployee VALUES (%s,%s)",(emp_id,project_id))
        self.mydb.commit()

    def get_empprojects(self,emp_id):
        self.cursor.execute("SELECT * FROM project WHERE idproject in (SELECT projectid from projectemployee where empid = '%s')",(emp_id,))
        result = self.cursor.fetchall()
        if result:
            return result
        return None
    
    def get_project(self,project_id):
        self.cursor.execute("SELECT * FROM project WHERE idproject = '%s'",(project_id,))
        result = self.cursor.fetchone()
        if result:
            return result
        return None
    
    def all_project(self):
        self.cursor.execute("SELECT * FROM project")
        result = self.cursor.fetchall()
        if result:return result
        return None
    
    def currentmonthproject(self):
        self.cursor.execute("select * from project where (select month(startdate)) = (select month(curdate())) and (select year(startdate)) = (select year(curdate()))")
        result = self.cursor.fetchall()
        if result: return result
        return None
    
    def modify_projectmanager(self,emp_id,project_id):
        self.cursor.execute("UPDATE project set projectmanagerId = %s WHERE idproject = %s",(emp_id,project_id))
        self.mydb.commit()


class projectmethods:
    def __init__(self,project_db):
        self.project_db = project_db

    def new_project(self,project):
        self.project_db.add_project(project)
        print(f"{project.get_projecttitle()} has been added.")

  
    
    def addProjectToEmployee(self,emp_id,project_id):
        self.project_db.add_to_projectemp(emp_id,project_id)
        print("added")

    def getEmployeeProjects(self,emp_id):
        result = self.project_db.get_empprojects(emp_id)
        if result:
            return result
        return "No projects assigned"
    
    def getProjectDetails(self,project_id):
        result = self.project_db.get_project(project_id)
        if result:
            return result
        return "No such project available"
    
    def getprojectlist(self):
        result = self.project_db.all_project()
        if result:return result
        return "No projects exist"
    
    def getcurrentprojects(self):
        result = self.project_db.currentmonthproject()
        if result : return result
        return None
    
    def changeprojectmanager(self,emp_id,project_id):
        self.project_db.modify_projectmanager(emp_id,project_id)
        print("project manager changed")