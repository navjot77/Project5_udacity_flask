# This is server file that renders html pages and do operation on Database.
from flask import Flask, render_template,request,redirect,jsonify,url_for,flash
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests
import traceback


app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Item Menu Application"

# Connect to Database and create database session
engine = create_engine('sqlite:///itemCatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''
    for x in xrange(32):
        state = state + (random.choice(string.digits + string.letters))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/')
@app.route('/catalog')
def showCatalog():
    # This function renderes the main page for App. Sends Catalog and items
    # from database to html.
    catalog = session.query(Category).order_by(asc(Category.name)).all()
    items = session.query(Item).order_by(Item.time_modified.desc()).all()
    return render_template('catalog.html', catalog=catalog, items=items)


@app.route('/catalog/category/json')
def categoryJSON():
    # This function generates the JSON file for Catalog entries from Database.
    if 'username' in login_session:
        catalog = session.query(Category).order_by(asc(Category.name)).all()
        return jsonify(Category=[r.serialize for r in catalog])
    else:
        flash("Kindly LogIn to access the items.")
        return redirect(url_for('showCatalog'))


@app.route('/catalog/users/json')
def usersJSON():
    # This function generates the JSON file for Users entries from Database.
    if 'username' in login_session:
        catalog = session.query(User).order_by(asc(User.name)).all()
        return jsonify(Users=[r.serialize for r in catalog])
    else:
        flash("Kindly LogIn to access the items.")
        return redirect(url_for('showCatalog'))


@app.route('/catalog/category/<int:catalog_id>/items/json')
def itemsJSON(catalog_id):
    # This function generates the JSON file for ITEMS from Database.
    if 'username' in login_session:
        items = session.query(Item).filter_by(category_id=catalog_id).all()
        return jsonify(Category=[r.serialize for r in items])
    else:
        flash("Kindly LogIn to access the items.")
        return redirect(url_for('showCatalog'))


@app.route('/catalog/<int:catalog_id>')
@app.route('/catalog/<int:catalog_id>/items/')
def showItems(catalog_id):
    # This function firstly checks whether User is logged In, if yes then
    # this will get Items requested from Database and will pass that as
    # parameter to catalog.html
    # Parameters: catalog_id -> The catalog for which items are to fetched.
    if 'username' in login_session:
        catalog = session.query(Category).order_by(asc(Category.name)).all()

        items = session.query(Item).filter_by(category_id=catalog_id).all()
        return render_template('catalog.html', catalog=catalog,
                               items=items, no_show=True)
    else:
        flash("Kindly LogIn to access the items.")
        return redirect(url_for('showCatalog'))


@app.route('/catalog/<int:catalog_id>/item/<int:item_id>')
def showItem(catalog_id, item_id):
    # This function firstly checks whether User is logged In, if yes then
    # this will get Item requested from Database and will render item.html
    # Parameters: item_id -> The item which is to be fetched.
    # session.rollback()
    if 'username' not in login_session:
        flash("Kindly LogIn to access the items.")
        return redirect(url_for('showCatalog'))

    item = session.query(Item).filter_by(id=item_id).one()
    return render_template('item.html', item=item)


@app.route('/catalog/newItem', methods=['GET', 'POST'])
def newCatalogItem():
    # This function firstly checks whether User is logged In, if yes then
    # this will receive POST request and create a new entry for Item in
    # database. If this function gets GET request, then renders page for
    # adding new item.

    if 'username' not in login_session:
        flash("Kindly LogIn to access the items.")
        return redirect(url_for('showCatalog'))

    if request.method == 'POST':
        newItem = Item(
            name=request.form['name'],
            price=request.form['price'],
            description=request.form['description'],
            category=session.query(Category).filter_by(
                name=request.form['category']).one(),
            user_id=login_session['user_id']
        )
        session.add(newItem)
        session.commit()
        return redirect(url_for('showCatalog'))
    else:
        catalog = session.query(Category).all()
        return render_template('addItem.html', category=catalog)


@app.route('/catalog/edit/<int:item_id>', methods=['GET', 'POST'])
def editItem(item_id):
    # This function firstly checks whether User is logged In, if yes then
    # this will receive POST request edit an existing entry for Item in
    # database. If this function gets GET request, then renders page for
    # edit item.
    if 'username' not in login_session:
        flash("Kindly LogIn to access the items.")
        return redirect(url_for('showCatalog'))

    if request.method == 'POST':
        print "Inside EditItem PoST"
        item = session.query(Item).filter_by(
            id=(request.form['item_id'])).one()
        item.name = request.form['name']
        item.price = request.form['price']
        item.description = request.form['description']
        item.category = session.query(Category).filter_by(
            name=request.form['category']).one()
        item.user_id = login_session['user_id']
        session.add(item)
        session.commit()
        return redirect(url_for('showCatalog'))
    else:
        catalog = session.query(Category).all()
        item = session.query(Item).filter_by(id=item_id).one()
        return render_template('editItem.html', item=item, category=catalog)


@app.route('/catalog/delete/<int:item_id>', methods=['GET', 'POST'])
def deleteItem(item_id):
    # This function firstly checks whether User is logged In, if yes then
    # this will receive POST request and  deletes entry for Item in
    # database. If this function gets GET request, then renders confirmation
    # page to confirm for deletion of item.
    if 'username' not in login_session:
        flash("Kindly LogIn to access the items.")
        return redirect(url_for('showCatalog'))

    if request.method == 'POST':
        print "Inside deleetItem POST"
        item = session.query(Item).filter_by(id=request.form['item_id']).one()
        session.delete(item)
        session.commit()
        return redirect(url_for('showCatalog'))
    else:
        item = session.query(Item).filter_by(id=item_id).one()
        return render_template('deleteItem.html', item=item)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # This function gets called when user uses Google for sign In.
    # Validate state token first followed by validation of access token.
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response
        (json.dumps('Current user is already connected.'),
         200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    user_id = getUserID(login_session['email'])
    print "Got user id is%s" % user_id
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id
    login_session['provider'] = 'google'
    print login_session['user_id']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


def createUser(login_session):
    # If user's email id is not in database then a new entry is added to User
    #table.
    print "Inside create user"
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    # This function return User Id if corresponding email is found in database.
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# DISCONNECT - Revoke a current user's token and reset their login_session

@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session['access_token']
    print 'In gdisconnect access token is %s', access_token

    if access_token is None:
        print 'Access Token is None'
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url ='https://accounts.google.com/o/oauth2/revoke?token=%s'% login_session[
        'access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result:
        del login_session['access_token']
        del login_session['gplus_id']
        if 'username' in login_session:
            del login_session['username']
        del login_session['email']
        del login_session['picture']
        if 'user_id' in login_session:
            del login_session['user_id']
      #  del login_session['credentials']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:

        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content   -Type'] = 'application/json'
        return response


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token

    app_id = json.loads(open('fbClientSecrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fbClientSecrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=' \
          'fb_exchange_token&client_id=%s&client_secret=' \
          '%s&fb_exchange_token=%s'\
          % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.4/me"
    # strip expire tag from access token
    token = result.split("&")[0]

    url = 'https://graph.facebook.com/v2.4/me?%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly
    # logout, let's strip out the information before the equals sign in our
    # token
    stored_token = token.split("=")[1]
    login_session['access_token'] = stored_token

    # Get user picture
    url = 'https://graph.facebook.com/v2.4/me/picture?%s&redirect=0&height=' \
          '200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # check if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        print "creating new user"
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;"> '

    flash("Now logged in as %s" % login_session['username'])
    return output


@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (
        facebook_id, access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    del login_session['facebook_id']
    if 'user_id' in login_session:
        del login_session['user_id']
    if 'username' in login_session:
        del login_session['username']
    del login_session['email']
    del login_session['picture']
    del login_session['access_token']

    return "you have been logged out"


# Disconnect based on provider
@app.route('/disconnect')
def disconnect():
    # This function called when user wishes to log out.
    # Firstly, the provider in login_session is checked to see whether user is
    # logged in or not, and if Logged-In then it check the provider and calls
    # particular function.
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
        if login_session['provider'] == 'facebook':
            fbdisconnect()

        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('showCatalog'))
    else:
        flash("You are not logged in")
        return redirect(url_for('showCatalog'))


if __name__ == '__main__':
    app.secret_key = 'Mines'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
