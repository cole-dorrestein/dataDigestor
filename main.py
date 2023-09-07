import openai
import os

from misc import openai_key
from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI()

openai.api_key = openai_key

function_desc = [
    {
        'name': 'extract_info_from_email',
        'description': 'categorise and extract key info from an email, such as: use case, company name, contact details, etc.',
        'parameters': {
            'type': 'object',
            'properties': {
                'companyName': {
                    'type': 'string',
                    'description': 'the name of the company that sent the email. If no company is found, use the name of the sender'
                },
                'useCase': {
                    'type': 'string',
                    'description': "the purpose & use case of this company's enquiry"
                },
                'priority': {
                    'type': 'string',
                    'description': "Try to give a priority score to this email based on how likely the email will lead to a good business opportunity for Legal consulting, from 0 to 10"
                },
                'category': {
                    'type': 'string',
                    'description': "Try categorise this email into categories like these: 1. customer support; 2. consulting; 3. job; 4. partnership; etc."
                },
                'product': {
                    'type': 'string',
                    'description': "try identify the product being requested, if any"
                },
                'amount': {
                    'type': 'string',
                    'description': "try identify the amount of products the client is requesting, if any"
                },
                'nextStep': {
                    'type': 'string',
                    'description': "What is the suggest next step to move this forward?"
                },
            },
            'required': ['companyName', 'useCase', 'priority', 'category', 'product', 'amount', 'nextStep']
        }
    }
]


demo_email = """
Dear MayFair Attorneys,

I hope this email finds you very well. 

I was referred to you by a colleague. He mentioned that your firm specialises in offshore tax law.
My company Oil&Co is looking for some legal advice on our new ventures in Mauritius.

Who would be best to speak to, if the above applies?

All the best,
Jonathan Shirley.

COO at Oil@Co
"""

# prompt = f'Please extract the key information from this email: \n {demo_email}'
#
# messages = [
#     {
#         'role': 'user',
#         'content': prompt
#     }
# ]
#
# response = openai.ChatCompletion.create(
#     model='gpt-3.5-turbo-16k',
#     messages=messages,
#     functions=function_desc,
#     function_call='auto'
# )
#
# print(response)


class Email(BaseModel):
    from_email: str
    content: str

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/")
def digest_email(email: Email):
    content = email.content

    query = f'Please extract the key information from this email: \n {content}'

    messages = [{'role': 'user', 'content': query}]

    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo-16k',
        messages=messages,
        functions=function_desc,
        function_call='auto'
    )

    arguments = response.choices[0]['message']['function_call']['arguments']

    companyName = eval(arguments).get('companyName')
    priority = eval(arguments).get('priority')
    product = eval(arguments).get('product')
    category = eval(arguments).get('category')
    amount = eval(arguments).get('amount')
    nextStep = eval(arguments).get('nextStep')

    return {
        'companyName': companyName,
        'priority': priority,
        'product': product,
        'category': category,
        'amount': amount,
        'nextStep': nextStep
    }


# email = Email(
#     from_email='kjkslns@gmail.com',
#     content=demo_email
# )
#
# digested = digest_email(email)
#
# print("Original Email: \n")
# print('___________________')
# print(demo_email)
# print('\n\n')
# print("Digested Email: \n")
# print('___________________')
# print(digested)
