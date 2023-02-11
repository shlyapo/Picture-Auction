
import psycopg2
from flask import Flask, render_template
import os
from flask_bootstrap import Bootstrap
from views import IndexStart, Login, Logout, IndexUser, IndexAuthor, IndexAct, IndexAdmin, AuctionView, \
    PictureView, LogsView, PictureAuthor, PictureAdmin, PictureAct, AuctionAuthor, \
    AuctionAdmin, AuctionAct, AddPicture, PictureDetails, AppMy, AppAuctionMy, Register, AppView, AppAccView, AddApp, \
    AppAddAdmin, PictureRev, PicturesRev, AddPictureToAuction, OwnerAuction, IndexOwner

app = Flask(__name__, template_folder='templates')

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='picture_gallery',
                            user=os.environ['test_user'],
                            password=os.environ['1111'])
    return conn


app.add_url_rule('/', view_func=IndexStart.as_view('index_start'))
app.add_url_rule('/login', view_func=Login.as_view('login'))
app.add_url_rule('/register', view_func=Register.as_view('register'))
app.add_url_rule('/logout', view_func=Logout.as_view('logout'))
app.add_url_rule('/index', view_func=IndexUser.as_view('index'))
app.add_url_rule('/index_author', view_func=IndexAuthor.as_view('index_author'))
app.add_url_rule('/index_act', view_func=IndexAct.as_view('index_act'))
app.add_url_rule('/index_admin', view_func=IndexAdmin.as_view('index_admin'))
app.add_url_rule('/author_auctions', view_func=AuctionAuthor.as_view('auctorauctions'))
app.add_url_rule('/admin_auctions', view_func=AuctionAdmin.as_view('adminauctions'))
app.add_url_rule('/act_auctions', view_func=AuctionAct.as_view('actauctions'))
app.add_url_rule('/auctions', view_func=AuctionView.as_view('auctions'))
app.add_url_rule('/pictures', view_func=PictureView.as_view('pictures'))
app.add_url_rule('/owner_auction', view_func=OwnerAuction.as_view('owner_auction'))
app.add_url_rule('/pictures_rev', view_func=PicturesRev.as_view('pictures_rev'))
app.add_url_rule('/pictures/<int:picture_id>', view_func=PictureDetails.as_view('picture'))
app.add_url_rule('/pictures_rev/<int:picture_id>', view_func=PictureRev.as_view('picture_rev'))
app.add_url_rule('/author_pictures', view_func=PictureAuthor.as_view('authorpictures'))
app.add_url_rule('/admin_pictures', view_func=PictureAdmin.as_view('adminpictures'))
app.add_url_rule('/act_pictures', view_func=PictureAct.as_view('actpictures'))
app.add_url_rule('/add_pic', view_func=AddPicture.as_view('add_pick'))
app.add_url_rule('/add_succesful', view_func=AddPictureToAuction.as_view('add_succesful'))
app.add_url_rule('/logs', view_func=LogsView.as_view('logs'))
app.add_url_rule('/apps', view_func=AppView.as_view('apps'))
app.add_url_rule('/apps_auction', view_func=AppAccView.as_view('apps_auction'))
app.add_url_rule('/my_apps', view_func=AppMy.as_view('my_apps'))
app.add_url_rule('/my_apps_ac', view_func=AppAuctionMy.as_view('my_apps_ac'))
app.add_url_rule('/list_apps_auction', view_func=Logout.as_view('list_apps_auction'))
app.add_url_rule('/send_app', view_func=AddApp.as_view('send_app'))
app.add_url_rule('/apps/<int:app_id>', view_func=AppAddAdmin.as_view('add_apps'))
app.add_url_rule('/index_owner', view_func=IndexOwner.as_view('index_owner'))
#app.add_url_rule('/logout', view_func=Logout.as_view('logout'))
#app.add_url_rule('/logout', view_func=Logout.as_view('logout'))
#app.add_url_rule('/logout', view_func=Logout.as_view('logout'))
#app.add_url_rule('/logout', view_func=Logout.as_view('logout'))
#app.add_url_rule('/logout', view_func=Logout.as_view('logout'))
#app.add_url_rule('/logout', view_func=Logout.as_view('logout'))


"""app.add_url_rule('/profile', view_func=Profile.as_view('profile'))
app.add_url_rule('/user/<int:user_id>', view_func=User_.as_view('user'))
app.add_url_rule('/create_article', view_func=CreateArticle.as_view('create_article'))
app.add_url_rule('/article/<int:article_id>', view_func=Article_.as_view('article'))
app.add_url_rule('/search', view_func=Search.as_view('search'))"""

#@app.errorhandler(404)
#ef page_not_found(e):
  #  return render_template('404.html'), 404


#@app.errorhandler(500)
#def internal_server_error(e):
 #   return render_template('500.html'), 500

"""basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgresql://test_user:1111@host:port/picture_gallery'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'hard to guess'
db = SQLAlchemy(app)
login_manager = LoginManager(app)"""

if __name__ == '__main__':
    bootstrap = Bootstrap(app)
    app.run()
