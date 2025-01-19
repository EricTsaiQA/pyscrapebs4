import requests
from bs4 import BeautifulSoup
import os, json
from dotenv import load_dotenv
from datetime import datetime

# config by loading dotenv content
load_dotenv()
json_root_path = os.getenv('JSON_PATH')
user_agent = os.getenv('USER_AGENT')
os.makedirs(json_root_path, exist_ok=True)


def scrape_etherscan(filter_value):
    base_url = "https://etherscan.io"
    url = f"{base_url}/txs"
    transaction_detail = []
    # session
    session = requests.Session()
    # headers
    headers = {
        'User-Agent': user_agent
    }
    # get
    response = session.get(url, headers=headers)

    if response.status_code == 200:
        # analysis html
        soup = BeautifulSoup(response.text, 'html.parser')

        # collect link of each transaction on the page
        transactions = soup.find_all('tr')
        transaction_links = []
        for transaction in transactions:
            columns = transaction.find_all('td')
            if columns:
                tx_hash = columns[1].find('a').get('href')
                transaction_links.append(base_url + tx_hash)

    # try get details of a transaction from its page
    for link in transaction_links:
        details = get_transaction_details(session,link)
        # filter out data according to user input
        if details and filter_transaction(details, filter_value):
            transaction_detail.append(details)
    # save to json
    save_to_json(transaction_detail)


def get_transaction_details(session, link):
    global transaction_data
    headers = {
        'User-Agent': user_agent
    }

    response = session.get(link, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        try:
            tx_hash = soup.find('span', id='spanTxHash').text.strip()
            status = soup.find('div', class_='col col-md-9').text.strip()  #col col-md-9
            block = soup.find('span', class_='d-flex align-items-center gap-1').find('a').get_text()
            timestamp = soup.find('span', id='showUtcLocalDate').text.strip()
            transaction_action = soup.find('div', class_='d-flex align-items-baseline').get_text().strip()
            sponsored = \
            soup.find('div', class_='overflow-x-auto scrollbar-custom').find('div', class_='coinzilla')['class'][0]
            from_address = soup.find('div', class_='col-md-9 from-address-col').text.strip()
            to_address = soup.find('div', class_='col-md-9 to-address-col').text.strip()
            value = soup.find('span', id='ContentPlaceHolder1_spanValue').text.strip()
            transaction_fee = soup.find('span', id='ContentPlaceHolder1_spanTxFee').text.strip()
            gas_price = soup.find('span', id='ContentPlaceHolder1_spanGasPrice').text.strip()

            transaction_data = {
                "Transaction Hash": tx_hash,
                "Status": status,
                "Block": block,
                "Timestamp": timestamp,
                "Transaction Action": transaction_action,
                "Sponsored": sponsored,
                "From": from_address,
                "To": to_address,
                "Value": value,
                "Transaction Fee": transaction_fee,
                "Gas Price": gas_price
            }

        except AttributeError as e:
            print("error while reading a transaction", e)

        return transaction_data


def filter_transaction(transaction, filter_value):
    if filter_value == '0':
        return transaction['Value'] == '0 ETH ($0.00)'
    elif filter_value == 'non-zero':
        return transaction['Value'] != '0 ETH ($0.00)'
    elif filter_value == 'all':
        return True

def save_to_json(data):
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"transactions_{current_time}.json"
    filepath = os.path.join(json_root_path, filename)
    with open(filepath, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file,indent=4, ensure_ascii=False)

    print(f"json file has been created, {filename}")

if __name__ == "__main__":
    print("Please input value filter 0 or non-zero or all")
    filter_value = input()
    while filter_value not in ['0', 'non-zero', 'all']:
        print("invalid format, try again")
        filter_value = input()
    print("Please wait, we are working on it...")
    scrape_etherscan(filter_value)
