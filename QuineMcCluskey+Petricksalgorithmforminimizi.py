# Quine McCluskey algorithm for minimizing logical expressions + Petrick's method directly from the expression

all_states = []
litere = []


def mul(x, y):  # Multiply 2 minterms
    res = []
    for i in x:
        if i + "'" in y or (len(i) == 2 and i[0] in y):
            return []
        else:
            res.append(i)
    for i in y:
        if i not in res:
            res.append(i)
    return res


def multiply(x, y):  # Multiply 2 expressions
    res = []
    for i in x:
        for j in y:
            tmp = mul(i, j)
            res.append(tmp) if len(tmp) != 0 else None
    return res


def refine(
    my_list, dc_list
):  # Removes don't care terms from a given list and returns refined list
    res = []
    for i in my_list:
        if int(i) not in dc_list:
            res.append(i)
    return res


def findEPI(
    x,
):  # Function to find essential prime implicants from prime implicants chart
    res = []
    for i in x:
        if len(x[i]) == 1:
            res.append(x[i][0]) if x[i][0] not in res else None
    return res


def findVariables(
    x,
):  # Function to find variables in a meanterm. For example, the minterm --01 has C' and D as variables
    var_list = []
    for i in range(len(x)):
        if x[i] == "0":
            var_list.append("¬" + litere[i])
        elif x[i] == "1":
            var_list.append(litere[i])
    if len(var_list) == 0:
        return "T"
    return var_list


def flatten(x):  # Flattens a list
    flattened_items = []
    for i in x:
        flattened_items.extend(x[i])
    return flattened_items


def findminterms(
    a,
):  # Function for finding out which minterms are merged. For example, 10-1 is obtained by merging 9(1001) and 11(1011)
    gaps = a.count("-")
    if gaps == 0:
        return [str(int(a, 2))]
    x = [bin(i)[2:].zfill(gaps) for i in range(pow(2, gaps))]
    temp = []
    for i in range(pow(2, gaps)):
        temp2, ind = a[:], -1
        for j in x[0]:
            if ind != -1:
                ind = ind + temp2[ind + 1 :].find("-") + 1
            else:
                ind = temp2[ind + 1 :].find("-")
            temp2 = temp2[:ind] + j + temp2[ind + 1 :]
        temp.append(str(int(temp2, 2)))
        x.pop(0)
    if len(temp) == 0:
        temp.append("T")
    return temp


def compare(a, b):  # Function for checking if 2 minterms differ by 1 bit only
    c = 0
    for i in range(len(a)):
        if a[i] != b[i]:
            mismatch_index = i
            c += 1
            if c > 1:
                return (False, None)
    return (True, mismatch_index)


def removeTerms(_chart, terms):  # Removes minterms which are already covered from chart
    for i in terms:
        for j in findminterms(i):
            try:
                del _chart[j]
            except KeyError:
                pass


#####################################################################################################################
def da(s, l, r):

    if l == r:
        if s[l] >= "A" and s[l] <= "Z":
            return 1
        return 0

    if s[l] != "(" or s[r] != ")":
        return 0

    if (
        (s[l + 1] == "¬")
        and (s[r - 1] >= "A")
        and (s[r - 1] <= "Z")
        and (r - l + 1 == 4)
    ):
        return 1

    if s[l + 1] == "¬":
        return da(s, l + 2, r - 1)

    now = 0
    for i in range(l + 1, r):
        if s[i] == "(":
            now += 1
        if s[i] == ")":
            now -= 1
        if (s[i] == "⇒" or s[i] == "⇔" or s[i] == "∨" or s[i] == "∧") and now == 0:
            return da(s, l + 1, i - 1) and da(s, i + 1, r - 1)
    return 0


def strict_structure(s):

    # propozitie atomica
    if len(s) == 1 and s[0] >= "A" and s[0] <= "Z":
        return s

    # initializare
    open = 0
    closed = 0
    x = 0
    good = 1
    st = 0
    dr = len(s) - 1
    for i in range(len(s)):
        it = s[i]
        if it == "(":
            x += 1
        if it == ")":
            x -= 1
        if x == 0 and i > 0 and i < len(s) - 1:
            good = 0
    if s[dr] == ")" and s[st] == "(" and good:
        st += 1
        dr -= 1
    cur = ""  # componenta

    # equivalence
    l = []
    while st <= dr:
        i = st
        if s[i] == ")":
            closed += 1
        if s[i] == "(":
            open += 1
        if (s[i] == "⇔") and (open == closed):
            l.append(cur)
            cur = ""
        else:
            cur += s[i]
        st += 1

    ans = ""
    if len(l) != 0:
        for i in range(len(l)):
            ans += ")"

        ans = strict_structure(cur) + ans

        l.reverse()  # stored components

        for i in range(len(l)):
            ans = "(" + strict_structure(l[i]) + "⇔" + ans

        return ans

    # initializare
    open = 0
    closed = 0
    x = 0
    good = 1
    st = 0
    dr = len(s) - 1
    for i in range(len(s)):
        it = s[i]
        if it == "(":
            x += 1
        if it == ")":
            x -= 1
        if x == 0 and i > 0 and i < len(s) - 1:
            good = 0
    if s[dr] == ")" and s[st] == "(" and good:
        st += 1
        dr -= 1
    cur = ""  # componenta

    # implication
    l = []
    while st <= dr:
        i = st
        if s[i] == ")":
            closed += 1
        if s[i] == "(":
            open += 1
        if (s[i] == "⇒") and (open == closed):
            l.append(cur)
            cur = ""
        else:
            cur += s[i]
        st += 1

    ans = ""
    if len(l) != 0:
        for i in range(len(l)):
            ans += ")"

        ans = strict_structure(cur) + ans

        l.reverse()  # stored components

        for i in range(len(l)):
            ans = "(" + strict_structure(l[i]) + "⇒" + ans

        return ans

    # initializare
    open = 0
    closed = 0
    x = 0
    good = 1
    st = 0
    dr = len(s) - 1
    for i in range(len(s)):
        it = s[i]
        if it == "(":
            x += 1
        if it == ")":
            x -= 1
        if x == 0 and i > 0 and i < len(s) - 1:
            good = 0
    if s[dr] == ")" and s[st] == "(" and good:
        st += 1
        dr -= 1
    cur = ""  # componenta

    # or and and
    l = []
    l1 = []
    while st <= dr:
        i = st
        if s[i] == ")":
            closed += 1
        if s[i] == "(":
            open += 1
        if (s[i] == "∨" or s[i] == "∧") and (open == closed):
            l1.append(s[i])
            l.append(cur)
            cur = ""
        else:
            cur += s[i]
        st += 1

    ans = ""
    if len(l) != 0:
        for i in range(len(l)):
            ans += ")"

        ans = strict_structure(cur) + ans

        l.reverse()  # stored components
        l1.reverse()  # stored binary operators

        for i in range(len(l)):
            ans = "(" + strict_structure(l[i]) + l1[i] + ans

        return ans
    # negatie
    if s[0] == "¬":
        ans = ""
        for i in range(1, len(s)):
            ans += s[i]
        return "(¬" + strict_structure(ans) + ")"

    # negatie cu paranteze
    if s[0] == "(" and s[1] == "¬" and s[len(s) - 1] == ")":
        ans = ""
        for i in range(2, len(s) - 1):
            ans += s[i]
        return "(¬" + strict_structure(ans) + ")"

    return s


def val(s, l, r):

    if l == r:
        return 1 - (1 - (s[l] == "1"))

    if (
        (s[l + 1] == "¬")
        and (s[r - 1] >= "A")
        and (s[r - 1] <= "Z")
        and (r - l + 1 == 4)
    ):
        return 1 - (1 - (s[r - 1] == "0"))

    if s[l + 1] == "¬":
        return 1 - val(s, l + 2, r - 1)

    now = 0
    for i in range(l + 1, r):
        if s[i] == "(":
            now += 1
        if s[i] == ")":
            now -= 1
        if s[i] == "⇒" and now == 0:
            return (1 - val(s, l + 1, i - 1)) or val(s, i + 1, r - 1)
        if s[i] == "⇔" and now == 0:
            return val(s, l + 1, i - 1) == val(s, i + 1, r - 1)
        if s[i] == "∨" and now == 0:
            return val(s, l + 1, i - 1) or val(s, i + 1, r - 1)
        if s[i] == "∧" and now == 0:
            return val(s, l + 1, i - 1) and val(s, i + 1, r - 1)
    return 0


print("Insert expression : ", end="")
s = input()
s = s.split()
s = "".join(s)
s = strict_structure(s)

ans = da(s, 0, len(s) - 1)
if not ans:
    print("Nu este formula propozitionala bine formata")
    exit()

litere = set(litere)
d = dict()
for it in s:
    if it >= "A" and it <= "Z":
        litere.add(it)
        d[it] = 0
cnt = len(litere)
litere = list(litere)
litere.sort()

mt = []

# printing the letters
print("", end=" | ")
for it in litere:
    print(it, end=" | ")
print(s)
# generating the truth table
for i in range(2 ** cnt):
    cur = ""
    for j in range(cnt):
        if ((2 ** j) & i) != 0:
            cur += "1"
        else:
            cur += "0"
    cur = cur[::-1]

    x = 0
    for it in litere:
        d[it] = cur[x]
        x += 1

    g = ""
    for it in s:
        if it >= "A" and it <= "Z":
            g += d[it]
        else:
            g += it
        # printing the line in the truth table
    print("", end=" | ")
    for it in cur:
        print(it, end=" | ")
    nw = val(g, 0, len(g) - 1)

    if nw:
        mt.append(i)
    print(nw)

print("MT = ", mt)

if len(mt) == 0:
    print("F = ⊥")
    exit()


mt.sort()
dc = []
minterms = mt
minterms.sort()
size = len(bin(minterms[-1])) - 2
groups, all_pi = {}, set()

# Primary grouping starts
for minterm in minterms:
    try:
        groups[bin(minterm).count("1")].append(bin(minterm)[2:].zfill(size))
    except KeyError:
        groups[bin(minterm).count("1")] = [bin(minterm)[2:].zfill(size)]
# Primary grouping ends

# Primary group printing starts
print("\n\n\n\nGroup No.\tMinterms\tBinary of Minterms\n%s" % ("=" * 50))
for i in sorted(groups.keys()):
    print("%5d:" % i)  # Prints group number
    for j in groups[i]:
        print(
            "\t\t    %-20d%s" % (int(j, 2), j)
        )  # Prints minterm and its binary representation
    print("-" * 50)
# Primary group printing ends

# Process for creating tables and finding prime implicants starts

while True:
    tmp = groups.copy()
    groups, m, marked, should_stop = {}, 0, set(), True
    l = sorted(list(tmp.keys()))
    current_state = []
    # print(current_state)
    for i in range(len(l)):
        for j in tmp[l[i]]:  # Loop which iterates through current group elements
            if len(findVariables(j)) > 0:
                current_state.append("".join(findVariables(j)))
            if i == len(l) - 1:
                continue
            for k in tmp[l[i + 1]]:  # Loop which iterates through next group elements
                if len(findVariables(k)) > 0:
                    current_state.append("".join(findVariables(k)))
                res = compare(j, k)  # Compare the minterms
                if res[0]:  # If the minterms differ by 1 bit only
                    try:
                        # current_state.append(j[: res[1]] + "-" + j[res[1] + 1 :])
                        groups[m].append(j[: res[1]] + "-" + j[res[1] + 1 :]) if j[
                            : res[1]
                        ] + "-" + j[res[1] + 1 :] not in groups[
                            m
                        ] else None  # Put a '-' in the changing bit and add it to corresponding group
                    except KeyError:
                        # current_state.append(j[: res[1]] + "-" + j[res[1] + 1 :])
                        groups[m] = [
                            j[: res[1]] + "-" + j[res[1] + 1 :]
                        ]  # If the group doesn't exist, create the group at first and then put a '-' in the changing bit and add it to the newly created group
                    should_stop = False
                    marked.add(j)  # Mark element j
                    marked.add(k)  # Mark element k
        m += 1
    local_unmarked = set(flatten(tmp)).difference(
        marked
    )  # Unmarked elements of each table
    # print(current_state)
    for it in all_pi:
        current_state.append("".join(findVariables(it)))
    if len(current_state) > 0:
        current_state = set(current_state)
        all_states.append(" ∨ ".join(current_state))

    all_pi = all_pi.union(local_unmarked)  # Adding Prime Implicants to global list

    # print("Till now : ", current_state)

    print(
        "Unmarked elements(Prime Implicants) of this table:",
        None if len(local_unmarked) == 0 else ", ".join(local_unmarked),
    )  # Printing Prime Implicants of current table
    if should_stop:  # If the minterms cannot be combined further
        print(
            "\n\nAll Prime Implicants: ",
            None if len(all_pi) == 0 else ", ".join(all_pi),
        )  # Print all prime implicants
        break
    # Printing of all the next groups starts
    print("\n\n\n\nGroup No.\tMinterms\tBinary of Minterms\n%s" % ("=" * 50))
    for i in sorted(groups.keys()):
        print("%5d:" % i)  # Prints group number
        for j in groups[i]:
            print(
                "\t\t%-24s%s" % (",".join(findminterms(j)), j)
            )  # Prints minterms and its binary representation
        print("-" * 50)
    # Printing of all the next groups ends
# Process for creating tables and finding prime implicants ends


# Printing and processing of Prime Implicant chart starts
sz = len(str(mt[-1]))  # The number of digits of the largest minterm
chart = {}
print(
    "\n\n\nPrime Implicants chart:\n\n    Minterms    |%s\n%s"
    % (
        " ".join((" " * (sz - len(str(i)))) + str(i) for i in mt),
        "=" * (len(mt) * (sz + 1) + 16),
    )
)
for i in all_pi:
    merged_minterms, y = findminterms(i), 0
    print("%-16s|" % ",".join(merged_minterms), end="")
    for j in refine(merged_minterms, dc):
        x = mt.index(int(j)) * (sz + 1)  # The position where we should put 'X'
        print(" " * abs(x - y) + " " * (sz - 1) + "X", end="")
        y = x + sz
        try:
            chart[j].append(i) if i not in chart[j] else None  # Add minterm in chart
        except KeyError:
            chart[j] = [i]
    print("\n" + "-" * (len(mt) * (sz + 1) + 16))
# Printing and processing of Prime Implicant chart ends

EPI = findEPI(chart)  # Finding essential prime implicants
print("\nEssential Prime Implicants: " + ", ".join(str(i) for i in EPI))
removeTerms(chart, EPI)  # Remove EPI related columns from chart

neededPetrick = 1
if len(chart) == 0:  # If no minterms remain after removing EPI related columns
    final_result = [findVariables(i) for i in EPI]  # Final result with only EPIs
    neededPetrick = 0
else:  # Else follow Petrick's method for further simplification
    P = [[findVariables(j) for j in chart[i]] for i in chart]
    while len(P) > 1:  # Keep multiplying until we get the SOP form of P
        P[1] = multiply(P[0], P[1])
        P.pop(0)
    final_result = [
        min(P[0], key=len)
    ]  # Choosing the term with minimum variables from P
    final_result.extend(
        findVariables(i) for i in EPI
    )  # Adding the EPIs to final solution

answer = all_states

for i in range(len(answer)):
    it = answer[i]
    if i == len(answer) - 1 and neededPetrick:
        print(it, "  ∼  (Acoperire minima Petrick's Method) ")
    else:
        print(it, "  ∼  (Distributivitate + Anihilare) ")
if len(" ∨ ".join("".join(i) for i in final_result)) == 0:
    print("T")
else:
    print(" ∨ ".join("".join(i) for i in final_result))

if len(" ∨ ".join("".join(i) for i in final_result)) == 0:
    print("\n\nSolution: F = ⊤")
else:
    print("\n\nSolution: F = " + " ∨ ".join("".join(i) for i in final_result))

input("\nPress enter to exit...")
