MATCH (a)-[r:SUPPLIES_RAW_MATERIAL]->(b)
SET r.weight = 0.9,
    r.cost = 200,
    r.timestamp = datetime("2026-08-12T17:00:00");

MATCH (a)-[r:OPERATED_BY]->(b)
SET r.weight = 0.8,
    r.confidence = 0.65;

MATCH (a)-[r:SENDS_DATA_TO]->(b)
SET r.weight = 0.75,
    r.cost = 120;

MATCH (a)-[r:PACKED_IN]->(b)
SET r.weight = 0.5,
    r.cost = 180,
    r.timestamp = datetime("2026-08-14T12:00:00");