import requests

# this is to interact with the fmp data base, now supports stock news
financial_prep_apikey = 'c8fc248088cc9d0687ea4d069f304d97'

def get_single_stock_news(ticker, limit=50):
    api_key = financial_prep_apikey
    url = f"https://financialmodelingprep.com/api/v3/stock_news?tickers={ticker}&limit={limit}&apikey={api_key}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

def get_stock_news(tickers):
  return get_single_stock_news(tickers[0], limit = 5)


def get_latest_earnings_call_transcript(ticker):
    api_key = financial_prep_apikey
    base_url = "https://financialmodelingprep.com/api/v4"
    
    # Get available transcripts for the symbol
    url_transcripts = f"{base_url}/earning_call_transcript?symbol={ticker}&apikey={api_key}"
    response = requests.get(url_transcripts)
    
    if response.status_code != 200:
        print(f"Error fetching data: {response.status_code}")
        return
    
    transcripts = response.json()
    
    if not transcripts:
        print(f"No transcripts available for {ticker}")
        return
    print(transcripts)
    # Sort transcripts by date in descending order
    transcripts.sort(key=lambda x: x[2], reverse=True)
    
    # Get the latest transcript
    latest_transcript = transcripts[0]
    transcript_qtr = latest_transcript[0]
    transcript_yr = latest_transcript[1]

    
    # Get the transcript content
    base_url = "https://financialmodelingprep.com/api/v3"
    url_transcript_content = f"{base_url}/earning_call_transcript/{ticker}?quarter={transcript_qtr}&year={transcript_yr}&apikey={api_key}"
    response = requests.get(url_transcript_content)
    
    if response.status_code != 200:
        print(f"Error fetching transcript content: {response.status_code}")
        return
    
    transcript_ret = response.json()
    transcript_content = transcript_ret[0]["content"]
    print(transcript_content)
    return transcript_content[:int(len(transcript_content)/2)]

def get_analyst_target_price(symbol,limit=10):
    # Define the API endpoint URL
    api_key = financial_prep_apikey
    url = f"https://financialmodelingprep.com/api/v4/price-target?symbol={symbol}&apikey={api_key}"
    
    # Send a GET request to the API endpoint
    response = requests.get(url)
    price_ret = ""
    # Check if the response status code is 200 (OK)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        
        # Print the analyst target price for each entry
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

def fetch_financial_ratios(symbol,limit=50):
    # Define the API endpoint URL
    api_key = financial_prep_apikey
    # /api/v3/ratios/AAPL?period=quarter&limit=140

    url = f"https://financialmodelingprep.com//api/v3/ratios/{symbol}?period=quarter&limit={limit}&apikey={api_key}"
    
    # Send a GET request to the API endpoint
    response = requests.get(url)
    price_ret = ""
    # Check if the response status code is 200 (OK)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        return data
        
        # # find which ratios are actually important
        # important_ratios = ["symbol","date","period"]
        # important_ratios += identify_important_financial_ratios_for_company(8, symbol, data[0].keys())["answer"]

        # data = [keep_designated_keys(x,important_ratios) for x in data]
        # return data[:limit]

    else:
        print(f"Failed to get data. Status code: {response.status_code}")


# Call the function to get the analyst target price
# print(get_analyst_target_price(symbol, api_key))





def default_case(data_name):
  if data_name in data_documentation:
    print("this method not implemented yet!")
  else:
    print(f"data_name {data_name} does not exist")




data_documentation = [
        "Financial Ratios", # financials
        "Earning Call Transcript",
        "SEC Fillings",
        "ESG SCORE",
        "Price Target By Analyst Summary",
        "Stock news",
        "Stock Insider Trading",
]

# switch = {data_documentation[6]:get_stock_news}

# def execute_retrieve_fiancial_data_base(tickers,data_names,user_query,related_questions):
def execute_retrieve_fiancial_data_base(tickers,data_names):
  # perform for each data needed, parameter as tickers for now
  result = {}
  for data_name in data_names:
    # stock news
    if data_name == data_documentation[5]:
      ret = get_stock_news(tickers)
      result[data_name] = ret
      
    elif data_name == data_documentation[0]:
      ret = get_financial_ratios(tickers[0])
      result[data_name] = ret
    
    elif data_name == data_documentation[1]:
      ret = get_latest_earnings_call_transcript(tickers[0])
      result[data_name] = ret
    
    elif data_name == data_documentation[4]:
      ret = get_analyst_target_price(tickers[0])
      result[data_name] = ret
      
      
    else:
      default_case(data_name)

  return result


fetch_financial_ratios("AAPL")