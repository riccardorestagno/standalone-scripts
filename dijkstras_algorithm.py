def dijkstra(map, start, end):
    distance_dictionary = {start: 0}
    next_nodes = [start]

    for node in map:
        if node[0] not in distance_dictionary:
            distance_dictionary[node[0]] = -1
        if node[1] not in distance_dictionary:
            distance_dictionary[node[1]] = -1
        if not [node_check for node_check in map if node_check[1] == node[0]]:
            if end == node[0] and end != start:
                print("There are no paths connecting the start and end points entered!")
                return
            map.remove(node)

    if start not in distance_dictionary or end not in distance_dictionary:
        print("One of the edges entered does not exist!")
        return

    while map:
        nodes_to_search = [node for node in map if node[0] in next_nodes]
        next_nodes = []
        for node in nodes_to_search:
            if distance_dictionary[node[1]] == -1 or (node[2] + distance_dictionary[node[0]]) < distance_dictionary[node[1]]:
                distance_dictionary[node[1]] = node[2] + distance_dictionary[node[0]]
            map.remove(node)
            if node[1] not in next_nodes:
                next_nodes.append(node[1])

    print(f"The shortest distance between points {start} and {end} is: {distance_dictionary[end]}")


if __name__ == "__main__":
    map = [("A", "B", 4), ("A", "C", 2), ("C", "B", 1), ("B", "C", 3), ("C", "D", 4), ("C", "E", 5), ("B", "E", 3),
           ("E", "D", 1), ("B", "D", 2)]
    dijkstra(map, "A", "D")
