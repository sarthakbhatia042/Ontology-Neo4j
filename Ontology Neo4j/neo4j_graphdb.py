# import os
# from dotenv import load_dotenv
# from neo4j import GraphDatabase

# load_dotenv()

# URI = os.getenv("NEO4J_URI")
# USERNAME = os.getenv("NEO4J_USERNAME")
# PASSWORD = os.getenv("NEO4J_PASSWORD")

# driver = GraphDatabase.driver(
#     URI,
#     auth=(USERNAME, PASSWORD)
# )

# def execute_query(query, parameters=None):
#     with driver.session() as session:
#         result = session.run(query, parameters or {})
#         return list(result)

# if __name__ == "__main__":
#     with driver.session() as session:
#         result = session.run("RETURN 1 AS test")
#         print(result.single()["test"])















import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

URI = os.getenv("NEO4J_URI")
USERNAME = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")

driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD)
)


def execute_query(query, parameters=None):
    """
    Execute a single Cypher query.
    """
    with driver.session() as session:
        result = session.run(query, parameters or {})
        return list(result)


def execute_fixture_transaction(statements):
    with driver.session() as session:

        transaction = session.begin_transaction()

        try:

            results = []

            for statement in statements:

                statement = statement.strip()

                if not statement:
                    continue

                result = transaction.run(statement)

                summary = result.consume()

                results.append({
                    "statement": statement,
                    "counters": {
                        "nodes_created": summary.counters.nodes_created,
                        "nodes_deleted": summary.counters.nodes_deleted,
                        "relationships_created": summary.counters.relationships_created,
                        "relationships_deleted": summary.counters.relationships_deleted,
                        "properties_set": summary.counters.properties_set
                    }
                })

            transaction.commit()

            return results

        except Exception:
            transaction.rollback()
            raise


def close_driver():
    driver.close()