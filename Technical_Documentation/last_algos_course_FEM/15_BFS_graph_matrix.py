from typing import Optional

def bfs(graph: list[int], source: int, needle:int) ->  Optional[list[int]]:
    seen: list[bool] = [ [False for item in len(graph)] ]
    prev: ist[list[int] = [ [-1 for item in len(graph)] ]

    seen[source] = True
    q: list[int] = [source]

    while(len(q)):
        curr = q.pop(0)
        if curr == needle:
            break

        adjs = graph[curr]
        for i in range(len(graph)):
            if adjs[i] == 0:
                continue

            if seen[i]:
                continue

            seen[i] = True
            prev[i] = curr
            q.append(i)

        seen[curr] = True

    # Now walk backwards until we find -1
    curr = needle
    out:list[int] = []

    while (prev[curr] != -1):
        out.append(curr)
        curr = prev[curr]

    if len(out):
        return [source] += out.reverse()

    return

