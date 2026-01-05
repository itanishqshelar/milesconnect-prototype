package main

import (
	"log"
	"milesconnect-optimization/internal/api"
	"net/http"
	"os"
)

func main() {
	mux := http.NewServeMux()

	// Register Handlers
	mux.HandleFunc("/optimize", api.OptimizeRouteHandler)     // Existing TSP
	mux.HandleFunc("/optimize-load", api.OptimizeLoadHandler) // New Weight/Load Algo
	mux.HandleFunc("/health", api.HealthHandler)

	port := os.Getenv("PORT")
	if port == "" {
		port = "8081"
	}

	log.Printf("Starting Optimization Service on port %s", port)
	log.Printf("Enabled Solvers: TSP (Nearest Neighbor), FleetAlloc (Best Fit Decreasing)")

	if err := http.ListenAndServe(":"+port, mux); err != nil {
		log.Fatal(err)
	}
}
