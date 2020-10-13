package main

import (
	"database/sql"
	"fmt"
	_ "github.com/go-sql-driver/mysql"
)

func containsDestination(s []Destination, e Destination) bool {
	for _, a := range s {
		if a.Id == e.Id {
			return true
		}
	}
	return false
}


func createProblem(parcels []int) Problem{
	var listOfDestinations []Destination
	var listOfParcels []Parcel
	var initialState []State
	var goalState []State

	db, err := sql.Open("mysql", "root@tcp(127.0.0.1:3306)/courierail?parseTime=true")

	if err != nil {
		panic(err.Error())
	}
	defer db.Close()

	var listOfTrains = getTrains(db)

	for _, train := range listOfTrains{
		var state = NewState("train_at", [2]int {train.Id, train.StartDestination})
		initialState = append(initialState, state)
	}

	for _, parcel := range parcels {
		sqlRaw := fmt.Sprintf(`SELECT * FROM application_parcel WHERE id IN ('%d')`, parcel)
		parcel1, err := db.Query(sqlRaw)
		if err != nil {
			panic(err.Error())
		}

		for parcel1.Next(){
			var p Parcel
			err = parcel1.Scan(&p.Id, &p.Weight, &p.Price, &p.DestinationFrom, &p.DestinationTo,
				  &p.ReceiverId, &p.SenderId, &p.Date, &p.IsDelivered)
			if err != nil {
				panic(err.Error())
			}
			var state = NewState("at", [2]int {p.Id, p.DestinationFrom})
			var state2 = NewState("at", [2]int {p.Id, p.DestinationTo})
			initialState = append(initialState, state)
			goalState = append(goalState, state2)
			var destinationTo = getDestination(db, p.DestinationTo)
			var destinationFrom = getDestination(db, p.DestinationFrom)
			if !containsDestination(listOfDestinations, destinationTo) {
				listOfDestinations = append(listOfDestinations, destinationTo)
			}
			if !containsDestination(listOfDestinations, destinationFrom) {
				listOfDestinations = append(listOfDestinations, destinationFrom)
			}
			listOfParcels = append(listOfParcels, p)
		}
	}

	var problem = NewProblem(listOfParcels, listOfTrains, listOfDestinations, goalState, initialState)
	problem.listOfActions = AddActions(listOfParcels, listOfTrains, listOfDestinations, problem.listOfActions)
	return problem

}

func getDestination(db *sql.DB, id int) Destination{
	sqlRaw := fmt.Sprintf(`SELECT * FROM application_destination WHERE id IN ('%d')`, id)
	destinations, err := db.Query(sqlRaw)
	if err != nil {
		panic(err.Error())
	}
	var d Destination
	for destinations.Next(){
		err = destinations.Scan(&d.Id, &d.Name, &d.Country, &d.Zipcode, &d.State, &d.Longitude, &d.Latitude)
		if err != nil {
			panic(err.Error())
		}
	}
	return d
}

func getTrains(db *sql.DB) []Train{
	sqlRaw := fmt.Sprintf(`SELECT * FROM application_train WHERE isAvailable`)
	trains, err := db.Query(sqlRaw)
	if err != nil {
		panic(err.Error())
	}
	var allTrains []Train
	for trains.Next(){
		var t Train
		err = trains.Scan(&t.Id, &t.StartDestination, &t.IsAvailable)
		if err != nil {
			panic(err.Error())
		}
		allTrains = append(allTrains, t)
	}
	return allTrains
}


func main() {
	pcs := []int{1,2,3}
	var problem = createProblem(pcs)
	stateMap := make(map[string]int)
	for _, parcel := range problem.parcels{
		for _, destination := range problem.destination{
			s := fmt.Sprintf("at(%d,%d)", parcel.Id, destination.Id)
			if parcel.DestinationFrom == destination.Id {
				stateMap[s] = 1
			}else{
				stateMap[s] = 0
			}

		}
	}
	for _, destination := range problem.destination{
		for _, train := range problem.trains{
			s := fmt.Sprintf("train_at(%d,%d)", train.Id, destination.Id)
			if train.StartDestination == destination.Id {
				stateMap[s] = 1
			}else{
				stateMap[s] = 0
			}

		}
	}

	for _, parcel := range problem.parcels{
		for _, train := range problem.trains{
			s := fmt.Sprintf("in(%d,%d)", parcel.Id, train.Id)
			stateMap[s] = 0
		}
	}

	checkGoal(stateMap, problem.goalState)



}

func checkGoal(stateMap map[string]int, state []State) bool{
	for _, state1 := range state{
		s := fmt.Sprintf("%s(%d,%d)", state1.name, state1.arguments[0], state1.arguments[1])
		value, ok := stateMap[s]
		if ok {
			if value != 1{
				return false
			}
		}else{
			return false
		}
	}
	return true
}



