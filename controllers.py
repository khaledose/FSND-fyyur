#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from server import app, db
from flask import render_template, request, flash, redirect, url_for, jsonify
import babel
import dateutil.parser
from models import Venue, Artist, Show
from services import get_all_venues, get_search_venues, get_full_venue, get_search_artists, get_all_artists, get_full_artist, get_all_shows
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
    """
    Renders homepage of Fyyur App.
    """
    return render_template('pages/home.html')

#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    """
    Renders Venues list page.

    Returns: Renders all retrieved venues from the database 
             in a list filtered by city and state.
    """
    return render_template('pages/venues.html', areas=get_all_venues())

@app.route('/venues/search', methods=['POST'])
def search_venues():
    """
    Renders a page showing the search results.

    Input: Gets search term from the form.

    On POST: Retrieves all venues that matches the search term.

    Returns: Renders the list of retrieved venues.
        
    """
    return render_template('pages/search_venues.html', 
                            results=get_search_venues(request.form['search_term']), 
                            search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    """
    Renders a page with full details of the selected venue.

    Args: venue_id: ID of the selected venue.

    Returns: 
        Venue details: Name, City, State, Address, Phone, Genres, Website, Facebook, 
                       Image, Seeking Talent, Seeking Description, Past Shows 
                       and Upcoming Shows.
    """
    return render_template('pages/show_venue.html', venue=get_full_venue(venue_id))

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    """
        Renders new_venue.html page.

        Returns: Form object that will contain venue details after user fill 
                 the form page and pass it to the HTML page. 
    """
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    """
        Creates a new venue object from user's inputs.

        Input: Gets user inputs from the form object.

        On POST: Creates a new venue object from data captured by the user
                 and saves the data to the database

        Returns: renders the homepage after successful creation.
    """
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
    """
        Deletes selected venue.

        Args: venue_id: ID of selected venue.

        On DELETE: Gets the venue by ID and deletes it from the database.

        Returns: Renders homepage after successful deletion.
    """
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
    """
    Renders Artist list page.

    Returns: Renders all retrieved artists from the database in a list.
    """
    return render_template('pages/artists.html', artists=get_all_artists())

@app.route('/artists/search', methods=['POST'])
def search_artists():
    """
    Renders a page showing the search results.

    Input: Gets search term from the form.

    On POST: Retrieves all artists that matches the search term.

    Returns: Renders the list of retrieved artists.
        
    """
    return render_template('pages/search_artists.html', results=get_search_artists(request.form['search_term']), search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    """
    Renders a page with full details of the selected artist.

    Args: artist_id: ID of the selected artist.

    Returns: 
        Artist details: Name, City, State, Phone, Genres, Website, Facebook, 
                        Image, Seeking Talent, Seeking Description, Past Shows 
                        and Upcoming Shows.
    """
    return render_template('pages/show_artist.html', artist=get_full_artist(artist_id))

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    """
    Renders form for updating an artist.

    Args: artist_id: ID of the selected artist.

    On GET: Gets the artist from the database by ID and creates 
            an ArtistForm object to pass it to edit_artist page.

    Returns: renders the edit_artist page.
    """
    form = ArtistForm()
    artist = Artist.query.get(artist_id)
    return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    """
    Updates the selected artist object from user's inputs.

    Args: artist_id: ID of the selected artist.

    Input: Gets user inputs from the form object.

    On POST: Gets the artist from the database by ID and overrides its data 
             by the data captured by the user from the form object.

    Returns: renders the homepage after successful update.
    """
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
    """
    Renders form for updating a venue.

    Args: venue_id: ID of the selected venue.

    On GET: Gets the venue from the database by ID and creates 
            a VenueForm object to pass it to edit_venue page.

    Returns: renders the edit_venue page.
    """
    form = VenueForm()
    venue = Venue.query.get(venue_id).to_dict()
    return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    """
    Updates the selected venue object from user's inputs.

    Args: venue_id: ID of the selected venue.

    Input: Gets user inputs from the form object.

    On POST: Gets the venue from the database by ID and overrides its data 
             by the data captured by the user from the form object.

    Returns: renders the homepage after successful update.
    """
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
    """
    Renders form for creating a new artist.

    On GET: creates an ArtistForm object to pass it to new_artist page.

    Returns: renders the new_artist page.
    """
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    """
    creates a new artist object from user's inputs.

    Input: Gets user inputs from the form object.

    On POST: Creates new artits object with data captured from user 
             by the form object and add it to the database.

    Returns: renders the homepage after successful creation.
    """
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
    """
    Renders all Shows registered in the database.

    Returns: Renders all retrieved shows from the database in a list 
             showing the name of artist and venues in the show.
    """
    return render_template('pages/shows.html', shows=get_all_shows())

@app.route('/shows/create')
def create_shows():
    """
    Renders form for creating a new show.

    On GET: creates a ShowForm object to pass it to new_show page.

    Returns: renders the new_show page.
    """
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    """
    creates a new show object from user's inputs.

    Input: Gets user inputs from the form object.

    On POST: Creates a new show object with data captured from user 
             by the form object and add it to the database.

    Returns: renders the homepage after successful creation.
    """
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
    """
    renders 404.html on 404 error if data is not found.
    """
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    """
    renders 500.html on 500 error if an internal server error occured.
    """
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