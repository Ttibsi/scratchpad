# This is recursive

def walk(graph: list[int], curr:int, needle:int, seen:list[bool], path:list[int]) -> bool:
    if seen[curr]:
        return False

    seen[curr] = True

    #pre
    path.append(curr)
    if curr == needle:
        return True

    #recurse
    myList = graph[curr]

    for i in range(len(myList)):
        edge = myList[i]
        if walk(graph, edge, needle, seen, path):
        return True

    #post
    path.pop(0)

    return False


# Source is where we start
def dfs(graph: list[int], source: int, needle:int) -> Optional[list[int]]:
    seen: list[bool] = [ [False for item in len(graph)] ]
    path:list[int] = []

    walk(graph, source, needle, seen, path)
    if not len(a):
        return

    return path


