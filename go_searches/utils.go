package main
//import "C"

import (
	"context"
	"encoding/json"
	"fmt"
	"github.com/elliotchance/orderedmap"
	"googlemaps.github.io/maps"
	"io/ioutil"
	"log"
	"math"
	"net/http"
	"strings"
)

const googleApiUri = "https://maps.googleapis.com/maps/api/geocode/json?key=AIzaSyAIJCoIXnAfnAIM-XYrTnmzr8ya5pPehdQ&address="

func bool2int(b bool) int {
	if b {
		return 1
	}
	return 0
}

func containsState(s []State, e State) bool {
	s1 := fmt.Sprintf("%s(%s,%s)", e.name, e.arguments[0], e.arguments[1])
	for _, a := range s {
		s2 := fmt.Sprintf("%s(%s,%s)", a.name, a.arguments[0], a.arguments[1])
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
	s1 := fmt.Sprintf("%s(%s,%s)", e1.name, e1.arguments[0], e1.arguments[1])
	s2 := fmt.Sprintf("%s(%s,%s)", e2.name, e2.arguments[0], e2.arguments[1])
	if s1 == s2{
		return true
	}else{
		return false
	}
}


func containsDestination(s []string, e string) bool {
	for _, a := range s {
		if a == e {
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
		s := fmt.Sprintf("%s(%s,%s)", state1.name, state1.arguments[0], state1.arguments[1])
		stateMap.Set(s, 1)
	}
	return stateMap
}

func degreesToRadians(dg float64) float64{
	return dg * math.Pi /180
}

func distanceBetweenCities(destination1 string, destination2 string) float64 {
	var earthRadiusKm float64 = 6378.1370

	resp, err := http.Get(googleApiUri + strings.Replace(destination1, " ", "", -1))
	resp1, err1 := http.Get(googleApiUri + strings.Replace(destination2, " ", "", -1))

	if err != nil || err1 != nil{
		log.Fatal("Fetching google api uri data error: ", err)
	}

	bytes, err := ioutil.ReadAll(resp.Body)
	bytes1, err1 := ioutil.ReadAll(resp1.Body)
	defer resp.Body.Close()
	defer resp1.Body.Close()
	if err != nil || err1 != nil{
		log.Fatal("Reading google api data error: ", err)
	}

	var data googleApiResponse
	var data1 googleApiResponse
	json.Unmarshal(bytes, &data)
	json.Unmarshal(bytes1, &data1)

	dLat := degreesToRadians(data1.Results[0].Geometry.Location.Latitude - data.Results[0].Geometry.Location.Latitude)
	dLon := degreesToRadians(data1.Results[0].Geometry.Location.Longitude - data.Results[0].Geometry.Location.Longitude)

	lat1 := degreesToRadians(data.Results[0].Geometry.Location.Latitude)
	lat2 := degreesToRadians(data1.Results[0].Geometry.Location.Latitude)

	a := math.Pow(math.Sin(dLat/2), 2) + math.Pow(math.Sin(dLon/2), 2) * math.Cos(lat1) * math.Cos(lat2)
	c := 2 * math.Atan2(math.Sqrt(a), math.Sqrt(1-a)) * earthRadiusKm
	return c
}


func distanceBetweenCitiesByRail(destination1 string, destination2 string) float64{
	c, err := maps.NewClient(maps.WithAPIKey("AIzaSyAIJCoIXnAfnAIM-XYrTnmzr8ya5pPehdQ"))
	if err != nil {
		log.Fatalf("fatal error: %s", err)
	}
	r := &maps.DistanceMatrixRequest{
		Origins:      []string{destination1},
		Destinations: []string{destination2},
		Units:        maps.UnitsMetric,
		Mode: maps.TravelModeTransit,
		TransitMode: []maps.TransitMode{maps.TransitModeTrain},
	}
	route, err := c.DistanceMatrix(context.Background(), r)

	if err != nil {
		log.Fatalf("fatal error: %s", err)
	}
	var result float64 = 0
	result = float64(route.Rows[0].Elements[0].Distance.Meters)*0.001

	if result == 0 {
		r := &maps.DistanceMatrixRequest{
			Origins:      []string{destination1},
			Destinations: []string{destination2},
			Units:        maps.UnitsMetric,
			Mode: maps.TravelModeDriving,
		}
		route, err := c.DistanceMatrix(context.Background(), r)

		if err != nil {
			log.Fatalf("fatal error: %s", err)
		}
		result = float64(route.Rows[0].Elements[0].Distance.Meters)*0.001
	}
	return result

}








