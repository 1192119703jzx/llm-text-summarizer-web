import os
from dotenv import load_dotenv
from openai import OpenAI


from prompt.casual_prompt import CASUAL_PROMPT
from prompt.formal_prompt import FORMAL_PROMPT
from prompt.technical_prompt import TECHINCAL_PROMPT


load_dotenv()

def first_call(model, max_tokens, text, temperature, style):
    client = OpenAI(api_key=os.getenv('DEEPSEEK_API'), base_url="https://api.deepseek.com")
    if style == "Technical":
        prompt_format = TECHINCAL_PROMPT.format(prompt=text)
    elif style == "Casual":
        prompt_format = CASUAL_PROMPT.format(prompt=text)
    elif style == "Formal":
        prompt_format = FORMAL_PROMPT.format(prompt=text)
    else:
        raise ValueError("Invalid style. Choose from 'technical', 'casual', or 'formal'.")
    ans = client.chat.completions.create(
        model=model,
        max_tokens=max_tokens,
        messages=[
            {'role': 'system', 'content': f'You are a helpful assistant who is an expert in text summarization. Your task is to summarize the text I provide in a {style} style, following the examples given.'},
            {'role': 'user', 'content': prompt_format.format(prompt=text)},],
        temperature=temperature)
    return [choice.message.content for choice in ans.choices]

def second_call(model, text, style, first_response):
    client = OpenAI(api_key=os.getenv('DEEPSEEK_API'), base_url="https://api.deepseek.com")
    ans = client.chat.completions.create(
        model=model,
        messages=[
            {'role': 'system', 'content': f'You are a helpful assistant who is an expert in text summarization. Your task is to provide the critical comments and helpful suggestions for the summary, which summarizes the article in a {style} style.'},
            {'role': 'user', 'content': f'<article>: {text}\n <summary>: {first_response}'},])
    return [choice.message.content for choice in ans.choices]

def third_call(model, text, max_tokens, style, first_response, second_response):
    client = OpenAI(api_key=os.getenv('DEEPSEEK_API'), base_url="https://api.deepseek.com")
    ans = client.chat.completions.create(
        model=model,
        max_tokens=max_tokens,
        messages=[
            {'role': 'system', 'content': f'You are a helpful assistant who is an expert in text summarization. Your task is to refine the summary based on the critique, where the summary summarizes the article in a {style} style. You should address all issues in the critique and ensure that all suggestions from the critique are incorporated. Please only return the refined summary.'},
            {'role': 'user', 'content': f'<article>: {text}\n <summary>: {first_response}\n <critique>: {second_response}'},])
    return [choice.message.content for choice in ans.choices]

def chat_api(model, max_tokens, text, temperature, style):
    first_response = first_call(model, max_tokens, text, temperature, style)
    #print("First response:", first_response[0])
    second_response = second_call(model, text, style, first_response[0])
    #print("Second response:", second_response[0])
    third_response = third_call(model, text, max_tokens, style, first_response[0], second_response[0])
    return third_response