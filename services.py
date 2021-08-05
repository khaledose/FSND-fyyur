#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from models import Venue, Artist, Show, db
from datetime import date
from sqlalchemy.sql.functions import func

#----------------------------------------------------------------------------#
# Venues' Services.
#----------------------------------------------------------------------------#

def get_mini_venue(id, name):
    """
    Args: id: Venue ID, name: Venue name

    Returns: Dictionary containing the id, name and number of upcoming shows.
    """
    return {
        'id': id,
        'name': name,
        'num_upcoming_shows': db.session
        .query(Show)
        .filter(Show.venue_id == id)
        .filter(Show.start_time > date.today())
        .count()
    }


def get_all_venues():
    """
    Gets all venues from the database ordered by city and state.

    Returns: List of dictionaries containing all venues for each city 
             containing id, name and number of upcoming shows.
    """
    areas = db.session.query(Venue.city, Venue.state).distinct()
    venues_list = []
    for area in areas:
        area = dict(area)
        query_result = db.session.query(Venue.id, Venue.name).filter_by(
            city=area['city'], state=area['state']).all()
        venues = [get_mini_venue(v['id'], v['name']) for v in query_result]
        area['venues'] = venues
        venues_list.append(area)
    return venues_list


def get_search_venues(search_term):
    """
    Searches for venues that contains the given search term.

    Args: search_term: User's input looking for a specific venue.

    Returns: Dictionary containing results' count and a list of found venues.
    """
    query_result = db.session.query(Venue.id, Venue.name).filter(
        Venue.name.ilike(f'%{search_term}%')).all()
    response = [get_mini_venue(v['id'], v['name']) for v in query_result]
    return {'count': len(response), 'data': response}


def get_shows_with_artist(id):
    """
    Gets a list of upcoming and past shows with artist details.

    Args: id: ID of the selected venue.

    Returns: past_shows and upcoming shows these are lists each one contains 
             artist details and show date which are related to the venue in 
             the past or in the future.
    """
    keys = ['artist_id', 'artist_name', 'artist_image_link', 'start_time']
    past_shows = []
    upcoming_shows = []
    shows = db.session.query(
        Artist.id,
        Artist.name,
        Artist.image_link,
        Show.start_time
    ).join(Artist
           ).filter(Show.venue_id == id).all()

    for show in shows:
        show = dict(zip(keys, show))
        date_temp = show['start_time'].date()
        show['start_time'] = str(show['start_time'])
        if(date_temp > date.today()):
            upcoming_shows.append(show)
        else:
            past_shows.append(show)
    return past_shows, upcoming_shows


def get_full_venue(id):
    """
    Gets all details of the selected venue including past and upcoming shows.

    Args: id: ID of the selected venue.

    Returns: Dictionary of all details related to that venue.
    """
    venue = Venue.query.get(id).to_dict()
    past_shows, upcoming_shows = get_shows_with_artist(id)
    venue['past_shows'] = past_shows
    venue['upcoming_shows'] = upcoming_shows
    venue['past_shows_count'] = len(past_shows)
    venue['upcoming_shows_count'] = len(upcoming_shows)
    return venue

#----------------------------------------------------------------------------#
# Artists' Services.
#----------------------------------------------------------------------------#


def get_mini_artist(id, name):
    """
    Args: id: Artist ID, name: Artist name

    Returns: Dictionary containing the id, name and number of upcoming shows.
    """
    return {
        'id': id,
        'name': name,
        'num_upcoming_shows': db.session
        .query(Show)
        .filter(Show.artist_id == id)
        .filter(Show.start_time > date.today())
        .count()
    }


def get_all_artists():
    """
    Gets all artists from the database.

    Returns: list of dictionaries containing id and name of each artist.
    """
    return db.session.query(Artist.id, Artist.name).order_by('id').all()


def get_search_artists(search_term):
    """
    Searches for artists that contains the given search term.

    Args: search_term: User's input looking for a specific artist.

    Returns: Dictionary containing results' count and a list of found artists.
    """
    query_result = db.session.query(Artist.id, Artist.name).filter(
        Artist.name.ilike(f'%{search_term}%')).all()
    response = [get_mini_artist(v['id'], v['name']) for v in query_result]
    return {'count': len(response), 'data': response}


def get_shows_with_venues(id):
    """
    Gets a list of upcoming and past shows with venue details.

    Args: id: ID of the selected artist.

    Returns: past_shows and upcoming shows these are lists each one contains 
             venue details and show date which are related to the artist in 
             the past or in the future.
    """
    keys = ['venue_id', 'venue_name', 'venue_image_link', 'start_time']
    past_shows = []
    upcoming_shows = []
    shows = db.session.query(
        Venue.id,
        Venue.name,
        Venue.image_link,
        Show.start_time
    ).join(Venue
           ).filter(Show.artist_id == id).all()

    for show in shows:
        show = dict(zip(keys, show))
        date_temp = show['start_time'].date()
        show['start_time'] = str(show['start_time'])
        if(date_temp > date.today()):
            upcoming_shows.append(show)
        else:
            past_shows.append(show)

    return past_shows, upcoming_shows


def get_full_artist(id):
    """
    Gets all details of the selected artist including past and upcoming shows.

    Args: id: ID of the selected artist.

    Returns: Dictionary of all details related to that artist.
    """
    artist = Artist.query.get(id)
    artist = artist.to_dict()
    past_shows, upcoming_shows = get_shows_with_venues(id)
    artist['past_shows'] = past_shows
    artist['upcoming_shows'] = upcoming_shows
    artist['past_shows_count'] = len(past_shows)
    artist['upcoming_shows_count'] = len(upcoming_shows)
    return artist

#----------------------------------------------------------------------------#
# Shows' Services.
#----------------------------------------------------------------------------#


def get_all_shows():
    """
    Gets all shows from the database.

    Returns: List of dictionaries containing venue name, artist name and artist's image.
    """
    shows = db.session.query(
        Show,
        Venue.name,
        Artist.name,
        Artist.image_link
    ).join(
        Venue
    ).join(
        Artist
    ).all()
    result = []
    for show in shows:
        show_dict = show['Show'].to_dict()
        show_dict['start_time'] = str(show_dict['start_time'])
        show_dict['venue_name'] = show[1]
        show_dict['artist_name'] = show[2]
        show_dict['artist_image_link'] = show['image_link']
        result.append(show_dict)
    return result
