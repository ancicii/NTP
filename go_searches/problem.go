package main
//import "C"

import (
	"database/sql"
	"fmt"
	"github.com/elliotchance/orderedmap"
	"strconv"
	"strings"
)

type Problem struct {
	parcels       []Parcel
	trains        []Train
	destination   []string
	goalState     []State
	initialState  []State
	listOfActions []Action
}


func (p Problem) possibleActions(states []State) []Action{
	var possibleActions []Action
	for _, action := range p.listOfActions{
		isPossible := true
		for _, precondition := range action.preconditionsPositive{
			if !containsState(states, precondition){
				isPossible = false
				break
			}
		}
		for _, precondition := range action.preconditionsNegative{
			if containsState(states, precondition) {
				isPossible = false
				break
			}
		}
		if isPossible{
			possibleActions = append(possibleActions, action)
		}
	}
	return possibleActions
}

func (p Problem) checkGoal(stateMap *orderedmap.OrderedMap) bool {
	for _, state1 := range p.goalState{
		s := fmt.Sprintf("%s(%s,%s)", state1.name, state1.arguments[0], state1.arguments[1])
		value, ok := stateMap.Get(s)
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

//heuristika racuna koliko ciljnih stanja nije ispunjeno
func (p Problem) calculateH(stateMap *orderedmap.OrderedMap) float64 {
	var h float64= 0
	for _, state1 := range p.goalState{
		s := fmt.Sprintf("%s(%s,%s)", state1.name, state1.arguments[0], state1.arguments[1])
		value, ok := stateMap.Get(s)
		if ok {
			if value != 1{
				h += 1
			}
		}
	}
	return h
}


func getTrainsDestination(stateMap *orderedmap.OrderedMap, train string) string {
	for el := stateMap.Front(); el != nil; el = el.Next() {
		if el.Value == 1 {
			str := fmt.Sprintf("%s", el.Key)
			prefix := "train_at(" + train
			if strings.HasPrefix(str, prefix) {
				trainCurrentDestination := strings.TrimSuffix(strings.Split(str, ",")[1] + ", " + strings.Split(str, ",")[2], ")")
				return trainCurrentDestination
			}
		}

	}
	return ""
}


func (p Problem) possibleNodes(state []State, node *Node) []*Node {
	actions := p.possibleActions(state)
	var allNodes []*Node
	for _, action := range actions{
		state1 := make([]State, len(state))
		copy(state1, state)
		for _, remove := range action.effectsRemove {
			state1 = removeState(state1, remove)
		}
		for _, add := range action.effectsAdd{
			state1 = append(state1, add)
		}
		n1 := NewChildNode(state1, node, action.expression)
		allNodes = append(allNodes, n1)
	}
	return allNodes

}

func NewProblem(parcels []Parcel, trains []Train, destination []string, goalState []State, initialState []State) Problem {
	listOfActions := make([]Action, 0)
	p := Problem {parcels, trains, destination, goalState, initialState, listOfActions}
	return p
}

func AddActions(parcels []Parcel, trains []Train, destination []string, listOfActions []Action, db *sql.DB) []Action{
	listOfActions1 := LoadActions(parcels, trains, destination, listOfActions)
	listOfActions2 := UnloadActions(parcels, trains, destination, listOfActions1)
	listOfActions3 := TravelActions(trains, destination, listOfActions2, db)
	return listOfActions3
}

//   Action(Load(p, t, d),
//   PRECOND: At(p, d) ∧ Train_at(t, d) ∧ Parcel(p) ∧ Train(t) ∧ Destination(d)
//   EFFECT: ¬ At(p, d) ∧ In(p, t))
func LoadActions(parcels []Parcel, trains []Train, destination []string, listOfActions []Action) []Action {
	for _, d := range destination {
		for _, p := range parcels {
			for _, t := range trains {
				argsPositive := [2]string{strconv.Itoa(p.Id), d}
				argsPositive1 := [2]string{strconv.Itoa(t.Id), d}
				argsAdd := [2]string{strconv.Itoa(p.Id), strconv.Itoa(t.Id)}
				argsRemove := [2]string{strconv.Itoa(p.Id), d}
				effectsAdd := []State{NewState("in", argsAdd)}
				effectsRemove := []State{NewState("at", argsRemove)}
				preconditionsPositive := []State{NewState("at", argsPositive), NewState("train_at", argsPositive1)}
				var preconditionsNegative []State

				var operator = Load
				argsExpr := []string{strconv.Itoa(p.Id), strconv.Itoa(t.Id), d}
				var aex = NewActionExpression(operator, argsExpr)
				action := NewAction(aex, preconditionsPositive, preconditionsNegative, effectsAdd, effectsRemove)
				listOfActions = append(listOfActions, action)
			}
		}
	}
	return listOfActions
}

//   Action(Unload(p, t, d),
//   PRECOND: In(p, t) ∧ Train_at(t, d) ∧ Parcel(p) ∧ Train(t) ∧ Destination(d)
//   EFFECT: At(p, d) ∧ ¬ In(p, t))
func UnloadActions(parcels []Parcel, trains []Train, destination []string, listOfActions []Action) []Action {
	for _, d := range destination {
		for _, p := range parcels {
			for _, t := range trains {
				argsPositive := [2]string{strconv.Itoa(p.Id), strconv.Itoa(t.Id)}
				argsPositive1 := [2]string{strconv.Itoa(t.Id), d}
				argsAdd := [2]string{strconv.Itoa(p.Id), d}
				argsRemove := [2]string{strconv.Itoa(p.Id), strconv.Itoa(t.Id)}
				effectsAdd := []State{NewState("at", argsAdd)}
				effectsRemove := []State{NewState("in", argsRemove)}
				preconditionsPositive := []State{NewState("in", argsPositive), NewState("train_at", argsPositive1)}
				var preconditionsNegative []State

				var operator = Unload
				argsExpr := []string{strconv.Itoa(p.Id), strconv.Itoa(t.Id), d}
				var aex = NewActionExpression(operator, argsExpr)
				action := NewAction(aex, preconditionsPositive, preconditionsNegative, effectsAdd, effectsRemove)
				listOfActions = append(listOfActions, action)
			}
		}
	}
	return listOfActions
}

//   Action(Travel(t, d1, d2),
//   PRECOND: Train_at(t, d1) ∧ Train(t) ∧ Destination(d1) ∧ Destination(d2)
//   EFFECT: Train_at(t, d2) ∧ ¬ Train_at(t, d1)
func TravelActions(trains []Train, destination []string, listOfActions []Action, db *sql.DB) []Action {
	for _, from := range destination {
		for _, to := range destination {
			if from!= to {
				for _, t := range trains {
					argsPositive := [2]string{strconv.Itoa(t.Id), from}
					argsAdd := [2]string{strconv.Itoa(t.Id), to}
					argsRemove := [2]string{strconv.Itoa(t.Id), from}
					effectsAdd := []State{NewState("train_at", argsAdd)}
					effectsRemove := []State{NewState("train_at", argsRemove)}
					preconditionsPositive := []State{NewState("train_at", argsPositive)}
					var preconditionsNegative []State

					var operator = Travel
					argsExpr := []string{strconv.Itoa(t.Id), from, to}
					var aex = NewActionExpression(operator, argsExpr)
					action := NewAction(aex, preconditionsPositive, preconditionsNegative, effectsAdd, effectsRemove)
					listOfActions = append(listOfActions, calculateCostOfAction(action))
				}
			}
		}
	}
	return listOfActions
}

func calculateCostOfAction(action Action) Action {
	var cost float64
	if action.expression.operator == Load || action.expression.operator == Unload{
		cost = 0
	}else{
		var destinationFrom = action.expression.arguments[1]
		var destinationTo = action.expression.arguments[2]
		cost = distanceBetweenCitiesByRail(destinationFrom, destinationTo)
	}
	action.cost = cost
	return action
}