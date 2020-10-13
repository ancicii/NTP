package main

func BreadthFirstSearch(problem Problem, stateMap map[string]int) *Node {
	state := problem.initialState
	node := NewNode(state)

	if problem.checkGoal(stateMap) {
		return node
	}
	queue := []*Node{ node } // FIFO queue
	var explored []string

	for {
		if len(queue) == 0 {
			break // no solution
		}

		leaf := queue[0]
		queue = queue[1:]

		explored = append(explored, stateTo10(leaf.NodeState, stateMap))

		for _, child := range problem.possibleNodes(leaf.NodeState, leaf) {
			stateMap = createStateMap(child.NodeState, stateMap)
			childToString := stateTo10(child.NodeState, stateMap)
			if !isInExplored(explored, childToString) && !containsNode(queue, child){
				if problem.checkGoal(stateMap){
					return child
				}else{
					queue = append(queue, child)
				}
			}
		}
	}
	return nil
}