import sys
import os
import base64
import requests
import json

MP_APP_ID = os.environ.get('MATHPIX_APP_ID')
MP_APP_KEY = os.environ.get('MATHPIX_APP_KEY')

WA_APP_ID = os.environ.get('WOLFRAM_APP_ID')

def main():
    file_path = 'quadratic.jpg'
    image_uri = "data:image/jpg;base64," + base64.b64encode(open(file_path, "rb").read()).decode()
    latex = 'solve {}'.format(parse_image(image_uri))
    print(latex)
    print(solve(latex))


def parse_image(image_uri):
    r = requests.post("https://api.mathpix.com/v3/text",
        data=json.dumps({'src': image_uri}),
        headers={"app_id": MP_APP_ID, "app_key": MP_APP_KEY,
                "Content-type": "application/json"})
    return json.loads(r.text)['latex_styled']

def solve(latex):
    r = requests.post(
            "https://api.wolframalpha.com/v2/query",
            params={"appid": WA_APP_ID},
            data={"input": latex, "output": "JSON", "format": "plaintext"}
        )
    result = json.loads(r.text)['queryresult']
    output_str = ''
    if result['success']:
        for pod in result["pods"]:
            if pod["title"] == "Results":
                for subpod in pod["subpods"]:
                    if len(output_str):
                        output_str += ', '
                    output_str += subpod["plaintext"]
    return output_str

if __name__ == '__main__':
    main()
