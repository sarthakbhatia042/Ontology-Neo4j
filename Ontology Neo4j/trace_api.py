from fastapi import APIRouter, HTTPException
from neo4j_graphdb import execute_query

router = APIRouter(prefix="/api/v1")


@router.get("/traceability/{lot_id}")
def traceability(lot_id: str):

    query = """
    MATCH path =
    (rl:RawMaterialLot {lot_id: $lot_id})
    -[:STREAMS_DATA_TO]->(edge:EdgeGateway)
    -[:PUBLISHES_TO]->(mqtt:MQTTBroker)
    -[:SENDS_DATA_TO]->(zone:Zone)
    -[:HAS_LINE]->(line:ProductionLine)
    -[:HAS_MACHINE]->(machine:Machine)
    -[:PRODUCES]->(product:ReadyProduct)
    -[:PACKED_IN]->(fg:FinishedGoodsLot)

    RETURN path
    """

    records = execute_query(query, {"lot_id": lot_id})

    if not records:
        raise HTTPException(
            status_code=404,
            detail=f"No traceability path found for {lot_id}"
        )

    paths = []

    for record in records:

        path = record["path"]

        nodes = []
        relationships = []

        for node in path.nodes:
            nodes.append({
                "id": node.element_id,
                "labels": list(node.labels),
                "properties": dict(node)
            })

        for relationship in path.relationships:
            relationships.append({
                "id": relationship.element_id,
                "type": relationship.type,
                "source": relationship.start_node.element_id,
                "target": relationship.end_node.element_id,
                "properties": dict(relationship)
            })

        paths.append({
            "nodes": nodes,
            "relationships": relationships
        })

    return {
        "lot_id": lot_id,
        "paths_found": len(paths),
        "paths": paths
    }
