from app import app, db
from flask import render_template, flash, redirect, url_for, request
from datetime import datetime
from werkzeug.urls import url_parse
import urllib.request, json
import requests
from app.forms import SearchForm
from app.models import Symbol



@app.route('/')
@app.route('/index')
# @login_required
def index():
    newurl = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/market/get-movers?&region=US&lang=en"
    headers = {'X-RapidAPI-Key': '2700cac5b5msh2621b9602e858f1p117364jsn648fb90776eb'}
    result = requests.get(newurl, headers=headers)
    test = result.json()
    items = test["result"][0]["quotes"]
    return render_template('index.html', title='Home', dataitem=items)





@app.route('/load')
def loadToDatabase():
    nUrl = "https://stock.p.rapidapi.com/v1/funds"
    headers = {'X-RapidAPI-Key': '2700cac5b5msh2621b9602e858f1p117364jsn648fb90776eb'}
    result = requests.get(nUrl, headers=headers)
    jsonFromat = result.json()
    funds = jsonFromat['result']['funds']
    fundList = []

    symbolList = []
    for item in funds:
        symbolList.append(item['symbol'])



    for item in funds:
        stock = Symbol(symbol=item['symbol'], company_name=item['name'],sentiment_score=item['sentimentscore'])
        db.session.add(stock)
        db.session.commit()
    return redirect(url_for('index'))



def headers(apikey):
    return {'Authorization': 'Bearer {}'.format(apikey),
            'Content-Type': 'application/json'}



# @app.route('/stockDetails', methods=['GET', 'POST'])
# def details():
#     form = SearchForm(request.form)
#     searchTerm = 'AWSM'
#     if form.validate_on_submit():
#         searchTerm = form.stock_symbol.data
#     newurl = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/get-detail?region=US&lang=en&symbol=" + searchTerm
#     headers = {'X-RapidAPI-Key': '2700cac5b5msh2621b9602e858f1p117364jsn648fb90776eb'}
#     result = requests.get(newurl, headers=headers)
#     stockData = result.json()
#     return render_template('stockDetails.html', title='Stock Details', stockData=stockData, form=form, stockName=searchTerm)


@app.route('/stockSearch', methods=['GET', 'POST'])
def stockSearch():
    form = SearchForm(request.form)
    searchTerm = 'A'
    if form.validate_on_submit():
        searchTerm = form.stock_symbol.data
    newurl = "https://www.worldtradingdata.com/api/v1/stock_search?search_term="+ searchTerm +"&search_by=symbol,name&limit=50&page=1&api_token=MyCkuCYIniSmfOo5jNMttDtjLlHE4VpeiCQNJDJzCSJc6J5Z2NkWaNhQxOF9"
    result = requests.get(newurl)
    stockData = result.json()
    numItems = len(stockData['data'])-1
    return render_template('stockSearch.html', title='Stock Search', stockData=stockData, form=form, numItems=numItems)

def queryStock(stock_symbol):
    newurl = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/get-detail?region=US&lang=en&symbol=" + stock_symbol
    headers = {'X-RapidAPI-Key': '2700cac5b5msh2621b9602e858f1p117364jsn648fb90776eb'}
    result = requests.get(newurl, headers=headers)
    stockData = result.json()
    return stockData

@app.route('/stockDetails', methods=['GET', 'POST'])
def stockDetails():
    ticker_symbol = request.args.get('ticker_symbol')
    newurl = "https://www.worldtradingdata.com/api/v1/stock?symbol=" + str(ticker_symbol) + "&api_token=MyCkuCYIniSmfOo5jNMttDtjLlHE4VpeiCQNJDJzCSJc6J5Z2NkWaNhQxOF9"
    result = requests.get(newurl)
    stockData = result.json()
    if 'data' in stockData:
        listItems = PEAnalysis(ticker_symbol)
        MorningStar = MSR(ticker_symbol)
        news = getStockNews(ticker_symbol)
        return render_template('stockDetails.html', title=ticker_symbol, stockData=stockData, listItems=listItems, MSR=MorningStar, news=news)
    return render_template('stockDetails.html', title=ticker_symbol, stockData=stockData, listItems=[], MSR=0, news=[])


def PEAnalysis(stock_symbol):
    stockData = queryStock(stock_symbol)
    try:
        peRatio = stockData['defaultKeyStatistics']['forwardPE']['raw']
    except:
        return [0,"text-danger", "PE Ratio Not Applicable"]
    color = ""
    message = ""
    if peRatio <= 15:
        color = "text-success"
        message = "a low PE ratio indicates that this stock may be undervalued"
    elif peRatio <= 25:
        color = "text-warning"
        message = "A mid-range PE ratio indicates that this stock may be under or overvalued"
    else:
        color = "text-danger"
        message = "A high PE ratio indicates that this stock may be overvalued"
    returnList = [peRatio, color, message]
    return returnList

def MSR(stock_symbol):
    stockData = queryStock(stock_symbol)
    MSR = stockData['defaultKeyStatistics']['morningStarRiskRating']
    return MSR

def getStockNews(stock_symbol):
    newurl = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/get-news?region=US&category=" + stock_symbol
    headers = {'X-RapidAPI-Key': '2700cac5b5msh2621b9602e858f1p117364jsn648fb90776eb'}
    result = requests.get(newurl, headers=headers)
    stockNews = result.json()
    return stockNews

@app.route('/sentiment', methods=['GET', 'POST'])
def sentiment():
    nUrl = "https://stock.p.rapidapi.com/v1/funds"
    headers = {'X-RapidAPI-Key': '2700cac5b5msh2621b9602e858f1p117364jsn648fb90776eb'}
    result = requests.get(nUrl, headers=headers)
    jsonFromat = result.json()
    funds = jsonFromat['result']['funds']
    fundList = []
    sentimentList = []
    for item in funds:
        fundList.append(item['symbol'])
    for item in sentimentList:
        sentimentList.append(item['sentimentscore'])
    return render_template('sentiment.html', jsonFromat=jsonFromat, fundList=fundList, sentimentList=sentimentList)