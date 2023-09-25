# IS3240
<h2>1. set up</h2>
1. clone or download from GitHub
<br>
2. under root of requirements.txt, open terminal and run command "pip install -r requirements.txt"
<br>
3. run app.py to see if the web application is available

<h2>2. modify the project code (using pycharm)</h2>
1. for convenience, just modify your own part and then commit and push to GitHub
<br>
- click "commit" in the top right corner 
<br>
- enter commit message (e.g., "v1"), and then click "commit and push"
<br>
- click "push"
<br>
2. find the latest version
<br>
- click "pull" under Git (merge if necessary)

<h2>3. project structure</h2>
1. back-end and web scraping
<br>
- services: web scraping programs
<br>
- utils: utility functions like md5 encryption
<br>
- app.py (main run function)
<br>
- config.py (all static variables for configuration)
<br>
- models.py (ORM class like User), sqlite3.db (database)
<br>
2. front-end
<br>
- static (css, images, js)
<br>
- templates (all .html files)