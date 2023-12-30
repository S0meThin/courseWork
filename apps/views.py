from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.views import View
from django.urls import reverse
from .models import itemList, orders, itemOrdered, transactions, returns, Store
import json
from django.db.models import Q
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt
import random
import calendar
from django.contrib.auth.decorators import login_required

#helps create a unique order number
def getADelN(orders):
    newDelN = f'{random.randrange(1, 10**9):09}'
    for order in orders:
        if newDelN == order.delN:
            return getADelN(orders)
    return newDelN

#sorts from highest to lowest by total
def sortFn(value):
    return value["total"]

# Create your views here.
class AppsView(View):
    def default(request):
        return HttpResponseRedirect(reverse('mainMenu'))

    #article lookup page
    @login_required(login_url='/login/')
    def artLookup(request):
        if request.method == "GET":
            return render(request, 'articleLookup.html')
    
    #inventory corrections
    @csrf_exempt
    @login_required(login_url='/login/')
    def inventoryCount(request):
        if request.method == "GET":
            return render(request, 'inventoryCount.html')
        
        elif request.method == "PUT":
            store = Store.objects.get(number = request.user.store)
            req = json.loads(request.body)
            try:
                obj = itemList.objects.get(UPC=req["upc"], store = store)
                old = int(obj.oh)
                obj.oh = req['qty']
                obj.save()

                diff = int(req['qty']) - old
                btran = transactions(store = store, item = obj, type = "Inv. corr", qty = diff, timeTr = datetime.now())
                btran.save()
            except itemList.DoesNotExist:
                return HttpResponse(status=400)
            return HttpResponse(status=200)

    #on order
    @login_required(login_url='/login/')
    def onOrder(request):
        if request.method == "GET":
            store = Store.objects.get(number = request.user.store)
            list_of_orders = orders.objects.all().filter(store = store).values()
            return render(request, 'OnOrder.html', {
                "list_of_orders": list_of_orders,
            })

    #manual order
    @csrf_exempt
    @login_required(login_url='/login/')
    def manualOrder(request):
        if request.method == "GET":
            return render(request, 'ManualOrder.html')
        elif request.method == "POST":
            store = Store.objects.get(number = request.user.store)
            req = json.loads(request.body)
            try:
                for r in req:
                    obj = itemList.objects.get(UPC=r["upc"], store = store)
                    newSuitOrder = ''

                    r1=Q(dateD__gt = datetime.now())
                    r2=Q(status=False)
                    r3=Q(store = store)

                    suitableOrders = orders.objects.filter(r1 & r2 & r3)
                    #try to get the products in an already existing order
                    if len(suitableOrders):
                        newSuitOrder = suitableOrders.first() 
                    
                    #if there isnt one, create a new one
                    else:
                        newDelN = getADelN(suitableOrders)

                        newOrder = orders(store = store, delN = newDelN, dateO = datetime.now(), dateD = datetime.now()+timedelta(days=2), status = False)
                        newOrder.save()
                        newSuitOrder = newOrder

                    items = itemOrdered.objects.filter(order = newSuitOrder)
                    areAny = False

                    for i in items:
                        if i.item == obj:
                            areAny = True
                            i.qty += int(r['qty'])
                            i.save()
                    if (areAny == False):
                        orderitem = itemOrdered(order = newSuitOrder, item = obj, qty = r['qty'])
                        orderitem.save()

            except itemList.DoesNotExist:
                return HttpResponse(status=400)
            return HttpResponse(status=200)

    #receiving
    @csrf_exempt
    @login_required(login_url='/login/')
    def receiving(request):
        if request.user.allowedToReceive == False:
            return HttpResponse(status=433)
        if request.method == "GET":
            return render(request, 'receiving.html')
        if request.method == "POST":
            store = Store.objects.get(number = request.user.store)
            req = json.loads(request.body)
            try:
                obj = orders.objects.get(store = store, delN = req["delN"])
                
                if obj.status == True:
                    return HttpResponse(status = 444)
                obj.status = True
                obj.save()

                orderItems = itemOrdered.objects.filter(order = obj)
                for i in orderItems:
                    l = i.item
                    l.oh += (i.qty * i.item.pack)
                    l.save()
                    
                    btran = transactions(store = store, item = i.item, type = "Received", qty = (i.qty*i.item.pack), timeTr = datetime.now())
                    btran.save()

            except itemList.DoesNotExist:
                return HttpResponse(status=400)
            return HttpResponse(status=200)

    #order info
    @login_required(login_url='/login/')
    def orderInfo(request, order_n):
        if request.method == "GET":
            store = Store.objects.get(number = request.user.store)

            finalobject = {
                "ord_n": 'NA',
                "expDelD": 'NA',
                "numberOfP": 'NA'
            }

            try:
                order = orders.objects.get(store = store,delN = order_n)
                finalobject['ord_n'] = order.delN
                if order.status == True:
                    finalobject['ord_n'] = 'RCD'
                finalobject['expDelD'] = str(order.dateD)
                try:
                    total = 0
                    itemorderinfo = itemOrdered.objects.all().filter(order = order)
                    for i in itemorderinfo:
                        total+=int(i.qty)
                    finalobject['numberOfP'] = total
                except itemOrdered.DoesNotExist:
                    return HttpResponse(status=400)
            except orders.DoesNotExist:
                finalobject['ord_n'] = "NA"
            
            finaljson = json.dumps(finalobject)
            return HttpResponse(finaljson, content_type = 'application/json')

    #returns
    @csrf_exempt
    @login_required(login_url='/login/')
    def return_f(request):
        if request.method == "GET":
            return render(request, 'returns.html')
        elif request.method == "PUT":
            store = Store.objects.get(number = request.user.store)
            req = json.loads(request.body)
            try:
                obj = itemList.objects.get(store = store, UPC=req["upc"])
                if int(obj.oh) - int(req['qty']) < 0:
                    return HttpResponse(status=444)
                obj.oh = int(obj.oh) - int(req['qty'])
                obj.save()

                b = returns(store = store, item = obj, dateR = datetime.now(), qty = req['qty'], user = request.user.username, status = False)
                b.save()

                btran = transactions(store = store, item = obj, type = "Return", qty = req['qty'], timeTr = datetime.now())
                btran.save()
            except itemList.DoesNotExist:
                return HttpResponse(status=400)
            return HttpResponse(status=200)
        
    #returns history
    @login_required(login_url='/login/')
    def returns_history(request):
        if request.method == "GET":
            store = Store.objects.get(number = request.user.store)
            rets = returns.objects.filter(store = store)
        return render(request, "returnsHistory.html", {
            "returns": rets
        })
        
    #sales analysis
    @login_required(login_url='/login/')
    def salesAnalysis(request):
        if request.user.allowedToSalesStat == False:
            return HttpResponse(status=433)
        if request.method == "GET":
            store = Store.objects.get(number = request.user.store)
            today = datetime.now()

            year = today.year
            month = today.month
            if month == 1:
                month = 13
                year = year-1

            month = month - 1

            tran = transactions.objects.filter(store = store, timeTr__year = year, timeTr__month = month)
            ret = returns.objects.filter(store = store, dateR__year = year, dateR__month = month)

            returnsList = []
            salesList = []

            for t in tran:
                if t.type == "Sale":
                    salesList.append(t)

            for r in ret:
                returnsList.append(r)

            topReturnsList = []

            totalP=0
            totalMONEY=0

            for r in returnsList:
                totalP+=r.qty
                totalMONEY+=r.item.price*r.qty
                topReturnsList.append({"upc": r.item.UPC, "total": r.item.price * r.qty})
            
            topReturnsList.sort(key=sortFn, reverse=True)
            del topReturnsList[5:]

            finalObject = {
                "month": calendar.month_name[month],
                "returns": [],
                "sales":[],
                "info": {
                    "turnover": '',
                    "profit": '',
                    "totalPRet": '',
                    "totalRet": ''
                }
            }

            for r in returnsList:
                obj = {
                    "name": r.item.name,
                    "upc": r.item.UPC,
                    "qty": r.qty,
                    "user": r.user,
                    "price": round(r.item.price*r.qty, 2),
                    "retail": round(r.item.retail*r.qty, 2), 
                    "date": r.dateR
                }
                finalObject["returns"].append(obj)
            
            turnover = 0
            profit = 0

            topSalesList = []

            items = itemList.objects.all().filter(store = store)
            for i in items:
                total = 0
                for s in salesList:
                    if s.item == i:
                        total += s.qty
                if total > 0:
                    topSalesList.append({"upc": i.UPC, "total": total})

            for s in topSalesList:
                i = items.get(UPC = s["upc"])
                turnover += i.retail * s["total"]
                profit += (i.retail * s["total"]) - (i.price * s["total"])

            topSalesList.sort(key=sortFn, reverse=True)
            del topSalesList[5:]

            for s in topSalesList:
                i = items.get(UPC = s["upc"])
                obj = {
                    "name": i.name,
                    "upc": i.UPC,
                    "qty": s["total"],
                    "price": round(i.price * s["total"],2),
                    "retail": round(i.retail * s["total"],2)
                }
                finalObject["sales"].append(obj)
            
            finalObject["info"]["turnover"] = turnover
            finalObject["info"]["profit"] = round(profit,2)
            finalObject["info"]["totalPRet"] = totalP
            finalObject["info"]["totalRet"] = round(totalMONEY,2)

            return render(request, 'salesAnalysis.html', {"info": finalObject})

    #pull up order by number   
    @login_required(login_url='/login/')
    def order(request, order_n):
        if request.method == "GET":
            store = Store.objects.get(number = request.user.store)
            ord = orders.objects.get(store = store, delN = order_n)
            orderitems = itemOrdered.objects.all().filter(order = ord)

            finalItems = []
            for i in orderitems:
                temp = {"name": i.item.name, "upc": i.item.UPC, "qty": i.qty}
                finalItems.append(temp)
            return render(request, 'Order.html', {
                "stuff": finalItems,
                "delN": order_n,
                "order": ord,
            })

    #pull up item by upc
    @login_required(login_url='/login/')
    def item(request, upc):
        if request.method == "GET":
            try:
                store = Store.objects.get(number = request.user.store)
            except Store.DoesNotExist:
                store = Store(number = request.user.store)
                store.save()
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
                iteminfo = itemList.objects.get(store = store, UPC = upc)
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
                    for t in last_w:
                        total_sales+=t.qty
                    finalobject['transaction']['avg'] = str((total_sales)/7)
                    for trn in transactionsinfo:
                        index+=1
                        finalobject['transaction']['list'].append({"type":trn.type, "qty": trn.qty, "date":str(trn.timeTr)})
                        if index == 10:
                            break
                except transactions.DoesNotExist:
                    pass
                        
            except itemList.DoesNotExist:
                iteminfo = None
                finalobject['main'] = "NA"

            finaljson = json.dumps(finalobject)
            return HttpResponse(finaljson, content_type = 'application/json')