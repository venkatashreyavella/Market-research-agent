import json
from app.config import MOCK_MODE, GROQ_API_KEY, GROQ_MODEL


def llm_json(system: str, user: str, schema=None):
    if MOCK_MODE:
        return None
    from langchain_groq import ChatGroq
    model = ChatGroq(api_key=GROQ_API_KEY, model=GROQ_MODEL, temperature=0)
    try:
        if schema:
            return model.with_structured_output(schema).invoke([("system", system), ("human", user)])
        response = model.invoke([("system", system), ("human", user)])
        return json.loads(response.content)
    except Exception as exc:
        message = str(exc)
        if "model_not_found" in message or "model does not exist" in message.lower():
            raise RuntimeError(
                f"Groq model '{GROQ_MODEL}' is unavailable for this project. "
                "Set GROQ_MODEL to a model enabled in your Groq Console, such as openai/gpt-oss-120b."
            ) from exc
        raise RuntimeError(f"Groq request failed: {message}") from exc
