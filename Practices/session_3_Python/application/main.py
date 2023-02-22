import psycopg2
from typing import Type
from animals import Animal, Mammal, Fish, Bird

import os

# Define the connection parameters
conn_params = {
    "host": os.getenv('DB_HOST'),
    "port": os.getenv('DB_PORT'),
    "database": os.getenv('DB_NAME'),
    "user": os.getenv('DB_USER'),
    "password": os.getenv('DB_PASSWORD')
}

# Connect to the database
conn = psycopg2.connect(**conn_params)
cur = conn.cursor()

# Define the SQL insert statement
sql = "INSERT INTO animal (name, most_liked_food, animal_classification) VALUES (%s, %s, %s)"

# Define a list of animals to insert
animals = [Mammal('monkey', 'banana', 4),
           Fish('shark', 'fish', 2),
           Bird('parrot', 'seeds', 2)]

# Loop through the animals and insert them into the database
for animal in animals:
    # Get the animal's classification based on its type
    classification = animal.__class__.__name__
    # Execute the SQL insert statement
    cur.execute(sql, (animal.name, animal.most_liked_food, classification))

# Commit the changes and close the connection
conn.commit()
cur.close()
conn.close()

print("Animals were inserted into Database")