# Dataflow
## Overview
The dataflow architecture for test-wright is designed to efficiently process and store data from various sources, providing a scalable and secure system for AI-powered automated testing.

## System Dataflow Architecture
```
                                      +---------------+
                                      |  External    |
                                      |  Data Sources  |
                                      +---------------+
                                             |
                                             |
                                             v
                                      +---------------+
                                      |  Ingestion    |
                                      |  Layer        |
                                      |  (API Gateway,|
                                      |   Message Queue)|
                                      +---------------+
                                             |
                                             |
                                             v
                                      +---------------+
                                      |  Processing/  |
                                      |  Transform Layer|
                                      |  (Worker Nodes, |
                                      |   AI Engine)    |
                                      +---------------+
                                             |
                                             |
                                             v
                                      +---------------+
                                      |  Storage Tier  |
                                      |  (Database,    |
                                      |   Data Warehouse)|
                                      +---------------+
                                             |
                                             |
                                             v
                                      +---------------+
                                      |  Query/Serving |
                                      |  Layer         |
                                      |  (API Gateway, |
                                      |   Web Server)   |
                                      +---------------+
                                             |
                                             |
                                             v
                                      +---------------+
                                      |  Egress to User|
                                      |  (Web Interface,|
                                      |   API)         |
                                      +---------------+
```

## Components and Tiers
* **External Data Sources**
	+ GitHub API
	+ GitLab API
	+ Bitbucket API
	+ Other version control system APIs
* **Ingestion Layer**
	+ API Gateway (e.g., NGINX, AWS API Gateway)
	+ Message Queue (e.g., RabbitMQ, Apache Kafka)
	+ Authentication Boundary: OAuth 2.0, JWT tokens
* **Processing/Transform Layer**
	+ Worker Nodes (e.g., Docker containers, Kubernetes pods)
	+ AI Engine (e.g., TensorFlow, PyTorch)
	+ Authentication Boundary: Internal API keys, service accounts
* **Storage Tier**
	+ Database (e.g., PostgreSQL, MySQL)
	+ Data Warehouse (e.g., Amazon Redshift, Google BigQuery)
	+ Authentication Boundary: Database credentials, IAM roles
* **Query/Serving Layer**
	+ API Gateway (e.g., NGINX, AWS API Gateway)
	+ Web Server (e.g., Apache HTTP Server, Nginx)
	+ Authentication Boundary: OAuth 2.0, JWT tokens
* **Egress to User**
	+ Web Interface (e.g., React, Angular)
	+ API (e.g., RESTful API, GraphQL API)
	+ Authentication Boundary: OAuth 2.0, JWT tokens

## Auth Boundaries
* Ingestion Layer: OAuth 2.0, JWT tokens
* Processing/Transform Layer: Internal API keys, service accounts
* Storage Tier: Database credentials, IAM roles
* Query/Serving Layer: OAuth 2.0, JWT tokens
* Egress to User: OAuth 2.0, JWT tokens

Note: The auth boundaries are designed to ensure secure data flow and access control throughout the system.