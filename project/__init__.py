from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(test_config)
    from project.api import api

    app.register_blueprint(api)
    return app
