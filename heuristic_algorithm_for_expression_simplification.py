class BstNode:
    def __init__(self, key):
        self.key = key
        self.right = None
        self.left = None

    def insert(self, key):

        if self.key == key:
            return
        elif self.key < key:
            if self.right is None:
                self.right = BstNode(key)
            else:
                self.right.insert(key)
        else:  # self.key > key
            if self.left is None:
                self.left = BstNode(key)
            else:
                self.left.insert(key)

    def display(self):
        lines, *_ = self._display_aux()
        for line in lines:
            print(line)

    def _display_aux(self):
        """Returns list of strings, width, height, and horizontal coordinate of the root."""
        # No child.
        if self.right is None and self.left is None:
            line = "%s" % self.key
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        # Only left child.
        if self.right is None:
            lines, n, p, x = self.left._display_aux()
            s = "%s" % self.key
            u = len(s)
            first_line = (x + 1) * " " + (n - x - 1) * "_" + s
            second_line = x * " " + "/" + (n - x - 1 + u) * " "
            shifted_lines = [line + u * " " for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        # Only right child.
        if self.left is None:
            lines, n, p, x = self.right._display_aux()
            s = "%s" % self.key
            u = len(s)
            first_line = s + x * "_" + (n - x) * " "
            second_line = (u + x) * " " + "\\" + (n - x - 1) * " "
            shifted_lines = [u * " " + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        # Two children.
        left, n, p, x = self.left._display_aux()
        right, m, q, y = self.right._display_aux()
        s = "%s" % self.key
        u = len(s)
        first_line = (x + 1) * " " + (n - x - 1) * "_" + s + y * "_" + (m - y) * " "
        second_line = (
            x * " " + "/" + (n - x - 1 + u + y) * " " + "\\" + (m - y - 1) * " "
        )
        if p < q:
            left += [n * " "] * (q - p)
        elif q < p:
            right += [m * " "] * (p - q)
        zipped_lines = zip(left, right)
        lines = [first_line, second_line] + [a + u * " " + b for a, b in zipped_lines]
        return lines, n + m + u, max(p, q) + 2, n + u // 2


def rec(s, l, r):

    if l == r:
        if s[l] >= "A" and s[l] <= "Z":
            c = BstNode(s[l])
            return c
        return None

    if s[l] != "(" or s[r] != ")":
        return None

    if (
        (s[l + 1] == "¬")
        and (s[r - 1] >= "A")
        and (s[r - 1] <= "Z")
        and (r - l + 1 == 4)
    ):
        c = BstNode("¬")
        c.left = BstNode(s[r - 1])
        return c

    if s[l + 1] == "¬":
        b = BstNode("¬")
        b.left = rec(s, l + 2, r - 1)
        return b

    now = 0
    for i in range(l + 1, r):
        if s[i] == "(":
            now += 1
        if s[i] == ")":
            now -= 1
        if (s[i] == "⇒" or s[i] == "⇔" or s[i] == "∨" or s[i] == "∧") and now == 0:
            c = BstNode(s[i])
            c.left = rec(s, l + 1, i - 1)
            c.right = rec(s, i + 1, r - 1)
            return c
    return None


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
        if it != "∧":
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
        if s[i] == "∧" and now == 0:
            l = halves(s[1:i])
            if len(l) == 3 and l[0] == "∨":
                return (
                    "(("
                    + distribuie(l[1])
                    + "∧"
                    + distribuie(s[i + 1 : r])
                    + ")∨("
                    + distribuie(l[2])
                    + "∧"
                    + distribuie(s[i + 1 : r])
                    + "))"
                )
            l = halves(s[i + 1 : r])
            if len(l) == 3 and l[0] == "∨":
                return (
                    "(("
                    + distribuie(l[1])
                    + "∧"
                    + distribuie(s[1:i])
                    + ")∨("
                    + distribuie(l[2])
                    + "∧"
                    + distribuie(s[1:i])
                    + "))"
                )
        if s[i] == "∨" and now == 0:
            return "(" + distribuie(s[1:i]) + "∨" + distribuie(s[i + 1 : r]) + ")"

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
        if it != "∧":
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
        if s[i] == "∨" and now == 0:
            return frumos(s[1:i]) + "∨" + frumos(s[i + 1 : r])

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

s = "(¬A ∨ A) ∨ ( (P ∨ ¬R) ∧ (¬Q ∨ ¬R) ∧ ¬(P ∧ R) )"
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
componente = s.split("∨")
util = [1] * len(componente)

for i in range(len(componente)):
    for j in range(len(componente)):
        if i == j:
            continue

        it = componente[i]
        if len(it) > 1:
            it = it[1 : len(it) - 1]
        it = it.split("∧")
        jt = componente[j]
        if len(jt) > 1:
            jt = jt[1 : len(jt) - 1]
        jt = jt.split("∧")

        lista_noua = it + jt
        lista_noua = set(lista_noua)
        it = set(it)
        jt = set(jt)

        if len(lista_noua) == len(it) and util[j]:
            util[i] = 0
        elif len(lista_noua) == len(jt) and util[i]:
            util[j] = 0

componente = [componente[i] for i in range(len(componente)) if util[i]]
if len(componente) == 0:
    componente.append("⊥")
l.append("∨".join(componente))

# anihilare
util = [1] * len(componente)
for i in range(len(componente)):

    el = componente[i]
    if len(el) > 1:
        el = el[1 : len(el) - 1]
    el = el.split("∧")

    d = dict()
    for it in el:
        if len(it) == 2:
            d[it] = 1
    for it in el:
        if len(it) == 1 and d.get("¬" + it) != None:
            util[i] = 0

componente = [componente[i] for i in range(len(componente)) if util[i]]
if len(componente) == 0:
    componente.append("⊥")
l.append("∨".join(componente))


letter = set()
for it in "∨".join(componente):
    if it >= "A" and it <= "Z":
        letter.add(it)
letter = list(letter)


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


nr_factor_comun = 0
while 1:

    if componente[0] == "⊥":
        break

    # tranforming in binary representation
    formele_binare = []
    for it in componente:
        formele_binare.append(binary(it))

    new_s = factor_comun(formele_binare)  ##simpyfind by common factor + anihilation
    for i in range(len(new_s)):
        new_s[i] = findVariables(new_s[i])  ##transforming from binary to letters

    if len(new_s) == 0:
        new_s.append("⊥")

    if set(new_s) == set(componente):
        break

    componente = new_s
    if len(componente) == 0:
        componente.append("⊥")

    l.append("∨".join(componente))
    nr_factor_comun += 1

nr_idempotenta_2 = 0
while 1:

    if componente[0] == "⊥":
        break
    # tranforming in binary representation
    formele_binare = []
    for it in componente:
        formele_binare.append(binary(it))

    new_s = idempotenta_2(formele_binare)  ##simpyfind by common factor + anihilation
    for i in range(len(new_s)):
        new_s[i] = findVariables(new_s[i])  ##transforming from binary to letters

    if set(new_s) == set(componente):
        break
    componente = new_s
    l.append("∨".join(componente))
    nr_idempotenta_2 += 1

tautologie = 0
for it in l[K + nr_factor_comun + 6 + nr_idempotenta_2]:
    if it == "T" and len(l[K + nr_factor_comun + 6 + nr_idempotenta_2]) != 1:
        tautologie = 1
        l.append("T")

print()
print()
print()
# print(l)
print("F = ", l[0], " ∼ (Definition of equivalence)")
print(l[1], " ∼ (Definition of implication)")

for i in range(K):
    print(l[2 + i], " ∼ (Distributivity of conjunction over disjunction)")

print(l[K + 2], " ∼ (Relaxed syntax)")
print(l[K + 3], " ∼ (Idempotency)")
print(l[K + 4], " ∼ (Idempotency)")
print(l[K + 5], " ∼ (Anihilation)")

for i in range(nr_factor_comun):
    print(l[K + 6 + i], " ∼ (Common factor + anihilation)")
for i in range(nr_idempotenta_2):
    print(l[K + nr_factor_comun + 6 + i], " ∼ (Idempotency)")

if tautologie:
    print(l[K + nr_factor_comun + 6 + nr_idempotenta_2], " ∼ (Anihilation)")
    print(l[K + nr_factor_comun + 6 + nr_idempotenta_2 + tautologie])
else:
    print(l[K + nr_factor_comun + 6 + nr_idempotenta_2])

print(
    "Simplified logical expressions (not necessarily the shortest form) : ",
    l[K + nr_factor_comun + 6 + nr_idempotenta_2 + tautologie],
)

print()
print()
