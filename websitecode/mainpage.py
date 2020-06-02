from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, validators
import comment_analysis
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

import io
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
# import numpy as np
import pandas as pd

# App config.
DEBUG = True

# app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
SQLALCHEMY_DATABASE_URI ='mysql://hzx957:sql104957@hzx957.mysql.pythonanywhere-services.com/hzx957$toxic'
SQLALCHEMY_BINDS = {
    'db1': SQLALCHEMY_DATABASE_URI,
    'db2': 'mysql://hzx957:sql104957@hzx957.mysql.pythonanywhere-services.com/hzx957$contact'
}
app = Flask(__name__, static_url_path='/static')
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
db = SQLAlchemy(app)

class CommentForm(Form):
    comment = TextField('Comment:', validators=[validators.required()])

class ContactForm(Form):
    name = TextField('Name:', validators=[validators.required()])
    message = TextField('Message:', validators=[validators.required()])

class User(db.Model):
    __tablename__='toxic'
    __bind_key__ = 'db1'
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"User('{self.id}', '{self.date_posted}')"

class Contact(db.Model):
    __tablename__ = 'contact'
    __bind_key__ = 'db2'
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.Text, nullable=False)
    Message = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"User('{self.id}', '{self.Name}')"

@app.route("/", methods=['GET', 'POST'])
def mainpage():
    # # initialization
    global percentage
    percentage=[[0,0,0,0,0,0]]
    form1 = CommentForm(request.form)
    form2 = ContactForm(request.form)

    if request.method == 'POST':

        if request.form.get('submit') == 'submit-1':
            # # input comment
            comment=request.form.get("comment", False)
            print(comment)

            # # verify and add user info
            if form1.validate():
                user=User(content=comment)
                db.session.add(user)
                db.session.commit()
                flash('Thanks for input ')
                print('form1 valid')
            else:
                flash('Error: Can not be empty. ')

            # # analysis comment
            percentage=comment_analysis.com_analysis(comment)

        elif request.form.get('submit') == 'submit-2':
            print('get form2')
            if form2.validate():
                print('form2 valid')
                contact=Contact(Name=request.form.get("name", False),
                            Message=request.form.get("message", False))
                db.session.add(contact)
                db.session.commit()
                flash('Thanks for input ')
            else:
                print('form2 not valid')
                flash('Error: Can not be empty. ')

    return render_template('index.html')


@app.route('/plot.png', methods=['GET', 'POST'])
# define canvas, output
def plot_png():
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

# draw figure
def create_figure():
    # fig, ax = plt.subplots()
    # my_range = np.arange(6)
    # # ax.xaxis.set_visible(False)
    # ax.yaxis.set_visible(False)
    # ax.set_frame_on(False)
    # plt.bar(my_range, percentage[0])
    # plt.ylim((0,1))
    # plt.xticks(my_range, ('toxic','severe_toxic','obscence','threat','insult','identity_hate'))
    # for i, v in enumerate(percentage[0]):
    #     plt.text(my_range[i] - 0.25, v + 0.01, str(round(v, 2)))
    # return fig


    # set font
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = 'Helvetica'

    # set the style of the axes and the text color
    plt.rcParams['axes.edgecolor']='#333F4B'
    plt.rcParams['axes.linewidth']=0.8
    plt.rcParams['xtick.color']='#333F4B'
    plt.rcParams['ytick.color']='#333F4B'
    plt.rcParams['text.color']='#333F4B'

    # create some fake data
    percentages = pd.Series(percentage[0],
                        index=['Toxic','Severe toxic','Obscence','Threat','Insult','Identity hate'])
    df = pd.DataFrame({'percentage' : percentages})
    df = df.sort_values(by='percentage')

    # we first need a numeric placeholder for the y axis
    my_range=list(range(1,len(df.index)+1))

    fig, ax = plt.subplots(figsize=(6,5))

    # create for each expense type an horizontal line that starts at x = 0 with the length
    # represented by the specific expense percentage value.
    plt.hlines(y=my_range, xmin=0, xmax=df['percentage'], color='#007ACC', alpha=0.2, linewidth=8)
    # plt.xlim((0,1))

    # create for each expense type a dot at the level of the expense percentage value
    plt.plot(df['percentage'], my_range, "o", markersize=5, color='#007ACC', alpha=0.6)

    # set labels
    ax.set_xlabel('Percentage', fontsize=18, fontweight='black', color = '#333F4B')
    ax.set_ylabel('')

    # set axis
    ax.tick_params(axis='both', which='major', labelsize=16)
    plt.yticks(my_range, df.index)

    # # add labels
    # for i, v in enumerate(df['percentage']):
    #     plt.text(v + 0.02, my_range[i], str(round(v, 3)), ha='right', va='center')

    # add an horizonal label for the y axis
    # fig.text(-0.23, 0.96, 'Type', fontsize=15, fontweight='black', color = '#333F4B')

    # change the style of the axis spines
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')
    ax.spines['left'].set_smart_bounds(True)
    ax.spines['bottom'].set_smart_bounds(True)

    # set the spines position
    ax.spines['bottom'].set_position(('axes', -0.04))
    ax.spines['left'].set_position(('axes', 0.015))

    plt.subplots_adjust(left=0.25, bottom=0.25, right=0.7, top=0.95)

    return fig

if __name__ == "__main__":
    app.run()
