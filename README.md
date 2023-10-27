## IS3240

## 1. set up
#### 1. clone from GitHub
#### 2. under root of requirements.txt, open terminal and run command "pip install -r requirements.txt"
#### 3. run app.py to see if the web application is available
###


## 2. project structure
#### 1. controllers: APIs
#### 2. models: SQL model definitions
#### 3. resources: scraping data csv like stock prices
#### 4. services: main logics of program execution for controllers
#### 5. utils: general utilities like jwt and md5
#### 7. app.py: bootstrap function
#### 8. general_config.py: static configuration variables or functions like path or token interceptor
#### 9. sqlite3.db: database
##### * reminder: use "pipreqs --force ." to generate new requirements.txt</h2>
###


## Data Collection
#### 1. Stock Price & Stock Symbol Searching
- Data source: Tiger Trade
- Method: 
  - Obtain their authorization token from the web page
  - Request their APIs 
- Data cleaning: get necessary fields only, such as 
  - {date, open, high, low, close and volume} for stock price
  - {symbol, name, market} for stock search
#### * To reduce API requests, we save the stock price data of a stock according to the K-line and date as .csv under resource folder, and delete out of date files if detected
###

#### 2. news data
- Data source: Routers
- Method: 
  - Obtain their API by clicking "load more" button
  - Request their APIs by entering required parameters like offset
  - Store the news data to db, and then sync the data that did not present in the db when start the server
- Data Cleaning: get necessary fields only, such as 
  - {title, url, image_url, category, publish_time}
###
