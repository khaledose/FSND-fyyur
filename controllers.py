#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from server import app, db
from flask import render_template, request, flash, redirect, url_for, jsonify
import babel
import dateutil.parser
from models import Venue, Artist, Show
from services import get_all_venues, get_search_venues, get_full_venue, get_search_artists, get_all_artists, get_full_artist, get_all_shows
from sqlalchemy import func
from forms import *
import logging
from logging import Formatter, FileHandler

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format="EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format="EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
    return render_template('pages/home.html')

#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    return render_template('pages/venues.html', areas=get_all_venues())

@app.route('/venues/search', methods=['POST'])
def search_venues():
    return render_template('pages/search_venues.html', 
                            results=get_search_venues(request.form['search_term']), 
                            search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    return render_template('pages/show_venue.html', venue=get_full_venue(venue_id))

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    try:
        venue = Venue(
            name=request.form['name'],
            city=request.form['city'],
            state=request.form['state'],
            address=request.form['address'],
            phone=request.form['phone'],
            genres=request.form.getlist('genres'),
            image_link=request.form['image_link'],
            website=request.form['website_link'],
            facebook_link=request.form['facebook_link'],
            seeking_talent= True if 'seeking_talent' in request.form else False,
            seeking_description=request.form['seeking_description']
        )
        db.session.add(venue)
        db.session.commit()
        flash('Venue ' + venue.name + ' was successfully listed!')
    except:
        db.session.rollback()
        flash('An error occurred. Venue ' + venue.name + ' could not be listed.')
    finally:
        db.session.close()
    return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    success = False
    try:
        Venue.query.filter_by(id=venue_id).delete()
        db.session.commit()
        flash('Venue was successfully deleted!')
        success = True
    except:
        db.session.rollback()
        success = False
        flash('An error occurred. Venue could not be deleted.')
    finally:
        db.session.close()
    return jsonify({'success': success})

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    return render_template('pages/artists.html', artists=get_all_artists())

@app.route('/artists/search', methods=['POST'])
def search_artists():
    return render_template('pages/search_artists.html', results=get_search_artists(request.form['search_term']), search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    return render_template('pages/show_artist.html', artist=get_full_artist(artist_id))

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    artist = Artist.query.get(artist_id)
    return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    try:
        artist = Artist.query.get(artist_id)
        artist.name = request.form['name']
        artist.city = request.form['city']
        artist.state = request.form['state']
        artist.phone = request.form['phone']
        artist.genres = request.form.getlist('genres')
        artist.image_link = request.form['image_link']
        artist.website = request.form['website_link']
        artist.facebook_link = request.form['facebook_link']
        artist.seeking_venue = True if 'seeking_venue' in request.form else False
        artist.seeking_description = request.form['seeking_description']
        db.session.commit()
        flash('Artist ' + artist.name + ' was successfully updated!')
    except:
        db.session.rollback()
        flash('An error occurred. Artist ' + artist.name + ' could not be updated.')
    finally:
        db.session.close()
    return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue = Venue.query.get(venue_id).to_dict()
    return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    try:
        venue = Venue.query.get(venue_id)
        venue.name = request.form['name']
        venue.address = request.form['address']
        venue.city = request.form['city']
        venue.state = request.form['state']
        venue.phone = request.form['phone']
        venue.genres = request.form.getlist('genres')
        venue.image_link = request.form['image_link']
        venue.website = request.form['website_link']
        venue.facebook_link = request.form['facebook_link']
        venue.seeking_talent = True if 'seeking_talent' in request.form else False
        venue.seeking_description = request.form['seeking_description']
        db.session.commit()
        flash('Venue ' + venue.name + ' was successfully updated!')
    except:
        db.session.rollback()
        flash('An error occurred. Venue ' + venue.name + ' could not be updated.')
    finally:
        db.session.close()
    return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    try:
        artist = Artist(
        name=request.form['name'],
        city=request.form['city'],
        state=request.form['state'],
        phone=request.form['phone'],
        genres=request.form.getlist('genres'),
        image_link=request.form['image_link'],
        website=request.form['website_link'],
        facebook_link=request.form['facebook_link'],
        seeking_venue= True if 'seeking_venue' in request.form else False,
        seeking_description=request.form['seeking_description']
        )
        db.session.add(artist)
        db.session.commit()
        flash('Artist ' + artist.name + ' was successfully listed!')
    except:
        db.session.rollback()
        flash('An error occurred. Artist ' + artist.name + ' could not be listed.')
    finally:
        db.session.close()
    return render_template('pages/home.html')

#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    return render_template('pages/shows.html', shows=get_all_shows())

@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    try:
        show = Show(
            artist_id=request.form['artist_id'],
            venue_id=request.form['venue_id'],
            start_time=request.form['start_time']
        )
        db.session.add(show)
        db.session.commit()
        flash('Show was successfully listed!')
    except:
        db.session.rollback()
        flash('An error occured. Show could not be listed.')
    finally:
        db.session.close()
    return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')