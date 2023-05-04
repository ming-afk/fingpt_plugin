import requests

# Constants
BASE_URL = "https://financialmodelingprep.com/api"
FINANCIAL_PREP_API_KEY = '7515c2dce5befb8dc63a9cfca91732fe'
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

def fetch_company_quote(ticker):
    url = f"{BASE_URL}/v3/quote/{ticker}?apikey={FINANCIAL_PREP_API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

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
        return data
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
    url = f"https://financialmodelingprep.com/api/v4/insider-trading?symbol={symbol}&apikey={FINANCIAL_PREP_API_KEY}&page=0"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get data. Status code: {response.status_code}")
        return None


def fetch_esg_data(symbol):
    url = f"https://financialmodelingprep.com/api/v4/esg-environmental-social-governance-data?symbol={symbol}&apikey={FINANCIAL_PREP_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get data. Status code: {response.status_code}")
        return None
#>>>>>>>>sales by product segmentation<<<<<<<<<<<<<
def fetch_revenue_product_segmentation_annually(symbol):
    url = f"{BASE_URL}/v4/revenue-product-segmentation?symbol={symbol}&structure=flat&apikey={FINANCIAL_PREP_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get data. Status code: {response.status_code}")
        return None

def fetch_sales_revenue_by_product_segement_quarterly(symbol):
    url = f"https://financialmodelingprep.com/api/v4/revenue-product-segmentation?symbol={symbol}&period=quarter&apikey={FINANCIAL_PREP_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get data. Status code: {response.status_code}")
        return None
# >>>>>>>>>>sales by geographic segmentation <<<<<<<<<<<<
def fetch_sales_revenue_by_geographic_segmentation_annually(symbol):
    url = f"https://financialmodelingprep.com/api/v4/revenue-geographic-segmentation?symbol={symbol}&apikey={FINANCIAL_PREP_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get data. Status code: {response.status_code}")
        return None

def fetch_sales_revenue_by_geographic_segmentation_quarterly(symbol):
    url = f"https://financialmodelingprep.com/api/v4/revenue-geographic-segmentation?symbol={symbol}&period=quarter&apikey={FINANCIAL_PREP_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get data. Status code: {response.status_code}")
        return None


# >>>>>>> social media sentiments <<<<<<<<<<<<
def social_media_sentiments(symbol):
    url = f"https://financialmodelingprep.com/api/v4/historical/social-sentiment?symbol={symbol}&page=0&apikey={FINANCIAL_PREP_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get data. Status code: {response.status_code}")
        return None





#>>>>>>>>>>>> company profile <<<<<<<<<<<<<<<<

def fetch_company_profile(symbol):
    url = f"https://financialmodelingprep.com/api/v3/profile/{symbol}?apikey={FINANCIAL_PREP_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get data. Status code: {response.status_code}")
        return None
    
def fetch_company_executives(symbol):
    url = f"https://financialmodelingprep.com/api/v3/key-executives/{symbol}?apikey={FINANCIAL_PREP_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get data. Status code: {response.status_code}")
        return None
    

def fetch_company_DCF(symbol):
    url = f"https://financialmodelingprep.com/api/v3/discounted-cash-flow/{symbol}?apikey={FINANCIAL_PREP_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get data. Status code: {response.status_code}")
        return None

def fetch_detailed_dcf_projection_including_wacc_data(symbol):
    url = f"https://financialmodelingprep.com/api/v4/advanced_discounted_cash_flow?symbol={symbol}&apikey={FINANCIAL_PREP_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get data. Status code: {response.status_code}")
        return None


# >>>>>> financial Statements <<<<<<<<<<<<
def fetch_income_statement_quarterly(symbol,limit=12):
    url = f"https://financialmodelingprep.com/api/v3/income-statement/{symbol}?period=quarter&limit={limit}&apikey={FINANCIAL_PREP_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get data. Status code: {response.status_code}")
        return None


def fetch_balance_sheet_quarterly(symbol,limit=12):
    url = f"https://financialmodelingprep.com/api/v3/balance-sheet-statement/{symbol}?period=quarter&limit={limit}&apikey={FINANCIAL_PREP_API_KEY}"
    print(url)
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get data. Status code: {response.status_code}")
        return None

def fetch_cash_flow_quarterly(symbol,limit=12):
    url = f"https://financialmodelingprep.com/api/v3/cash-flow-statement/{symbol}?period=quarter&limit={limit}&apikey={FINANCIAL_PREP_API_KEY}"
    print(url)
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get data. Status code: {response.status_code}")
        return None

def fetch_sec_filings(symbol,limit=12):
    url = f"https://financialmodelingprep.com/api/v3/sec_filings/{symbol}?type=10-k&page=0&apikey={FINANCIAL_PREP_API_KEY}"
    print(url)
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


# /api/v4/revenue-product-segmentation?symbol=AAPL&structure=flat


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


print(fetch_sec_filings("TSLA"))