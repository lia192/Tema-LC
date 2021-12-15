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

litere = set()
d = dict()
for it in s:
    if it >= "A" and it <= "Z":
        litere.add(it)
        d[it] = 0
cnt = len(litere)
litere = list(litere)
litere.sort()

clauze = []

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
    formula = []
    for it in litere:
        if cur[x] == "0":
            formula.append(it)
        else:
            formula.append("¬" + it)
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

    if not nw:
        clauze.append(",".join(formula))
    print(nw)


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


def echiv(s, negatie):

    if len(s) == 1:
        if negatie:
            return "(¬" + s[0] + ")"
        return s[0]

    if (s[1] == "¬") and (s[2] >= "A") and (s[2] <= "Z") and (len(s) == 4):
        if negatie:
            return s[2]
        return "(¬" + s[2] + ")"

    if s[1] == "¬":
        cur = s[2 : len(s) - 1]
        return echiv(cur, 1 - negatie)

    now = 0
    l = 0
    r = len(s) - 1
    for i in range(1, len(s) - 1):
        if s[i] == "(":
            now += 1
        if s[i] == ")":
            now -= 1
        if s[i] == "⇔" and now == 0:
            if negatie:
                return (
                    "(("
                    + echiv(s[l + 1 : i], 0)
                    + "∧"
                    + echiv(s[i + 1 : r], 1)
                    + ")∨("
                    + echiv(s[l + 1 : i], 1)
                    + "∧"
                    + echiv(s[i + 1 : r], 0)
                    + "))"
                )
            return (
                "(("
                + echiv(s[l + 1 : i], 1)
                + "∧"
                + echiv(s[i + 1 : r], 1)
                + ")∨("
                + echiv(s[l + 1 : i], 0)
                + "∧"
                + echiv(s[i + 1 : r], 0)
                + "))"
            )
        if s[i] == "⇒" and now == 0:
            if negatie:
                return (
                    "(¬(" + echiv(s[l + 1 : i], 0) + "⇒" + echiv(s[i + 1 : r], 0) + "))"
                )
            return "(" + echiv(s[l + 1 : i], 0) + "⇒" + echiv(s[i + 1 : r], 0) + ")"
        if s[i] == "∨" and now == 0:
            if negatie:
                return "(" + echiv(s[l + 1 : i], 1) + "∧" + echiv(s[i + 1 : r], 1) + ")"
            return "(" + echiv(s[l + 1 : i], 0) + "∨" + echiv(s[i + 1 : r], 0) + ")"
        if s[i] == "∧" and now == 0:
            if negatie:
                return "(" + echiv(s[l + 1 : i], 1) + "∨" + echiv(s[i + 1 : r], 1) + ")"
            return (
                "("
                + echiv(s[l + 1 : i], negatie)
                + "∧"
                + echiv(s[i + 1 : r], negatie)
                + ")"
            )

    return s[l : r + 1]


### ((¬(P⇒Q))⇔((P∨Q)∧((¬P)⇒Q)))
### ((¬(P⇒Q))⇒((P∨Q)∧((¬P)⇒Q))) ((¬(P⇒Q))⇒((P∨Q)∧((¬P)⇒Q)))
###  (  ((¬(P⇒Q))   ⇒   ((P∨Q)∧((¬P)⇒Q)))  ) ∧  (  ((P∨Q)∧((¬P)⇒Q)))  ⇒   ((¬(P⇒Q))    )


def implicatie(s, negatie):

    if len(s) == 1:
        if negatie:
            return "(¬" + s[0] + ")"
        return s[0]

    if (s[1] == "¬") and (s[2] >= "A") and (s[2] <= "Z") and (len(s) == 4):
        if negatie:
            return s[2]
        return "(¬" + s[2] + ")"

    if s[1] == "¬":
        cur = s[2 : len(s) - 1]
        return implicatie(cur, 1 - negatie)

    now = 0
    l = 0
    r = len(s) - 1
    for i in range(1, len(s) - 1):
        if s[i] == "(":
            now += 1
        if s[i] == ")":
            now -= 1
        if s[i] == "⇒" and now == 0:
            if negatie:
                return (
                    "("
                    + implicatie(s[l + 1 : i], 0)
                    + "∧"
                    + implicatie(s[i + 1 : r], 1)
                    + ")"
                )
            return (
                "("
                + implicatie(s[l + 1 : i], 1)
                + "∨"
                + implicatie(s[i + 1 : r], 0)
                + ")"
            )
        if s[i] == "∨" and now == 0:
            if negatie:
                return (
                    "("
                    + implicatie(s[l + 1 : i], 1)
                    + "∧"
                    + implicatie(s[i + 1 : r], 1)
                    + ")"
                )
            return (
                "("
                + implicatie(s[l + 1 : i], 0)
                + "∨"
                + implicatie(s[i + 1 : r], 0)
                + ")"
            )
        if s[i] == "∧" and now == 0:
            if negatie:
                return (
                    "("
                    + implicatie(s[l + 1 : i], 1)
                    + "∨"
                    + implicatie(s[i + 1 : r], 1)
                    + ")"
                )
            return (
                "("
                + implicatie(s[l + 1 : i], negatie)
                + "∧"
                + implicatie(s[i + 1 : r], negatie)
                + ")"
            )

    return s[l : r + 1]


def distribuie(s):

    # print("callh ", s)

    if len(s) == 1:
        return s

    if (s[1] == "¬") and (s[2] >= "A") and (s[2] <= "Z") and (len(s) == 4):
        return s

    #########
    now = 0
    l = 0
    r = len(s) - 1
    for i in range(1, len(s) - 1):
        if s[i] == "(":
            now += 1
        if s[i] == ")":
            now -= 1
        if s[i] == "∧" and now == 0:
            s = "(" + distribuie(s[1:i]) + "∧" + distribuie(s[i + 1 : r]) + ")"
            break
        if s[i] == "∨" and now == 0:
            s = "(" + distribuie(s[1:i]) + "∨" + distribuie(s[i + 1 : r]) + ")"
            break
    ###############

    perfect = 1
    for it in s:
        if it == "(" or it == ")" or it == "¬" or ((it >= "A") and (it <= "Z")):
            continue
        if it != "∨":
            perfect = 0

    if perfect:
        ans = ""
        for it in s:
            if it == "(" or it == ")":
                continue
            ans += it
        return s  # "(" + ans + ")"
    ############

    now = 0
    l = 0
    r = len(s) - 1
    for i in range(1, len(s) - 1):
        if s[i] == "(":
            now += 1
        if s[i] == ")":
            now -= 1
        if s[i] == "∨" and now == 0:
            l = halves(s[1:i])
            if len(l) == 3 and l[0] == "∧":
                return (
                    "(("
                    + distribuie(l[1])
                    + "∨"
                    + distribuie(s[i + 1 : r])
                    + ")∧("
                    + distribuie(l[2])
                    + "∨"
                    + distribuie(s[i + 1 : r])
                    + "))"
                )
            l = halves(s[i + 1 : r])
            if len(l) == 3 and l[0] == "∧":
                return (
                    "(("
                    + distribuie(l[1])
                    + "∨"
                    + distribuie(s[1:i])
                    + ")∧("
                    + distribuie(l[2])
                    + "∨"
                    + distribuie(s[1:i])
                    + "))"
                )
        if s[i] == "∧" and now == 0:
            return "(" + distribuie(s[1:i]) + "∧" + distribuie(s[i + 1 : r]) + ")"

    return s[l : r + 1]


def frumos(s):

    if len(s) == 1:
        return s

    if (s[1] == "¬") and (s[2] >= "A") and (s[2] <= "Z") and (len(s) == 4):
        return s

    ###############

    perfect = 1
    for it in s:
        if it == "(" or it == ")" or it == "¬" or ((it >= "A") and (it <= "Z")):
            continue
        if it != "∨":
            perfect = 0

    if perfect:
        ans = ""
        for it in s:
            if it == "(" or it == ")":
                continue
            ans += it
        return "(" + ans + ")"
    ############

    now = 0
    l = 0
    r = len(s) - 1
    for i in range(1, len(s) - 1):
        if s[i] == "(":
            now += 1
        if s[i] == ")":
            now -= 1
        if s[i] == "∧" and now == 0:
            return frumos(s[1:i]) + "∧" + frumos(s[i + 1 : r])

    return s[l : r + 1]


def halves(s):

    if len(s) == 1:
        return [s]

    if (s[1] == "¬") and (s[2] >= "A") and (s[2] <= "Z") and (len(s) == 4):
        return [s]

    now = 0
    l = 0
    r = len(s) - 1
    for i in range(1, len(s) - 1):
        if s[i] == "(":
            now += 1
        if s[i] == ")":
            now -= 1
        if s[i] == "∨" and now == 0:
            return ["∨", s[l + 1 : i], s[i + 1 : r]]
        if s[i] == "∧" and now == 0:
            return ["∧", s[l + 1 : i], s[i + 1 : r]]
    return [s]


def idempotenta(s):

    if len(s) == 1:
        return s

    if (s[0] == "¬") and (s[2] >= "A") and (s[2] <= "Z") and (len(s) == 2):
        return s

    ###############

    perfect = 1
    for it in s:
        if it == "(" or it == ")" or it == "¬" or ((it >= "A") and (it <= "Z")):
            continue
        if it != "∧":
            perfect = 0

    if perfect:
        ans = ""
        s = s[1 : len(s) - 1]
        x = s.split("∧")
        x = set(x)
        for it in x:
            ans += it + "∧"
        ans = ans[0 : len(ans) - 1]
        return "(" + ans + ")"
    ############

    now = 0
    l = 0
    r = len(s)
    for i in range(len(s)):
        if s[i] == "(":
            now += 1
        if s[i] == ")":
            now -= 1
        if s[i] == "∨" and now == 0:
            return idempotenta(s[0:i]) + "∨" + idempotenta(s[i + 1 : r])

    return s[l:r]


# b = rec(s, 0, len(s) - 1)
# b.display()

s = "(¬(F ⇔ G) ∨ ¬(G ⇒ H)) ∧ (G ∧ ¬H)"
print("Insert expression : ", end="")
s = input()
s = s.split()
s = "".join(s)
s = strict_structure(s)

ans = da(s, 0, len(s) - 1)
if not ans:
    print("Nu este formula propozitionala bine formata")
    exit()


print("Strict: ", s)

l = []
l.append(s)
s = echiv(s, 0)
l.append(s)
s = implicatie(s, 0)
l.append(s)

K = 0
while 1:
    new_s = distribuie(s)
    if s == new_s:
        break
    s = new_s
    l.append(s)
    K += 1


s = frumos(s)
l.append(s)

s = idempotenta(s)
l.append(s)

##idempotenta
componente = s.split("∧")
lst = []

for i in componente:
    if len(i) <= 2:
        x = i
    else:
        x = i[1 : len(i) - 1]
    lst.append("∨".join(set(x.split("∨"))))

if len(lst) == 0:
    lst.append("T")
l.append("(" + ")∧(".join(lst) + ")")
s = l[len(l) - 1]

#####
# letter = set()
# for it in "∨".join(componente):
# if it >= "A" and it <= "Z":
# letter.add(it)
# letter = list(letter)


def binary(s):
    if s[0] == "(":
        s = s[1 : len(s) - 1]
    s = set(s.split("∧"))

    bin = ["-"] * len(letter)
    for i in range(len(letter)):
        if letter[i] in s:
            bin[i] = "1"
        if ("¬" + letter[i]) in s:
            bin[i] = "0"
    return "".join(bin)


def factor_comun(forms):
    util = [1] * len(forms)
    new_forms = []

    for i in range(len(forms)):
        for j in range(len(forms)):
            if i == j:
                continue
            nr_dif = 0
            pos = -1
            for k in range(len(forms[i])):
                if forms[i][k] == forms[j][k]:
                    continue
                if (forms[i][k] == "-" and forms[j][k] != "-") or (
                    forms[j][k] == "-" and forms[i][k] != "-"
                ):
                    nr_dif += 1
                    continue
                nr_dif += 1
                pos = k
            if nr_dif == 1 and pos != -1:
                ans = ""
                for k in range(len(forms[i])):
                    if k == pos:
                        ans += "-"
                        continue
                    ans += forms[i][k]
                new_forms.append(ans)
                util[i] = 0
                util[j] = 0
    good = [forms[i] for i in range(len(forms)) if util[i]]
    good += new_forms
    good = set(good)
    good = list(good)
    return good


def idempotenta_2(forms):
    util = [1] * len(forms)
    new_forms = []

    for i in range(len(forms)):
        for j in range(len(forms)):
            if i == j:
                continue
            nr_dif = 0
            pos = set()
            type_left = 0
            type_right = 0
            for k in range(len(forms[i])):
                if forms[i][k] == forms[j][k]:
                    continue
                if forms[i][k] == "-" and forms[j][k] != "-":
                    nr_dif += 1
                    type_left += 1
                    continue
                if forms[j][k] == "-" and forms[i][k] != "-":
                    nr_dif += 1
                    type_right += 1
                    continue
                nr_dif += 1
                pos.add(k)

            if type_left and not type_right:
                ans = ""
                for k in range(len(forms[i])):
                    if k == pos:
                        ans += "-"
                        continue
                    ans += forms[i][k]
                new_forms.append(ans)
                util[i] = 0
            if type_left and not type_right:
                ans = ""
                for k in range(len(forms[j])):
                    if k in pos:
                        ans += "-"
                        continue
                    ans += forms[j][k]
                new_forms.append(ans)
                util[j] = 0
    good = [forms[i] for i in range(len(forms)) if util[i]]
    good += new_forms
    good = set(good)
    good = list(good)
    return good


def findVariables(
    x,
):  # Function to find variables in a meanterm. For example, the minterm --01 has C' and D as variables
    var_list = []
    for i in range(len(x)):
        if x[i] == "0":
            var_list.append("¬" + letter[i])
        elif x[i] == "1":
            var_list.append(letter[i])
    if len(var_list) == 0:
        return "T"
    if len(var_list) == 1:
        return "".join(var_list)
    return "(" + "∧".join(var_list) + ")"


print()
print()
print()
# print(l)
print("F = ", s)

################################################################
def good(a):
    A = a.split(",")
    for i in range(len(A)):
        for j in range(len(A)):
            if A[i] == ("¬" + A[j]) or A[j] == ("¬" + A[i]):
                return 0
    return 1


clauze = []

lst = s.split("∧")
for it in lst:
    if len(it) <= 2:
        clauze.append(",".join(it.split("∨")))
    else:
        x = it[1 : len(it) - 1]
        clauze.append(",".join(x.split("∨")))


print("Clauze = ", clauze)

if len(clauze) == 0:
    print("F = T")
    exit()

nr = 0
the = dict()
din = dict()
clauze.sort()

for it in clauze:
    the[it] = str(nr + 1)
    din[it] = str(nr + 1)
    nr += 1

for it in clauze:
    print("(" + the[it] + ")  ", "{ ", it, " } din ", din[it])


print()
print()
print()

clauze_noi = []
for it in clauze:
    if not good(it):
        continue
    clauze_noi.append(it)

clauze = []
clauze += clauze_noi


def rezolva(a, b):
    A = a.split(",")
    B = b.split(",")

    rs = []

    for i in range(len(A)):
        for j in range(len(B)):
            if A[i] == ("¬" + B[j]) or B[j] == ("¬" + A[i]):
                now = ",".join(
                    set(A[0:i] + A[i + 1 : len(A)] + B[0:j] + B[j + 1 : len(B)])
                )
                if good(now):
                    rs.append(now)

    return rs


contradictie = 0
while 1:

    clauze_noi = []

    for i in range(len(clauze)):
        for j in range(len(clauze)):
            if i == j:
                continue
            rezolventi = rezolva(clauze[i], clauze[j])

            for it in rezolventi:

                if len(it) == 0:
                    contradictie = 1

                acum = it.split(",")
                acum.sort()
                acum = ",".join(acum)

                if the.get(it) == None:
                    the[it] = str(nr + 1)
                    nr += 1
                    din[it] = din[clauze[i]] + "," + din[clauze[j]]
                    clauze_noi.append(it)

    if len(clauze_noi) == 0:
        break

    clauze += clauze_noi
    for it in clauze:
        print("(" + the[it] + ")  ", "{ ", it, " } din ", din[it])
    print()
    print()
    print()

    if contradictie:
        print("F = ⊥")
        exit()
