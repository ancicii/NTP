package main
//import "C"

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

type googleApiResponse struct {
	Results Results `json:"results"`
}

type Results []Geometry

type Geometry struct {
	Geometry Location `json:"geometry"`
}

type Location struct {
	Location Coordinates `json:"location"`
}

type Coordinates struct {
	Latitude float64  `json:"lat"`
	Longitude float64  `json:"lng"`
}


// STATE
type State struct {
	name string
	arguments [2]string

}

func NewState(name string, arguments [2]string) State{
	s := State{name, arguments}
	return s

}

//ACTION EXPRESSION
//ex. load(p,t,d)
type ActionExpression struct {
	operator  Operator
	arguments []string

}

func NewActionExpression(operator Operator, arguments []string) ActionExpression{
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
	cost				  float64
	heuristicCost		  float64

}

func NewAction(expression ActionExpression, preconditionsPos []State, preconditionsNeg []State, effectsAdd []State, effectsRemove []State) Action{
	action := Action{expression, preconditionsPos, preconditionsNeg, effectsAdd, effectsRemove, 0,0}
	return action
}


//TRAIN
type Train struct {
	Id int
	StartDestination string
	IsAvailable bool

}

//PARCEL
type Parcel struct {
	Id int
	Weight int
	Price float64
	DestinationFrom string
	DestinationTo string
	ReceiverId sql.NullInt64
	SenderId sql.NullInt64
	DateCreated time.Time
	DateSent sql.NullTime
	IsDelivered bool
	IsSent bool
	IsApproved bool
	SenderName sql.NullString
	SenderSurname sql.NullString
	SenderContact sql.NullString
	ReceiverName sql.NullString
	ReceiverSurname sql.NullString
	ReceiverContact sql.NullString
	Description string


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
	Action ActionExpression //akcija koja nas je dovela u ovo stanje
	Cost float64 //g(x) cena od pocetnog cvora do cvora x
	Depth int
	index int //potrebno za priority queue
	h float64 //h(x) heuristika, procenjena cena najjeftinije putanje od cvora x do cilja
	f float64 //cost + h, za A* pretragu
}


func NewNode(state []State) *Node{
	var actionEx ActionExpression
	node := &Node{state, nil, actionEx, 0, 0, 0, 0, 0}
	return node
}

func NewChildNode(state []State, parent *Node, actionEx ActionExpression) *Node{
	node := &Node{state, parent, actionEx, 0, parent.Depth+1, 0 , 0, 0}
	return node
}

func NewChildNodeCost(state []State, parent *Node, action Action) *Node{
	cost := parent.Cost + action.cost
	h := parent.h + action.heuristicCost
	f := cost + h
	node := &Node{state, parent, action.expression, cost, parent.Depth+1, 0 , h, f}
	return node
}

