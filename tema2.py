def strict_structure(s):

    # propozitie atomica
    if len(s) == 1 and s[0] >= "A" and s[0] <= "Z":
        return s

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

    # initializare
    open = 0
    closed = 0
    st = 0
    dr = len(s) - 1
    if s[dr] == ")" and s[st] == "(":
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
    st = 0
    dr = len(s) - 1
    if s[dr] == ")" and s[st] == "(":
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
    st = 0
    dr = len(s) - 1
    if s[dr] == ")" and s[st] == "(":
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
    return s


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
        if s[i] == "→" and now == 0:
            return (1 - val(s, l + 1, i - 1)) or val(s, i + 1, r - 1)
        if s[i] == "⇔" and now == 0:
            return val(s, l + 1, i - 1) == val(s, i + 1, r - 1)
        if s[i] == "∨" and now == 0:
            return val(s, l + 1, i - 1) or val(s, i + 1, r - 1)
        if s[i] == "∧" and now == 0:
            return val(s, l + 1, i - 1) and val(s, i + 1, r - 1)
    return 0


s = input()
k = ""
for it in s:
    if it != " ":
        k += it

s = strict_structure(k)

litere = set()
d = dict()
for it in s:
    if it >= "A" and it <= "Z":
        litere.add(it)
        d[it] = 0
cnt = len(litere)

ans = da(s, 0, len(s) - 1)

if ans == 1:
    print("Forma in sintaxa stricta : ", s)
    b = rec(s, 0, len(s) - 1)
    b.display()
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
        print(val(g, 0, len(g) - 1))
else:
    print("Nu este o propozitie bine formata in sintaxa relaxata")
    #print(s)


# print(ans)

# // (((P⇒Q)∨S)⇔T)
# // (A^B)
# // P⇒Q∧S⇒T
# // (¬(B(¬Q))∧R)
# // (P∧((¬Q)∧(¬(¬(Q⇔(¬R))))))
# // ((P∨Q)⇒¬(P∨Q))∧(P∨(¬(¬Q)))
# // (P⇒((Q∧A)⇒(S⇒T)))
