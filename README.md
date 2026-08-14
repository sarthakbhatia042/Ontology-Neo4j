### Core Graph Architecture

Supplier
   ↓
Raw Material
   ↓
Raw Material Lot
   ↓
Sensor
   ↓
IIoT Edge Gateway
   ↓
MQTT Broker
   ↓
Zones   
   ↓
Lines   
   ↓
Machines   
   ↓
Machine Operators   
   ↓
Finished Goods
   ↓
Finished Goods Lot


### Neo4j Data Model

The graph uses Neo4j relationships to represent the manufacturing ontology.

Representative relationships

SUPPLIES

HAS_LOT

MONITORS

STREAMS_DATA_TO

PUBLISHES_TO

SENDS_DATA_TO

EXECUTES

ASSIGNED_TO

USES

PRODUCES

PACKAGED_AT

CREATES

STORED_IN

HAS_LINE

HAS_MACHINE

OPERATED_BY

PACKED_IN

TRACEABLE_TO

The exact relationship vocabulary should remain consistent across all fixture files and API operations.

### Weighted Graph Extension

Relationships can contain properties in addition to their relationship type.

The project supports metadata such as:

Property

Purpose

weight

Relationship strength/importance

cost

Operational or monetary cost

confidence

Confidence/reliability of the relationship

timestamp

Time at which the relationship/event was observed

Example conceptual relationship:

MQTT Broker
     │
     │ SENDS_DATA_TO
     │ weight = 0.75
     │ cost = 120
     │ confidence = 0.97
     │ timestamp = ...
     ↓
Zone B

This allows the graph to evolve from a simple topology into a weighted and metadata-rich industrial knowledge graph, which can later support graph algorithms, ranking, traceability, anomaly detection, GraphRAG, and graph ML.

### API Architecture

The backend uses FastAPI as the service layer and the Neo4j Python driver for database communication.

Architecture

                    ┌─────────────────────┐
                    │  Frontend / Client   │
                    └──────────┬──────────┘
                               │ HTTP
                               ▼
                    ┌─────────────────────┐
                    │      FastAPI        │
                    │      API Layer      │
                    └──────────┬──────────┘
                               │
                         Neo4j Driver
                               │
                               ▼
                    ┌─────────────────────┐
                    │     Neo4j Aura      │
                    │    Graph Database   │
                    └─────────────────────┘

The frontend should not connect directly to Neo4j. Neo4j credentials and database access remain inside the backend.

### Read APIs

Read APIs retrieve information from the graph without modifying it.

Current API examples include:

GET /api/v1/graph
GET /api/v1/traceability/{lot_id}

Example:

GET /api/v1/traceability/RMLOT-001

The traceability API can identify connected manufacturing paths beginning from a raw-material lot and continuing through downstream manufacturing entities.

The read layer is intended to support:

Graph retrieval

Traceability

Entity lookup

Relationship exploration

Future path/ranking queries

Frontend graph visualization

### Write APIs & Fixture Ingestion

The write layer allows controlled modification of the Neo4j graph.

A key feature is the fixture ingestion pipeline.

A user can submit a .cypher fixture document containing multiple Cypher statements. The backend executes the statements within a transaction.

User
 │
 │ POST fixture
 ▼
FastAPI
 │
 ├── Parse statements
 ├── Execute statement 1
 ├── Execute statement 2
 ├── Execute statement 3
 │
 ├──────────────► COMMIT
 │
 └── If failure ─► ROLLBACK

This provides a flexible mechanism for:

Creating nodes

Creating relationships

Modifying properties

Adding new zones/lines/machines

Updating existing entities

Removing entities

Bulk graph ingestion

MERGE is used where operations should be idempotent, while MATCH is used when an existing entity must be located without creating a new one.

### Transaction Safety

Multiple fixture statements are treated as a single logical operation.

For example:

Statement 1 ✓
Statement 2 ✓
Statement 3 ✗
       ↓
    ROLLBACK
       ↓
No partial graph modification

This is important for enterprise ingestion because a partially applied fixture could leave the manufacturing graph in an inconsistent state.

### Project File Structure

The current backend is organized around the following files:

Ontology Neo4j/
│
├── main.py
├── neo4j_graphdb.py
├── fixture_endpoint.py
├── read_api.py
├── trace_api.py
│
└── test_fixture.cypher

File responsibilities

File

Responsibility

main.py

FastAPI application entry point and router registration

neo4j_graphdb.py

Neo4j driver/database connection and graph operations

fixture_endpoint.py

Cypher fixture ingestion and transactional writes

read_api.py

Graph read/query endpoints

trace_api.py

Manufacturing traceability endpoints

test_fixture.cypher

Example multi-statement graph modification fixture

### Running the API

Start the development server with:

uvicorn main:app --reload

The API is then available locally at:

http://127.0.0.1:8000

FastAPI's interactive documentation is available at:

http://127.0.0.1:8000/docs#

The /docs interface can be used to test GET and POST endpoints without requiring a separate frontend.

### Example Graph Operations

Retrieve graph information

GET /api/v1/graph

Trace a raw-material lot

GET /api/v1/traceability/RMLOT-001

Submit a Cypher fixture

POST /api/v1/fixtures

A fixture can contain multiple statements separated by semicolons.

For example, a single fixture can create a zone, production line, machines, operators, products, and finished-goods lots.

### Design Principles

The project follows several important principles:

Neo4j as the graph source of truthManufacturing entities and relationships are stored in the graph database.

FastAPI as the application boundaryExternal applications communicate with the graph through APIs rather than direct database access.

Idempotent ingestion where appropriateMERGE prevents accidental duplication when fixtures are re-run.

Explicit matching for existing entitiesMATCH is preferred when the intention is to connect or modify an already-existing node.

Transactional writesMulti-statement fixture operations should either complete successfully or roll back.

Stable business identifiersApplication logic should prefer identifiers such as zone_id, line_id, machine_id, and lot_id instead of relying on Neo4j internal elementId() values as permanent identifiers.

Frontend/backend separationThe frontend is responsible for visualization and interaction; the backend handles database access and business logic.

### Summary

Database: Neo4j / Neo4j Aura

Backend: FastAPI + Neo4j Python Driver

Graph: Supplier → Raw Material → Lots → IIoT → MQTT → MES → Production → Packaging → Finished Goods, with Zone → Line → Machine → Operator hierarchy.

Read layer: Retrieves graph data and manufacturing traceability.

Write layer: Modifies the graph through API-controlled Cypher execution.

Ingestion: Users can submit multi-statement .cypher fixture documents.

Transaction model: All statements in a fixture are executed atomically with rollback on failure.

Graph metadata: Relationships can contain weight, cost, confidence, and timestamp.

Architecture:

Frontend / External Systems
            ↓
         FastAPI
       ↙         ↘
    READ         WRITE
     ↓             ↓
       Neo4j Driver
            ↓
         Neo4j Aura

Key outcome: The project transforms Neo4j from a standalone graph database into an API-accessible industrial knowledge graph platform, providing a foundation for traceability, graph analytics, weighted graph reasoning, GraphRAG, and future intelligent manufacturing applications.
