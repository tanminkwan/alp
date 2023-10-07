from flask import make_response, render_template
from miniagent import app

@app.route('/nogame')
def nogame_page():
    
    return make_response(render_template('nogame.html'))