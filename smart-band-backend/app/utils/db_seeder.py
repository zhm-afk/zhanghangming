from app.extensions import db
from app.models.customer import Customer
from app.models.device import Device
from app.models.health_data import HealthData
from app.models.feedback import Feedback
from app.utils.data_generator import (
    generate_customer_data,
    generate_device_data,
    generate_health_data,
    generate_feedback_data
)

def seed_customers(count=50):
    """Seed customers into the database"""
    print(f"Seeding {count} customers...")
    
    customer_data = generate_customer_data(count)
    customer_ids = []
    
    for data in customer_data:
        customer = Customer(
            username=data['username'],
            nickname=data['nickname'],
            age=data['age'],
            gender=data['gender'],
            phone=data['phone'],
            email=data['email']
        )
        db.session.add(customer)
    
    db.session.commit()
    
    # Get the IDs of all customers
    customers = Customer.query.all()
    customer_ids = [customer.id for customer in customers]
    
    print(f"Seeded {len(customer_ids)} customers.")
    return customer_ids

def seed_devices(customer_ids, count=100):
    """Seed devices into the database"""
    print(f"Seeding {count} devices...")
    
    device_data = generate_device_data(customer_ids, count)
    device_ids = []
    
    for data in device_data:
        device = Device(
            device_id=data['device_id'],
            device_name=data['device_name'],
            customer_id=data['customer_id'],
            status=data['status'],
            battery_level=data['battery_level'],
            firmware=data['firmware'],
            last_sync=data['last_sync'],
            latitude=data['latitude'],
            longitude=data['longitude'],
            area=data['area'],
            location_updated_at=data['location_updated_at']
        )
        db.session.add(device)
    
    db.session.commit()
    
    # Get the IDs of all devices
    devices = Device.query.all()
    device_ids = [device.id for device in devices]
    
    print(f"Seeded {len(device_ids)} devices.")
    return device_ids

def seed_health_data(customer_ids, device_ids, days=7, readings_per_day=24):
    """Seed health data into the database"""
    print(f"Seeding health data for {len(customer_ids)} customers over {days} days...")
    
    # Create customer-device pairs (each customer has one or more devices)
    customer_device_pairs = []
    devices = Device.query.all()
    
    for device in devices:
        customer_device_pairs.append((device.customer_id, device.id))
    
    # Generate health data
    health_data_entries = generate_health_data(customer_device_pairs, days, readings_per_day)
    
    # Batch insert for better performance
    batch_size = 1000
    total_entries = len(health_data_entries)
    
    for i in range(0, total_entries, batch_size):
        batch = health_data_entries[i:i+batch_size]
        health_data_objects = []
        
        for data in batch:
            health_data = HealthData(
                customer_id=data['customer_id'],
                device_id=data['device_id'],
                timestamp=data['timestamp'],
                heart_rate=data['heart_rate'],
                systolic_pressure=data['systolic_pressure'],
                diastolic_pressure=data['diastolic_pressure'],
                steps=data['steps'],
                calories=data['calories'],
                sleep_duration=data['sleep_duration'],
                oxygen_saturation=data['oxygen_saturation'],
                temperature=data['temperature'],
                environment_temperature=data['environment_temperature'],
                humidity=data['humidity'],
                pressure=data['pressure']
            )
            health_data_objects.append(health_data)
        
        db.session.add_all(health_data_objects)
        db.session.commit()
        
        print(f"Seeded batch {i//batch_size + 1}/{(total_entries-1)//batch_size + 1} of health data...")
    
    print(f"Seeded {total_entries} health data entries.")

def seed_feedback(customer_ids, count=20):
    """Seed feedback into the database"""
    print(f"Seeding {count} feedback entries...")
    
    feedback_data = generate_feedback_data(customer_ids, count)
    
    for data in feedback_data:
        feedback = Feedback(
            customer_id=data['customer_id'],
            type=data['type'],
            status=data['status'],
            subject=data['subject'],
            content=data['content'],
            created_at=data['created_at']
        )
        db.session.add(feedback)
    
    db.session.commit()
    print(f"Seeded {count} feedback entries.")

def seed_database(customer_count=50, device_count=100, days=7, feedback_count=20):
    """Seed the entire database with sample data"""
    print("Starting database seeding...")
    
    # Clear existing data if needed
    db.session.query(HealthData).delete()
    db.session.query(Feedback).delete()
    db.session.query(Device).delete()
    db.session.query(Customer).delete()
    db.session.commit()
    
    # Seed data
    customer_ids = seed_customers(customer_count)
    device_ids = seed_devices(customer_ids, device_count)
    seed_health_data(customer_ids, device_ids, days)
    seed_feedback(customer_ids, feedback_count)
    
    print("Database seeding completed!")
    
    # Return summary
    return {
        'customers': customer_count,
        'devices': device_count,
        'days_of_health_data': days,
        'feedback_entries': feedback_count
    } 