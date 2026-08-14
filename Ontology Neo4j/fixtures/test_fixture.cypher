MERGE (op1:Operator {operator_id: "OPERATOR-B1"})
SET op1.name = "Operator B1";

MERGE (op2:Operator {operator_id: "OPERATOR-B2"})
SET op2.name = "Operator B2";

MATCH (m1:Machine {machine_id: "MACHINE-B1"})
MATCH (m2:Machine {machine_id: "MACHINE-B2"})
MATCH (op1:Operator {operator_id: "OPERATOR-B1"})
MATCH (op2:Operator {operator_id: "OPERATOR-B2"})
MERGE (m1)-[:OPERATED_BY]->(op1)
MERGE (m2)-[:OPERATED_BY]->(op2);

MERGE (p1:ReadyProduct {product_id: "PRODUCT-B1"})
SET p1.name = "Ready Product B1";

MERGE (p2:ReadyProduct {product_id: "PRODUCT-B2"})
SET p2.name = "Ready Product B2";

MATCH (m1:Machine {machine_id: "MACHINE-B1"})
MATCH (m2:Machine {machine_id: "MACHINE-B2"})
MATCH (p1:ReadyProduct {product_id: "PRODUCT-B1"})
MATCH (p2:ReadyProduct {product_id: "PRODUCT-B2"})
MERGE (m1)-[:PRODUCES]->(p1)
MERGE (m2)-[:PRODUCES]->(p2);

MERGE (fg1:FinishedGoodsLot {lot_id: "FGLOT-B1"})
SET fg1.name = "Finished Goods Lot B1";

MERGE (fg2:FinishedGoodsLot {lot_id: "FGLOT-B2"})
SET fg2.name = "Finished Goods Lot B2";

MATCH (p1:ReadyProduct {product_id: "PRODUCT-B1"})
MATCH (p2:ReadyProduct {product_id: "PRODUCT-B2"})
MATCH (fg1:FinishedGoodsLot {lot_id: "FGLOT-B"})
MERGE (p1)-[:PACKED_IN]->(fg)
MERGE (p2)-[:PACKED_IN]->(fg)