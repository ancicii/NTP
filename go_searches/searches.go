package main
//import "C"
import (
	"container/heap"
	"github.com/elliotchance/orderedmap"
)

func BreadthFirstSearch(problem Problem, stateMap *orderedmap.OrderedMap) *Node {
	state := problem.initialState
	node := NewNode(state)			//pocetni cvor je pocetno stanje problema

	if problem.checkGoal(stateMap) {	//proverimo da li je pocetno stanje resenje
		return node
	}
	queue := []*Node{ node } // kreiramo FIFO queue
	var list []string		// lista cvorova iz queue-a u string reprezentaciji 1/0
	var explored []string	// lista pretrazenih cvorova

	for {
		if len(queue) == 0 {
			break // ne postoji resenje
		}
		leaf := queue[0]
		queue = queue[1:]

		explored = append(explored, stateTo10(createStateMap(leaf.NodeState, stateMap)))
		for _, child := range problem.possibleNodes(leaf.NodeState, leaf) {
			stateMap = createStateMap(child.NodeState, stateMap)
			childToString := stateTo10(createStateMap(child.NodeState, stateMap))
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

func DepthFirstSearch(node *Node, problem Problem, stateMap *orderedmap.OrderedMap, list []string, explored []string) *Node{
	stateMap1 := createStateMap(node.NodeState, stateMap)
	if problem.checkGoal(stateMap1) {	//proverimo da li je pocetno stanje resenje
		return node
	}
	explored = append(explored, stateTo10(stateMap1))
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
		childToString := stateTo10(createStateMap(child.NodeState, stateMap1))
		if (!isInExplored(explored, childToString)) && (!containsNode(list, childToString)){
			list = append(list, childToString)
			result := DepthFirstSearch(child, problem, stateMap1, list, explored)
			if result != nil {
				return result
			}
		}
	}
	return nil // nema resenja
}

func UniformCostSearch(problem Problem, stateMap *orderedmap.OrderedMap) *Node{
	state := problem.initialState
	node := NewNode(state)

	priorityQueue := &PriorityQueue{}
	heap.Init(priorityQueue)
	heap.Push(priorityQueue, node)

	var list []string		//lista cvorova iz queue-a u string reprezentaciji 1/0
	var explored []string	//lista pretrazenih cvorova

	list = append(list, stateTo10(createStateMap(state, stateMap)))

	for {
		if priorityQueue.Len() == 0 {
			break // no solution
		}

		leaf := heap.Pop(priorityQueue).(*Node)
		stateMap = createStateMap(leaf.NodeState, stateMap)
		if problem.checkGoal(stateMap) {
			return leaf
		}
		explored = append(explored, stateTo10(stateMap))

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

			childToString := stateTo10(createStateMap(child.NodeState, stateMap))
			if (!isInExplored(explored, childToString)) && (!containsNode(list, childToString)){
				heap.Push(priorityQueue, child)
				list = append(list, childToString)
			}
		}

	}

	return nil
}
