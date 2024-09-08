#!/bin/bash

# Variables
NEO4J_CONTAINER_NAME="neo4j-container"
MONGODB_CONTAINER_NAME="mongodb-container"
NEO4J_IMAGE="neo4j:latest"
MONGODB_IMAGE="mongo:latest"
NEO4J_PORT=7474
MONGODB_PORT=27017
NEO4J_USERNAME="neo4j"
NEO4J_PASSWORD="neo4j_password"
VECTOR_DIMENSIONS=4096

# Run MongoDB container
echo "Starting MongoDB container..."
docker run -d --name $MONGODB_CONTAINER_NAME -p $MONGODB_PORT:27017 $MONGODB_IMAGE

# Run Neo4j container
echo "Starting Neo4j container..."
docker run -d --name $NEO4J_CONTAINER_NAME -p $NEO4J_PORT:7474 -p 7687:7687 -e NEO4J_AUTH=$NEO4J_USERNAME/$NEO4J_PASSWORD $NEO4J_IMAGE


echo "Setup complete."

