# FRESCO Database API

## Introduction
This API exposes the FRESCO database to the FRESCO website, facilitating data retrieval and manipulation. It's built using FastAPI and is designed to operate within a Docker container on a Kubernetes cluster alongside the FRESCO DB.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Dependencies](#dependencies)
- [Configuration](#configuration)

## Installation
This application is designed to run in a Docker container within a Kubernetes cluster. To set up the environment:

1. Ensure Docker and Kubernetes are installed and configured on your system.
2. Clone the repository to your local machine.
3. Build the Docker container with the provided Dockerfile.
4. Deploy the container to your Kubernetes cluster.

## Usage
After deploying the application to your Kubernetes cluster, it can be accessed through its service URL or via port forwarding for local development and testing.

## Features
- Secure access to the FRESCO database.
- CRUD operations for managing host and job data.
- User authentication and JWT token handling.
- Data validation and serialization with Pydantic models.

## Dependencies
The project dependencies are listed in `requirements.txt`. To install them, run:

```bash
pip install -r requirements.txt
```

## Configuration
The application requires the following environment variables:
- `DBUSER`: Database user for access.
- `DBPW`: Database password.
- `DBHOST`: Host where the database is running.
- `DBNAME`: Name of the database.
- `DBUSER_API`: API user for database access.
- `DBPW_API`: API password for database access.
- `FASTAPI_SECURITY_KEY`: Security key for FastAPI.
- `FASTAPI_SECURITY_KEY_ALGO`: Security algorithm for FastAPI.
