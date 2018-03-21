from flask import Flask, render_template, request, redirect, jsonify, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
sys.path.insert(0, 'Modules')
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
	countries = session.query(Country).order_by(Country.name).all()
	return jsonify(countries=[c.serialize for c in countries])
	
# Show all countries
@app.route('/')
@app.route('/countries')
def countries():
	countries = session.query(Country).order_by(Country.name).all()
	return render_template('countries.html', countries=countries)
	
# Show all country highlights
@app.route('/countries/<country_name>/highlights')
def countryHighlights(country_name):
	countries = session.query(Country).order_by(Country.name).all()
	country = session.query(Country).filter_by(name=country_name).first()
	highlights = session.query(Highlight).filter_by(
		country_id=country.id).all()
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
			return redirect(url_for('countries'))
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
			countries = session.query(Country).order_by(Country.name).all()
			return render_template('addNewHighlight.html', countries=countries, country=country)
	else:
		return error('Unable to find Country in database.')

# Perform checks to ensure highlight name integrity
def addHighlightConditions(country, name):
	exists = session.query(Highlight).filter_by(country_id=country.id,
		name=name).scalar() is not None
	if (exists):
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
			message = addHighlightConditions(country, newName)
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