from IBKR.ibkrApi import ibkrApi as ibkr

try:
    ib = ibkr()
    #ib.orderStatusEvent += onOrderUpdate
    ib.connect(host='127.0.0.1', port=7496, clientId=1)
    Trading = True

    try:
        mintickrule = ib.reqMarketRule(110)
        print(mintickrule)
        rulelowthresh = float(mintickrule[0][0])
        rulelowtick = float(mintickrule[0][1])
        rulehighthresh = float(mintickrule[1][0])
        rulehightick = float(mintickrule[1][1])


    except:
        rulelowthresh = float(0)
        rulelowtick = float(.05)
        rulehighthresh = float(3.00)
        rulehightick = float(0.1)

except:
    print(
        "--------------------------------------------------------------------------------------------------------------------------------")
    print(
        "Trading offline: There was a problem connecting to IB. Make sure Trader Workstation is open and try restarting the python script")
    print(
        "--------------------------------------------------------------------------------------------------------------------------------")
    Trading = False


ib.openPosition()