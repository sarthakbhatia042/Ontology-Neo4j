MATCH (mqtt:MQTTBroker)
WHERE elementId(mqtt) = "4:c8e61e0b-0b97-4f3b-995d-158413e1f560:91"

MATCH (z:Zone {zone_id: "ZONE-B"})

MERGE (mqtt)-[:SENDS_DATA_TO]->(z);