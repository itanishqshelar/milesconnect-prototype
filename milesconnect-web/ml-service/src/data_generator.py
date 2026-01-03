"""
Synthetic Data Generator for ML Training

Generates realistic training data for:
- Driver performance scoring
- Vehicle maintenance prediction  
- Demand forecasting
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import json
from pathlib import Path


class SyntheticDataGenerator:
    def __init__(self, seed=42):
        np.random.seed(seed)
        random.seed(seed)
        self.output_dir = Path(__file__).parent.parent / "data"
        self.output_dir.mkdir(exist_ok=True)
    
    def generate_driver_data(self, n_drivers=100):
        """Generate synthetic driver performance data"""
        data = []
        
        for i in range(n_drivers):
            driver_id = f"DR-{i+1:04d}"
            experience_months = np.random.randint(6, 120)  # 6 months to 10 years
            
            # Base performance influenced by experience
            experience_factor = min(experience_months / 60, 1.0)  # Caps at 5 years
            
            total_trips = np.random.randint(50, 500)
            
            # On-time delivery rate (70-98%, better with experience)
            base_on_time_rate = 0.7 + (experience_factor * 0.2)
            on_time_rate = np.clip(np.random.normal(base_on_time_rate, 0.1), 0.5, 0.99)
            on_time_deliveries = int(total_trips * on_time_rate)
            late_deliveries = total_trips - on_time_deliveries
            
            # Average speed (40-80 km/h)
            avg_speed = np.random.uniform(40, 80)
            
            # Safety metrics (harsh events, inversely related to experience)
            harsh_braking_count = np.random.poisson(max(20 - (experience_factor * 15), 5))
            harsh_acceleration_count = np.random.poisson(max(25 - (experience_factor * 18), 7))
            
            # Idle time (10-60 mins per trip on average)
            idle_time_mins = np.random.uniform(10, 60) * total_trips
            
            # Fuel efficiency (8-18 km/l, better with experience)
            base_fuel_eff = 10 + (experience_factor * 4)
            fuel_efficiency = np.clip(np.random.normal(base_fuel_eff, 2), 8, 18)
            
            # Total distance
            distance_km = total_trips * np.random.uniform(30, 150)
            
            # Incidents (rare, 0-3)
            incident_count = np.random.choice([0, 0, 0, 1, 1, 2], p=[0.5, 0.3, 0.1, 0.05, 0.03, 0.02])
            
            # Customer rating (3.5-5.0, correlated with on-time rate)
            customer_rating = np.clip(3.0 + (on_time_rate * 2) + np.random.normal(0, 0.3), 3.0, 5.0)
            
            # Calculate driver score (0-100)
            # Weights: on-time (35%), fuel (20%), safety (25%), rating (10%), experience (10%)
            safety_score = 100 * (1 - (harsh_braking_count + harsh_acceleration_count) / (total_trips * 2))
            safety_score = max(0, min(100, safety_score))
            
            driver_score = (
                on_time_rate * 35 +
                (fuel_efficiency / 18) * 20 +
                (safety_score / 100) * 25 +
                (customer_rating / 5) * 10 +
                experience_factor * 10
            )
            
            data.append({
                'driver_id': driver_id,
                'total_trips': total_trips,
                'on_time_deliveries': on_time_deliveries,
                'late_deliveries': late_deliveries,
                'avg_speed_kmh': round(avg_speed, 2),
                'harsh_braking_count': harsh_braking_count,
                'harsh_acceleration_count': harsh_acceleration_count,
                'idle_time_mins': round(idle_time_mins, 2),
                'fuel_efficiency_kmpl': round(fuel_efficiency, 2),
                'distance_km': round(distance_km, 2),
                'experience_months': experience_months,
                'incident_count': incident_count,
                'customer_rating': round(customer_rating, 2),
                'driver_score': round(driver_score, 2)
            })
        
        df = pd.DataFrame(data)
        output_path = self.output_dir / "driver_performance.csv"
        df.to_csv(output_path, index=False)
        print(f"✓ Generated {len(df)} driver records → {output_path}")
        return df
    
    def generate_maintenance_data(self, n_vehicles=80):
        """Generate synthetic vehicle maintenance data"""
        data = []
        makes_models = [
            "Tata Ace Gold", "Mahindra Jeeto", "Eicher Pro 3015",
            "Ashok Leyland Dost", "Force Motors Traveller",
            "Maruti Suzuki Super Carry", "Piaggio Ape Auto"
        ]
        
        for i in range(n_vehicles):
            vehicle_id = f"VH-{i+1:04d}"
            age_months = np.random.randint(6, 60)  # 6 months to 5 years
            make_model = random.choice(makes_models)
            
            # Odometer (20k-150k km based on age)
            base_km = age_months * np.random.uniform(500, 2500)
            odometer_km = int(base_km + np.random.normal(0, 5000))
            
            # Last maintenance (0-90 days ago)
            days_since_maintenance = np.random.randint(0, 90)
            
            # Usage patterns
            total_trips = np.random.randint(100, 800)
            avg_trip_distance = odometer_km / total_trips if total_trips > 0 else 50
            
            # Harsh usage score (0-100, higher = more harsh)
            harsh_usage_score = np.random.uniform(20, 80)
            
            # Fuel consumption variance (0-30%, higher = potential issue)
            fuel_variance = np.random.uniform(0, 30)
            
            # Reported issues
            reported_issues = np.random.poisson(age_months / 12)  # More issues with age
            
            # Determine maintenance risk
            # Factors: days since maintenance, odometer, harsh usage, age
            risk_score = (
                (days_since_maintenance / 90) * 30 +
                (odometer_km / 150000) * 25 +
                (harsh_usage_score / 100) * 20 +
                (age_months / 60) * 15 +
                (reported_issues / 5) * 10
            )
            
            # days until maintenance needed
            if risk_score > 70:
                maintenance_class = "immediate"
                days_until = np.random.randint(1, 7)
            elif risk_score > 40:
                maintenance_class = "soon"
                days_until = np.random.randint(7, 30)
            else:
                maintenance_class = "normal"
                days_until = np.random.randint(30, 90)
            
            data.append({
                'vehicle_id': vehicle_id,
                'make_model': make_model,
                'age_months': age_months,
                'odometer_km': odometer_km,
                'days_since_last_maintenance': days_since_maintenance,
                'total_trips': total_trips,
                'avg_trip_distance_km': round(avg_trip_distance, 2),
                'harsh_usage_score': round(harsh_usage_score, 2),
                'fuel_consumption_variance': round(fuel_variance, 2),
                'reported_issues_count': reported_issues,
                'maintenance_class': maintenance_class,
                'days_until_maintenance': days_until,
                'risk_score': round(risk_score, 2)
            })
        
        df = pd.DataFrame(data)
        output_path = self.output_dir / "vehicle_maintenance.csv"
        df.to_csv(output_path, index=False)
        print(f"✓ Generated {len(df)} vehicle maintenance records → {output_path}")
        return df
    
    def generate_demand_forecast_data(self, n_days=730):
        """Generate synthetic shipment demand data (2 years)"""
        data = []
        start_date = datetime.now() - timedelta(days=n_days)
        
        # Base trend (slight growth over time)
        base_demand = 50
        growth_rate = 0.0005  # Daily growth
        
        # Indian holidays for 2024-2025 (sample)
        holidays = [
            "2024-01-26", "2024-03-25", "2024-08-15", "2024-10-02",
            "2024-10-31", "2024-11-01", "2024-12-25",
            "2025-01-26", "2025-03-14", "2025-08-15", "2025-10-02"
        ]
        holiday_dates = set(holidays)
        
        for day in range(n_days):
            current_date = start_date + timedelta(days=day)
            date_str = current_date.strftime("%Y-%m-%d")
            
            # Day of week effect (weekdays higher)
            day_of_week = current_date.weekday()
            dow_factor = 1.2 if day_of_week < 5 else 0.6  # Mon-Fri vs Sat-Sun
            
            # Monthly seasonality (higher in Q4, festival season)
            month = current_date.month
            if month in [10, 11, 12]:  # Diwali, year-end
                seasonal_factor = 1.3
            elif month in [6, 7, 8]:  # Monsoon slowdown
                seasonal_factor = 0.9
            else:
                seasonal_factor = 1.0
            
            # Holiday effect (reduced demand)
            is_holiday = date_str in holiday_dates
            holiday_factor = 0.5 if is_holiday else 1.0
            
            # Trend
            trend = base_demand + (day * growth_rate * base_demand)
            
            # Random noise
            noise = np.random.normal(0, 5)
            
            # Calculate demand
            shipments = max(0, int(
                trend * dow_factor * seasonal_factor * holiday_factor + noise
            ))
            
            # Historical context (rolling averages)
            if day >= 7:
                last_7d = [data[i]['shipments'] for i in range(max(0, day-7), day)]
                hist_7d = int(np.mean(last_7d))
            else:
                hist_7d = shipments
            
            if day >= 30:
                last_30d = [data[i]['shipments'] for i in range(max(0, day-30), day)]
                hist_30d = int(np.mean(last_30d))
            else:
                hist_30d = shipments
            
            # Average shipment weight
            avg_weight = np.random.uniform(200, 800)
            
            # Active vehicles (correlated with demand)
            active_vehicles = int(np.clip(shipments /10, 5, 15))
            
            data.append({
                'date': date_str,
                'day_of_week': day_of_week,
                'month': month,
                'is_holiday': is_holiday,
                'historical_shipments_7d': hist_7d,
                'historical_shipments_30d': hist_30d,
                'avg_shipment_weight_kg': round(avg_weight, 2),
                'active_vehicles_count': active_vehicles,
                'seasonal_index': round(seasonal_factor, 2),
                'shipments': shipments
            })
        
        df = pd.DataFrame(data)
        output_path = self.output_dir / "demand_forecast.csv"
        df.to_csv(output_path, index=False)
        print(f"✓ Generated {len(df)} demand forecast records → {output_path}")
        return df
    
    def generate_all(self):
        """Generate all synthetic datasets"""
        print("\n🔄 Generating synthetic training data...\n")
        
        driver_df = self.generate_driver_data(n_drivers=150)
        maintenance_df = self.generate_maintenance_data(n_vehicles=100)
        demand_df = self.generate_demand_forecast_data(n_days=730)
        
        print(f"\n✅ All datasets generated successfully!")
        print(f"\nDataset Statistics:")
        print(f"  - Drivers: {len(driver_df)} records")
        print(f"  - Vehicles: {len(maintenance_df)} records")
        print(f"  - Demand History: {len(demand_df)} days")
        
        return driver_df, maintenance_df, demand_df


if __name__ == "__main__":
    generator = SyntheticDataGenerator()
    generator.generate_all()
