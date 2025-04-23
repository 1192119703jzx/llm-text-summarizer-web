from openai import OpenAI


def chat_api(model, max_tokens, prompt, temperature,
            style):
    client = OpenAI(api_key="<your_deepseek_api_key>", base_url="https://api.deepseek.com")
    ans = client.chat.completions.create(
        model=model,
        max_tokens=max_tokens,
        messages=[
            {'role': 'system', 'content': f'You are an expert AI text summarizer. Your task is to generate a summary of the text I will be provided in a {style} style.'},
            {'role': 'user', 'content': prompt}],
        temperature=temperature)
    return [choice.message.content for choice in ans.choices]