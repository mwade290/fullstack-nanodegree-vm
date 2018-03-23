from flask import Flask, render_template, request, redirect, jsonify, url_for, make_response, flash
from flask import session as login_session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import sys
import random
import string
import httplib2
import json
import requests
sys.path.insert(0, 'Modules')
from database_setup import Base, Country, Highlight

app = Flask(__name__)
app.secret_key = 'super_secret_key'

CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog App"

engine = create_engine('sqlite:///countries.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Login
@app.route('/login')
def showLogin():
	state = ''.join(random.choice(string.ascii_uppercase + string.digits)
					for x in xrange(32))
	login_session['state'] = state
	countries = session.query(Country).order_by(Country.name).all()
	return render_template('login.html', countries=countries, STATE=state)

# Logout
@app.route('/logout')
def disconnect():
	if 'username' in login_session:
		gdisconnect()
		flash("Log out successful")
	else:
		flash("You were not logged in.")
	return redirect(url_for('countries'))


@app.route('/gconnect', methods=['POST'])
def gconnect():
	# Validate state token
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
		response = make_response(json.dumps('Failed to upgrade the authorization code.'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response

	# Check that the access token is valid.
	access_token = credentials.access_token
	url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
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
		response = make_response(json.dumps("Token's user ID doesn't match given user ID."), 401)
		response.headers['Content-Type'] = 'application/json'
		return response

	# Verify that the access token is valid for this app.
	if result['issued_to'] != CLIENT_ID:
		response = make_response(json.dumps("Token's client ID does not match app's."), 401)
		print("Token's client ID does not match app's.")
		response.headers['Content-Type'] = 'application/json'
		return response

	stored_access_token = login_session.get('access_token')
	stored_gplus_id = login_session.get('gplus_id')
	if stored_access_token is not None and gplus_id == stored_gplus_id:
		response = make_response(json.dumps('Current user is already connected.'),
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

	output = ''
	output += '<h1>Welcome, '
	output += login_session['username']
	output += '!</h1>'
	#output += '<img src="'
	#output += login_session['picture']
	#output += ' " style = "width: 300px; height: 300px;border-radius:
	#150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
	flash("you are now logged in as %s" % login_session['username'])
	print("done!")
	return output

	# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect', methods=['POST'])
def gdisconnect():
	access_token = login_session.get('access_token')
	if access_token is None:
		print('Access Token is None')
		response = make_response(json.dumps('Current user not connected.'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response
	print('In gdisconnect access token is %s'), access_token
	print('User name is: ')
	print(login_session['username'])
	url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
	h = httplib2.Http()
	result = h.request(url, 'GET')[0]
	print('result is ')
	print(result)
	if result['status'] == '200':
		del login_session['access_token']
		del login_session['gplus_id']
		del login_session['username']
		del login_session['email']
		del login_session['picture']
		response = make_response(json.dumps('Successfully disconnected.'), 200)
		response.headers['Content-Type'] = 'application/json'
		flash("Successfully disconnected.")
		return response
	else:
		response = make_response(json.dumps('Failed to revoke token for given user. %s' % result['status'], 400))
		response.headers['Content-Type'] = 'application/json'
		return response

# Show all countries in serialised format
@app.route('/JSON')
@app.route('/countries/JSON')
def countriesJSON():
	countries = session.query(Country).order_by(Country.name).all()
	return jsonify(countries=[c.serialize for c in countries])
	
# Show all countries
@app.route('/')
@app.route('/countries')
def countries():
	countries = session.query(Country).order_by(Country.name).all()
	highlights = session.query(Highlight).all()
	return render_template('countries.html', countries=countries, highlights=highlights, session=login_session)

# Show all country highlights in serialised format
@app.route('/countries/<country_name>/highlights/JSON')
def countryHighlightsJSON(country_name):
	country = session.query(Country).filter_by(name=country_name).first()
	highlights = session.query(Highlight).filter_by(country_id=country.id).all()
	return jsonify(highlights=[h.serialize for h in highlights])

# Show all country highlights
@app.route('/countries/<country_name>/highlights')
def countryHighlights(country_name):
	countries = session.query(Country).order_by(Country.name).all()
	country = session.query(Country).filter_by(name=country_name).first()
	highlights = session.query(Highlight).filter_by(country_id=country.id).all()
	return render_template('countryHighlights.html', countries=countries, highlights=highlights, country=country)
	
# Add new country
@app.route('/countries/add', 
		   methods=['GET', 'POST'])
def addNewCountry():
	if request.method == 'POST':
		newName = request.form['name']
		message = addCountryConditions(newName)
		if (message == ''):
			country = Country(name=newName)
			session.add(country)
			session.commit()
			return redirect(url_for('countryHighlights', country_name=country.name))
		else:
			return error(message)
	else:
		countries = session.query(Country).order_by(Country.name).all()
		return render_template('addNewCountry.html', countries=countries)
		
# Delete country
@app.route('/countries/<country_name>/delete', 
		   methods=['GET', 'POST'])
def deleteCountry(country_name):
	country = session.query(Country).filter_by(name=country_name).first()
	if country > 0:
		if request.method == 'POST':
			highlights = session.query(Highlight).filter_by(country_id=country.id).all()
			for highlight in highlights:
				session.delete(highlight)
			session.delete(country)
			session.commit()
			return redirect(url_for('countries'))
		else:
			countries = session.query(Country).order_by(Country.name).all()
			return render_template('deleteCountry.html', countries=countries, country=country)
	else:
		return error('Unable to find entry in database.')
		
# Perform checks to ensure country name integrity
def addCountryConditions(name):
	exists = session.query(Country.id).filter_by(name=name).scalar() is not None
	if (exists):
		return 'Country name already exists.'
	elif (name == ''):
		return 'Country name cannot be blank.'
	else:
		return ''
	
# Show country highlight description in serialised format
@app.route('/countries/<country_name>/highlights/<highlight_name>/description/JSON')
def highlightDescriptionJSON(country_name, highlight_name):
	country = session.query(Country).filter_by(name=country_name).first()
	highlight = session.query(Highlight).filter_by(country_id=country.id,
		name=highlight_name).first()
	if country > 0 and highlight > 0:
		countries = session.query(Country).order_by(Country.name).all()
		return jsonify(highlight=highlight.serialize)
	else:
		return error('Unable to find entry in database.')

# Show description for highlight
@app.route('/countries/<country_name>/highlights/<highlight_name>/description')
def highlightDescription(country_name, highlight_name):
	country = session.query(Country).filter_by(name=country_name).first()
	highlight = session.query(Highlight).filter_by(country_id=country.id,
		name=highlight_name).first()
	if country > 0 and highlight > 0:
		countries = session.query(Country).order_by(Country.name).all()
		return render_template('highlightDescription.html', countries=countries, highlight=highlight, country=country)
	else:
		return error('Unable to find entry in database.')
		
# Add new highlight
@app.route('/countries/<country_name>/highlights/add', 
		   methods=['GET', 'POST'])
def addNewHighlight(country_name):
	country = session.query(Country).filter_by(name=country_name).first()
	if country > 0:
		if request.method == 'POST':
			newName = request.form['name']
			message = addHighlightConditions(country, newName, False)
			if (message == ''):
				highlight = Highlight(name=newName,
					description=request.form['description'],
					country_id=country.id)
				session.add(highlight)
				session.commit()
				return redirect(url_for('countryHighlights', country_name=country.name))
			else:
				return error(message)
		else:
			countries = session.query(Country).order_by(Country.name).all()
			return render_template('addNewHighlight.html', countries=countries, country=country)
	else:
		return error('Unable to find Country in database.')

# Perform checks to ensure highlight name integrity
def addHighlightConditions(country, name, edit):
	exists = session.query(Highlight).filter_by(country_id=country.id,
		name=name).scalar() is not None
	if (exists and not edit):
		return 'Highlight name already exists.'
	elif (name == ''):
		return 'Highlight name cannot be blank.'
	else:
		return ''
		
# Edit highlight description
@app.route('/countries/<country_name>/highlights/<highlight_name>/description/edit',
		   methods=['GET', 'POST'])
def editHighlightDescription(country_name, highlight_name):
	country = session.query(Country).filter_by(name=country_name).first()
	highlight = session.query(Highlight).filter_by(country_id=country.id,
		name=highlight_name).first()
	if country > 0 and highlight > 0:
		if request.method == 'POST':
			newName = request.form['name']
			message = addHighlightConditions(country, newName, True)
			if (message == ''):
				highlight.name = request.form['name']
				highlight.description = request.form['description']
				session.add(highlight)
				session.commit()
				return redirect(url_for('highlightDescription', highlight_name=highlight.name, country_name=country.name))
			else:
				return error(message)
		else:
			countries = session.query(Country).order_by(Country.name).all()
			return render_template('editHighlightDescription.html', countries=countries, highlight=highlight, country=country)
	else:
		return error('Unable to find entry in database.')
		
# Delete highlight description
@app.route('/countries/<country_name>/highlights/<highlight_name>/description/delete',
		   methods=['GET', 'POST'])
def deleteHighlightDescription(country_name, highlight_name):
	country = session.query(Country).filter_by(name=country_name).first()
	highlight = session.query(Highlight).filter_by(country_id=country.id,
		name=highlight_name).first()
	if country > 0 and highlight > 0:
		if request.method == 'POST':
			session.delete(highlight)
			session.commit()
			count = session.query(Highlight).filter_by(country_id=country.id).count()
			if count < 1:
				session.delete(country)
			return redirect(url_for('countries'))
		else:
			countries = session.query(Country).order_by(Country.name).all()
			return render_template('deleteHighlightDescription.html', countries=countries, highlight=highlight, country=country)
	else:
		return error('Unable to find entry in database.')

@app.route('/error')		
def error(message):
	countries = session.query(Country).order_by(Country.name).all()
	return render_template('error.html', countries=countries, message=message)
	
if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port=8000)