# WaterControlSystem
A python based script to control water sensors and pumps

## Scope
This is the backend of a system that controls water pumps and moisture sensors. The idea is to measure soil moisture, control pumps, measure the water level in a reservoir and to generate some insights into the water consumption and well-being of the plants.

This is a spare-time project and not intended for production use. Collaboration is encouraged if you have any feedback, input or oppinions.

## Database
This project uses a Atlas Cloud database to store measurments and the system configuration. Later on we will build a web client to visualize that data and to control the system. The file `config.py` stores the config data, such as the access key for the databse.

