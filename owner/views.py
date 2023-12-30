import calendar
from datetime import datetime, timedelta
from http.client import HTTPResponse
from django.shortcuts import HttpResponse
from django.shortcuts import render
from apps.models import Store, transactions, itemList, returns, itemOrdered, orders
from django.db.models import Q
import json 

def sortFn(value):
    return value["price"]

def mainPage(request):
    if request.user.is_authenticated:
        if request.user.owner:
            return render(request, 'mainPage.html')
        
def sales(request):
    if request.user.is_authenticated:
        if request.user.owner:
            if request.method == "GET":
                stores = Store.objects.all()
                return render(request, 'sales.html', {"stores": stores})
            
def salesInfo(request, store):
    if request.user.is_authenticated:
        if request.user.owner:
            if request.method == "GET":
                storeN = Store.objects.get(number = store)

                today = datetime.now()

                year = today.year
                month = today.month
                if month == 1:
                    month = 13
                    year = year-1

                month = month - 1

                turnover = 0
                profit = 0

                salesList = transactions.objects.filter(store = storeN, type = "Sale", timeTr__year = year, timeTr__month = month)

                for s in salesList:
                    profit+=s.qty*(s.item.retail - s.item.price)
                    turnover+=s.qty*s.item.retail
                    print(1)
                    print(s)
                
                SalesList = []

                for s in salesList:
                    SalesList.append(s)

                SalesList = SalesList[:5]
                print(SalesList)
                finalSalesList = []

                for s in SalesList:
                    obj = {
                        "name": s.item.name,
                        "upc": s.item.UPC,
                        "qty": s.qty,
                        "price": round(s.item.price * s.qty,2),
                        "retail": round(s.item.retail * s.qty,2)
                    }
                    finalSalesList.append(obj)


                finalObject= {
                    "month": calendar.month_name[month],
                    "transactions": finalSalesList,
                    "profit": profit,
                    "turnover": turnover
                }

                finaljson = json.dumps(finalObject)
                return HttpResponse(finaljson, content_type = 'application/json')

def returnsO(request):
    if request.user.is_authenticated:
        if request.user.owner:
            if request.method == "GET":
                stores = Store.objects.all()
                return render(request, 'returnsO.html', {"stores": stores})

def returnsInfo(request, store):
    if request.user.is_authenticated:
        if request.user.owner:
            if request.method == "GET":
                storeN = Store.objects.get(number = store)

                today = datetime.now()

                year = today.year
                month = today.month
                if month == 1:
                    month = 13
                    year = year-1

                ret = returns.objects.filter(store = store, dateR__year = year, dateR__month = month)

                returnsList = []

                totalP=0
                totalMONEY=0

                for r in ret:
                    totalP += r.qty
                    totalMONEY += r.qty*r.item.price
                    returnsList.append(r)
            

                topReturnsList = []

                for s in returnsList:
                    obj = {
                        "name": s.item.name,
                        "upc": s.item.UPC,
                        "qty": s.qty,
                        "price": round(s.item.price * s.qty,2),
                        "retail": round(s.item.retail * s.qty,2),
                        "user": s.user
                    }
                    topReturnsList.append(obj)
                
                topReturnsList.sort(key=sortFn, reverse=True)

                topReturnsList = topReturnsList[:5]
                finalObject = {
                    "month": calendar.month_name[month],
                    "transactions": topReturnsList,
                    "totalP": totalP,
                    "totalM": totalMONEY
                }
                finaljson = json.dumps(finalObject)
                return HttpResponse(finaljson, content_type = 'application/json')

def items(request):
    if request.user.is_authenticated:
        if request.user.owner:
            if request.method == "GET":
                stores = Store.objects.all()
                return render(request, 'itemsInfo.html', {"stores": stores})

def itemsInfo(request, store, item):
    if request.user.is_authenticated:
        if request.user.owner:
            if request.method == "GET":
                storeN = Store.objects.get(number = store)

                finalobject = {
                "main": {
                    "name": 'NA',
                    "oh": 'NA',
                    "pack": 'NA',
                    "oo": 'NA',
                    "nsd": 'NA',
                    "or": 'NA',
                    "nrd": 'NA'
                },
                "transaction":{
                    "list": [],
                    "avg": ''
                }

            }

            try:
                iteminfo = itemList.objects.get(store = storeN, UPC = item)
                finalobject['main']['name'] = iteminfo.name
                finalobject['main']['oh'] = iteminfo.oh
                finalobject['main']['pack'] = iteminfo.pack
                try:
                    orderdate = "NA"
                    onorder = "NA"
                    itemorderinfo = itemOrdered.objects.all().filter(item = iteminfo)
                    ordersinfo = orders.objects.order_by('dateD').filter(store = store, status = False)
                    for ord in ordersinfo:
                        for item in itemorderinfo:
                            if item.order == ord:
                                orderdate = ord.dateD
                                onorder = item.qty
                                break
                    finalobject['main']['nsd'] = str(orderdate)
                    finalobject['main']['oo'] = onorder
                except itemOrdered.DoesNotExist:
                    pass
                
                try:
                    returnsinfo = returns.objects.order_by('dateR').all().filter(store = store, item = iteminfo)
                    for ret in returnsinfo:
                        if ret.status == False:
                            finalobject['main']['or'] = ret.qty
                            finalobject['main']['nrd'] = str(ret.dateR)
                            break
                except returns.DoesNotExist:
                    pass

                try:
                    transactionsinfo = transactions.objects.filter(store = store, item = iteminfo)
                    index = 0
                    r1 = Q(timeTr__gte = datetime.now()-timedelta(days=7))
                    r2 = Q(type = 'Sale')
                    last_w = transactionsinfo.filter(r1&r2)
                    total_sales = 0
                    print(last_w)
                    for t in last_w:
                        total_sales+=t.qty
                    finalobject['transaction']['avg'] = str((total_sales)/7)
                    print(total_sales)
                    for trn in transactionsinfo:
                        index+=1
                        finalobject['transaction']['list'].append({"type":trn.type, "qty": trn.qty})
                        if index == 10:
                            break
                except transactions.DoesNotExist:
                    pass
                        
            except itemList.DoesNotExist:
                iteminfo = None
                finalobject['main'] = "NA"

            finaljson = json.dumps(finalobject)

            return HttpResponse(finaljson, content_type = 'application/json')
