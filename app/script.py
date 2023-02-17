from datetime import datetime

from sqlalchemy import create_engine

from models import User, Picture, Auction, Log

engine = create_engine('postgresql://test_user:1111@localhost/picture_gallery')


def get_user(log):
    print("SELECT id, login, password FROM users WHERE login = '{}';".format(log))
    with engine.connect() as con:
        user = con.execute("SELECT id, login, password FROM users WHERE login = '{}';".format(log)).fetchall()
        print(user)
        if len(user) == 0:
            return None
        us = User(id=user[0][0],
                  login=user[0][1],
                  password=user[0][2])
    # user = cursor.execute("SELECT id, login, password FROM users WHERE login = '{}';".format(log))
        return us


def add_user(cursor, con, us):
    ss = """INSERT INTO users (login, name_user, email, surname, password) 
                   VALUES ('{}', '{}', '{}', '{}', '{}')"""
    cursor.execute(ss.format(us.login, us.name_user, us.email, us.surname, us.password))
    con.commit()


def get_picture():
    with engine.connect() as con:
        picture = con.execute('SELECT id, name_pick, path_pick FROM pictures').fetchall()
        pictures = []
        for row in picture:
            pick = Picture(id=row[0],
                           name_pick=row[1],
                           path_pick=row[2])
            pictures.append(pick)
        return picture


def get_auction():
    with engine.connect() as con:
        auction = con.execute('SELECT id, date_of_action  FROM auctions WHERE status_apll = True').fetchall()
        auctions = []
        for row in auction:
            auc = Auction(id=row[0],
                          date_of_action=row[1])
            auctions.append(auc)
        print(auctions)
        return auctions


def add_pick(cursor, con, pick):
    cursor.execute(f'INSERT INTO pictures(auth_id, name_pick, genre, date_of_create, path_pick) '
                   f'VALUES ({pick.auth_id}, {pick.name_pick}, {pick.genre}, {pick.date_of_create}, {pick.path_pick});')
    con.commit()


def add_auction(cur, con, new_auc):
    cur.execute(f'INSERT INTO auctions (actioneer_id, date_of_action) '
                f'VALUES ({new_auc.actionner_id}, {new_auc.date_of_action})')
    con.commit()


def is_admin(id):
    with engine.connect() as con:
        user = con.execute(f"SELECT * FROM administrators WHERE user_id = {id}").fetchall()
        if len(user) == 0:
            return None
        return user


def is_rev(id):
    with engine.connect() as con:
        user = con.execute(f"SELECT * FROM reviewers WHERE user_id = {id}").fetchall()
        if len(user) == 0:
            return None
        return user


def is_author(id):
    with engine.connect() as con:
        user = con.execute(f"SELECT * FROM authors WHERE user_id = {id}").fetchall()
        if len(user) == 0:
            return None
        return user


def is_actionner(id):
    with engine.connect() as con:
        user = con.execute(f"SELECT * FROM actioneers WHERE user_id = {id}").fetchall()
        if len(user) == 0:
            return None
        return user


def is_owner(id):
    with engine.connect() as con:
        user = con.execute(f"SELECT * FROM owners WHERE user_id = {id}").fetchall()
        if len(user) == 0:
            return None
        return user


def get_picture_id(id):
    with engine.connect() as con:
        picture = con.execute(f"WITH rev_pick as( SELECT message, pick_id, date_of_review, rev_id, education "
                              f"FROM reviews "
                              f"NATURAL RIGHT JOIN reviewers WHERE reviews.pick_id = {id} "
                              f"and reviews.rev_id = reviewers.user_id ), "
                              f" rev_user AS (SELECT name_user, surname, pick_id, message, date_of_review, rev_id, "
                              f"education FROM "
                              f"users JOIN rev_pick on users.id = rev_pick.rev_id),"
                              f" auth_pick AS ( SELECT pictures.id, auth_id, owner_id, cost_pick, name_pick, "
                              f"date_of_create, path_pick, date_of_birth, education FROM "
                              f"pictures NATURAL JOIN authors WHERE pictures.id={id} and auth_id=authors.user_id),"
                              f" all_pick AS (SELECT * FROM auth_pick full join rev_user"
                              f" on auth_pick.id = rev_user.pick_id)"
                              f"SELECT * FROM all_pick;").fetchall()
        picture = picture[0]
        print(picture)
        #picture = con.execute(f"SELECT * FROM pictures WHERE id = {id}")
    return picture


def add_rev(cur, con, pick_id, rev_id, message):
    cur.execute("INSERT INTO reviews (rev_id, pick_id, message, date_of_review) VALUES ({}, {}, '{}', '{}');".format(rev_id, pick_id, message, datetime.now()))
    con.commit()


def get_pick_author(cur, author_id):
    pic = cur.execute(f"SELECT id, name_pick FROM pictures WHERE auth_id = {author_id} and owner_id = NULL")
    return pic


def add_auction_pick(cur, con, pick_id, auction_id):
    cur.execute(f"INSERT INTO auction_pictures (auction_id, pick_id) VALUES ({auction_id}, {pick_id});")
    con.commit()


def add_app(cur, con, id, var):
    con.commit()
    cur.execute("INSERT INTO applications (user_id, variant_request) VALUES ({}, '{}')".format(id, var))
    con.commit()


def get_logs():
    with engine.connect() as con:
        log = con.execute('SELECT * FROM logs').fetchall()
        logs = []
        for row in log:
            pick = Log(id=row[0],
                           user_id=row[1],
                           description=row[2],
                       added=row[3])
            logs.append(pick)
        return logs


def add_owner_to_auction(cursor, con, auction_id, owner_id):
    cursor.execute(f"INSERT INTO auction_buyers (auction_id, owner_id) VALUES ({auction_id}, {owner_id});")
    con.commit()


def get_app():
    with engine.connect() as con:
        apps = con.execute('SELECT applications.id, variant_request, users.login, users.email '
                           'FROM applications join users on applications.user_id = users.id and admin_id is null').fetchall()
        print(apps)
        return apps


def get_ac_app():
    with engine.connect() as con:
        apps = con.execute('SELECT application_auction.id, date_of_action, auction_id FROM application_auction '
                           ' JOIN auctions on admin_id is NULL and auction_id = auctions.id;').fetchall()
        print(apps)
        return apps


def update_app(cur, con, admin_id, ap_id):
    print(ap_id)
    cur.execute(f"UPDATE applications SET admin_id = {admin_id} WHERE id = {ap_id};")
    con.commit()


def update_app_auc(cur, con, admin_id, ap_id):
    cur.execute(f"UPDATE application_auction SET admin_id = {admin_id} WHERE id = {ap_id};")
    con.commit()


def get_my_app(admin_id):
    with engine.connect() as con:
        apps = con.execute('SELECT applications.id, variant_request, users.login, users.email '
                           f'FROM applications natural inner join WHERE admin_id = {admin_id} and user_id = users.id;').fetchall()
        return apps


def get_my_app_ac(admin_id):
    with engine.connect() as con:
        apps = con.execute(f'SELECT application_auction.id, date_of_action, auction_id FROM application_auction '
                           f'NATURAL INNER JOIN auctions WHERE admin_id = {admin_id} and auction_id = auctions.id;').fetchall()
        return apps


def update_app_2(cur, con, ap_id):
    cur.execute(f"UPDATE applications SET status = True WHERE id = {ap_id};")
    con.commit()


def update_app_ac_2(cur, con, ap_id):
    cur.execute(f"UPDATE application_auction SET admin_id = True WHERE id = {ap_id};")
    con.commit()


def get_picture_author(auth_id):
    with engine.connect() as con:
        picture = con.execute('SELECT id, name_pick, path_pick FROM pictures WHERE auth_id ={} and owner_id = NULL'.format(auth_id)).fetchall()
        pictures = []
        for row in picture:
            pick = Picture(id=row[0],
                           name_pick=row[1],
                           path_pick=row[2])
            pictures.append(pick)
        return picture
