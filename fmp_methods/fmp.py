import requests

# Constants
BASE_URL = "https://financialmodelingprep.com/api"
FINANCIAL_PREP_API_KEY = 'c8fc248088cc9d0687ea4d069f304d97'
DATA_DOCUMENTATION = [
    "Financial Ratios",
    "Earning Call Transcript",
    "SEC Fillings",
    "ESG SCORE",
    "Price Target By Analyst Summary",
    "Stock news",
    "Stock Insider Trading",
]

# Functions
def fetch_single_stock_news(ticker, limit=50):
    url = f"{BASE_URL}/v3/stock_news?tickers={ticker}&limit={limit}&apikey={FINANCIAL_PREP_API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

def fetch_stock_news(tickers):
    return fetch_single_stock_news(tickers[0], limit=5)

def fetch_latest_earnings_call_transcript(ticker):
    url_transcripts = f"{BASE_URL}/v4/earning_call_transcript?symbol={ticker}&apikey={FINANCIAL_PREP_API_KEY}"
    response = requests.get(url_transcripts)

    if response.status_code != 200:
        print(f"Error fetching data: {response.status_code}")
        return

    transcripts = response.json()

    if not transcripts:
        print(f"No transcripts available for {ticker}")
        return

    transcripts.sort(key=lambda x: x[2], reverse=True)
    latest_transcript = transcripts[0]
    transcript_qtr = latest_transcript[0]
    transcript_yr = latest_transcript[1]

    url_transcript_content = f"{BASE_URL}/v3/earning_call_transcript/{ticker}?quarter={transcript_qtr}&year={transcript_yr}&apikey={FINANCIAL_PREP_API_KEY}"
    response = requests.get(url_transcript_content)

    if response.status_code != 200:
        print(f"Error fetching transcript content: {response.status_code}")
        return

    transcript_ret = response.json()
    transcript_content = transcript_ret[0]["content"]
    print(transcript_content)
    return transcript_content[:int(len(transcript_content)/2)]

def fetch_analyst_target_price(symbol, limit=10):
    url = f"{BASE_URL}/v4/price-target?symbol={symbol}&apikey={FINANCIAL_PREP_API_KEY}"
    response = requests.get(url)
    price_ret = ""

    if response.status_code == 200:
        data = response.json()
        i = 0
        for entry in data:
            published_date = entry.get("publishedDate")[:10]
            analyst_name = entry.get("analystName")
            price_target = entry.get("priceTarget")
            link = entry.get("newsURL")
            news_title = entry.get("newsTitle")
            price_ret += f"Published Date: {published_date},\nAnalyst Name: {analyst_name},\nPrice Target: {price_target},\n news title: {news_title},\n url: {link} \n\n "
            i += 1
            if i == 10:
                break
        return price_ret
    else:
        print(f"Failed to get data. Status code: {response.status_code}")

def fetch_financial_ratios(symbol, limit=3):
    url = f"{BASE_URL}/v3/ratios/{symbol}?period=quarter&limit={limit}&apikey={FINANCIAL_PREP_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Failed to get data. Status code: {response.status_code}")

def fetch_insider_trading(symbol):
    url = f"https://financialmodelingprep.com/api/v4/insider-trading?symbol={ticker}&apikey={FINANCIAL_PREP_API_KEY}&page=0"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get data. Status code: {response.status_code}")
        return None

import requests

def fetch_esg_data(symbol):
    url = f"https://financialmodelingprep.com/api/v4/esg-environmental-social-governance-data?symbol={ticker}&apikey={FINANCIAL_PREP_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get data. Status code: {response.status_code}")
        return None

def fetch_sec_filings(symbol):
    url = f"https://financialmodelingprep.com/api/v3/sec_filings?symbol={ticker}&apikey={FINANCIAL_PREP_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get data. Status code: {response.status_code}")
        return None

def default_case(data_name):
    if data_name in DATA_DOCUMENTATION:
        print("This method not implemented yet!")
    else:
        print(f"data_name {data_name} does not exist")

import requests

def execute_retrieve_financial_data_base(tickers, data_names):
    result = {}
    for data_name in data_names:
        if data_name == DATA_DOCUMENTATION[5]:
            ret = fetch_stock_news(tickers)
            result[data_name] = ret
        elif data_name == DATA_DOCUMENTATION[0]:
            ret = fetch_financial_ratios(tickers[0])
            result[data_name] = ret
        elif data_name == DATA_DOCUMENTATION[1]:
            ret = fetch_latest_earnings_call_transcript(tickers[0])
            result[data_name] = ret
        elif data_name == DATA_DOCUMENTATION[4]:
            ret = fetch_analyst_target_price(tickers[0])
            result[data_name] = ret
        elif data_name == DATA_DOCUMENTATION[6]:
            ret = fetch_insider_trading(tickers[0])
            result[data_name] = ret
        elif data_name == DATA_DOCUMENTATION[3]:
            ret = fetch_esg_data(tickers[0])
            result[data_name] = ret
        elif data_name == DATA_DOCUMENTATION[2]:
            ret = fetch_sec_filings(tickers[0])
            result[data_name] = ret
        else:
            default_case(data_name)
    return result


fetch_latest_earnings_call_transcript("GOOG")