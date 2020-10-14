package main

import "container/heap"

func BreadthFirstSearch(problem Problem, stateMap map[string]int) *Node {
	state := problem.initialState
	node := NewNode(state)			//pocetni cvor je pocetno stanje problema

	if problem.checkGoal(stateMap) {	//proverimo da li je pocetno stanje resenje
		return node
	}
	queue := []*Node{ node } // kreiramo FIFO queue
	var list []string		//lista cvorova iz queue-a u string reprezentaciji 1/0
	var explored []string	//lista pretrazenih cvorova

	for {
		if len(queue) == 0 {
			break // ne postoji resenje
		}
		leaf := queue[0]
		queue = queue[1:]

		explored = append(explored, stateTo10(leaf.NodeState, stateMap))
		for _, child := range problem.possibleNodes(leaf.NodeState, leaf) {
			stateMap = createStateMap(child.NodeState, stateMap)
			childToString := stateTo10(child.NodeState, stateMap)
			if (!isInExplored(explored, childToString)) && (!containsNode(list, childToString)){
				if problem.checkGoal(stateMap){
					return child
				}else{
					list = append(list,childToString)
					queue = append(queue, child)
				}
			}
		}
	}
	return nil
}

func DepthFirstSearch(node *Node, problem Problem, stateMap map[string]int, visitedNodes []string) *Node{
	stateMap1 := createStateMap(node.NodeState, stateMap)
	if problem.checkGoal(stateMap1) {	//proverimo da li je pocetno stanje resenje
		return node
	}
	for _, action := range problem.possibleActions(node.NodeState) {
		state1 := make([]State, len(node.NodeState))
		copy(state1, node.NodeState)
		for _, remove := range action.effectsRemove {
			state1 = removeState(state1, remove)
		}
		for _, add := range action.effectsAdd{
			state1 = append(state1, add)
		}
		child := NewChildNode(state1, node, action.expression)
		childToString := stateTo10(child.NodeState, stateMap1)
		if !containsNode(visitedNodes, childToString){
			visitedNodes = append(visitedNodes, childToString)
			result := DepthFirstSearch(child, problem, stateMap1, visitedNodes)
			if result != nil {
				return result
			}
		}
	}
	return nil // nema resenja
}

func UniformCostSearch(problem Problem, stateMap map[string]int) *Node{
	state := problem.initialState
	node := NewNode(state)

	priorityQueue := &PriorityQueue{}
	heap.Init(priorityQueue)
	heap.Push(priorityQueue, node)

	var list []string		//lista cvorova iz queue-a u string reprezentaciji 1/0
	var explored []string	//lista pretrazenih cvorova

	list = append(list, stateTo10(state, stateMap))

	for {
		if priorityQueue.Len() == 0 {
			break // no solution
		}

		leaf := heap.Pop(priorityQueue).(*Node)
		stateMap = createStateMap(leaf.NodeState, stateMap)
		if problem.checkGoal(stateMap) {
			return leaf
		}
		explored = append(explored, stateTo10(leaf.NodeState, stateMap))

		for _, action := range problem.possibleActions(leaf.NodeState) {
			state1 := make([]State, len(leaf.NodeState))
			copy(state1, leaf.NodeState)
			for _, remove := range action.effectsRemove {
				state1 = removeState(state1, remove)
			}
			for _, add := range action.effectsAdd{
				state1 = append(state1, add)
			}
			child := NewChildNodeCost(state1, leaf, action)

			stateMap = createStateMap(child.NodeState, stateMap)
			childToString := stateTo10(child.NodeState, stateMap)
			if (!isInExplored(explored, childToString)) && (!containsNode(list, childToString)){
				heap.Push(priorityQueue, child)
				list = append(list, stateTo10(child.NodeState, stateMap))
			}else {
				//priorityQueue.SwapIfLowerCost(node)
			}
		}

	}

	return nil
}
