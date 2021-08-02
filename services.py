#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from models import Venue, Artist, Show, db
from datetime import date
from sqlalchemy import func

#----------------------------------------------------------------------------#
# Venues' Services.
#----------------------------------------------------------------------------#

def format_genres(genres):
    return genres[1:-1].split(',')

def get_mini_venue(id, name):
    return {
        'id': id,
        'name': name,
        'num_upcoming_shows': db.session
            .query(Show)
            .filter(Show.venue_id==id)
            .filter(Show.start_time > date.today())
            .count()
    }

def get_areas():
    query_result = db.session.query(Venue.city, Venue.state).order_by('id').all()
    areas = []
    for area in [dict(a) for a in query_result]:
        if area not in areas:
            areas.append(area)
    return areas

def get_all_venues():
    areas = get_areas()
    for area in areas:
        query_result = db.session.query(Venue.id, Venue.name).filter_by(city=area['city'], state=area['state']).all()
        venues = [get_mini_venue(v['id'], v['name']) for v in query_result]
        area['venues'] = venues
    return areas

def get_search_venues(search_term):
    query_result = db.session.query(Venue.id, Venue.name).filter(func.lower(Venue.name).contains(search_term.lower())).all()
    response = [get_mini_venue(v['id'], v['name']) for v in query_result]
    return {'count': len(response), 'data': response}

def get_shows_with_artist(id):
    shows = Show.query.filter_by(venue_id=id).all()
    past_shows = []
    upcoming_shows = []
    for i in range(len(shows)):
        artist = db.session.query(Artist.name, Artist.image_link).filter(Artist.id==shows[i].artist_id).first()
        shows[i] = {
            'artist_id': shows[i].artist_id,
            'artist_name': artist['name'],
            'artist_image_link': artist['image_link'],
            'start_time': shows[i].start_time
        }
        if shows[i]['start_time'].date() >= date.today():
            upcoming_shows.append(shows[i])
        else:
            past_shows.append(shows[i])
        shows[i]['start_time'] = str(shows[i]['start_time'])
    return past_shows, upcoming_shows

def get_full_venue(id):
    venue = Venue.query.get(id)
    venue.genres = format_genres(venue.genres)
    venue = venue.to_dict()
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
    return {
        'id': id,
        'name': name,
        'num_upcoming_shows': db.session
            .query(Show)
            .filter(Show.artist_id==id)
            .filter(Show.start_time > date.today())
            .count()
    }

def get_all_artists():
    return db.session.query(Artist.id, Artist.name).order_by('id').all()

def get_search_artists(search_term):
    query_result = db.session.query(Artist.id, Artist.name).filter(func.lower(Artist.name).contains(search_term.lower())).all()
    response = [get_mini_artist(v['id'], v['name']) for v in query_result]
    return {'count': len(response), 'data': response}

def get_shows_with_venues(id):
    shows = Show.query.filter_by(artist_id=id).all()
    past_shows = []
    upcoming_shows = []
    for i in range(len(shows)):
        venue = db.session.query(Venue.name, Venue.image_link).filter(Venue.id==shows[i].venue_id).first()
        shows[i] = {
            'venue_id': shows[i].venue_id,
            'venue_name': venue['name'],
            'venue_image_link': venue['image_link'],
            'start_time': shows[i].start_time
        }
        if shows[i]['start_time'].date() >= date.today():
            upcoming_shows.append(shows[i])
        else:
            past_shows.append(shows[i])
        shows[i]['start_time'] = str(shows[i]['start_time'])
    return past_shows, upcoming_shows

def get_full_artist(id):
    artist = Artist.query.get(id)
    artist.genres = format_genres(artist.genres)
    artist = artist.to_dict()
    past_shows, upcoming_shows = get_shows_with_venues(id)
    artist['past_shows'] = past_shows
    artist['upcoming_shows'] = upcoming_shows
    artist['past_shows_count'] = len(past_shows)
    artist['upcoming_shows_count'] = len(upcoming_shows)
    print(artist)
    return artist

#----------------------------------------------------------------------------#
# Shows' Services.
#----------------------------------------------------------------------------#

def get_all_shows():
    shows = Show.query.all()
    for i in range(len(shows)):
        venue = db.session.query(Venue.name).filter(Venue.id==shows[i].venue_id).first()
        artist = db.session.query(Artist.name, Artist.image_link).filter(Artist.id==shows[i].artist_id).first()
        shows[i] = shows[i].to_dict()
        shows[i]['venue_name'] = venue['name']
        shows[i]['artist_name'] = artist['name']
        shows[i]['artist_image_link'] = artist['image_link']
    return shows