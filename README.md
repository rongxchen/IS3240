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
1. controllers: APIs, backend
<br>
2. models: connections to database
<br>
3. services: bridge between controllers and models, i.e., mean logics will be written here
<br>
but for some services, models might not be involved, i.e., web scraping
<br>
4. static: frontend tools including css, js, images
<br>
5. templates: .html files
<br>
6. utils: general utilities
<br>
7. app.py: mean run function
<br>
8. sqlite3.db: database
<br>