def testrecursive(num):
    for i in range(1,10):

        if num == 1 or i == 10:
            print("function done")
            quit

        else:
            print("function runs again")
            print(num)
            testrecursive(num-1)

testrecursive(5)



