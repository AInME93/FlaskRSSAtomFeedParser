from . import users
from flask import render_template
from flask_security import login_required


# Views
@users.route('/register', methods = ['POST'])
@login_required
def register():
    return render_template('security/register_user.html')

@users.route('/login')
@login_required
def logging_in():
    return render_template('security/register_user.html')