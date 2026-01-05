package main

import (
	"encoding/json"
	"fmt"
	"math"
	"net/http"
)

// Coordinate represents a GPS location
type Coordinate struct {
	Lat float64 `json:"latitude"`
	Lon float64 `json:"longitude"`
	ID  string  `json:"id,omitempty"` // Shipment ID or custom identifier
}

// OptimizationRequest is the input payload
type OptimizationRequest struct {
	Start    Coordinate   `json:"start"`
	Stops    []Coordinate `json:"stops"`
}

// Distance calculates haversine distance between two points
func Distance(p1, p2 Coordinate) float64 {
	const R = 6371 // Earth radius in km
	dLat := (p2.Lat - p1.Lat) * (math.Pi / 180.0)
	dLon := (p2.Lon - p1.Lon) * (math.Pi / 180.0)

	lat1 := p1.Lat * (math.Pi / 180.0)
	lat2 := p2.Lat * (math.Pi / 180.0)

	a := math.Sin(dLat/2)*math.Sin(dLat/2) +
		math.Sin(dLon/2)*math.Sin(dLon/2)*math.Cos(lat1)*math.Cos(lat2)
	c := 2 * math.Atan2(math.Sqrt(a), math.Sqrt(1-a))

	return R * c
}

// SolveTSPNearestNeighbor solves TSP using Nearest Neighbor heuristic
// This is O(N^2) which is very fast for typical delivery route sizes (< 100 stops)
func SolveTSPNearestNeighbor(start Coordinate, stops []Coordinate) []Coordinate {
	if len(stops) == 0 {
		return []Coordinate{}
	}

	remaining := make([]Coordinate, len(stops))
	copy(remaining, stops)

	route := make([]Coordinate, 0, len(stops))
	current := start

	for len(remaining) > 0 {
		nearestIdx := -1
		minDist := math.MaxFloat64

		for i, stop := range remaining {
			dist := Distance(current, stop)
			if dist < minDist {
				minDist = dist
				nearestIdx = i
			}
		}

		nextStop := remaining[nearestIdx]
		route = append(route, nextStop)
		current = nextStop

		// Remove selected stop from remaining
		remaining = append(remaining[:nearestIdx], remaining[nearestIdx+1:]...)
	}

	return route
}

func optimizeHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	var req OptimizationRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, "Invalid request body", http.StatusBadRequest)
		return
	}

	optimizedRoute := SolveTSPNearestNeighbor(req.Start, req.Stops)

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(optimizedRoute)
}

func main() {
	http.HandleFunc("/optimize", optimizeHandler)
	
	port := ":8081"
	fmt.Printf("Go Optimization Service running on port %s\n", port)
	if err := http.ListenAndServe(port, nil); err != nil {
		fmt.Printf("Failed to start server: %v\n", err)
	}
}
