import copy

tabel = []


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
            return 1 - (1 - (val(s, l + 1, i - 1) == val(s, i + 1, r - 1)))
        if s[i] == "∨" and now == 0:
            return 1 - (1 - (val(s, l + 1, i - 1) or val(s, i + 1, r - 1)))
        if s[i] == "∧" and now == 0:
            return 1 - (1 - (val(s, l + 1, i - 1) and val(s, i + 1, r - 1)))
    return 0


def da(s, l, r):

    if l == r:
        if s[l] >= "A" and s[l] <= "Z":
            # tabel.append(s[l : r + 1])
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
        tabel.append(s[l : r + 1])
        return 1

    if s[l + 1] == "¬":
        tabel.append(s[l : r + 1])
        return da(s, l + 2, r - 1)

    now = 0
    for i in range(l + 1, r):
        if s[i] == "(":
            now += 1
        if s[i] == ")":
            now -= 1
        if (s[i] == "⇒" or s[i] == "⇔" or s[i] == "∨" or s[i] == "∧") and now == 0:
            tabel.append(s[l : r + 1])
            return da(s, l + 1, i - 1) and da(s, i + 1, r - 1)
    return 0


s = input()
k = ""
for it in s:
    if it != " ":
        k += it

s = strict_structure(k)

print("Propoziia in forma stricta: ", s)

a = BstNode("„F”")
now = a

ans = ""
pos = []
p = dict()

litere = set()
d = dict()
for it in s:
    if it >= "A" and it <= "Z":
        litere.add(it)
        d[it] = 0
cnt = len(litere)

exista_true = 0
exista_false = 0

hehe = da(s, 0, len(s) - 1)

spatii = "                                                                "

for i in range(len(s)):
    if s[i] == "(":

        B = copy.deepcopy(a)
        C = copy.deepcopy(a)

        b = B
        c = C

        for it in pos:
            if it == "l":
                b = b.left
                c = c.left
            else:
                b = b.right
                c = c.right

        b.key = "„□”"
        b.left = BstNode("„F”")
        b.right = BstNode("„F”")

        c.key = "„¬”"
        c.left = BstNode("„F”")

        print("'('")
        print("Avem două posibilităţi")
        print("(1)")
        B.display()
        print()
        print("(2)")
        C.display()
        print()

        if (i < len(s) - 1) and (s[i + 1] != "¬"):
            now.key = "„□”"

            now.left = BstNode("„F”")
            p[now.left] = now
            now.right = BstNode("„F”")
            p[now.right] = now

            now = now.left
            pos.append("l")

        elif i < len(s) - 1:

            now.key = "¬"
            now.left = BstNode("„F”")
            p[now.left] = now
            now = now.left
            pos.append("l")

    elif s[i] >= "A" and s[i] <= "Z":
        if now.key != "„F”":
            print("Se astepta operator logic sau paranteza inchisa")
            print("Nu este propozitie bine formata")
            exit()
        now.key = s[i]
        if now != a:
            now = p[now]
        if len(pos) > 0:
            pos.pop()
        print(
            "Propozitia atomica închide ramura arborelui, mutăm poziţia la nivelul părintelui."
        )
        print("Propozitie atomica:")
        a.display()

    elif s[i] == "∧" or s[i] == "∨" or s[i] == "⇒" or s[i] == "⇔":
        if now.key != "„□”":
            print("Nu se cere un conector binar")
            print("Nu este propozitie bine formata")
            exit()
        now.key = s[i]
        now = now.right
        pos.append("r")

        print("Conector binar:")
        a.display()

    elif s[i] == "¬":
        if (i == 0) or (i > 0 and s[i - 1] != "("):
            print("Nu se astepta o negatie")
            print("Nu este propozitie bine formata")
            exit()
        print("'¬':")
        a.display()

    elif s[i] == ")":
        if now.key >= "A" and now.key <= "Z":
            print("Nu se astepta o paranteza inchisa")
            print("Nu este propozitie bine formata")
            exit()

        if now == a and i != (len(s) - 1):
            print(
                "Nu este formula propozitionala bine formata, arborele a fost completatat inainte sa terminam sirul"
            )
            exit()

        if now != a:
            now = p[now]

        if len(pos) > 0:
            pos.pop()

        print("Paranteza inchisa, ne urcam spre parinte")
        a.display()
    else:
        print("Simbol necunoscut")
        exit()

if ans == "" and now != a:
    ans = "Nu este formula propozitionala bine formata, sirul nu a fost destul pentru completarea arborelui"
else:
    ans = "Este formula propozitionala bine formata"
print(ans)
print()
print("Tabelul de adevar:")

# printing the letters
print("", end=" | ")
for it in litere:
    print(it, end=" | ")

tabel = list(sorted(tabel, key=len))
for it in tabel:
    print(it, end=" | ")
print()

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

    print("", end=" | ")
    for it in cur:
        print(it, end=" | ")

    for now in tabel:
        g = ""
        for it in now:
            if it >= "A" and it <= "Z":
                g += d[it]
            else:
                g += it

        nw = val(g, 0, len(g) - 1)
        if len(g) == len(s):
            exista_true = max(exista_true, nw == 1)
            exista_false = max(exista_false, nw == 0)
        print(spatii[0 : max(0, len(now) - 2)], nw, end=" | ")
    print()
if exista_true == 1:
    print("Formula este satisfiabila")
else:
    print("Formula este nesatisfiabila")
if exista_false == 0:
    print("Formula este valida")
else:
    print("Formula este invalida")

