# from flask import Flask, render_template

# app = Flask(__name__)

# @app.route('/')
# def home():
#     # This will render the front.html
#     return render_template('front.html')

# @app.route('/book-appointment')
# def book_appointment():
#     # This will render the question.html
#     return render_template('question.html')

# if __name__ == '__main__':
#     app.run(debug=True)
from flask import Flask
from controllers.main_controller import main_routes

app = Flask(__name__,template_folder="views")

# Register Blueprints
app.register_blueprint(main_routes)

if __name__ == '__main__':
    app.run(debug=True)
