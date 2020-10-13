package main

type Problem struct {
	parcels       []Parcel
	trains        []Train
	destination   []Destination
	goalState     []State
	initialState  []State
	listOfActions []Action

}

func NewProblem(parcels []Parcel, trains []Train, destination []Destination, goalState []State, initialState []State) Problem {
	listOfActions := make([]Action, 0)
	p := Problem {parcels, trains, destination, goalState, initialState, listOfActions}
	return p
}

func AddActions(parcels []Parcel, trains []Train, destination []Destination, listOfActions []Action) []Action{
	listOfActions1 := LoadActions(parcels, trains, destination, listOfActions)
	listOfActions2 := UnloadActions(parcels, trains, destination, listOfActions1)
	listOfActions3 := TravelActions(trains, destination, listOfActions2)
	return listOfActions3
}
//   Action(Load(p, t, d),
//   PRECOND: At(p, d) ∧ At(t, d) ∧ Parcel(p) ∧ Train(t) ∧ Destination(d)
//   EFFECT: ¬ At(p, d) ∧ In(p, t))

func LoadActions(parcels []Parcel, trains []Train, destination []Destination, listOfActions []Action) []Action {
	for _, d := range destination {
		for _, p := range parcels {
			for _, t := range trains {
				argsPositive := [2]int{p.Id, d.Id}
				argsPositive1 := [2]int{t.Id, d.Id}
				argsAdd := [2]int{p.Id, t.Id}
				argsRemove := [2]int{p.Id, d.Id}
				effectsAdd := []State{NewState("in", argsAdd)}
				effectsRemove := []State{NewState("at", argsRemove)}
				preconditionsPositive := []State{NewState("at", argsPositive), NewState("train_at", argsPositive1)}
				var preconditionsNegative []State

				var operator = Load
				argsExpr := []int{p.Id, t.Id, d.Id}
				var aex = NewActionExpression(operator, argsExpr)
				action := NewAction(aex, preconditionsPositive, preconditionsNegative, effectsAdd, effectsRemove)
				listOfActions = append(listOfActions, action)
			}
		}
	}
	return listOfActions
}
//   Action(Unload(p, t, d),
//   PRECOND: In(p, t) ∧ At(t, d) ∧ Parcel(p) ∧ Train(t) ∧ Destination(d)
//   EFFECT: At(p, d) ∧ ¬ In(p, t))

func UnloadActions(parcels []Parcel, trains []Train, destination []Destination, listOfActions []Action) []Action {
	for _, d := range destination {
		for _, p := range parcels {
			for _, t := range trains {
				argsPositive := [2]int{p.Id, t.Id}
				argsPositive1 := [2]int{t.Id, d.Id}
				argsAdd := [2]int{p.Id, d.Id}
				argsRemove := [2]int{p.Id, t.Id}
				effectsAdd := []State{NewState("at", argsAdd)}
				effectsRemove := []State{NewState("in", argsRemove)}
				preconditionsPositive := []State{NewState("in", argsPositive), NewState("train_at", argsPositive1)}
				var preconditionsNegative []State

				var operator = Unload
				argsExpr := []int{p.Id, t.Id, d.Id}
				var aex = NewActionExpression(operator, argsExpr)
				action := NewAction(aex, preconditionsPositive, preconditionsNegative, effectsAdd, effectsRemove)
				listOfActions = append(listOfActions, action)
			}
		}
	}
	return listOfActions
}

func TravelActions(trains []Train, destination []Destination, listOfActions []Action) []Action {
	for _, from := range destination {
		for _, to := range destination {
			if from!= to {
				for _, t := range trains {
					argsPositive := [2]int{t.Id, from.Id}
					argsAdd := [2]int{t.Id, to.Id}
					argsRemove := [2]int{t.Id, from.Id}
					effectsAdd := []State{NewState("train_at", argsAdd)}
					effectsRemove := []State{NewState("train_at", argsRemove)}
					preconditionsPositive := []State{NewState("train_at", argsPositive)}
					var preconditionsNegative []State

					var operator = Travel
					argsExpr := []int{t.Id, from.Id, to.Id}
					var aex = NewActionExpression(operator, argsExpr)
					action := NewAction(aex, preconditionsPositive, preconditionsNegative, effectsAdd, effectsRemove)
					listOfActions = append(listOfActions, action)
				}
			}


		}
	}
	return listOfActions
}