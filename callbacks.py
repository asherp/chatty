
import os
from dotenv import load_dotenv

load_dotenv()

import openai

import dash
from dash.exceptions import PreventUpdate

def get_triggered():
    ctx = dash.callback_context
    if not ctx.triggered:
        button_id = None
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    return button_id

openai.api_key = os.getenv("OPENAI_API_KEY")


# @app.route("/", methods=("GET", "POST"))
# def index():
#     if request.method == "POST":
#         animal = request.form["animal"]
#         response = openai.Completion.create(
#             model="text-davinci-002",
#             prompt=generate_prompt(animal),
#             temperature=0.6,
#         )
#         return redirect(url_for("index", result=response.choices[0].text))

#     result = request.args.get("result")
#     return render_template("index.html", result=result)


import unicodedata
import re

def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')

def save_prompt(prompt, char_length=20, min_length=100):
    """save the prompt to a file named after the first and last characters"""
    if len(prompt) > min_length:
        fname = prompt[:char_length] + '__' + prompt[-char_length:]
        fname = slugify(fname).strip()
        with open(f'stories/{fname}.txt', 'w') as f:
            f.write(prompt)

    
def pass_through(submit,
    opt_1_clicks, opt_2_clicks, opt_3_clicks,
    prompt, opt_1, opt_2, opt_3, temperature):


    button_id = get_triggered()

    if button_id is not None:
        if '1' in button_id:
            prompt += opt_1
        elif '2' in button_id:
            prompt += opt_2
        elif '3' in button_id:
            prompt += opt_3

    save_prompt(prompt)

    options = []
    for i in range(3):
        response = openai.Completion.create(
                model="text-davinci-002",
                prompt=prompt.strip(), # strip prevents response from stopping
                temperature=temperature,
            )

        print(response.choices)

        options.append(response.choices[0].text)

    return prompt, *options

