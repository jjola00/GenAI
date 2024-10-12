from flask import Flask
import main as legalAdvice
app = Flask(__name__)

@app.route('/generate/<inp>')
def generate(inp):
    response = legalAdvice.GetResponse(inp)
    return response

if __name__=='__main__': 
   app.run(debug=True) 