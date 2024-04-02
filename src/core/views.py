from flask import Blueprint, render_template, flash, redirect, url_for, request, session
from flask_login import current_user, login_required, login_user, logout_user

import requests
from requests.exceptions import JSONDecodeError

from src import db
from src.core.models import Post

from datetime import datetime
from decouple import config

import praw

core_bp = Blueprint("core", __name__)

REDDIT_CLIENT_ID = config("REDDIT_CLIENT_ID")
REDDIT_SECRET = config("REDDIT_SECRET")
REFRESH_TOKEN = config("REFRESH_TOKEN")
RAPID_API_KEY = config("RAPID_API_KEY")

@core_bp.route("/")
@login_required
def home():
    page = request.args.get('page', 1, type=int)
    per_page = 20
    # Query all posts from the database
    # posts = Post.query.order_by(Post.created_utc.desc()).all()
    pagination = Post.query.order_by(Post.created_utc.desc()).paginate(page, per_page, error_out=False)
    # Render them in the posts.html template
    posts = pagination.items
    return render_template("core/posts.html", posts=posts, pagination=pagination, per_page=per_page)
    # return render_template("core/index.html")

@core_bp.route("/edit_notes/<int:post_id>", methods=["POST"])
@login_required
def edit_notes(post_id):
    post = Post.query.get_or_404(post_id)
    post.notes = request.form['notes']
    print("New notes:", post.notes)
    db.session.commit()
    flash('Notes updated successfully', 'success')
    category_filter = session.get('category_filter', 'All')
    status = session.get('status', 'All')
    return redirect(url_for('core.filter', category_filter=category_filter, status=status))

@core_bp.route("/update_post_status/<int:post_id>", methods=["POST"])
@login_required
def update_post_status(post_id):
    post = Post.query.get_or_404(post_id)
    new_status = request.form.get('new_status', 'Unread')  # Default to 'Unread' if not provided
    post.status = new_status
    db.session.commit()
    flash('The post status has been updated.', 'success')
    category_filter = session.get('category_filter', 'All')
    status = session.get('status', 'All')
    return redirect(url_for('core.filter', category_filter=category_filter, status=status))

@core_bp.route("/add_post", methods=["POST"])
@login_required
def add_post():
    title = request.form['title']
    url = request.form['url']
    other = request.form['other']
    publisher = request.form['publisher']
    publisher_url = request.form['publisher_url']
    category = request.form['category']
    created_utc = datetime.utcnow()
    new_post = Post(title=title, url=url, other=other, publisher=publisher, publisher_url=publisher_url, created_utc=created_utc, category=category)
    db.session.add(new_post)
    db.session.commit()
    flash('The post has been added.', 'success')
    return redirect(url_for('core.home'))

def store_posts(post_list):
    new_posts = []
    for post_data in post_list:
        # Check if post already exists based on the unique URL
        exists = db.session.query(Post.id).filter_by(url=post_data['url']).scalar() is not None
        if not exists:
            # Post does not exist yet, so we create a new Post instance
            new_post = Post(
                title=post_data['title'],
                other=post_data['other'],
                url=post_data['url'],
                publisher=post_data['publisher'],
                publisher_url=post_data['publisher_url'],
                created_utc=post_data['created'],
                category='Reddit',
                status='Unread'
            )
            new_posts.append(new_post)

    # Add all new posts to the session and commit
    db.session.add_all(new_posts)
    db.session.commit()

@core_bp.route("/reddit_refresh/", methods=["POST"])
@login_required
def refresh_reddit():
    reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_SECRET,
        refresh_token=REFRESH_TOKEN,
        user_agent="testscript by u/fakebot3",
    )
    if request.method == 'POST':
        post_list = []
        for submission in reddit.subreddit("all").search("deepfake"):
            url = "https://www.reddit.com"+ submission.permalink
            title = submission.title
            publisher = submission.author.name
            publisher_url = "https://www.reddit.com/user/" + publisher
            subred = submission.subreddit.display_name
            created_utc = datetime.utcfromtimestamp(submission.created_utc)
            post_list.append({'title': title, 'other': subred, 'url': url, 'publisher': publisher, 'publisher_url': publisher_url, 'created': created_utc})
        store_posts(post_list)
        flash('Updated reddit posts', 'success')
        
    category_filter = session.get('category_filter', 'All')
    status_filter = session.get('status_filter', 'All')
    return redirect(url_for('core.filter', category_filter=category_filter, status_filter=status_filter))
    # return render_template('core/table.html', posts=post_list)
    # return f"Updated reddit posts."

def store_news(news_list):
    new_news = []
    for news_data in news_list:
        # Check if news article already exists based on the unique URL
        exists = db.session.query(Post.id).filter_by(url=news_data['url']).scalar() is not None
        if not exists:
            new_article = Post(
                title=news_data['title'],
                url=news_data['url'],
                publisher=news_data['publisher'],
                publisher_url=news_data['publisher_url'],
                created_utc=news_data['published'],
                category='News',
                other=None,
                status='Unread'
            )
            new_news.append(new_article)

    db.session.add_all(new_news)
    db.session.commit()

@core_bp.route("/news_refresh/", methods=["POST"])
@login_required
def refresh_news():
    url = "https://news-api14.p.rapidapi.com/search"
    querystring = {"q": "deepfake", "country": "us", "language": "en",}
    headers = {
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "news-api14.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        news_data = response.json()
        news_list = []

        for article in news_data['articles']:
            title = article['title']
            url = article['url']
            published_date = datetime.strptime(article['published_date'], "%Y-%m-%dT%H:%M:%S+00:00")

            publisher = article['publisher']['name'] if article['publisher'] else 'Unknown'
            publisher_url = article['publisher']['url']

            news_list.append({'title': title, 'url': url, 'publisher': publisher, 'publisher_url': publisher_url, 'published': published_date})

        store_news(news_list)
        flash('Updated news articles', 'success')
    else:
        flash('Failed to fetch news articles', 'error')

    category_filter = session.get('category_filter', 'All')
    status_filter = session.get('status_filter', 'All')
    return redirect(url_for('core.filter', category_filter=category_filter, status_filter=status_filter))

@core_bp.route('/posts/filter')
def filter():
    page = request.args.get('page', 1, type=int)
    per_page = 20
    category_filter = request.args.get('category_filter')
    status_filter = request.args.get('status_filter', 'All')

    session['category_filter'] = category_filter
    session['status_filter'] = status_filter

    query = Post.query

    if category_filter != "All":
        query = query.filter(Post.category == category_filter)

    if status_filter != "All":
        query = query.filter(Post.status == status_filter)

    posts = query.order_by(Post.created_utc.desc()).all()
    pagination = query.order_by(Post.created_utc.desc()).paginate(page, per_page, error_out=False)
    posts = pagination.items

    return render_template("core/posts.html", posts=posts, category_filter=category_filter, status_filter=status_filter, pagination=pagination, per_page=per_page)

