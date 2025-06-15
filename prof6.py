
import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello Hello hello"
    
    
    

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render impose un port
    app.run(host="0.0.0.0", port=port)

