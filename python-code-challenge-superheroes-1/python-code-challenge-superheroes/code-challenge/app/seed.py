from app import app, db
from models import Hero, Power, HeroPower
from datetime import datetime

# Set the app context
app.app_context().push()

def clear_database():
    # Drop all tables to clear the database
    db.drop_all()
    db.create_all()

def create_seed_data():
    # Create some powers
    power1 = Power(name="Super Strength", description="Incredible physical strength. Superhuman power.", created_at=datetime.now(), updated_at=datetime.now())
    power2 = Power(name="Flight", description="Ability to fly. Soaring through the skies.", created_at=datetime.now(), updated_at=datetime.now())
    power3 = Power(name="Telekinesis", description="Move objects with the mind. Telekinetic abilities.", created_at=datetime.now(), updated_at=datetime.now())
    
    # Create some heroes
    hero1 = Hero(name="Superman", super_name="Clark Kent", created_at=datetime.now(), updated_at=datetime.now())
    hero2 = Hero(name="Wonder Woman", super_name="Diana Prince", created_at=datetime.now(), updated_at=datetime.now())
    hero3 = Hero(name="Professor X", super_name="Charles Xavier", created_at=datetime.now(), updated_at=datetime.now())
    
    # Add the powers and heroes to the database session and commit
    db.session.add_all([power1, power2, power3, hero1, hero2, hero3])
    db.session.commit()
    
    # Create hero powers after the heroes and powers are committed to the database
    hero_power1 = HeroPower(strength="Strong", hero_id=hero1.id, power_id=power1.id, created_at=datetime.now(), updated_at=datetime.now())
    hero_power2 = HeroPower(strength="Strong", hero_id=hero2.id, power_id=power2.id, created_at=datetime.now(), updated_at=datetime.now())
    hero_power3 = HeroPower(strength="Average", hero_id=hero3.id, power_id=power3.id, created_at=datetime.now(), updated_at=datetime.now())
    
    # Add the hero powers to the database session and commit
    db.session.add_all([hero_power1, hero_power2, hero_power3])
    db.session.commit()

if __name__ == '__main__':
    clear_database()  # Clear the database before adding seeds
    create_seed_data()  # Create and add seed data with updated values
    print("Seed data added successfully!")
