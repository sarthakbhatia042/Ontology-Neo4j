read_api.py       → /api/v1/graph
trace_api.py      → /api/v1/traceability/
fixture_endpoint.py → /api/v1/fixtures
                         ↓
                      main.py
                         ↓
                     FastAPI app


basic ingestion pipeline:

.cypher fixture
      ↓
POST /fixtures
      ↓
FastAPI
      ↓
Neo4j Driver
      ↓
Neo4j Aura
      ↓
Graph modified

Create a .env file according to your Neo4j credentials

Go to browser.neo4j.io to see the graph executed after posting the fixture through API manufacturinig locally in ur system 

### How to run
1. python3 pip install fastapi uvicorn neo4j python-dotenv python-multipart 
2. python neo4j_graphdb.py
3. python3 -m uvicorn main:app --reload

after the above, go to http://127.0.0.1:8000 to check api status. If it is running, it will display : {api_status : 'running'}.

Next, go to  http://127.0.0.1:8000/docs# to work with recieve(GET/) and write(POST/) commands.
 Check /GET to check for checking read_api.py and trace_api.py.
 Check /POST to work with ingestion pipeline.

We can upload any fixture document and get the expected results for modifications (CRUD operations) in the Graph.



To work with fixture documents, start with add_zone.cypher



## Graph display query
MATCH (z:Zone)
RETURN z;
