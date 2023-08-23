import logging

import openai


logger = logging.getLogger(__name__)


async def angrify(text: str) -> str:
    logger.info(f"deangrifying this text: {text}")
    completion = await openai.ChatCompletion.acreate(
        model="gpt-4",
        messages=[
            {
                "role": "system", "content":
                (
                    "You are a messenger user in an official, polite conversation, "
                    "where swears are strictly prohibited, and people show mutual respect to each other."
                )
            },
            {
                "role": "user", "content":
                (
                    f"You are given an impolite message. Rewrite it, "
                    f"so that it is appropriate to use in a formal chat. "
                    f"Remove any aggression, even passive one. "
                    f"The message is: {text}"
                )
            }
        ],
        max_tokens=1000,
        temperature=0.6,
    )
    return completion["choices"][0]["message"]["content"]
