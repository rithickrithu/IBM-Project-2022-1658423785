import json
from os import environ as env
from urllib.parse import quote_plus, urlencode

from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from flask import Flask, redirect, render_template, session, url_for, request

from newsapi import NewsApiClient

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

app = Flask(__name__)
# env_config = env.getenv("APP_SETTINGS", "config.DevelopmentConfig")
# app.config.from_object(env_config)
app.secret_key = env.get("APP_SECRET_KEY")

newsapi = NewsApiClient(api_key=env.get("NEWS_API_KEY"))

oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id= env.get("AUTH0_CLIENT_ID"),
    client_secret= env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)

all_categories = ["business", "entertainment", "general", "health", "science", "sports", "technology"]
# @app.route("/")
# def index():
#     sample_config_data = app.config.get("SAMPLE")
#     return sample_config_data

@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        #should be redirect_uri and not redirect_url
        redirect_uri=url_for("callback", _external=True)
    )

@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://" + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("home", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )

@app.route("/")
def home():
    # all_articles = get_news()
    all_articles = get_top_headlines_today()
    return render_template(
        # "home.html", 
        "home_og.html",
        session=session.get('user'),
        all_articles = all_articles,
        categories= all_categories
        # pretty=json.dumps(session.get('user'),indent=4)
    )

@app.route("/news")
def get_news():
    all_articles = newsapi.get_everything(q='bitcoin',
                                      sources='bbc-news,the-verge',
                                      domains='bbc.co.uk,techcrunch.com',
                                      from_param='2022-10-10',
                                      to='2022-10-12',
                                      language='en',
                                      sort_by='relevancy',
                                      page=1)
    return all_articles

# @app.route("/ind-cat", methods=["POST", "GET"])
# def get_individual_category_news():

#     category_news = newsapi.get_everything(category)


@app.route("/top-headlines-today")
def get_top_headlines_today():
    user_categories = ["business", "entertainment", "general", "health", "science", "sports", "technology"]
    top_headlines = {}
    for i in range(len(user_categories)):
        top_headlines[user_categories[i]] = newsapi.get_top_headlines(
                                                        # sources="",
                                                        category=user_categories[i],
                                                        language='en',
                                                        page_size=5)
        # top_headlines.append(newsapi.get_top_headlines(
        #                                   category='business',
        #                                   language='en'))
        
    return top_headlines

@app.route("/user-info")
def user_info():
    return session.get('user')

@app.route("/news-from-sources")
def get_news_from_sources():
    return 

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=env.get("PORT", 5000))
