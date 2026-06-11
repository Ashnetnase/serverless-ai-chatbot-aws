import json
import os
import boto3
import urllib.request
from datetime import datetime, timezone, timedelta

s3 = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")
secrets = boto3.client("secretsmanager")

table = dynamodb.Table(os.environ["TABLE_NAME"])
rate_table = dynamodb.Table(os.environ["RATE_TABLE_NAME"])

MAX_MESSAGES_PER_SESSION = 20
MAX_REQUESTS_PER_MINUTE = 10
MAX_REQUESTS_PER_DAY = 100


def response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "content-type",
            "Access-Control-Allow-Methods": "POST,OPTIONS"
        },
        "body": json.dumps(body)
    }


def get_openai_key():
    secret_name = os.environ["OPENAI_SECRET_NAME"]
    secret = secrets.get_secret_value(SecretId=secret_name)
    return secret["SecretString"]


def get_portfolio_knowledge():
    bucket = os.environ["KNOWLEDGE_BUCKET"]
    key = os.environ["KNOWLEDGE_KEY"]

    obj = s3.get_object(Bucket=bucket, Key=key)
    return obj["Body"].read().decode("utf-8")


def get_session_count(session_id):
    result = table.get_item(
        Key={
            "session_id": session_id,
            "timestamp": "META"
        }
    )
    return int(result.get("Item", {}).get("message_count", 0))


def increment_session_count(session_id):
    expires_at = int((datetime.now(timezone.utc) + timedelta(days=7)).timestamp())

    table.update_item(
        Key={
            "session_id": session_id,
            "timestamp": "META"
        },
        UpdateExpression="SET updated_at = :now, expires_at = :expires_at ADD message_count :inc",
        ExpressionAttributeValues={
            ":inc": 1,
            ":now": datetime.now(timezone.utc).isoformat(),
            ":expires_at": expires_at
        }
    )


def check_rate_limit(session_id):
    now = datetime.now(timezone.utc)

    minute_key = f"{session_id}#{now.strftime('%Y-%m-%dT%H:%M')}"
    day_key = f"{session_id}#{now.strftime('%Y-%m-%d')}"

    minute_expires = int((now + timedelta(minutes=2)).timestamp())
    day_expires = int((now + timedelta(days=2)).timestamp())

    minute_result = rate_table.update_item(
        Key={"rate_key": minute_key},
        UpdateExpression="SET expires_at = :expires_at ADD request_count :inc",
        ExpressionAttributeValues={
            ":inc": 1,
            ":expires_at": minute_expires
        },
        ReturnValues="UPDATED_NEW"
    )

    day_result = rate_table.update_item(
        Key={"rate_key": day_key},
        UpdateExpression="SET expires_at = :expires_at ADD request_count :inc",
        ExpressionAttributeValues={
            ":inc": 1,
            ":expires_at": day_expires
        },
        ReturnValues="UPDATED_NEW"
    )

    minute_count = int(minute_result["Attributes"]["request_count"])
    day_count = int(day_result["Attributes"]["request_count"])

    if minute_count > MAX_REQUESTS_PER_MINUTE:
        return False, "The chatbot is receiving too many messages. Please wait a minute and try again."

    if day_count > MAX_REQUESTS_PER_DAY:
        return False, "The chatbot has reached the daily message limit for this session. Please try again tomorrow."

    return True, ""


def save_message(session_id, role, content):
    expires_at = int((datetime.now(timezone.utc) + timedelta(days=7)).timestamp())

    table.put_item(Item={
        "session_id": session_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "role": role,
        "content": content,
        "expires_at": expires_at
    })


def call_openai(message):
    openai_key = get_openai_key()
    knowledge = get_portfolio_knowledge()

    system_prompt = f"""You are a helpful assistant for a professional portfolio website.

Use the following public portfolio knowledge as the source of truth:

{knowledge}

Rules:
- Keep answers short and professional.
- Talk about the site owner in third person.
- Do not invent details.
- If the answer is not in the knowledge, say the visitor can contact the site owner directly."""

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
        ],
        "max_tokens": 200
    }

    req = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {openai_key}",
            "Content-Type": "application/json"
        },
        method="POST"
    )

    with urllib.request.urlopen(req, timeout=20) as res:
        data = json.loads(res.read().decode("utf-8"))

    return data["choices"][0]["message"]["content"]


def lambda_handler(event, context):
    try:
        if event.get("requestContext", {}).get("http", {}).get("method") == "OPTIONS":
            return response(200, {})

        body = json.loads(event.get("body", "{}"))

        message = body.get("message", "").strip()
        session_id = body.get("sessionId", "anonymous-session").strip()

        if not message:
            return response(400, {"response": "Message is required"})

        if len(message) > 500:
            return response(400, {"response": "Message is too long"})

        rate_allowed, rate_message = check_rate_limit(session_id)

        if not rate_allowed:
            return response(429, {"response": rate_message})

        current_count = get_session_count(session_id)

        if current_count >= MAX_MESSAGES_PER_SESSION:
            return response(429, {
                "response": "The chatbot has reached the message limit for this session. Please try again later."
            })

        increment_session_count(session_id)
        save_message(session_id, "user", message)

        bot_reply = call_openai(message)

        save_message(session_id, "assistant", bot_reply)

        return response(200, {
            "response": bot_reply,
            "sessionId": session_id,
            "messagesUsed": current_count + 1,
            "messagesLimit": MAX_MESSAGES_PER_SESSION
        })

    except Exception as error:
        print("ERROR:", str(error))
        return response(500, {
            "response": "The chatbot is having trouble responding right now."
        })