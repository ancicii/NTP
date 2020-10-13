package main

import "fmt"

func containsState(s []State, e State) bool {
	s1 := fmt.Sprintf("%s(%d,%d)", e.name, e.arguments[0], e.arguments[1])
	for _, a := range s {
		s2 := fmt.Sprintf("%s(%d,%d)", a.name, a.arguments[0], a.arguments[1])
		if s1 == s2 {
			return true
		}
	}
	return false
}

func removeState(list []State, toRemove State) []State{
	toDel := -1
	for i, state := range list{
		if equalsState(state, toRemove){
			toDel = i
			break
		}
	}
	if toDel != -1{
		list[len(list)-1], list[toDel] = list[toDel], list[len(list)-1]
		return list[:len(list)-1]
	}
	return list
}

func equalsState(e1 State, e2 State) bool{
	s1 := fmt.Sprintf("%s(%d,%d)", e1.name, e1.arguments[0], e1.arguments[1])
	s2 := fmt.Sprintf("%s(%d,%d)", e2.name, e2.arguments[0], e2.arguments[1])
	if s1 == s2{
		return true
	}else{
		return false
	}
}


func containsDestination(s []Destination, e Destination) bool {
	for _, a := range s {
		if a.Id == e.Id {
			return true
		}
	}
	return false
}

func containsNode(nodes []*Node, toCheck *Node) bool {
	for _, a := range nodes {
		if a.Id == toCheck.Id {
			return true
		}
	}
	return false
}

func isInExplored(explored []string, str string) bool {
	for _, a := range explored {
		if a == str {
			return true
		}
	}
	return false
}

func reverse(input []string) []string {
	if len(input) == 0 {
		return input
	}
	return append(reverse(input[1:]), input[0])
}


