from database import engine

try:
    with engine.connect() as connection:
        print("✅ PostgreSQL connection successful!")
        print("✅ Connected to CodingBodhi database.")

except Exception as e:
    print("❌ Database connection failed!")
    print(e)