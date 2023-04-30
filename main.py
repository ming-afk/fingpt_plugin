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



def main():
    app.run(debug=True, host="0.0.0.0", port=5003)

if __name__ == "__main__":
    main()