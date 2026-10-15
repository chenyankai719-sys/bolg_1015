from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# 設定 SQLite 資料庫
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


# 定義文章模型 (Model)
class Post(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(100), nullable=False)
  author = db.Column(db.String(50), nullable=False)
  content = db.Column(db.Text, nullable=False)

  def __repr__(self):
    return f"<Post {self.title}>"


# 初始化資料庫
with app.app_context():
  db.create_all()


# 首頁：顯示所有文章列表
@app.route("/")
def index():
  posts = Post.query.all()
  return render_template("index.html", posts=posts)


# 檢視單篇文章
@app.route("/post/<int:post_id>")
def post_detail(post_id):
  post = Post.query.get_or_404(post_id)
  return render_template("post.html", post=post)


# 新增文章
@app.route("/new", methods=["GET", "POST"])
def new_post():
  if request.method == "POST":
    title = request.form["title"]
    author = request.form["author"]
    content = request.form["content"]

    new_article = Post(title=title, author=author, content=content)
    db.session.add(new_article)
    db.session.commit()
    return redirect(url_for("index"))

  return render_template("new_post.html")


if __name__ == "__main__":
  app.run(debug=True)
  