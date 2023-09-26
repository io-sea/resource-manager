# Resource Manager

Python application for managing resources on the data servers of the IO-SEA project. The project consists of two docker containers. The first one is the MySQL database and the second one contains the resource manager (RM) itself. SQL Alchemy and Flask-restx were used for RM development. An API interface is used to communicate with RM.

## Documentation

The API documentation is located in the Docs folder - [Orchestrator_API.pdf](https://code.it4i.cz/io-sea/resource-manager/-/blob/main/Docs/Orchestrator_API.pdf?ref_type=heads)

The database schema of RM.
![DB Schema](https://code.it4i.cz/io-sea/resource-manager/-/raw/main/Docs/RM_DB_Tables.png?ref_type=heads)

## Config files

There are three configuration files - config.txt, flavors_init.txt, servers_init.txt

**config.txt** - is the main configuration file. It contains the necessary information to connect to the database. There is also a setting for the API - port and IP, but it only works without using a docker container. When running via Docker, you need to edit the dockerfile. It contains the paths to the two remaining configuration files.

**servers_init.txt** - contains the necessary information about the available servers for resource allocation during the initial initialization of the SQL DB.
Data format:
```
[name, max_size_RAM, free_space_RAM, min_chunk_RAM, max_size_Disk, free_space_Disk, min_chunk_Disk, max_size_CPU, free_space_CPU, min_chunk_CPU]
```

**flavors_init.txt** - contains the information about flavors.
Data format:
```
[name, CPU_size, RAM_size, Disk_size]
```

## Log file

**logfile.log** is created at the first startup in the root directory (same directory as config.txt)

## Deploy

The project is ready to run via Docker. Type the command to run:
```
docker-compose up
```