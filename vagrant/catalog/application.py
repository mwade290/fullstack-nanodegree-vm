from flask import Flask, render_template, request, redirect, jsonify, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Country, Highlight

app = Flask(__name__)

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
	
# Show description for highlight
@app.route('/countries/<country_name>/highlights/<int:highlight_id>/description')
def highlightDescription(country_name, highlight_id):
	country = session.query(Country).filter_by(name=country_name).first()
	highlight = session.query(Highlight).filter_by(country_id=country.id,
		id=highlight_id).first()
	if country > 0 and highlight > 0:
		return render_template('highlightDescription.html', highlight=highlight, country=country)
	else:
		return error()
		
# Edit highlight description
@app.route('/countries/<country_name>/highlights/<int:highlight_id>/description/edit',
           methods=['GET', 'POST'])
def editHighlightDescription(country_name, highlight_id):
	country = session.query(Country).filter_by(name=country_name).first()
	highlight = session.query(Highlight).filter_by(country_id=country.id,
		id=highlight_id).first()
	if country > 0 and highlight > 0:
		if request.method == 'POST':
			if request.form['name']:
				highlight.name = request.form['name']
			if request.form['description']:
				highlight.description = request.form['description']
			session.add(highlight)
			session.commit()
			return redirect(url_for('highlightDescription', highlight_id=highlight.id, country_name=country.name))
		else:
			return render_template('editHighlightDescription.html', highlight=highlight, country=country)
	else:
		return error()
		
# Delete highlight description
@app.route('/countries/<country_name>/highlights/<int:highlight_id>/description/delete',
           methods=['GET', 'POST'])
def deleteHighlightDescription(country_name, highlight_id):
	country = session.query(Country).filter_by(name=country_name).first()
	highlight = session.query(Highlight).filter_by(country_id=country.id,
		id=highlight_id).first()
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
		return error()

@app.route('/error', strict_slashes=False)		
def error():
	return render_template('error.html')
	
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)