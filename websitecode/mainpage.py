from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, validators
import comment_analysis
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

import io
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
# app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
app.config['SQLALCHEMY_DATABASE_URI']='mysql://hzx957:sql104957@hzx957.mysql.pythonanywhere-services.com/hzx957$toxic'
db=SQLAlchemy(app)

class User(db.Model):
    __tablename__='toxic'
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"User('{self.id}', '{self.date_posted}')"

class ReusableForm(Form):
    comment = TextField('Comment:', validators=[validators.required()])

@app.route("/", methods=['GET', 'POST'])
def mainpage():
    # # initialization
    global percentage
    percentage=[[0,0,0,0,0,0]]
    form = ReusableForm(request.form)
    print(form.errors)

    if request.method == 'POST':
        # # input comment
        comment=request.form.get("comment", False)
        print(comment)

        # # verify and add user info
        if form.validate():
            user=User(content=comment)
            db.session.add(user)
            db.session.commit()
            flash('Thanks for input ')
        else:
            flash('Error: Can not be empty. ')

        # # analysis comment
        percentage=comment_analysis.com_analysis(comment)

    return render_template('mainpage.html', form=form)


@app.route('/plot.png', methods=['GET', 'POST'])
# define canvas, output
def plot_png():
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

# draw figure
def create_figure():
    fig, ax = plt.subplots()
    x = np.arange(6)
    # ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    ax.set_frame_on(False)
    plt.bar(x, percentage[0])
    plt.ylim((0,1))
    plt.xticks(x, ('toxic','severe_toxic','obscence','threat','insult','identity_hate'))
    for i, v in enumerate(percentage[0]):
        plt.text(x[i] - 0.25, v + 0.01, str(round(v, 2)))
    return fig

if __name__ == "__main__":
    app.run()
