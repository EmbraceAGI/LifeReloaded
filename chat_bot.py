import asyncio

import semantic_kernel as sk
from semantic_kernel.connectors.ai import ChatRequestSettings
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion

chat_request_settings = ChatRequestSettings(
    max_tokens=2000,
    temperature=0.7,
    top_p=1,
    frequency_penalty=0.5,
    presence_penalty=0.5,
)

kernel = sk.Kernel()

api_key, org_id = sk.openai_settings_from_dot_env()
kernel.add_chat_service('chat-gpt',
                        OpenAIChatCompletion('gpt-3.5-turbo', api_key, org_id))
oai_chat_service = OpenAIChatCompletion('gpt-3.5-turbo', api_key, org_id)


async def chat(context, input_text: str) -> None:
    # Save new message in the context variables
    print(f'User: {input_text}')
    context['user_input'] = input_text
    # Process the user message and get an answer
    answer = await chat_function.invoke_async(context=context)
    print(f'ChatBot: {answer}')
    return answer


async def stream_chat(context, input_text: str) -> None:
    print(f'User: {input_text}')
    context['user_input'] = input_text
    prompt = sk_prompt.replace('{{$user_input}}', input_text)
    stream = oai_chat_service.complete_chat_stream_async([('user', prompt)],
                                                         chat_request_settings)

    idx = 0  # to skip the first word "assistant:"
    async for text in stream:
        if idx == 0:
            idx += 1
            continue
        yield text

sk_prompt = '请扮演好，你现在是一个非常优秀的搜索引擎，百科全书，我将用任意语言问你任何问题' \
    '，你都要根据你的知识库做出详细的解答。如果有不确定的地方，请告知这一点。' \
    'User: {{$user_input}}' \
    'ChatBot:'

chat_function = kernel.create_semantic_function(sk_prompt,
                                                'ChatBot',
                                                max_tokens=1000,
                                                temperature=0.7,
                                                top_p=0.5)

context = kernel.create_new_context()
context['user_input'] = ''

if __name__ == '__main__':
    with open('LifeReloaded/LifeReloaded.txt', 'r') as fp:
        sk_prompt = fp.readlines()
    sk_prompt = ''.join(sk_prompt)
    chat_function = kernel.create_semantic_function(sk_prompt,
                                                    'ChatBot',
                                                    max_tokens=500,
                                                    temperature=0.7,
                                                    top_p=0.5)

    context = kernel.create_new_context()
    context['user_input'] = ''

    context = asyncio.run(chat(context, '你好'))
    context = asyncio.run(chat(context, '开始'))
