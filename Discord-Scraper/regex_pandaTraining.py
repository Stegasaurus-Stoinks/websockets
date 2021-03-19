import re



"""
BTO CRWD $210C 3/26 @2.38
 Long: CRWD Mar 26 2021 $210.00 Call @ 2.38 | market : $2.4

STC FSLY 77c 3/19 @.19 all
 Closed long: FSLY Mar 19 2021 $77.00 Call @ 0.19 | market : $0.19

STC NFLX 500p 3/19 @1.45
Closed long: NFLX Mar 19 2021 $500.00 Put @ 1.45 | market : $1.45

BTO FB 280p 3/19 @1.42 yolo still above 281.50 is strength but risking it
Long: FB Mar 19 2021 $280.00 Put @ 1.42 | market : $1.35

STC SQQQ 3/26/21 13P @ 0.66 (bot)
Closed long: SQQQ Mar 26 2021 $13.00 Put @ 0.66 | market : $0.36
"""


testy = "BTO CRWD $210.00C 3/26 @2.38"
x = re.split("\s", testy, 2)
print(x)
part1 = x[0]
part2 = x[1]
part3 = x[2]
print(part3)
price = re.search("[$]*[0-9.]*[cCpP]", part3)
print("Price = " + price.group())
date = re.search("[0-9]+[/][0-9]+[0-9/]*", part3)
print("Date = " + date.group())
putThing = re.search("[@][0-9.]+[0-9.]+", part3)
print("putThing = " + putThing.group())





#def securityCheck(message):