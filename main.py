MAXN = 144742
TOL = 1
ptr = 0


class Node:
    def __init__(self, x=None, recipe=None):
        self.keys = x  # список ключей
        self.recipe = recipe  # соответствующая информация о рецепте
        self.next = [0] * 100

    def __repr__(self):
        return f"Node({self.keys}, {self.recipe})"


tree = [Node() for _ in range(MAXN)]


def add(root, curr):
    if not root.keys:
        root.keys = curr.keys
        root.recipe = curr.recipe
        root.next = curr.next
        return

    dist = edit_distance(root.keys, curr.keys)
    if not tree[root.next[dist]] or not tree[root.next[dist]].keys:
        global ptr
        ptr += 1
        tree[ptr] = curr
        root.next[dist] = ptr
    else:
        add(tree[root.next[dist]], curr)


def get_similar_recipies(root, s, threshold=TOL):
    ret = []
    if not root or not root.keys:
        return ret

    dist = edit_distance(root.keys, s)
    if dist <= threshold:
        ret.append((root.keys, root.recipe))

    start = dist - threshold if dist - threshold > 0 else 1
    while start <= dist + threshold:
        tmp = get_similar_recipies(tree[root.next[start]], s, threshold)
        ret.extend(tmp)
        start += 1
    return ret


def edit_distance(a, b):
    a_list = list(a)
    b_list = list(b)
    m, n = len(a_list), len(b_list)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a_list[i - 1] != b_list[j - 1]:
                dp[i][j] = min(
                    dp[i - 1][j] + 1,  # удаление
                    dp[i][j - 1] + 1,  # вставка
                    dp[i - 1][j - 1] + 1  # замена
                )
            else:
                dp[i][j] = dp[i - 1][j - 1]
    return dp[m][n]
