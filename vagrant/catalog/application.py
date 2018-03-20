from flask import Flask, render_template, request, redirect, jsonify, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Country, Highlight

app = Flask(__name__)
app.secret_key = 'super_secret_key'

engine = create_engine('sqlite:///countries.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Show all countries in serialised format
@app.route('/countries/JSON')
def countriesJSON():
	countries = session.query(Country).all()
	return jsonify(countries=[c.serialize for c in countries])
	
# Show all countries
@app.route('/')
@app.route('/countries/', strict_slashes=False)
def countries():
	countries = session.query(Country).all()
	return render_template('countries.html', countries=countries)
	
# Show all country highlights
@app.route('/countries/<country_name>/highlights')
def countryHighlights(country_name):
	country = session.query(Country).filter_by(name=country_name).first()
	highlights = session.query(Highlight).filter_by(
		country_id=country.id).all()
	return render_template('countryHighlights.html', highlights=highlights, country=country)
	
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
			return redirect(url_for('countries'))
		else:
			return error(message)
	else:
		return render_template('addNewCountry.html')
		
# Perform checks to ensure country name integrity
def addCountryConditions(name):
	exists = session.query(Country.id).filter_by(name=name).scalar() is not None
	if (exists):
		return 'Cannot add Country, name already exists.'
	elif (name == ''):
		return 'Cannot add Country, name cannot be blank.'
	else:
		return ''
	
# Show description for highlight
@app.route('/countries/<country_name>/highlights/<highlight_name>/description')
def highlightDescription(country_name, highlight_name):
	country = session.query(Country).filter_by(name=country_name).first()
	highlight = session.query(Highlight).filter_by(country_id=country.id,
		name=highlight_name).first()
	if country > 0 and highlight > 0:
		return render_template('highlightDescription.html', highlight=highlight, country=country)
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
			message = addHighlightConditions(country, newName)
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
			return render_template('addNewHighlight.html', country=country)
	else:
		return error('Unable to find Country in database.')

# Perform checks to ensure highlight name integrity
def addHighlightConditions(country, name):
	exists = session.query(Highlight).filter_by(country_id=country.id,
		name=name).scalar() is not None
	if (exists):
		return 'Cannot add Highlight, name already exists.'
	elif (name == ''):
		return 'Cannot add Highlight, name cannot be blank.'
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
			if request.form['name']:
				highlight.name = request.form['name']
			if request.form['description']:
				highlight.description = request.form['description']
			session.add(highlight)
			session.commit()
			return redirect(url_for('highlightDescription', highlight_name=highlight.name, country_name=country.name))
		else:
			return render_template('editHighlightDescription.html', highlight=highlight, country=country)
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
			return render_template('deleteHighlightDescription.html', highlight=highlight, country=country)
	else:
		return error('Unable to find entry in database.')

@app.route('/error', strict_slashes=False)		
def error(message):
	return render_template('error.html', message=message)
	
if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port=8000)