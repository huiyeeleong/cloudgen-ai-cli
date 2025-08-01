from groq import Groq


def generate_iac(prompt):
    completion = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return completion.choices[0].message.content.strip()
