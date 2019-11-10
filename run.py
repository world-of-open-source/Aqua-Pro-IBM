from flaskblog import app
from flaskblog.routes import home
import time
if __name__ == '__main__':
    app.run(debug=True,threaded=True)