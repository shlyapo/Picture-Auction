import os
import random

import psycopg2
import tinify as tinify
from flask import render_template, session, redirect, url_for, request
from flask.views import MethodView, View
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from forms import RegisterForm, LoginForm, PictureForm, AuctionForm, RevForm, ApplicationForm, AppDetails, OwnerForm
from models import User, Picture, Auction, MyEnum
from script import get_picture, get_user, add_user, get_auction, add_pick, add_auction, get_picture_id, \
    add_rev, add_auction_pick, add_app, get_logs, get_pick_author, add_owner_to_auction, is_admin, is_author, \
    is_actionner, is_rev, update_app, get_app, get_ac_app, update_app_auc, get_my_app, get_my_app_ac, \
    update_app_2, update_app_ac_2, get_picture_author, is_owner


def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='picture_gallery',
                            user='test_user',
                            password='1111')
    return conn


class IndexStart(MethodView):
    def get(self):
        return render_template('index_start.html',
                               title='Home')


class IndexUser(MethodView):
    def get(self):
        return render_template('index.html',
                               title='Home')


class IndexAuthor(MethodView):
    def get(self):
        return render_template('author/index_author.html',
                               title='Home')


class IndexAct(MethodView):
    def get(self):
        return render_template('index_act.html')


class IndexAdmin(MethodView):
    def get(self):
        return render_template('admin/index_admin.html')


class IndexOwner(MethodView):
    def get(self):
        return render_template('owner/index.html')


class Register(MethodView):

    def get(self):

        registration_form = RegisterForm()
        return render_template('register.html',
                               registration_form=registration_form)

    def post(self):

        registration_form = RegisterForm()

        if registration_form.validate_on_submit():
            cur_user = get_user(registration_form.login.data)
            if cur_user is None:
                con = get_db_connection()
                cur = con.cursor()
                new_user = User(name_user=registration_form.name_user.data,
                                surname=registration_form.surname.data,
                                email=registration_form.email.data,
                                login=registration_form.login.data,
                                password=registration_form.password.data)
                add_user(cur, con, new_user)
        return redirect(url_for('index_start'))


class Login(MethodView):

    def get(self):

        if session.get('login'):
            return redirect(url_for('index'))

        login_form = LoginForm()
        return render_template('login.html',
                               title='Login',
                               login_form=login_form,
                               session=session.get('login'))

    def post(self):

        login_form = LoginForm()

        if login_form.validate_on_submit():
            con = get_db_connection()
            cur = con.cursor()
            print(login_form.login.data)
            user = get_user(login_form.login.data)
            print(user)
            if user is None:
                return redirect(url_for('login'))
            elif user.password == login_form.password.data:

                session['login'] = user.login
                if is_admin(user.id) is not None:
                    return redirect(url_for('index_admin'))
                elif is_author(user.id) is not None:
                    return redirect(url_for('index_author'))
                elif is_actionner(user.id) is not None:
                    return redirect(url_for('actioneer/index_act'))
                elif is_owner(user.id) is not None:
                    return redirect(url_for('index_owner'))
                else:
                    return redirect(url_for('index'))
            else:
                return redirect(url_for('login'))


class Logout(MethodView):

    def get(self):
        session.pop('login', None)
        return redirect(url_for('index_start'))


class PictureView(View):
    def dispatch_request(self):
        pictures = get_picture()
        return render_template("pictures.html", objects=pictures)


class PictureAuthor(MethodView):
    def get(self):
        current_user = get_user(session.get("login"))
        pictures = get_picture_author(current_user.id)
        return render_template("author/add_pick_auction.html", pictures=pictures)

    def post(self):
        con = get_db_connection()
        cur = con.cursor()
        current_user = get_user(session.get("login"))
        update_app(cur, con, current_user.id)

        return redirect(url_for('apps'))


class AddPictureToAuction(MethodView):
    def get(self, pick_id):
        con = get_db_connection()
        cur = con.cursor()
        current_user = get_user(session.get("login"))
        auction = get_auction()
        auction_id = random.randint(auction[0][0], auction[-1][0])
        add_auction_pick(cur, con, pick_id, auction_id)
        return render_template("admin/add_succesful.html")


class PicturesRev(View):
    def dispatch_request(self):
        pictures = get_picture()
        return render_template("reviewer/pictures.html", pictures=pictures)


class PictureAdmin(View):
    def dispatch_request(self):
        pictures = get_picture()
        return render_template("admin/adminpictures.html", pictures=pictures)


class PictureAct(View):
    def dispatch_request(self):
        con = get_db_connection()
        cur = con.cursor()
        pictures = get_picture()
        return render_template("actpictures.html", pictures=pictures)


class AuctionView(View):
    def dispatch_request(self):
        auctions = get_auction()
        return render_template("auctions.html", auctions=auctions)


class AuctionAuthor(View):
    def dispatch_request(self):
        auctions = get_auction()
        return render_template("author_auctions.html", auctions=auctions)


class AuctionAdmin(View):
    def dispatch_request(self):
        auctions = get_auction()
        return render_template("auctions_admin.html", auctions=auctions)


class AuctionAct(View):
    def dispatch_request(self):
        auctions = get_auction()
        return render_template("auctions_act.html", auctions=auctions)


class AddPicture(MethodView):
    def get(self):
        picture_form = PictureForm()

        return render_template('author/create_picture.html',
                               title='Create Picture',
                               picture_form=picture_form)

    def post(self):

        picture_form = PictureForm()
        if picture_form.validate():
            con = get_db_connection()
            cur = con.cursor()
            current_user = get_user(session.get('login'))
            myFile = secure_filename(picture_form.picture_image.file.filename)
            picture_form.picture_image.file.save("./static/images/" + myFile)

            new_pick = Picture(auth_id=current_user.id,
                               name_pick=picture_form.name_pick.data,
                               genre=picture_form.genre.data,
                               date_of_create=picture_form.date_of_create.data,
                               path_pick=f"static/images/{myFile}")
            add_pick(cur, con, new_pick)
            return redirect(url_for('index_author'))
        else:
            print(picture_form.data)
            return redirect(url_for('add_pick'))


class AddAuction(MethodView):
    def get(self):
        auction_form = AuctionForm()

        return render_template('create_auction.html',
                               title='Create Auction',
                               auction_form=auction_form)

    def post(self):
        con = get_db_connection()
        cur = con.cursor()
        auction_form = AuctionForm()
        if auction_form.validate_on_submit():
            current_user = get_user(session.get("login"))
            new_auction = Auction(actioneer_id=current_user.id,
                                  date_of_action=auction_form.date_of_action.data)
            add_auction(cur, con, new_auction)

            return redirect(url_for('auctions_act'))
        else:
            return redirect(url_for('create_auction'))


class PictureRev(MethodView):
    def get(self, picture_id):
        rev_form = RevForm()
        picture = get_picture_id(picture_id)

        return render_template('picture_rev.html',
                               title='Picture',
                               rev_form=rev_form,
                               pick=picture)

    def post(self, picture_id):
        rev_form = RevForm()
        con = get_db_connection()
        cur = con.cursor()
        if rev_form.validate_on_submit():
            current_user = get_user(session.get("login"))
            message = rev_form.message.data
            add_rev(cur, con, picture_id, current_user.id, message)
            return redirect(url_for('picture_rev',
                                    picture_id=picture_id))
        else:
            return redirect(url_for('picture_rev'))


class PictureDetails(MethodView):
    def get(self, picture_id):
        con = get_db_connection()
        cur = con.cursor()
        picture = get_picture_id(picture_id)

        return render_template('picture.html',
                               title='Picture',
                               pick=picture)

    def post(self, picture_id):
        rev_form = RevForm()
        con = get_db_connection()
        cur = con.cursor()
        current_user = get_user(session.get("login"))
        if is_rev(current_user.id) is not None:
            if rev_form.validate_on_submit():
                picture = get_picture_id(picture_id)
                message = rev_form.message.data
                add_rev(cur, con, picture.pick_id, current_user.id, message)
                return redirect(url_for('picture',
                                    picture_id=picture.pick_id))
            else:
                return redirect(url_for('picture_rev'))
        else:
            con = get_db_connection()
            cur = con.cursor()
            picture = get_picture_id(cur, picture_id)
            return redirect(url_for('article', picture=picture.pick_id))


"""class AuctionDetails(MethodView):
    def get(self, article_id):

        article = Article.query.filter_by(id=article_id).first()

        if article is None:
            return redirect(url_for('index'))

        user = User.query.filter_by(id=article.user_id).first()
        article.views += 1
        db.session.commit()

        offers_by_article = Offer.query.filter_by(article_id=article.id).order_by(Offer.price.desc()).limit(3).all()
        top_users = []
        if offers_by_article is not None:
            for offer in offers_by_article:
                top_users.append(User.query.filter_by(id=offer.user_id).first())

        session_username = session.get('username')
        if user.username == session_username:
            session_username = None

        return render_template('article.html',
                               title='Article | Aukcije Online',
                               article=article,
                               user=user,
                               offers_by_article=offers_by_article,
                               top_users=top_users,
                               session=session_username)

    def post(self, article_id):

        article = Article.query.filter_by(id=article_id).first()

        try:
            expected_value = int(request.form['new_price'])
            if expected_value < article.minimal_price:
                raise ValueError
        except ValueError:
            flash("Price lower than expected")
            return redirect(url_for('article', article_id=article_id))
        except Exception:
            flash("Invalid price")
            return redirect(url_for('article', article_id=article_id))

        us = User.query.filter_by(username=session.get('username')).first()
        new_offer = Offer(article_id=article.id,
                          user_id=us.id,
                          price=request.form['new_price'])
        db.session.add(new_offer)
        db.session.commit()
        return redirect(url_for('article', article_id=article_id))"""


class OwnerAuction(MethodView):
    def get(self):
        form = OwnerForm()
        auctions = get_auction()
        list_ac = [(i.id, i.date_of_action) for i in auctions]
        form.variant.choices = list_ac
        return render_template('owner/owner_auction.html',
                               title='Owner Auction',
                               form=form)

    def post(self):
        con = get_db_connection()
        cur = con.cursor()
        form = OwnerForm()
        if form.validate_on_submit():
            current_user = get_user(session.get("login"))
            add_owner_to_auction(cur, con, form.variant.id, current_user.id)
            return redirect(url_for('index'))
        else:
            return redirect(url_for('owner_auction'))


"""class OwnerNowAuction(MethodView):
    def get(self, auction_id):
        return render_template('owner_auction.html',
                               title='Owner Auction',
                               auction_id=auction_id)

    def post(self, auction_id):
        con = get_db_connection()
        cur = con.cursor()
        current_user = get_user(cur, login=session.get("login"))
        add_owner_to_auction(cur, con, auction_id, current_user.id)

        return redirect(url_for('auction',
                                auction_id=auction_id))"""


class AddApp(MethodView):
    def get(self):
        app_from = ApplicationForm()

        return render_template('send_app.html',
                               title='Application',
                               form=app_from)

    def post(self):

        app_form = ApplicationForm()
        con = get_db_connection()
        cur = con.cursor()
        if app_form.validate_on_submit():

            current_user = get_user(session.get("login"))
            if not current_user.role:
                var = ''
                if app_form.variant.data == 0:
                    var = MyEnum.one.value
                if app_form.variant.data == 1:
                    var = MyEnum.two.value
                if app_form.variant.data == 2:
                    var = MyEnum.three.value
                if app_form.variant.data == 3:
                    var = MyEnum.four.value
                add_app(cur, con, current_user.id, var)
                return redirect(url_for('index'))
            else:
                return redirect(url_for('wrong_app'))
        else:
            return redirect(url_for('send_app'))


class LogsView(MethodView):
    def dispatch_request(self):
        logs = get_logs()
        return render_template("admin/logs.html", logs=logs)

# доделать тоже самое сделать что и с appview
class AppView(MethodView):
    def get(self):
        ap = get_app()
        return render_template("admin/apps.html", apps=ap)

    def post(self, app_id):
        con = get_db_connection()
        cur = con.cursor()
        current_user = get_user(session.get("login"))
        update_app(cur, con, current_user.id, app_id)

        return redirect(url_for('apps'))


class AppAddAdmin(MethodView):
    def get(self, app_id):
        con = get_db_connection()
        cur = con.cursor()
        current_user = get_user(session.get("login"))
        update_app(cur, con, current_user.id, app_id)
        return render_template("admin/add_app.html", app_id=app_id)


class AppAccView(MethodView):
    def get(self):
        app_acc = get_ac_app()
        return render_template("admin/apps_auction.html", apps=app_acc)

    def post(self, app_id):
        con = get_db_connection()
        cur = con.cursor()
        current_user = get_user(session.get("login"))
        update_app_auc(cur, con, current_user.id, app_id)

        return redirect(url_for('apps_auction'))


class AppMy(MethodView):
    def get(self):
        current_user = get_user(session.get("login"))
        logs = get_my_app(current_user.id)
        return render_template("admin/my_apss.html", objects=logs)

    def post(self, app_id):
        con = get_db_connection()
        cur = con.cursor()
        update_app_2(cur, con, app_id)

        return render_template("admin/apps.html")


class AppAuctionMy(MethodView):
    def get(self):
        current_user = get_user(session.get("login"))
        logs = get_my_app_ac(current_user.id)
        return render_template("admin/my_apps_ac.html", objects=logs)

    def post(self, app_id):
        con = get_db_connection()
        cur = con.cursor()
        update_app_ac_2(cur, con, app_id)

        return redirect(url_for('my_apps_ac'))

