
from flask import Flask

@app.route("/")
def hello():
    return "Hello World!"

def start():
    app.run()

def stop():
    pass
    
if __name__ == "__main__":
    start()