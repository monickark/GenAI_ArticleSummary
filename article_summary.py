from dotenv import load_dotenv
import os
from openai import AzureOpenAI
from flask import Flask, request, render_template

app = Flask(__name__)
load_dotenv()

client = AzureOpenAI(
  azure_endpoint = os.getenv('AZURE_ENDPOINT'),
  api_key=os.getenv('API_KEY'),  
  api_version=os.getenv('API_VERSION')
)
 

def summarize_article(article_text):
    print("inside summarize article fn : ", article_text)
    response = client.chat.completions.create(     
        model="gpt-35-turbo",         
       # prompt="Summarize the following article:\n\n{article_text}",
         messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"Summarize the following article in 3 points as listed output:\n\n{article_text}?"},
    ]      
    )
    print("after summarize article ")
    summary = response.choices[0].message.content
    return summary

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        _article_text = request.form["article_text"]
        print("_article_text : ", _article_text[0])
        summary = summarize_article(_article_text)
        return render_template("index.html", summary=summary, article_text=_article_text)
    return render_template("index.html", summary="", article_text="")

if __name__ == "__main__":
    app.run(debug=True)
