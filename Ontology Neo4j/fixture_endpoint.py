from fastapi import APIRouter, UploadFile, File, HTTPException

from neo4j_graphdb import execute_fixture_transaction

router = APIRouter(prefix="/api/v1")


def split_cypher_statements(cypher: str):
    statements = []
    current = []

    in_single_quote = False
    in_double_quote = False
    in_backtick = False
    escaped = False

    for char in cypher:

        if escaped:
            current.append(char)
            escaped = False
            continue

        if char == "\\":
            current.append(char)
            escaped = True
            continue

        if char == "'" and not in_double_quote and not in_backtick:
            in_single_quote = not in_single_quote
            current.append(char)
            continue

        if char == '"' and not in_single_quote and not in_backtick:
            in_double_quote = not in_double_quote
            current.append(char)
            continue

        if char == "`" and not in_single_quote and not in_double_quote:
            in_backtick = not in_backtick
            current.append(char)
            continue

        if (
            char == ";"
            and not in_single_quote
            and not in_double_quote
            and not in_backtick
        ):
            statement = "".join(current).strip()

            if statement:
                statements.append(statement)

            current = []

        else:
            current.append(char)

    statement = "".join(current).strip()

    if statement:
        statements.append(statement)

    return statements


@router.post("/fixtures")
async def upload_fixture(file: UploadFile = File(...)):

    if not file.filename.lower().endswith(".cypher"):
        raise HTTPException(
            status_code=400,
            detail="Only .cypher files are allowed"
        )

    content = await file.read()

    try:
        cypher = content.decode("utf-8")

    except UnicodeDecodeError:
        raise HTTPException(
            status_code=400,
            detail="Fixture must be UTF-8 encoded"
        )

    if not cypher.strip():
        raise HTTPException(
            status_code=400,
            detail="Fixture is empty"
        )

    statements = split_cypher_statements(cypher)

    if not statements:
        raise HTTPException(
            status_code=400,
            detail="No Cypher statements found"
        )

    try:

        results = execute_fixture_transaction(statements)

        return {
            "status": "success",
            "filename": file.filename,
            "statements_executed": len(statements),
            "results": results
        }

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail={
                "message": "Fixture failed. Entire transaction was rolled back.",
                "error": str(e)
            }
        )

