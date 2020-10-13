package main

import (
	"database/sql"
	"time"
)

//OPERATOR load, unload, travel
type Operator int

const (
	Load   Operator = 0
	Unload Operator = 1
	Travel Operator = 2
)

func (op Operator) String() string {
	names := [...]string{
		"Load",
		"Unload",
		"Travel"}

	if op < Load || op > Travel {
		return "Unknown"
	}
	return names[op]
}

// STATE
type State struct {
	name string
	arguments [2]int

}

func NewState(name string, arguments [2]int) State{
	s := State{name, arguments}
	return s

}

//ACTION EXPRESSION
//ex. load(p,t,d)
type ActionExpression struct {
	operator  Operator
	arguments []int

}

func NewActionExpression(operator Operator, arguments []int) ActionExpression{
	expr := ActionExpression{operator,arguments}
	return expr

}

//ACTION with preconditions and effects
type Action struct {
	expression            ActionExpression
	preconditionsPositive []State
	preconditionsNegative []State
	effectsAdd            []State
	effectsRemove         []State

}

func NewAction(expression ActionExpression, preconditionsPos []State, preconditionsNeg []State, effectsAdd []State, effectsRemove []State) Action{
	action := Action{expression, preconditionsPos, preconditionsNeg, effectsAdd, effectsRemove}
	return action
}

//TRAIN
type Train struct {
	Id int
	StartDestination int
	IsAvailable bool

}

//PARCEL
type Parcel struct {
	Id int
	Weight int
	Price int
	DestinationFrom int
	DestinationTo int
	ReceiverId int
	SenderId int
	Date time.Time
	IsDelivered bool

}

//DESTINATION
type Destination struct {
	Id int
	Name string
	Country string
	Zipcode string
	State sql.NullString
	Longitude float32
	Latitude float32
}

//USER
type User struct {
	Id int
	Address string
	City string
}

//NODE
type Node struct {
	NodeState []State
	Parent *Node
	Children []*Node
	Action ActionExpression //that got us to this state
	Cost int
	Depth int
}

func NewNode(state []State) Node{
	var children []*Node
	node := Node{state, nil, children, nil, 0, 0}
	return node
}

