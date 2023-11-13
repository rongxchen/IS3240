## IS3240
## Project Structure
- controllers: APIs
- models: SQL model definitions
- resources: scraping data csv like stock prices
- services: main logics of program execution for controllers
- utils: general utilities like jwt and md5
- app.py: bootstrap function
- general_config.py: static configuration variables or functions like path or token interceptor
- sqlite3.db: database
* reminder: use "pipreqs --force ." to generate new requirements.txt</h2>

<br>
<br>


## Data Collection
#### 1. Stock Price & Stock Symbol Searching
- Data source: Tiger Trade
- Method: 
  - Obtain their authorization token from the web page, and save in a txt file
  - Request their APIs by carrying the authorization token
- Data cleaning: get necessary fields only, such as 
  - {date, open, high, low, close and volume} for stock price
  - {symbol, name, market} for stock search
- To reduce API requests, we save the stock price data of a stock according to the K-line and date as .csv under resource folder, and delete out-of-date files if detected
###

#### 2. news data
- Data source: Routers, Bloomberg
- Method: 
  - Obtain their APIs by clicking "load more" button
  - Request their APIs by entering required parameters like offset
  - Store the news data to db, and then sync the data that did not present in the db when start the server
- Data Cleaning: get necessary fields only, such as 
  - {title, url, image_url, category, publish_time}
- for those news without image url (especially for Bloomberg news), replace the image as the Bloomberg's image
###
