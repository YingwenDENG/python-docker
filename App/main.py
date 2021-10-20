from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
DB_URI= 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user="postgres",pw="abc",url="postgis:5432",db="postgres")

app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI # pass to where the database is
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Posts(db.Model):
    __tablename__="posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True)
    content = db.Column(db.String(120), unique=True)
    author = db.Column(db.String(80), unique=False)

    # the constructor for this object
    def __init__(self, title, content,author):
        self.title = title
        self.content = content
        self.author = author
    # print out whenever we get create something in the db (this is the format of what is returned by Posts.query.all()
    def __repr__(self):
        return '<Post %r>' % self.id

""" # dummie data for testing
all_posts = [
    {
        "title":"Post 1",
        "content": "Content post 1",
        "author":"yw"
    },
    {
        "title":"Post 2",
         "content": "Content post 2"
    }
] """


# define the base url
@app.route("/")
def index():
    return render_template("index.html") # whatever it returns back, it just spits to the browser (text, html....)

@app.route("/home/<string:name>")
# the code will be run whenever we get to the url
def hello_world(name):
    return 'Hello,' + name

# def connect_to_postgis():
#     HOST = 'postgis'
#     pass

@app.route("/posts", methods=['GET','POST'])
def posts():
    if request.method == "POST":
        post_title = request.form["title"]
        post_content = request.form["content"]
        post_author = request.form["author"]
        new_post = Posts(title=post_title, content=post_content, author=post_author)

        try:
             # add this new post to the database session (current runtime)
             db.session.add(new_post)
             # commit the changes
             db.session.commit()
        except IntegrityError:
             db.session.rollback()
        return redirect("/posts") # redirect to the same page
    else:
        # query the entries from the db Posts and order them by author
        all_posts = Posts.query.order_by(Posts.id).all()
        # if we are not posting
        # we just read from the database
        # send the query result to the front end
        return render_template("posts.html", posts= all_posts)

# delete the post of the specified id
@app.route("/posts/delete/<int:id>")
def delete(id):
    post = Posts.query.get_or_404(id) # get the post of the id
    db.session.delete(post)
    db.session.commit()
    return redirect("/posts") # redirect to the posts page

@app.route("/posts/edit/<int:id>", methods = ["GET", "POST"])
# edit the post of the specified id
def edit(id):
    post = Posts.query.get_or_404(id) # get the post of the id
    if request.method == "POST":
         post.title = request.form["title"]
         post.content = request.form["content"]
         post.author = request.form["author"]
         db.session.commit()
         return redirect("/posts")
    else:
        return render_template("edit.html", post = post)


@app.route("/posts/new", methods = ["GET", "POST"] )
def new_post():
     if request.method == "POST":
            post_title = request.form["title"]
            post_content = request.form["content"]
            post_author = request.form["author"]
            new_post = Posts(title=post_title, content=post_content, author=post_author)

            try:
                 # add this new post to the database session (current runtime)
                 db.session.add(new_post)
                 # commit the changes
                 db.session.commit()
            except IntegrityError:
                 db.session.rollback()
            return redirect("/posts") # redirect to the same page
     else:
        return render_template("new_post.html") # it will just render an empty form





@app.route("/getOnly", methods=['GET'])
def get_req():
    return "You can only get this webpage"



# if we run this directly from the command line
if __name__=="__main__":
    # we turn on the debug mode
    app.run(debug=True)


