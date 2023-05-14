import datetime

import pymongo
import pytz
from bson.objectid import ObjectId

from flask import Flask, Blueprint, current_app
from flask_admin import BaseView, expose
from flask_login import current_user

from .. import admin
from .. import mongo

from wtforms import form, fields

from flask_admin.form import Select2Widget
from flask_admin.contrib.pymongo import ModelView, filters
from flask_admin.model.fields import InlineFormField, InlineFieldList

# Create application
bp = Blueprint("admins", __name__, url_prefix="/admin")


class SecureModelView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated:
            current_user.writer = mongo.db.writers.find_one(
                {"_id": ObjectId(current_user.id)}
            )
        else:
            return False

        return current_user.writer["email"] in current_app.config["ADMIN_USER_EMAILS"]


class UserForm(form.Form):
    confirmed = fields.BooleanField("confirmed")
    email = fields.StringField("email")
    time = fields.SelectField("time", choices=[i for i in range(24)])
    extras = fields.SelectMultipleField(
        "extras", choices=["codingchallenge", "repositories"]
    )
    password = fields.StringField("password")
    frequency = fields.SelectField(
        "frequency",
        choices=[
            ([1, 2, 3, 4, 5, 6, 7], "everyday"),
            ([1, 2, 3, 4, 5], "weekdays"),
            ([6, 7], "weekends"),
        ],
    )
    theme = fields.SelectField("theme", choices=[("light", "light"), ("dark", "dark")])
    timezone = fields.SelectField("timezone", choices=pytz.all_timezones)


class UserView(SecureModelView):
    column_list = (
        "email",
        "confirmed",
        "time",
        "extras",
        "frequency",
        "theme",
        "timezone",
    )

    form = UserForm


class ArticleForm(form.Form):
    title = fields.StringField("title")
    description = fields.StringField("description")
    content = fields.TextAreaField("content")
    thumbnail = fields.StringField("thumbnail")
    categories = fields.SelectMultipleField(
        "categories",
        choices=[
            ("ai-news", "AI"),
            ("corporation-news", "Corporation"),
            ("crypto-news", "Crypto"),
            ("gadget-news", "Gadget"),
            ("gaming-news", "Gaming"),
            ("robotics-news", "Robotics"),
            ("science-news", "Science"),
            ("space-news", "Space"),
            ("other-news", "Other"),
        ],
    )
    source = fields.SelectField(
        "source",
        choices=[
            ("gmt", "GMT"),
            ("techcrunch", "TechCrunch"),
            ("verge", "TheVerge"),
            ("bbc", "BBC"),
            ("cnn", "CNN"),
            ("guardian", "Guardian"),
        ],
    )
    formatted_source = fields.SelectField(
        "source",
        choices=[
            ("GMT", "GMT"),
            ("TechCrunch", "TechCrunch"),
            ("TheVerge", "TheVerge"),
            ("BBC", "BBC"),
            ("CNN", "CNN"),
            ("Guardian", "Guardian"),
        ],
    )
    author = fields.StringField("author")
    url = fields.StringField("url")
    views = fields.IntegerField("views", default=0)
    date = fields.DateTimeField("date", default=datetime.datetime.utcnow())


class ArticleView(SecureModelView):
    column_list = (
        "title",
        "description",
        "content",
        "thumbnail",
        "categories",
        "source",
        "formatted_source",
        "author",
        "url",
        "views",
        "date",
    )

    form = ArticleForm


class WriterForm(form.Form):
    about = fields.TextAreaField("about")
    accepted = fields.BooleanField("accepted")
    badges = fields.SelectMultipleField(
        "badges", choices=[("dev", "Dev"), ("writer", "Writer"), ("tester", "Tester")]
    )
    confirmed = fields.BooleanField("confirmed")
    created_at = fields.DateTimeField("created_at")
    email = fields.StringField("email")
    github = fields.StringField("github")
    name = fields.StringField("name")
    password = fields.PasswordField("password")
    patreon = fields.StringField("patreon")
    paypal = fields.StringField("paypal")
    public_email = fields.StringField("public_email")
    reasoning = fields.TextAreaField("reasoning")
    timezone = fields.SelectField("timezone", choices=pytz.all_timezones)
    twitter = fields.StringField("twitter")
    user_name = fields.StringField("user_name")
    views = fields.IntegerField("views")
    website = fields.StringField("website")


class WriterView(SecureModelView):
    column_list = (
        "about",
        "accepted",
        "badges",
        "confirmed",
        "created_at",
        "email",
        "github",
        "name",
        "password",
        "patreon",
        "paypal",
        "public_email",
        "reasoning",
        "timezone",
        "twitter",
        "user_name",
        "views",
        "website",
    )

    form = WriterForm


admin.add_view(UserView(mongo.db.users, "Users"))
admin.add_view(ArticleView(mongo.db.articles, "Articles"))
admin.add_view(WriterView(mongo.db.writers, "Writers"))
