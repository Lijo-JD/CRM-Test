from app.core.config import settings
from app.core.database import get_connection


BLOCKED_KEYWORDS = ["drop", "truncate"]


def _get_model_response(prompt: str):
    provider = settings.AI_PROVIDER.lower()

    if provider == "groq":
        if not settings.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is not configured.")
        from groq import Groq

        client = Groq(api_key=settings.GROQ_API_KEY)
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content

    if not settings.GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is not configured.")

    from google import genai

    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt,
    )
    return response.text


def validate_sql(sql: str):
    sql_lower = sql.lower()
    for keyword in BLOCKED_KEYWORDS:
        if keyword in sql_lower:
            raise ValueError(f"Blocked Query Detected: {keyword}")
    return True


def generate_sql(user_question: str):
    schema_context = build_context()
    prompt = f"""
    You are an expert MySQL developer.
    DATABASE SCHEMA:
    {schema_context}
    RULES:
    1. Return ONLY executable MySQL.
    2. No markdown, no explanations, no comments.
    3. Use joins when required.
    4. Never generate DROP or TRUNCATE.
    USER QUESTION:
    {user_question}
    """
    response = _get_model_response(prompt)
    return response.replace("```sql", "").replace("```", "").strip()


def _fetch_schema_rows():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT table_name, column_name, data_type, is_nullable
                FROM information_schema.columns
                WHERE table_schema=%s
                ORDER BY table_name, ordinal_position
                """,
                (settings.DB_NAME,),
            )
            return cursor.fetchall()


def get_schema():
    rows = _fetch_schema_rows()
    schema = ""
    current_table = None
    for row in rows:
        table = row["TABLE_NAME"]
        column = row["COLUMN_NAME"]
        dtype = row["DATA_TYPE"]
        nullable = row["IS_NULLABLE"]
        if current_table != table:
            schema += f"\n\nTABLE: {table}\n"
            current_table = table
        schema += f"   {column} ({dtype}) NULLABLE={nullable}\n"
    return schema


def get_relationships():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT table_name, column_name, referenced_table_name, referenced_column_name
                FROM information_schema.key_column_usage
                WHERE table_schema=%s
                AND referenced_table_name IS NOT NULL
                """,
                (settings.DB_NAME,),
            )
            rows = cursor.fetchall()
    relationships = "\n\nRELATIONSHIPS:\n"
    for row in rows:
        relationships += f"{row['TABLE_NAME']}.{row['COLUMN_NAME']} --> {row['REFERENCED_TABLE_NAME']}.{row['REFERENCED_COLUMN_NAME']}\n"
    return relationships


def build_context():
    return get_schema() + get_relationships()


def explain_error(user_query: str, sql: str, error: str):
    prompt = f"""
    You are a CRM assistant.
    User Request: {user_query}
    Generated SQL: {sql}
    Database Error: {error}
    Explain the issue in simple business language and suggest what to do next.
    Do not show technical database jargon.
    """
    return _get_model_response(prompt)


def classify_intent(user_query: str):
    prompt = f"""
    You are a security and intent router for a CRM AI assistant.
    The database contains customers, products, orders, order items, leads, and employees.

    Analyze the user query: "{user_query}"

    Is this query related to querying, updating, or managing CRM data, business metrics, or entities?
    Answer ONLY with 'YES' or 'NO'.
    """
    text = _get_model_response(prompt).strip().upper()
    return text


def execute_sql_with_retry(sql: str, user_query: str, max_retries: int = 2):
    current_sql = sql
    for attempt in range(max_retries + 1):
        try:
            validate_sql(current_sql)
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(current_sql)
                    if current_sql.strip().lower().startswith("select"):
                        rows = cursor.fetchall()
                        return {"sql": current_sql, "rows": rows}
                    conn.commit()
                    return {"sql": current_sql, "message": "Operation successful"}
        except Exception as exc:
            error_msg = str(exc)
            if attempt == max_retries:
                return {"sql": current_sql, "error": explain_error(user_query, current_sql, error_msg)}
            correction_prompt = f"""
            You are an expert MySQL developer fixing a broken query.

            Original User Request: {user_query}
            Failed SQL Query: {current_sql}
            MySQL Error: {error_msg}

            Please analyze the error, fix the SQL query, and return ONLY executable MySQL code without markdown or explanations.
            """
            current_sql = _get_model_response(correction_prompt).replace("```sql", "").replace("```", "").strip()


def ask_crm_secure(question: str):
    intent = classify_intent(question)
    if "NO" in intent:
        return {
            "message": "I'm your CRM assistant. I can only help you query, manage, or analyze customer, product, order, and lead data.",
            "allowed": False,
        }

    sql = generate_sql(question)
    result = execute_sql_with_retry(sql, question)
    return {
        "question": question,
        "generated_sql": sql,
        "result": result,
        "allowed": True,
    }
