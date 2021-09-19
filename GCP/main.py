from URLshortener import app
from URLshortener.views import app_views


app.register_blueprint(app_views)


if __name__ == "__main__":
    app.run()

