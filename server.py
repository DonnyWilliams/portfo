from os import EX_TEMPFAIL
from flask import Flask, render_template, url_for, request, redirect
import csv

app = Flask(__name__)


# This is not how to automatically set it up so any given page already has code
# to make it load.
# See the code below for how to do it.
# def main(arg1):
#    page_file = arg1
#    try:
#        @app.route(f'/{page_file}')
#        def page_func():
#            return render_template(f'{page_file}')
#    except AssertionError:
#        print("You got an assertion error.")

# If employing the code below to automatically create code to load each page, still
# keep this for the main page.
@app.route('/')
def my_home():
    return render_template('index.html')

# This is instead of doing a different @app.route('/[]') for each page.
# This is instead of doing a function to automate this.
# I never enter anything for a page name, though, so I'm not sure where that's
# coming from. Somehow, it works, though.


@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(page_name)

# This is to record data received in contact.html into database.txt.


def write_to_file(data):
    # mode='a' is the append mode.
    with open('database.txt', mode='a') as database:
        # This is syntax for printing values from a dict.
        email = data["email"]
        subject = data["subject"]
        message = data["message"]
        # \n is to create a new line with each new entry.
        file = database.write(f"\n{email},{subject},{message}")

# This is to record data received in contact.html into database.csv.


def write_to_csv(data):
    with open('database.csv', newline='', mode='a') as database2:
        email = data["email"]
        subject = data["subject"]
        message = data["message"]
        # First param is where do we want to write to?
        # Second param is how do we want to separate the data we're writing?
        # This says with a comma.
        # Third param is if we want any quotes around the characters.
        # It'll throw a TypeError if we don't put anything, so we're putting ".
        # Fourth param is saying we only want to use quotes in exceptional circumstances.
        # Can copy and past all of this code from .csv documentation
        csv_writer = csv.writer(database2, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        # Syntax is bc email, subject and message are now variables and not pulled
        # from a dict.
        csv_writer.writerow([email, subject, message])

    # This is the code to make the contact page work.
    # Based off of code that was copied and pasted from:
    # https://flask.palletsprojects.com/en/2.0.x/quickstart/#accessing-request-data
    # 'POST' and 'GET methods are default methods.
    # 'GET' means that the browser wants us to send information.
    # 'POST' means that the browswer wants us to save information.


@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    # You can see if this is 'POST' or 'GET' in the <form> section of the .html page.
    if request.method == 'POST':
        try:
            # .to_dict() turns whatever into a dict
            # This makes the form data appear in our Terminal responses in dict form.
            data = request.form.to_dict()
            # This is to work with function above to pass responses into .csv file.
            write_to_csv(data)
            # We have to return something.
            # If nothing is returned here, it'll throw a TypeError.
            return redirect("/thankyou.html")
        except:
            return 'Did not save to database.'
    else:
        return "Something went wrong. Try again!"

# The .html reference here is what the URL will show.
# @app.route('/index.html')
# def home():
#    The .html reference here is the file that is being linked to.
#    return render_template('index.html')


# @app.route('/about.html')
# def about_me():
#    return render_template('about.html')


# @app.route('/works.html')
# def blog():
#    return render_template('works.html')


# @app.route('/contact.html')
# def contact():
#    return render_template('contact.html')


# main('index.html')
# main('about.html')
# main('works.html')
# main('contact.html')
