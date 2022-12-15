_dispatcher = {}

def _copy_list(l, dispatch):
    ret = l.copy()
    for idx, item in enumerate(ret):
        cp = dispatch.get(type(item))
        if cp is not None:
            ret[idx] = cp(item, dispatch)
    return ret

def _copy_dict(d, dispatch):
    ret = d.copy()
    for key, value in ret.items():
        cp = dispatch.get(type(value))
        if cp is not None:
            ret[key] = cp(value, dispatch)

    return ret

_dispatcher[list] = _copy_list
_dispatcher[dict] = _copy_dict

def deepcopy(sth):
    cp = _dispatcher.get(type(sth))
    if cp is None:
        return sth
    else:
        return cp(sth, _dispatcher)

def riv(x, y):
    global allowed
    global exists
    for i in allowed[x]:
        check = False
        for j in allowed[y]:
            if i != j:
                check = True
                break
        if not check:
            allowed[x].remove(i)
            exists[x][i - 1] = False
            return True
    return False

def addneighs(x, queue):
    ia = x // 10
    ja = x - ia * 10
    for k in range(1, 10):
        y = k * 10 + ja
        z = ia * 10 + k
        if y != x:
            queue.append([x, y])
        if z != x:
            queue.append([x, z])
    xs = (ja - 1) // 3 * 3 + 1  # finding where the square of that tile is
    ys = (ia - 1) // 3 * 3 + 1
    for xsi in range(xs, xs + 3):
        for ysi in range(ys, ys + 3):
            if ysi != ia and xsi != ja:
                y = ysi * 10 + xsi
                queue.append([x, y])

def ac3():
    queue = []
    for ia in range(1, 10):
        for ja in range(1, 10):
            x = ia * 10 + ja
            addneighs(x, queue)
    length = len(queue)
    while length > 0:
        [x, y] = queue.pop(0)
        length -= 1
        if riv(x, y):
            ia = x // 10
            ja = x - ia * 10
            for k in range(1, 10):
                y1 = k * 10 + ja
                z = ia * 10 + k
                if y1 != x:
                    queue.append([y1, x])
                if z != x:
                    queue.append([z, x])
            xs = (ja - 1) // 3 * 3 + 1  # finding where the square of that tile is
            ys = (ia - 1) // 3 * 3 + 1
            for xsi in range(xs, xs + 3):
                for ysi in range(ys, ys + 3):
                    if ysi != ia and xsi != ja:
                        y1 = ysi * 10 + xsi
                        queue.append([y1, x])

def lcv(var, result):
    a = []
    x = var
    for val in result[var]:
        lim = 0
        ia = x // 10
        ja = x - ia * 10
        for k in range(1, 10):
            y = k * 10 + ja
            z = ia * 10 + k
            if y != x:
                if val in result[y]:
                    lim += 1
            if z != x:
                if val in result[z]:
                    lim += 1
        xs = (ja - 1) // 3 * 3 + 1
        ys = (ia - 1) // 3 * 3 + 1
        for xsi in range(xs, xs + 3):
            for ysi in range(ys, ys + 3):
                if ysi != ia and xsi != ja:
                    y = ysi * 10 + xsi
                    if val in result[y]:
                        lim += 1
        a.append([lim, val])
    a.sort(key=lambda item: item[0])
    result[var] = list(map(lambda item: item[1], a))

def backtrack(result, mrvlg, count):
    if len(mrvlg) == 0:
        for i in range(1, 10):
            for j in range(1, 10):
                print(result[i * 10 + j][0], end=' ')
            print('\n')
        return True
    mrvl1 = list(mrvlg)
    var = mrvl1.pop(0)
    count += 1
    # LCV
    if count < 13:
        lcv(var, result)
    result1 = deepcopy(result)
    j = 0
    for value in result1[var]:
        if checkResult(var, value, result):
            result[var] = [value]
            if backtrack(result, mrvl1, count):
                return result
            result = deepcopy(result1)
            result[var] = result[var][j + 1:]
            j += 1
    return False

def checkResult(var, val, table):
    x = var
    ia = x // 10
    ja = x - ia * 10
    for k in range(1, 10):
        y = k * 10 + ja
        z = ia * 10 + k
        if y != x:
            if table[y] == [val]:
                return False
        if z != x:
            if table[z] == [val]:
                return False
    xs = (ja - 1) // 3 * 3 + 1  # finding where the square of that tile is
    ys = (ia - 1) // 3 * 3 + 1
    for xsi in range(xs, xs + 3):
        for ysi in range(ys, ys + 3):
            if ysi != ia and xsi != ja:
                y = ysi * 10 + xsi
                if table[y] == [val]:
                    return False
    for k in range(1, 10):
        y = k * 10 + ja
        z = ia * 10 + k
        if y != x:
            if val in table[y]:
                table[y].remove(val)
        if z != x:
            if val in table[z]:
                table[z].remove(val)
    for xsi in range(xs, xs + 3):
        for ysi in range(ys, ys + 3):
            if ysi != ia and xsi != ja:
                y = ysi * 10 + xsi
                if val in table[y]:
                    table[y].remove(val)
    return True

inpsud = []
allowed = {}
exists = {}

for i in range(9):
    inpsud.append(input().split())
    for j in range(9):
        index = (i + 1) * 10 + j + 1
        exists[index] = [False, False, False, False, False, False, False, False, False]
        allowed[index] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        if inpsud[i][j] != ".":
            value = int(inpsud[i][j])
            exists[index][value - 1] = True
            allowed[index] = [value]

ac3()
# MRV
allowed = dict(sorted(allowed.items(), key=lambda item: len(item[1])))
mrvl = list(allowed.keys())

while True:
    if len(allowed[mrvl[0]]) == 1:
        mrvl.remove(mrvl[0])
    else:
        break

res = backtrack(allowed, mrvl, 0)
