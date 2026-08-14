MERGE (z:Zone {zone_id: "ZONE-B"})
SET z.name = "Zone B";

MERGE (line:ProductionLine {line_id: "LINE-B"})
SET line.name = "Line B";

MATCH (z:Zone {zone_id: "ZONE-B"})
MATCH (line:ProductionLine {line_id: "LINE-B"})
MERGE (z)-[:HAS_LINE]->(line);

MERGE (m1:Machine {machine_id: "MACHINE-B1"})
SET m1.name = "Machine B1";

MERGE (m2:Machine {machine_id: "MACHINE-B2"})
SET m2.name = "Machine B2";

MATCH (line:ProductionLine {line_id: "LINE-B"})
MATCH (m1:Machine {machine_id: "MACHINE-B1"})
MATCH (m2:Machine {machine_id: "MACHINE-B2"})
MERGE (line)-[:HAS_MACHINE]->(m1)
MERGE (line)-[:HAS_MACHINE]->(m2);