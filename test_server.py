import requests

print(
    requests.post(
        "http://0.0.0.0:10000",
        json={
            "from_email": "johnshirley@oilco.com",
            "content": """
                Dear MayFair Attorneys,
                I hope this email finds you very well. 
                I was referred to you by a colleague. He mentioned that your firm specialises in offshore tax law. 
                My company Oil&Co is looking for some legal advice on our new ventures in Mauritius.
                Who would be best to speak to, if the above applies?
                All the best,
                Jonathan Shirley.
                COO at Oil@Co
                """
        }
    ).json()
)