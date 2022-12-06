
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



    
def pass_through(submit,
    opt_1_clicks, opt_2_clicks, opt_3_clicks,
    prompt, opt_1, opt_2, opt_3, temperature):

    # if opt_1_clicks == 0:
    #     raise PreventUpdate

    button_id = get_triggered()

    if button_id is not None:
        if '1' in button_id:
            prompt += opt_1
        elif '2' in button_id:
            prompt += opt_2
        elif '3' in button_id:
            prompt += opt_3

    options = []
    for i in range(3):
        response = openai.Completion.create(
                model="text-davinci-002",
                prompt=prompt.strip(),
                temperature=temperature,
            )

        print(response.choices)

        options.append(response.choices[0].text)

    return prompt, *options

