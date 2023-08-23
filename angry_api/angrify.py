import openai


async def angrify(text: str) -> str:
    completion = await openai.ChatCompletion.acreate(
        model="gpt-4", messages=[
            {
                "role": "system", "content":
                """
                You are a messenger user in an official, polite conversation, 
                where swears are strictly prohibited, and people show mutual respect to each other.
                """
            },
            {
                "role": "user", "content":
                f"""
                You are given an impolite message. Rewrite it, so that it is appropriate to use in a formal chat. 
                Remove any aggression, even passive one.
                The message is: {text}
                """
            }
        ]
    )
    return completion["choices"][0]["message"]["content"]
