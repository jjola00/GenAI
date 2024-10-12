from flask import Flask, render_template
from flask import jsonify
import app as legalAdvice
import lawyerFinder

app = Flask(__name__)
    
@app.route('/generate/<inp>')
def generate(inp):
    response = legalAdvice.GetResponse(inp)
    return response

@app.route('/get/lawyers/<tags>')
def GetAllLawyersWithTags(tags):
    client = lawyerFinder.LawyerFinder(tags)
    client.saveLawyersWithCorrectTags()
    return jsonify(client.lawyers)


if __name__=='__main__': 
   app.run(debug=True) 