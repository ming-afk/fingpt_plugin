import json

import quart
import quart_cors
from quart import request

from fmp_methods.fmp import *

app = quart_cors.cors(quart.Quart(__name__), allow_origin="https://chat.openai.com")

# Keep track of todo's. Does not persist if Python session is restarted.
_TODOS = {}

@app.post("/todos/<string:username>")
async def add_todo(username):
    request = await quart.request.get_json(force=True)
    if username not in _TODOS:
        _TODOS[username] = []
    _TODOS[username].append(request["todo"])
    return quart.Response(response='OK', status=200)

@app.get("/todos/<string:username>")
async def get_todos(username):
    return quart.Response(response=json.dumps(_TODOS.get(username, [])), status=200)

@app.delete("/todos/<string:username>")
async def delete_todo(username):
    request = await quart.request.get_json(force=True)
    todo_idx = request["todo_idx"]
    # fail silently, it's a simple plugin
    if 0 <= todo_idx < len(_TODOS[username]):
        _TODOS[username].pop(todo_idx)
    return quart.Response(response='OK', status=200)

@app.get("/logo.png")
async def plugin_logo():
    filename = 'logo.png'
    return await quart.send_file(filename, mimetype='image/png')

@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
    host = request.headers['Host']
    with open("./.well-known/ai-plugin.json") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/json")

@app.get("/openapi.yaml")
async def openapi_spec():
    host = request.headers['Host']
    with open("openapi.yaml") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/yaml")
    
    
@app.get("/financial_ratios/<string:ticker>")
async def get_financial_ratios(ticker):
    return quart.Response(response=json.dumps(fetch_financial_ratios(ticker,3)), status=200)

@app.get("/stock_news/<string:ticker>")
async def get_single_stock_news(ticker):
    return quart.Response(response=json.dumps(fetch_single_stock_news(ticker,20)), status=200)

@app.get("/earning_call_transcript/<string:ticker>")
async def get_latest_earnings_call_transcript(ticker):
    return quart.Response(response=json.dumps(fetch_latest_earnings_call_transcript(ticker)), status=200)

@app.get("/analyst_target_price/<string:ticker>")
async def get_fetch_analyst_target_price(ticker):
    return quart.Response(response=json.dumps(fetch_analyst_target_price(ticker, 10)), status=200)
# ! the link wshould allign with what is on openai.yaml
@app.get("/SEC_Filling/<string:ticker>")
async def get_sec_filings(ticker):
    return quart.Response(response=json.dumps(fetch_sec_filings(ticker)), status=200)

@app.get("/esg_score/<string:ticker>")
async def get_esg_data(ticker):
    return quart.Response(response=json.dumps(fetch_esg_data(ticker)), status=200)
# >>>>>>>>revenue product segmentation<<<<<
@app.get("/revenue_product_segmentation_annually/<string:ticker>")
async def get_revenue_product_segmentation_annually(ticker):
    return quart.Response(response=json.dumps(fetch_revenue_product_segmentation_annually(ticker)), status=200)

@app.get("/sales_revenue_by_product_segement_quarterly/<string:ticker>")
async def get_sales_revenue_by_product_segement_quarterly(ticker):
    return quart.Response(response=json.dumps(fetch_sales_revenue_by_product_segement_quarterly(ticker)), status=200)
# >>>>>>>>>> revenue geographic segmentation <<<<<<<<<<
@app.get("/sales_revenue_by_geographic_segmentation_annually/<string:ticker>")
async def get_sales_revenue_by_geographic_segmentation_annually(ticker):
    return quart.Response(response=json.dumps(fetch_sales_revenue_by_geographic_segmentation_annually(ticker)), status=200)

@app.get("/sales_revenue_by_geographic_segmentation_quarterly/<string:ticker>")
async def get_sales_revenue_by_geographic_segmentation_quarterly(ticker):
    return quart.Response(response=json.dumps(fetch_sales_revenue_by_geographic_segmentation_quarterly(ticker)), status=200)

# >>>>>>>>>> social sentiements <<<<<<<<<<
@app.get("/social_media_sentiments/<string:ticker>")
async def get_social_media_sentiments(ticker):
    return quart.Response(response=json.dumps(social_media_sentiments(ticker)), status=200)


# >>> company profile <<<<<<<
@app.get("/company_profile/<string:ticker>")
async def get_company_profile(ticker):
    return quart.Response(response=json.dumps(fetch_company_profile(ticker)), status=200)

@app.get("/company_executives/<string:ticker>")
async def get_company_executives(ticker):
    return quart.Response(response=json.dumps(fetch_company_executives(ticker)), status=200)

# >>>>>>>>>> company quotes <<<<<<<<<<
@app.get("/company_quote/<string:ticker>")
async def get_company_quotes(ticker):
    return quart.Response(response=json.dumps(fetch_company_quote(ticker)), status=200)


# >>>>>>>>>> company DCFs <<<<<<<<<<
@app.get("/company_dcf/<string:ticker>")
async def get_company_dcf(ticker):
    return quart.Response(response=json.dumps(fetch_company_DCF(ticker)), status=200)

@app.get("/detailed_dcf_projection_including_wacc_data/<string:ticker>")
async def get_detailed_dcf_projection_including_wacc_data(ticker):
    return quart.Response(response=json.dumps(fetch_detailed_dcf_projection_including_wacc_data(ticker)), status=200)


@app.get("/income_statement_quarter/<string:ticker>")
async def get_income_statement_quarter(ticker):
    return quart.Response(response=json.dumps(fetch_income_statement_quarterly(ticker)), status=200)

@app.get("/balance_sheet_quarter/<string:ticker>")
async def get_balance_sheet_quarter(ticker):
    return quart.Response(response=json.dumps(fetch_balance_sheet_quarterly(ticker)), status=200)

@app.get("/cash_flow_quarter/<string:ticker>")
async def get_cash_flow_statement_quarter(ticker):
    return quart.Response(response=json.dumps(fetch_cash_flow_quarterly(ticker)), status=200)



def main():
    app.run(debug=True, host="0.0.0.0", port=5003)

if __name__ == "__main__":
    main()