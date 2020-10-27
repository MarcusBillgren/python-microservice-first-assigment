"""
The flask application package.
"""

from flask import Flask, render_template, make_response, jsonify, request
app = Flask(__name__)

PORT = 8080

STUDENT = {
    "courses" : {
        "j" : "Java",
        "p" : "Python",
        "g" : "Go"
        },
    "books" : {
        "book1" : "Java basics",
        "book2" : "Python fundamentals",
        "book3" : "Go basics"
        },
    "schools" : {
        "school1" : "School1",
        "school2" : "School2",
        "school3" : "School3"
        }
    }

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/getAll")
def getAll():
    return make_response(jsonify(STUDENT), 200)

@app.route("/qstr")
def query():
    if request.args:
        req = request.args
        res = {}
        for key, value in req.items():
            print("key " + key)
            print("value " + value)
            res[key] = value
        res = make_response(jsonify(res), 200)
        return res

    return make_response(jsonify("no argz"), 404)
#Get
@app.route("/get/<collection>/<member>")
def get_member(collection, member):
    if collection in STUDENT:
        member = STUDENT[collection].get(member)
        if member:
            res = make_response(jsonify({"mem" : member}), 200)
            return res
        res = make_response(jsonify("no member found"), 404)
        return res
    res = make_response(jsonify("no collection found"), 404)
    return res
#Post
@app.route("/post/<collection>", methods=["POST"])
def add_collection(collection):
    req = request.get_json()

    if not collection in STUDENT:
        STUDENT.update({collection : req})
        res = make_response(jsonify({"success" : req}), 200)
        return res

    return make_response(jsonify("not great"),400)

#Put  
@app.route("/edit/<collection>/<member>", methods=["PUT"])
def edit_member(collection, member):
    req = request.get_json()
    if collection in STUDENT:
        if not STUDENT[collection].get(member):
            return make_response(jsonify({"error" : "no such member"}), 404)

        STUDENT[collection][member] = req["new"]
        res = make_response(jsonify({"res" : STUDENT[collection]}), 200)
        return res
    res = make_response(jsonify({"error" : "not found"}),400)
    return res
#Delete
@app.route("/delete/<collection>/<member>", methods=["DELETE"])
def deleteBook(collection, member):
    if member in STUDENT[collection]:
        del STUDENT[collection][member]
        return make_response(jsonify({"deleted" : member}), 200)
    return make_response(jsonify({"error" : "not found"}), 400)


if __name__ == "__main__":
    print("Server is running! PORT :: %s" % PORT)
    app.run(host='127.0.0.1', port=PORT)


