from flask import Flask, render_template, request, jsonify
import csv, os

app=Flask(__name__)
DATA="expenses.csv"
if not os.path.exists(DATA):
    open(DATA,"w").write("date,category,amount,note\n")

@app.route("/")
def index(): return render_template("index.html")

@app.route("/expenses",methods=["GET","POST"])
def expenses():
    if request.method=="POST":
        d=request.json
        with open(DATA,"a",newline="",encoding="utf8") as f:
            csv.writer(f).writerow([d.get("date",""),d.get("category","Other"),d.get("amount",0),d.get("note","")])
    rows=[]
    with open(DATA,encoding="utf8") as f:
        for r in csv.DictReader(f): rows.append(r)
    total=sum(float(r["amount"]) for r in rows)
    by={}
    for r in rows: by[r["category"]]=by.get(r["category"],0)+float(r["amount"])
    return jsonify({"expenses":rows,"total":round(total,2),"by_category":by})

if __name__=="__main__": app.run(debug=True)
