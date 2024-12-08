from flask import Flask
from controllers.main_controller import main_routes

app = Flask(__name__,template_folder="views")

# Register Blueprints
app.register_blueprint(main_routes)

if __name__ == '__main__':
    app.run(debug=True)
