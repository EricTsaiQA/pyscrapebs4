Use Python3 with BeautifulSoup4 to scrape the page https://etherscan.io/txs

this script can 
1. get each transaction details on page https://etherscan.io/txs
2. you can filter amount by input 0 , non-zero , all to filter out
3. save details to a json file under output folder


How to :

1. clone the code
2. go to folder pyscrapebs4
3. rename dotenv.exmpale to .env
4. run command "python3 etherscan_scraper.py"


Pending things need to discover (cause this script is for interview, there are things i haven't figure out lol

1. script 指定 block 區間 , 且上限為 100 block (ex. 21442021 - 21442120) ( i am not sure how to do it by bs4, i think if i go with api testing method maybe i can do that)
2. filter method ( i think this means transaction action file. but i have limited time to figure out how to do that)





