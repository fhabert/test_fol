class Node:
    def __init__(self, parent=None, left=None, right=None,  value=None):
        self.parent = parent
        self.left = left
        self.right = right
        self.value = value

MAX_CONSTANTS = 10
connectives = ['>', '^', 'v']

def parse(fmla):
    if fmla[0] == '-':
        counter_pred = 0
        counter_min = 0
        for i in range(len(fmla)):
            if (ord(fmla[i]) > 97) and (ord(fmla[i]) < 122):
                counter_pred += 1
            elif fmla[i] == "-":
                counter_min += 1
        if counter_pred == 1:
            if counter_min % 2 == 0:
                return 6
            else:
                return 7
        elif 'A' in fmla or 'E' in fmla:
            return 2

    if con(fmla) != None:
        if ('E' in fmla) and ('A' in fmla):
            return 5
        elif 'E' in fmla:
            return 4
        elif 'A' in fmla:
            return 3
    if ((con(fmla) == None or lhs(fmla) == None or rhs(fmla) == None) and len(fmla) > 2):
        return 0
    else:
        if fmla[0] == '-' and len(fmla) < 3:
            return 7
        if len(fmla) == 1:
            return 1
        elif len(fmla) < 6:
            return 8
        return 5


def con(fmla):
    connect = []
    for i in range(len(fmla)):
        if fmla[i] in connectives:
            connect.append([fmla[i], i])  
    if len(connect) == 1:
        return connect[0]
    elif len(connect) % 2 == 1:
        return connect[1]
    elif len(connect) > 1:
        for i in range(len(connect)):
            if connect[i][1] > 1 or connect[i][1] < len(fmla) - 1:
                if fmla[connect[i][1] - 1] == ')' or fmla[connect[i][1] + 1] == '(' or fmla[connect[i][1] + 2] == '(':
                    return connect[i]
    else:
        return None

def lhs(fmla):
    if con(fmla):
        conn, index = con(fmla)
        if conn:
            left_fmla = fmla[:index]
            left_p = 0
            right_p = 0
            for letter in left_fmla:
                if letter == '(':
                    left_p += 1
                elif letter == ')':
                    right_p += 1
            if left_p >= right_p:
                num = left_p - right_p
                added = ')' * num
                return left_fmla + added
            elif left_p <= right_p:
                num = -(right_p - left_p)
                return left_fmla[:num]
            else:
                return left_fmla
    return None

def rhs(fmla):
    if con(fmla):
        conn, index = con(fmla)
        right_fmla = fmla[index+1:]
        left_p = 0
        right_p = 0
        for letter in right_fmla:
            if letter == '(':
                left_p += 1
            elif letter == ')':
                right_p += 1
        if left_p >= right_p:
            num = left_p - right_p
            added = ")" * num
            return right_fmla + added
        elif left_p <= right_p:
            num = -(right_p - left_p)
            return right_fmla[:num]
        else:
            return right_fmla
    return None

def theory(fmla):
    inner_fmla = fmla
    if 'A' in inner_fmla or 'E' in inner_fmla:
        inner_fmla = parse_quantifier(fmla)

    if con(fmla):
        theory_list = [lhs(inner_fmla), rhs(inner_fmla)]
        return theory_list
    return inner_fmla

def parse_quantifier(fmla):
    inner_fmla = fmla
    letters_e = []
    letters_a = []
    for i in range(len(inner_fmla)):
        if inner_fmla[i] == "E":
            letters_e.append(inner_fmla[i+1])
        elif inner_fmla[i] ==  "A":
            letters_a.append(inner_fmla[i+1])
    string = ""
    for i in range(len(inner_fmla)):
        if inner_fmla[i] in letters_e and inner_fmla[i-1] != "E":
            string += "a"
        elif inner_fmla[i] in letters_a and inner_fmla[i-1] != "A":
            string += "b"
        else:
            if i !=0 and (inner_fmla[i] != "E" and inner_fmla[i] != "A") and (inner_fmla[i-1] != "E" and inner_fmla[i-1] != "A"):
                string += inner_fmla[i]
    return string
            


def parse_implication(fmla):
    beta = ""
    if fmla[0] != "-":
        counter = 0
        for i in range (len(fmla)):
            if ord(fmla[i]) > 97 and ord(fmla[i]) < 122 and counter == 0:
                counter += 1
                if fmla[i-1] != "-":
                    beta += "-"
            if fmla[i] == ">":
                beta += "v"
            else:
                beta += fmla[i]
    else:
        counter = 0
        for i in range(1, len(fmla)):
            if ord(fmla[i]) > 97 and ord(fmla[i]) < 122 and counter == 0:
                counter = 1
            elif ord(fmla[i]) > 97 and ord(fmla[i]) < 122 and counter == 1:
                if fmla[i-1] != "-":
                    beta += "-"
                counter += 1
            if fmla[i] == ">":
                beta += "^"
            else:
                beta += fmla[i]
    return beta


def sat(tableau, line):
    copy_tab = []
    if len(tableau) >= 2:
        for item in tableau:
            copy_tab.append(item)
        root = Node(value=copy_tab)
        node_f = Node(value=copy_tab[0])
        node_d = Node(value=copy_tab[1])
        conn = con(line)
        if conn != None:
            if conn[0] == "^":
                root.right = node_f
                node_f.parent = root
                node_f.right = node_d
                node_d.parent = node_f
            elif conn[0] == "v":
                root.left = node_f
                root.right = node_d
                node_f.parent = root
                node_d.parent = root
        nodes = [root, node_f, node_d]
        for inner_list in copy_tab:
            if ('E' in inner_list or 'A' in inner_list) or ('P' in inner_list or 'Q' in inner_list):
                sat_quant(tableau, nodes)
                return check_satis(nodes, root)
        launch_test(tableau, nodes)
        return check_satis(nodes, root)
    return 1

def sat_quant(tableau, nodes_list):
    inner_tab = []
    for item in tableau:
        inner_tab.append(item)
    inner_node_list = []
    for item in nodes_list:
        inner_node_list.append(item)
    while inner_tab != []:
        dequeue = inner_tab[-1]
        inner_tab = inner_tab[:-1]
        temp = dequeue
        if 'E' in dequeue or 'A' in dequeue:
            temp = dequeue[2:]
            string_temp = ""
            if 'E' in dequeue:
                letter = 'c'
            else:
                letter = 'b'
            for i in range(len(temp)):
                if temp[i] == dequeue[1]:
                    string_temp += letter
                else:
                    string_temp += temp[i]
            temp = string_temp
            if temp[0] == '(':
                left_p = 0
                right_p = 0
                for let in temp:
                    if let == '(':
                        left_p += 1
                    elif let == ')':
                        right_p += 1
                if left_p >= right_p:
                    dif = left_p - right_p
                    temp = temp[dif:]
                elif left_p <= right_p:
                    dif = right_p - left_p
                    temp = temp[:dif]
        if len(temp) <= 8:
            node = Node(value=temp)
            node.parent = inner_node_list[-1]
        connec = con(temp)
        if connec != None:
            if connec != None and connec[0] == ">":
                parse_imp = parse_implication(temp)
                connec = con(parse_imp)
                r_h = rhs(parse_imp)
                l_h = lhs(parse_imp)
            else:
                r_h = rhs(temp)
                l_h = lhs(temp)

            if connec != None and connec[0] == "^":
                for in_node in inner_node_list:
                    if in_node.right == None and in_node.left == None:
                        node_one = Node(value=r_h)
                        node_two = Node(value=l_h)
                        in_node.right = node_one
                        node_one.parent = in_node
                        node_one.right = node_two
                        node_two.parent = node_one
            elif connec != None and connec[0] == "v":
                for in_node in inner_node_list:
                    if in_node.left == None and in_node.right == None:
                        node_one = Node(value=r_h)
                        node_two = Node(value=l_h)
                        in_node.left = node_one
                        in_node.right = node_two
                        node_one.parent = in_node
                        node_two.parent = in_node
            inner_tab.append(l_h)
            inner_tab.append(r_h)
            inner_node_list.append(node_one)
            inner_node_list.append(node_two)
    return False


def launch_test(tableau, node_list):
    inner_tab = []
    for item in tableau:
        inner_tab.append(item)
    inner_node_list = []
    for item in node_list:
        inner_node_list.append(item)
    while inner_tab != []:
        dequeue = inner_tab[-1]
        inner_tab = inner_tab[:-1]
        counter_l = 0
        for i in range(len(dequeue)):
            if ord(dequeue[i]) > 97 and ord(dequeue[i]) < 122:
                counter_l += 1
        if len(dequeue) <= 2:
            node = Node(value=dequeue)
            node.parent = inner_node_list[-1]
            if len(node.value) > 2:
                inner_node_list[-1].right = node
        elif counter_l == 1:
            node = Node(value=dequeue[-2:])
            node.parent = inner_node_list[-1]
            if len(node.value) > 2:
                inner_node_list[-1].right = node
        else:
            connec = con(dequeue)
            if connec != None and connec[0] == ">":
                parse_imp = parse_implication(dequeue)
                connec = con(parse_imp)
                r_h = rhs(parse_imp)
                l_h = lhs(parse_imp)
            else:
                r_h = rhs(dequeue)
                l_h = lhs(dequeue)

            if connec != None and connec[0] == "^":
                for in_node in inner_node_list:
                    if in_node.right == None and in_node.left == None:
                        node_one = Node(value=r_h)
                        node_two = Node(value=l_h)
                        in_node.right = node_one
                        node_one.parent = in_node
                        node_one.right = node_two
                        node_two.parent = node_one
            elif connec[0] == "v":
                for in_node in inner_node_list:
                    if in_node.left == None and in_node.right == None:
                        node_one = Node(value=r_h)
                        node_two = Node(value=l_h)
                        in_node.left = node_one
                        in_node.right = node_two
                        node_one.parent = in_node
                        node_two.parent = in_node
            inner_tab.append(l_h)
            inner_tab.append(r_h)
            inner_node_list.append(node_one)
            inner_node_list.append(node_two)
    return False

def check_satis(nodes_list, root_node):
    node_leaf = []
    for node in nodes_list:
        if node.left == None and node.right == None:
            node_leaf.append(node)

    count_leaf = len(node_leaf)
    counter = 0
    for node in nodes_list:
        if node != root_node:
            if len(node.value) == 1:
                node_temp = node.value
                while node.parent != None:
                    if node.parent.value == "-" + node_temp:
                        counter += 1
                    node = node.parent
            else:
                node_temp = node.value
                while node.parent != None:
                    if node.parent.value == node_temp[1:]:
                        counter += 1
                    node = node.parent
        if counter == count_leaf:
            return 0
    return 1

f = open('input.txt')

parseOutputs = ['not a formula',
                'an atom',
                'a negation of a first order logic formula',
                'a universally quantified formula',
                'an existentially quantified formula',
                'a binary connective first order formula',
                'a proposition',
                'a negation of a propositional formula',
                'a binary connective propositional formula']

satOutput = ['is not satisfiable', 'is satisfiable', 'may or may not be satisfiable']


firstline = f.readline()

PARSE = False
if 'PARSE' in firstline:
    PARSE = True

SAT = False
if 'SAT' in firstline:
    SAT = True

for line in f:
    if line[-1] == '\n':
        line = line[:-1]
    parsed = parse(line)

    if PARSE:
        output = "%s is %s." % (line, parseOutputs[parsed])
        if parsed in [5,8]:
            output += " Its left hand side is %s, its connective is %s, and its right hand side is %s." % (lhs(line), con(line)[0], rhs(line))
        print(output)

    if SAT:
        if parsed:
            tableau = theory(line)
            print('%s %s.' % (line, satOutput[sat(tableau, line)]))
        else:
            print('%s is not a formula.' % line)