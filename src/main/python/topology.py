from sys import stdin


def direct_connection(n_nodes, size):
    return tree_like(n_nodes, 2)


def mesh(n_nodes, size):
    start_offset = (1 if size % 2 is 0 else 0) + 2

    def targets_of(src):
        start = max(start_offset + src - size, 1) \
                    if src + size < n_nodes \
                    else 1 + n_nodes - (size * 2)
        end   = (min(src + size, n_nodes) + 2) \
                    if src - size > 0 \
                    else size * 2

        return range(start, end, 2)

    return [(src, dst)
        for src in range(0, n_nodes, 2)
        for dst in targets_of(src)
        if dst > 0 and dst < n_nodes
    ]


def tree_like(n_nodes, size, reverse=False):
    root_nodes = [i for i in range(0, n_nodes, size)]

    return [
        (i, j) if not reverse else (j, i)
        for i in root_nodes
        for j in range(i + 1, i + size)
    ]


def tree(n_nodes, size):
    return tree_like(n_nodes, size)


def star(n_nodes, size):
    return tree_like(n_nodes, size, True)


algorithms = [
    direct_connection,
    mesh,
    tree,
    star,
]

if __name__ == '__main__':
    def make_topology(n_nodes, size):
        return [(algorithm, algorithm(n_nodes, size))
                for algorithm in algorithms]

    n_nodes, size = stdin.__next__().split()

    result = make_topology(int(n_nodes), int(size))

    for l in result:
        print(l)
