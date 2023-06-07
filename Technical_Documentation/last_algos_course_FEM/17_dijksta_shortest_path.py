import math

# O(v)
def hasUnvisited(seen: list[bool], dist:list[int]) -> bool:
    return any(not s and dists[i] < float(math.inf) 
        for i, s in enumerate(seen))


#O(v^2) because for every node, it's checking all other nodes
def getLowestUnvisited(seen: list[bool], dist:list[int]) -> int:
    idx = -1
    lowest = math.inf

    for i in range(len(seen)):
        if seen[i]:
            continue
        
        if lowest > dist[i]:
            lowest = dist[i]
            idx = i

    return idx


def dijkstra_list(source: int, sink: int, arr: list[int]) -> list[int]:
    #O(v)
    seen: list[bool] = [ [False for item in len(graph)] ]
    prev: list[bool] = [ [-1 for item in len(graph)] ]
    dist: list[bool] = [ [Math.inf for item in len(graph)] ]
    dist[source] = 0

    #O(v) for the while loop + O(v) for the function
    #O(v^2)
    while(hasUnvisited(seen, dist)):
        #O(v^2)
        curr = getLowestUnvisited(seen, dist)
        seen[curr] = True
        adjs = arr[curr]

        #O(E) - it checks every edge connected to a single node 
        # If we use an adjacencyMatrix, it would be O(V*E)
        for i in range(len(adjs)):
            edge = adjs[i]
            if seen[edge]:
                continue

            dists = dist[curr] + edge.weight
            if dists < dist[edge]:
                dist[edge] = dists #O(1)
                prev[edge] = curr

    # Walking backwards
    out: list[int] = []
    curr = sink

    while prev[curr] != -1:
        out.append(curr)
        curr = prev[curr]


    out.append(source)
    return out.reverse()

# Total running time: O(V^2 + E)

