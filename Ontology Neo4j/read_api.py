from fastapi import APIRouter
from neo4j_graphdb import execute_query

router = APIRouter(prefix="/api/v1")


@router.get("/graph")
def get_graph():

    query = """
    MATCH (n)-[r]->(m)
    RETURN n, r, m
    """

    records = execute_query(query)

    nodes = {}
    relationships = []

    for record in records:

        n = record["n"]
        m = record["m"]
        r = record["r"]

        nodes[n.element_id] = {
            "id": n.element_id,
            "labels": list(n.labels),
            "properties": dict(n)
        }

        nodes[m.element_id] = {
            "id": m.element_id,
            "labels": list(m.labels),
            "properties": dict(m)
        }

        relationships.append({
            "id": r.element_id,
            "type": r.type,
            "source": r.start_node.element_id,
            "target": r.end_node.element_id,
            "properties": dict(r)
        })

    return {
        "nodes": list(nodes.values()),
        "relationships": relationships
    }
