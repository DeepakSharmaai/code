import yaml
import openai
import os

# Load your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def parse_openapi(yaml_str):
    try:
        spec = yaml.safe_load(yaml_str)
        paths = spec.get("paths", {})
        summaries = []

        for path, methods in paths.items():
            for method, info in methods.items():
                summary = {
                    "path": path,
                    "method": method.upper(),
                    "description": info.get("summary") or info.get("description", "No description available.")
                }
                summaries.append(summary)
        return summaries
    except yaml.YAMLError:
        return []

def generate_summary(summaries):
    prompt = "Summarize the following API endpoints in plain language:\n\n"
    for item in summaries:
        prompt += f"{item['method']} {item['path']}: {item['description']}\n"

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
    )
    return response.choices[0].message.content.strip()
