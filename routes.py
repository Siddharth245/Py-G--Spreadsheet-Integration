
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from flask import Flask, render_template, request, json, jsonify, redirect, url_for
from enum import Enum

app = Flask(__name__)
app.debug = True

scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('corporate_client_secret.json', scope)
client = gspread.authorize(creds)

sheet = client.open('Corporate / Society Benefits')
worksheet = sheet.worksheet("Companies")
companies = worksheet.col_values(1)
twenty_per_cent_benefit = [5,7]

class Discounts(Enum):
    ANSI = 2
    SA = 3
    WSTA = 4
    EdAssist = 5
    Society_Co_Sponsor = 6
    Corporate_Member = 7

@app.errorhandler(404)
def page_not_found(e):
    print("Error!!!")
    return render_template('Error.html'),404

@app.route("/", methods=["GET","POST"])
def index():
    return render_template("index.htm")

@app.route("/searchcompany/<alpha>")
def searchcompany(alpha):
    companylist = []
    for company in companies:
        if company is not "":
            if alpha == "other":
                    if not company[0].isalpha():
                        companylist.append(company)
            if company.startswith(alpha):
                companylist.append(company)
    return render_template("companies.html", data=companylist)

@app.route("/getdetails/<name>")
def getdetails(name):
    result = []
    text = []
    companydetails = []
    print(name)
    if name in companies:
        companyindex = companies.index(name)
        companydetails = worksheet.row_values(companyindex+1)
        benefit = companydetails.index
        if benefit not in twenty_per_cent_benefit:
           discount = str(15)
        else:
            discount = str(20)
        #disp_benefit = text[0] + " has "+ str(Discounts(text.index("x")).name) + " discount of " + discount + "%"
        disp_benefit = companydetails[0] + " employees are eligible for a "+ discount + "%" + " discount of our programs"
        companydetails[0] = "Your Organization qualifies as our corporate member"
        companydetails[1] = disp_benefit
        companydetails[2] = "Yes"
        result = companydetails
    elif name not in companies:
        print("Something wrong")
        text.append("Your Organization does not qualify as our corporate member")
        text.append("Do you want to learn about becoming a Corporate Member?")
        text.append("No")
        result = text
    return render_template("companydetails.html", data=result)    

@app.route("/findcompany", methods=["GET","POST"])
def findcompany():
    if request.method =="POST": 
        query = request.form['searchPhrase']
        return redirect(url_for('getdetails',name=query))
    else:
        search = request.args.get('search')
        companylist = []
        for company in companies:
            companylist.append(company)
        companydetails = []
        companydetails = [companyname for companyname in companylist if search.lower() in companyname.lower()]
        return jsonify(companydetails)
    

if __name__ == '__main__':
    app.run()
