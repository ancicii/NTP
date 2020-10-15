package main
//import "C"

import (
	"fmt"
	"github.com/elliotchance/orderedmap"
	"math"
)

func bool2int(b bool) int {
	if b {
		return 1
	}
	return 0
}

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

func stateTo10(stateMap *orderedmap.OrderedMap) string {
	s1 := ""

	for el := stateMap.Front(); el != nil; el = el.Next() {
		if el.Value == 0{
			s1 += "0"
		}else{
			s1 += "1"
		}
	}
	return s1

}


func createStateMap(state []State, stateMap *orderedmap.OrderedMap) *orderedmap.OrderedMap {
	for el := stateMap.Front(); el != nil; el = el.Next() {
		stateMap.Set(el.Key, 0)
	}
	for _, state1 := range state{
		s := fmt.Sprintf("%s(%d,%d)", state1.name, state1.arguments[0], state1.arguments[1])
		stateMap.Set(s, 1)
	}
	return stateMap
}

func degreesToRadians(dg float64) float64{
	return dg * math.Pi /180
}

func distanceBetweenCities(destination1 Destination, destination2 Destination) float64{
	var earthRadiusKm float64 = 6378.1370

	dLat := degreesToRadians(destination2.Latitude - destination1.Latitude)
	dLon := degreesToRadians(destination2.Longitude - destination1.Longitude)

	lat1 := degreesToRadians(destination1.Latitude)
	lat2 := degreesToRadians(destination2.Latitude)

	a := math.Pow(math.Sin(dLat/2), 2) + math.Pow(math.Sin(dLon/2), 2) * math.Cos(lat1) * math.Cos(lat2)
	c := 2 * math.Atan2(math.Sqrt(a), math.Sqrt(1-a)) * earthRadiusKm
	return c


}


