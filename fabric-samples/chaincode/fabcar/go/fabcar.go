/*
SPDX-License-Identifier: Apache-2.0
*/

package main

import (
	"encoding/json"
	"fmt"
	"strconv"

	"github.com/hyperledger/fabric-contract-api-go/contractapi"
)

// SmartContract provides functions for managing a car
type SmartContract struct {
	contractapi.Contract
}

// Car describes basic details of what makes up a car
type Car struct {
	Make   string `json:"make"`
	Model  string `json:"model"`
	Colour string `json:"colour"`
	Owner  string `json:"owner"`
}
type Task struct {
	Task_number string `json:"Task_number"`
	Task_size string `json:"Task_size"`
	Cpu_cycles string `json:"Cpu_cycles"`
	Deadline string `json:"Deadline"`
}
type Server struct {
    Server_number string `json:"server_number"`
	Cpu_clock_frequency	string `json:"cpu_clock_frequency"`
	Memory string `json:"memory"`
	Tasks []Task `json:"tasks"`
	Hardware_info string `json:"hardware_info"`
	Power string `json:"power"`
}
// QueryResult structure used for handling result of query
type QueryResult struct {
	Key    string `json:"Key"`
	Record *Car
}

// InitLedger adds a base set of cars to the ledger
func (s *SmartContract) InitLedger(ctx contractapi.TransactionContextInterface) error {
	cars := []Car{
		Car{Make: "Toyota", Model: "Prius", Colour: "blue", Owner: "Tomoko"},
		Car{Make: "Ford", Model: "Mustang", Colour: "red", Owner: "Brad"},
		Car{Make: "Hyundai", Model: "Tucson", Colour: "green", Owner: "Jin Soo"},
		Car{Make: "Volkswagen", Model: "Passat", Colour: "yellow", Owner: "Max"},
		Car{Make: "Tesla", Model: "S", Colour: "black", Owner: "Adriana"},
		Car{Make: "Peugeot", Model: "205", Colour: "purple", Owner: "Michel"},
		Car{Make: "Chery", Model: "S22L", Colour: "white", Owner: "Aarav"},
		Car{Make: "Fiat", Model: "Punto", Colour: "violet", Owner: "Pari"},
		Car{Make: "Tata", Model: "Nano", Colour: "indigo", Owner: "Valeria"},
		Car{Make: "Holden", Model: "Barina", Colour: "brown", Owner: "Shotaro"},
	}

	for i, car := range cars {
		carAsBytes, _ := json.Marshal(car)
		err := ctx.GetStub().PutState("CAR"+strconv.Itoa(i), carAsBytes)

		if err != nil {
			return fmt.Errorf("Failed to put to world state. %s", err.Error())
		}
	}

	return nil
}

// CreateCar adds a new car to the world state with given details
func (s *SmartContract) CreateCar(ctx contractapi.TransactionContextInterface, carNumber string, make string, model string, colour string, owner string) error {
	car := Car{
		Make:   make,
		Model:  model,
		Colour: colour,
		Owner:  owner,
	}

	carAsBytes, _ := json.Marshal(car)

	return ctx.GetStub().PutState(carNumber, carAsBytes)
}
func (s *SmartContract) AddServer(ctx contractapi.TransactionContextInterface,server_number string,cpu_clock_frequency string, memory string, hardware_info string, power string) error {
	serverID, err := ctx.GetStub().CreateCompositeKey("", []string{"server", server_number})
    if err != nil {
		return fmt.Errorf("cannot create composite key: %v", err)
	}
	server_, err := ctx.GetStub().GetState(serverID)
	if err != nil {
		return fmt.Errorf("failed to read from world state: %v", err)
	}
	if server_ != nil {
		return fmt.Errorf("Server with this server number already exist: %v", err)
	}
	server := Server{
		Server_number: server_number,
		Cpu_clock_frequency: cpu_clock_frequency,
		Memory: memory,
		Hardware_info: hardware_info,
		Power: power,
		Tasks: []Task{},
	}
	serverAsBytes, _ :=json.Marshal(server)
	return ctx.GetStub().PutState(serverID, serverAsBytes)

}
func (s *SmartContract) QueryServer(ctx contractapi.TransactionContextInterface, server_number string) (*Server, error) {
	// serverAsBytes, err := ctx.GetStub().GetState(server_number)
	serverID, err := ctx.GetStub().CreateCompositeKey("", []string{"server", server_number})

	serverAsBytes, err := ctx.GetStub().GetState(serverID)

	if err != nil {
		return nil, fmt.Errorf("Failed to read from world state. %s", err.Error())
	}

	if serverAsBytes == nil {
		return nil, fmt.Errorf("%s does not exist", server_number)
	}

	var serverJSON Server
	err = json.Unmarshal(serverAsBytes, &serverJSON)
	if err != nil {
		return nil, err
	}
	
	return &serverJSON, nil
}
func (s *SmartContract) QueryAllServers(ctx contractapi.TransactionContextInterface) ([]*Server, error) {
	// startKey := ""
	// endKey := ""

	resultsIterator, err := ctx.GetStub().GetStateByPartialCompositeKey("", []string{"server"})
	// resultsIterator, err := ctx.GetStub().

	if err != nil {
		return nil, err
	}
	defer resultsIterator.Close()

	var servers []*Server
	for resultsIterator.HasNext() {
		queryResponse, err := resultsIterator.Next()
		if err != nil {
			return nil, err
		}

		var server Server
		_ = json.Unmarshal(queryResponse.Value, &server)
		servers = append(servers, &server)
		fmt.Println(servers)
	}
	return servers, nil
}
func (s *SmartContract) AddTaskToServer(ctx contractapi.TransactionContextInterface, server_number string, task Task) error {
	serverID, err := ctx.GetStub().CreateCompositeKey("", []string{"server", server_number})
	if err != nil {
		return fmt.Errorf("cannot create composite key: %v", err)
	}
	server, err := ctx.GetStub().GetState(serverID)
	//check whether student with given id already exist or not
	if err != nil {
		return fmt.Errorf("failed to read from world state: %v", err)
	}
	if server == nil {
		return fmt.Errorf("Server ID does not exist: %v", err)
	}

	var serverJSON Server
	_ = json.Unmarshal(server, &serverJSON)
	
	compositeKey, _ := ctx.GetStub().CreateCompositeKey("", []string{"task", task.Task_number})
	task_, err := ctx.GetStub().GetState(compositeKey)
	if err!= nil {
		return fmt.Errorf("failed to read from world state: %v", err)
	}
	if task_ != nil {
		return fmt.Errorf("Task with this task number is already assigned to some edge server: %v", err)
	}
	taskJSON := Task{
		Task_number: task.Task_number,
		Task_size: task.Task_size,
		Cpu_cycles: task.Cpu_cycles,
		Deadline: task.Deadline,
	}
	taskAsBytes, err := json.Marshal(taskJSON)
	if err != nil {
		return fmt.Errorf("failed to parse given Task object: %v", err)
	
	}
	
	_ = ctx.GetStub().PutState(compositeKey, taskAsBytes)
    serverJSON.Tasks = append(serverJSON.Tasks, task)
	server, _ = json.Marshal(serverJSON)
	// ctx.GetStub().SetEvent("choice", nil) //Event to measure execution time
	return ctx.GetStub().PutState(serverID, server)
}

func (s *SmartContract) ExchangeTask(ctx contractapi.TransactionContextInterface, source_server_number string, destination_server_number string, task Task) error {
	fmt.Println("In exchange task function")
	sourceserverID, err := ctx.GetStub().CreateCompositeKey("", []string{"server", source_server_number})
	if err != nil {
		return fmt.Errorf("cannot create composite key: %v", err)
	}
	sourceserver, err := ctx.GetStub().GetState(sourceserverID)
	//check whether student with given id already exist or not
	if err != nil {
		return fmt.Errorf("failed to read from world state: %v", err)
	}
	if sourceserver == nil {
		return fmt.Errorf("Source Server ID does not exist: %v", err)
	}
    destinationserverID, err := ctx.GetStub().CreateCompositeKey("", []string{"server", destination_server_number})
	if err != nil {
		return fmt.Errorf("cannot create composite key: %v", err)
	}
	destinationserver, err := ctx.GetStub().GetState(destinationserverID)
	//check whether student with given id already exist or not
	if err != nil {
		return fmt.Errorf("failed to read from world state: %v", err)
	}
	if destinationserver == nil {
		return fmt.Errorf("Source Server ID does not exist: %v", err)
	}
	var sourceserverJSON Server
	_ = json.Unmarshal(sourceserver, &sourceserverJSON)
	var destinationserverJSON Server
	_ = json.Unmarshal(destinationserver, &destinationserverJSON)

	
	compositeKey, _ := ctx.GetStub().CreateCompositeKey("", []string{"task", task.Task_number})
	task_, err := ctx.GetStub().GetState(compositeKey)
	if err!= nil {
		return fmt.Errorf("failed to read from world state: %v", err)
	}
	if task_ == nil {
		return fmt.Errorf("Task with this task number is not assigned to any edge server: %v", err)
	}
	taskJSON := Task{
		Task_number: task.Task_number,
		Task_size: task.Task_size,
		Cpu_cycles: task.Cpu_cycles,
		Deadline: task.Deadline,
	}
	taskAsBytes, err := json.Marshal(taskJSON)
	if err != nil {
		return fmt.Errorf("failed to parse given Task object: %v", err)
	
	}
	
	_ = ctx.GetStub().PutState(compositeKey, taskAsBytes)
    destinationserverJSON.Tasks = append(destinationserverJSON.Tasks, task)
	destinationserver, _ = json.Marshal(destinationserverJSON)
	// // ctx.GetStub().SetEvent("choice", nil) //Event to measure execution time
	_ = ctx.GetStub().PutState(destinationserverID, destinationserver)
	var position int
	position = -1
	for index, element := range sourceserverJSON.Tasks {
		if element == task {
			position = index
			break
		}
	}
	if position == -1 {
		return fmt.Errorf("Task not found in task list: %v", err)
	} else {
		sourceserverJSON.Tasks = append(sourceserverJSON.Tasks[:position], sourceserverJSON.Tasks[position+1:]...)
	}
	sourceserver, _ = json.Marshal(sourceserverJSON)
	
	return ctx.GetStub().PutState(sourceserverID, sourceserver)

}
// QueryCar returns the car stored in the world state with given id
func (s *SmartContract) QueryCar(ctx contractapi.TransactionContextInterface, carNumber string) (*Car, error) {
	carAsBytes, err := ctx.GetStub().GetState(carNumber)

	if err != nil {
		return nil, fmt.Errorf("Failed to read from world state. %s", err.Error())
	}

	if carAsBytes == nil {
		return nil, fmt.Errorf("%s does not exist", carNumber)
	}

	car := new(Car)
	_ = json.Unmarshal(carAsBytes, car)

	return car, nil
}

// QueryAllCars returns all cars found in world state
func (s *SmartContract) QueryAllCars(ctx contractapi.TransactionContextInterface) ([]QueryResult, error) {
	startKey := ""
	endKey := ""

	resultsIterator, err := ctx.GetStub().GetStateByRange(startKey, endKey)

	if err != nil {
		return nil, err
	}
	defer resultsIterator.Close()

	results := []QueryResult{}

	for resultsIterator.HasNext() {
		queryResponse, err := resultsIterator.Next()

		if err != nil {
			return nil, err
		}

		car := new(Car)
		_ = json.Unmarshal(queryResponse.Value, car)

		queryResult := QueryResult{Key: queryResponse.Key, Record: car}
		results = append(results, queryResult)
	}

	return results, nil
}

// ChangeCarOwner updates the owner field of car with given id in world state
func (s *SmartContract) ChangeCarOwner(ctx contractapi.TransactionContextInterface, carNumber string, newOwner string) error {
	car, err := s.QueryCar(ctx, carNumber)

	if err != nil {
		return err
	}

	car.Owner = newOwner

	carAsBytes, _ := json.Marshal(car)

	return ctx.GetStub().PutState(carNumber, carAsBytes)
}

func main() {

	chaincode, err := contractapi.NewChaincode(new(SmartContract))

	if err != nil {
		fmt.Printf("Error create fabcar chaincode: %s", err.Error())
		return
	}

	if err := chaincode.Start(); err != nil {
		fmt.Printf("Error starting fabcar chaincode: %s", err.Error())
	}
}
