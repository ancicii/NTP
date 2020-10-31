package main
import (

	/*
		typedef struct action{
			char* actionStrings[800];
		}action;

		typedef struct destinationC{
			char name;
			double longitude;
			double latitude;
		}destinationC;

		typedef struct parcelC{
			int id;
			destinationC destinationFrom;
			destinationC destinationTo;
		}parcelC;

	*/
	"C"
)

import (
	"database/sql"
	"fmt"
	"github.com/elliotchance/orderedmap"
	_ "github.com/go-sql-driver/mysql"
	"log"
	"strconv"
	"time"
)

func createProblem(parcels []int) Problem{
	var listOfDestinations []string
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
		var state = NewState("train_at", [2]string {strconv.Itoa(train.Id), train.StartDestination})
		//var destinationStart = getDestination(db, train.StartDestination)
		if !containsDestination(listOfDestinations, train.StartDestination) {
			listOfDestinations = append(listOfDestinations, train.StartDestination)
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
				&p.ReceiverId, &p.SenderId, &p.DateCreated, &p.IsDelivered, &p.DateSent, &p.IsSent,
				&p.SenderName, &p.SenderSurname, &p.SenderContact, &p.ReceiverName, &p.ReceiverSurname,
				&p.ReceiverContact, &p.Description, &p.IsApproved)
			if err != nil {
				panic(err.Error())
			}
			var state = NewState("at", [2]string {strconv.Itoa(p.Id), p.DestinationFrom})
			var state2 = NewState("at", [2]string {strconv.Itoa(p.Id), p.DestinationTo})
			initialState = append(initialState, state)
			goalState = append(goalState, state2)
			//var destinationTo = getDestination(db, p.DestinationTo)
			//var destinationFrom = getDestination(db, p.DestinationFrom)
			if !containsDestination(listOfDestinations,  p.DestinationTo) {
				listOfDestinations = append(listOfDestinations,  p.DestinationTo)
			}
			if !containsDestination(listOfDestinations, p.DestinationFrom) {
				listOfDestinations = append(listOfDestinations, p.DestinationFrom)
			}
			listOfParcels = append(listOfParcels, p)
		}
	}

	var problem = NewProblem(listOfParcels, listOfTrains, listOfDestinations, goalState, initialState)
	problem.listOfActions = AddActions(listOfParcels, listOfTrains, listOfDestinations, problem.listOfActions, db)
	return problem

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
	var s string
	for node.Parent != nil {
		if node.Action.operator == Load || node.Action.operator == Unload{
			s = fmt.Sprintf("%s(parcel_%s;train_%s;%s)", node.Action.operator, node.Action.arguments[0], node.Action.arguments[1],
				node.Action.arguments[2])
		}else {
			s = fmt.Sprintf("%s(train_%s;%s;%s)", node.Action.operator, node.Action.arguments[0], node.Action.arguments[1],
				node.Action.arguments[2])
		}

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
			s := fmt.Sprintf("at(%d,%s)", parcel.Id, destination)
			if parcel.DestinationFrom == destination {
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
			s := fmt.Sprintf("train_at(%d,%s)", train.Id, destination)
			if train.StartDestination == destination {
				stateMap.Set(s, 1)

			}else{
				stateMap.Set(s, 0)

			}

		}
	}
	var actionsReturn C.action

	if kindOfSearch == "BFS"{
		start := time.Now()
		fmt.Println("Starting Breadth First Search...")
		n := BreadthFirstSearch(problem, stateMap)
		fmt.Println(getActions(n))
		fmt.Println("End of Breadth First Search...")
		elapsed := time.Since(start)
		log.Printf("Time elapsed: %s", elapsed)
		allActions := getActions(n)
		for i, act := range  allActions{
			actionsReturn.actionStrings[i] = C.CString(act)

		}
	}else if kindOfSearch == "DFS"{
		start := time.Now()
		fmt.Println("Starting Depth First Search...")
		n := DepthFirstSearch(NewNode(problem.initialState), problem, stateMap, []string{}, []string{})
		fmt.Println(getActions(n))
		fmt.Println("End of Depth First Search...")
		elapsed := time.Since(start)
		log.Printf("Time elapsed: %s", elapsed)
		allActions := getActions(n)
		for i, act := range  allActions{
			actionsReturn.actionStrings[i] = C.CString(act)

		}
	}else if kindOfSearch == "UCS"{
		start := time.Now()
		fmt.Println("Starting Uniform Cost First Search...")
		n := UniformCostSearch(problem, stateMap)
		fmt.Println(getActions(n))
		fmt.Println("End of Uniform Cost Search...")
		elapsed := time.Since(start)
		log.Printf("Time elapsed: %s", elapsed)
		allActions := getActions(n)
		for i, act := range  allActions{
			actionsReturn.actionStrings[i] = C.CString(act)

		}
	}else if kindOfSearch == "A*H1"{
		start := time.Now()
		fmt.Println("Starting A* Search with Heuristic 1 (Sum of non achieved goal states)...")
		n := AStarSearch(problem, stateMap, "H1")
		fmt.Println(getActions(n))
		fmt.Println("End of A* Search with Heuristic 1 (Sum of non achieved goal states)...")
		elapsed := time.Since(start)
		log.Printf("Time elapsed: %s", elapsed)
		allActions := getActions(n)
		for i, act := range  allActions{
			actionsReturn.actionStrings[i] = C.CString(act)

		}
	}else {
		start := time.Now()
		fmt.Println("Starting A* Search with Heuristic 2 (Sum of distances from parcels current city to goal city)...")
		n := AStarSearch(problem, stateMap, "H2")
		fmt.Println(getActions(n))
		fmt.Println("End of A* Search with Heuristic 2 (Sum of distances from parcels current city to goal city)...")
		elapsed := time.Since(start)
		log.Printf("Time elapsed: %s", elapsed)
		allActions := getActions(n)
		for i, act := range  allActions{
			actionsReturn.actionStrings[i] = C.CString(act)

		}
	}

	return actionsReturn
}

func main() {
	//doSearches([]int {15,16}, "A*H1")
	//doSearches([]int {14,15,16}, "A*H2")

}





