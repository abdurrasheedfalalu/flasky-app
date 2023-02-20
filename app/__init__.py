import os
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

from config import config

bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(config[config_name])


    bootstrap.init_app(app)
    moment.init_app(app)
    db.init_app(app)


    from .main import main as main_blueprint

    app.register_blueprint(main_blueprint)

    from sendgrid import SendGridAPIClient
    from sendgrid.helpers.mail import Mail

    message = Mail(
        from_email='from_email@example.com',
        to_emails='to@example.com',
        subject='Sending with Twilio SendGrid is Fun',
        html_content='<strong>and easy to do anywhere, even with Python</strong>')
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)


    return app