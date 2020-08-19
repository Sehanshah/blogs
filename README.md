GraphQL API with Django

To run the application in local

1. Install python3

2. Open cmd or Terminal in the Project Root Folder and type the command
	> **pip install virtualenv**
	
	If already found ignore this step

3. Create a virtual environment to run the project by running the command,
	>**virtualenv venv**

4. After creating venv, A folder named **venv** will be created in Project Directory

5. Windows users , In cmd type,
	>**venv\Scripts\activate**
	
   Linux Users, In Terminal type,
	>**source venv\bin\activate**

6. You will find **(venv)** at the start of the prompt if it's activated

7. Install the dependencies by running the following command,
	>**pip install -r requirements.txt**

8. After Installation, To start the server Run
    >**python manage.py migrate**
    
    >**python manage.py runserver**
