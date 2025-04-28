import os
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


def chat_api(model, max_tokens, prompt, temperature, style):
    client = OpenAI(api_key=os.getenv('DEEPSEEK_API'), base_url="https://api.deepseek.com")
    ans = client.chat.completions.create(
        model=model,
        max_tokens=max_tokens,
        messages=[
            {'role': 'system', 'content': f'You are an expert AI text summarizer. Your task is to generate a summary of the text I will be provided in a {style} style.'},
            {'role': 'user', 'content': prompt}],
        temperature=temperature)
    return [choice.message.content for choice in ans.choices]