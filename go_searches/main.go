package main
import (

	/*
		typedef struct action{
		char* actionStrings[800];
		}action;

	*/
	"C"
)

import (
	"database/sql"
	"fmt"
	"github.com/elliotchance/orderedmap"
	_ "github.com/go-sql-driver/mysql"
)

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
		var destinationStart = getDestination(db, train.StartDestination)
		if !containsDestination(listOfDestinations, destinationStart) {
			listOfDestinations = append(listOfDestinations, destinationStart)
		}
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
	problem.listOfActions = AddActions(listOfParcels, listOfTrains, listOfDestinations, problem.listOfActions, db)
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

func getActions(n *Node) []string {
	node := n
	var actions []string

	for node.Parent != nil {
		s := fmt.Sprintf("%s(%d,%d,%d)", node.Action.operator, node.Action.arguments[0], node.Action.arguments[1],
			node.Action.arguments[2])
		actions = append(actions, s)
		node = node.Parent
	}

	return reverse(actions)
}
//export doSearches
func doSearches(pcs []int, kindOfSearch string) C.action{
	var problem = createProblem(pcs)
	stateMap := orderedmap.NewOrderedMap()
	for _, parcel := range problem.parcels{
		for _, destination := range problem.destination{
			s := fmt.Sprintf("at(%d,%d)", parcel.Id, destination.Id)
			if parcel.DestinationFrom == destination.Id {
				stateMap.Set(s, 1)
			}else{
				stateMap.Set(s, 0)

			}
		}
	}

	for _, parcel := range problem.parcels{
		for _, train := range problem.trains{
			s := fmt.Sprintf("in(%d,%d)", parcel.Id, train.Id)
			stateMap.Set(s, 0)

		}
	}

	for _, destination := range problem.destination{
		for _, train := range problem.trains{
			s := fmt.Sprintf("train_at(%d,%d)", train.Id, destination.Id)
			if train.StartDestination == destination.Id {
				stateMap.Set(s, 1)

			}else{
				stateMap.Set(s, 0)

			}

		}
	}
	var actionsReturn C.action

	if kindOfSearch == "BFS"{
		fmt.Println("Starting Breadth First Search...")
		n := BreadthFirstSearch(problem, stateMap)
		fmt.Println(getActions(n))
		fmt.Println("End of Breadth First Search...")
		allActions := getActions(n)
		for i, act := range  allActions{
			actionsReturn.actionStrings[i] = C.CString(act)

		}
	}else if kindOfSearch == "DFS"{
		fmt.Println("Starting Depth First Search...")
		n := DepthFirstSearch(NewNode(problem.initialState), problem, stateMap, []string{}, []string{})
		fmt.Println(getActions(n))
		fmt.Println("End of Depth First Search...")
		allActions := getActions(n)
		for i, act := range  allActions{
			actionsReturn.actionStrings[i] = C.CString(act)

		}
	}else{
		fmt.Println("Starting Uniform Cost First Search...")
		n := UniformCostSearch(problem, stateMap)
		fmt.Println(getActions(n))
		fmt.Println("End of Uniform Cost Search...")
		allActions := getActions(n)
		for i, act := range  allActions{
			actionsReturn.actionStrings[i] = C.CString(act)

		}
	}

	return actionsReturn
}

func main() {


}





