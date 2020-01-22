from flask import Flask, render_template, url_for, request
from forms import FilterForm
import bikeshare

app = Flask(__name__)
app.config['SECRET_KEY'] = 'udacity'


@app.route('/')
def homepage():
    return render_template("homepage.html")

@app.route('/input', methods=['GET','POST'])
def input():
    form = FilterForm()

    if form.is_submitted():
        result = request.form
        return render_template('confirmation_page.html', result=result)
    return render_template('input_page.html', form=form)


@app.route('/results')
def results():
    name = request.args.get('name')
    city = request.args.get('city')
    month = request.args.get('month')
    day = request.args.get('day')
    
    stats_dict = bikeshare.stats_calculator(city, month, day) 
    return render_template('results_page.html', name=name, city=city, month=month, day=day, stats_dict=stats_dict)

@app.route('/goodbye')
def goodbye():
    return render_template('goodbye_page.html')


if __name__ == "__main__":
    app.run(debug=True)


    