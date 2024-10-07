def theGen(genFlg=False):
    for i in range(100):
        s1 = f"Number_{i+1}th return\n"
        s2 = f"\tvalue is {i}"
        if genFlg == True:
            yield s1+s2
        else:
            print(f"non-gen:{s1+s2}")
    if genFlg==True:
        yield 'Done'
    else:
        return 0

# s = theGen(genFlg=True)
# while True:
#     p = next(s)
#     print(p)
#     if 'Done' in p:
#         break
#     if 'Completed' in p:
#         break
# print("gen test finished")

v = theGen()
print("non-gen test finished")