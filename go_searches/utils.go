package main

import (
	"fmt"
	"reflect"
	"sort"
	"strconv"
)

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

func containsNode(nodes []string, toCheck string) bool {
	for _, a := range nodes {
		if a == toCheck {
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

func stateTo10(state []State, stateMap map[string]int) string {
	s1 := ""
	keys := reflect.ValueOf(stateMap).MapKeys()
	keysOrder := func(i, j int) bool { return keys[i].Interface().(string) < keys[j].Interface().(string) }
	sort.Slice(keys, keysOrder)


	for _, key := range keys {
		found := false
		for _, state1 := range state{
			s := fmt.Sprintf("%s(%d,%d)", state1.name, state1.arguments[0], state1.arguments[1])
			if key.Interface().(string) == s {
				s1 += strconv.Itoa(stateMap[key.Interface().(string)])
				found = true
				break
			}
		}
		if !found{
			s1 += "0"
		}
	}
	return s1

}


func createStateMap(state []State, stateMap map[string]int) map[string]int {
	for key, _ := range stateMap{
		stateMap[key] = 0
	}
	for _, state1 := range state{
		s := fmt.Sprintf("%s(%d,%d)", state1.name, state1.arguments[0], state1.arguments[1])
		stateMap[s] = 1
	}
	return stateMap
}


