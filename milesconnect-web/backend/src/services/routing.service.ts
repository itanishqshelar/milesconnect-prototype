/**
 * Routing Service
 * Optimize waypoint sequences for trip sheets using TSP algorithm
 */

import prisma from "../prisma/client";
import {
    optimizeRouteSequence,
    calculateRouteMetrics,
    validateRouteSequence,
} from "../utils/tsp";
import { getCoordinates } from "../utils/distanceCalculator";

interface Waypoint {
    id: string;
    type: "pickup" | "drop";
    shipmentId: string;
    location: string;
    latitude?: number;
    longitude?: number;
}

interface OptimizedRoute {
    waypoints: Array<{
        order: number;
        shipmentId: string;
        type: "pickup" | "drop";
        location: string;
        distanceFromPrevious: number;
        eta: string;
    }>;
    metrics: {
        totalDistance: number;
        totalTime: number;
        pickupCount: number;
        dropCount: number;
    };
    isValid: boolean;
    errors: string[];
}

/**
 * Generate optimized route sequence for a trip sheet
 */
export async function optimizeTripSheetRoute(
    vehicleId: string,
    shipmentIds: string[]
): Promise<OptimizedRoute> {
    try {
        // Fetch shipments
        const shipments = await prisma.shipment.findMany({
            where: {
                id: { in: shipmentIds },
            },
            select: {
                id: true,
                referenceNumber: true,
                originAddress: true,
                destinationAddress: true,
            },
        });

        // Get vehicle (mock current location)
        const vehicle = await prisma.vehicle.findUnique({
            where: { id: vehicleId },
            select: { registrationNumber: true },
        });

        if (!vehicle) {
            throw new Error("Vehicle not found");
        }

        // Build waypoints
        const waypoints: Waypoint[] = [];
        for (const shipment of shipments) {
            // Pickup
            const pickupCoords = getCoordinates(shipment.originAddress);
            waypoints.push({
                id: `pickup_${shipment.id}`,
                type: "pickup",
                shipmentId: shipment.id,
                location: shipment.originAddress,
                latitude: pickupCoords?.latitude,
                longitude: pickupCoords?.longitude,
            });

            // Drop
            const dropCoords = getCoordinates(shipment.destinationAddress);
            waypoints.push({
                id: `drop_${shipment.id}`,
                type: "drop",
                shipmentId: shipment.id,
                location: shipment.destinationAddress,
                latitude: dropCoords?.latitude,
                longitude: dropCoords?.longitude,
            });
        }

        // Mock current vehicle location (use first pickup as starting point)
        const startLocation = waypoints[0]?.latitude
            ? { latitude: waypoints[0].latitude, longitude: waypoints[0].longitude! }
            : { latitude: 19.076, longitude: 72.8777 }; // Default: Mumbai

        // Optimize route
        const optimized = optimizeRouteSequence(waypoints, startLocation);

        // Calculate metrics
        const metrics = calculateRouteMetrics(optimized);

        // Validate sequence
        const validation = validateRouteSequence(optimized);

        // Format response
        const formattedWaypoints = optimized.map((wp) => ({
            order: wp.order,
            shipmentId: wp.shipmentId,
            type: wp.type,
            location: wp.location,
            distanceFromPrevious: Math.round(wp.distanceFromPrevious * 100) / 100,
            eta: wp.estimatedArrival?.toISOString().split("T")[1].slice(0, 5) || "N/A",
        }));

        return {
            waypoints: formattedWaypoints,
            metrics,
            isValid: validation.isValid,
            errors: validation.errors,
        };
    } catch (error) {
        console.error("Error optimizing route:", error);
        throw error;
    }
}

/**
 * Get route suggestions for pending shipments
 */
export async function suggestRoute(tripSheetId: string): Promise<OptimizedRoute> {
    try {
        // Fetch trip sheet with linked shipments
        const tripSheet = await prisma.tripSheet.findUnique({
            where: { id: tripSheetId },
            include: {
                shipments: {
                    include: {
                        shipment: {
                            select: {
                                id: true,
                                originAddress: true,
                                destinationAddress: true,
                            },
                        },
                    },
                },
                // Removed vehicle include, relying on vehicleId FK
            },
        });

        if (!tripSheet) {
            throw new Error("Trip sheet not found");
        }

        const shipmentIds = tripSheet.shipments.map(
            (link) => link.shipment.id
        );

        // Use the Foreign Key directly
        if (!tripSheet.vehicleId) {
            throw new Error("Trip sheet has no assigned vehicle");
        }
        return optimizeTripSheetRoute(tripSheet.vehicleId, shipmentIds);
    } catch (error) {
        console.error("Error suggesting route:", error);
        throw error;
    }
}
