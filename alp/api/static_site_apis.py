from flask import make_response, render_template
from miniagent import app

@app.route('/nogame')
def nogame_page():
    
    return make_response(render_template('nogame.html'))

@app.route('/dashboard/<string:event_id>')
def dashboard_page(event_id):
    
    return render_template('dashboard.html',event_id=event_id)