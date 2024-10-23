
r1 = "0 8 0 7" + " 0" * 3 + " 9 4"
r2 = "0 6 0 9 0 0 0 0 0"
r3 = "0 3 0 0 8 4 0 7 1"
r4 = "2 0 0 0 9 0 0 4 0"
r5 = "0 0 0 3 0 0 0 5 0"
r6 = "0 0 8 0 0 0 0 0 0 "
r7 = "0 " * 5 + "7 0 3 0"
r8 = "7 4 0 0 0 3 9 0 5"
r9 = "1 0 0 0 0 0 0 0 6"

rows = []
# rows_int = []
for k in range(1,10):
    a = f"r{k}"
    # eval(f"print(r{k})")
    eval(f"rows.append([r for r in r{k}.split()])")
    # eval(f"rows_int.append([int(r) for r in r{k}.split()])")

for row in rows:
    print(" , ".join(row))

