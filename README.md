# IS3240
<h2>1. set up</h2>
1. clone from GitHub
<br>
2. under root of requirements.txt, open terminal and run command "pip install -r requirements.txt"
<br>
3. run app.py to see if the web application is available

<h2>2. project structure</h2>
1. controllers: APIs
<br>
2. models: connection models of database
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
7. app.py: main run function
<br>
8. sqlite3.db: database
<br>

<h2>use "pipreqs --force ." to generate new requirements.txt</h2>
