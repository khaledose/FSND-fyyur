#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from server import db

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.String(160), nullable=False)
    image_link = db.Column(db.String(500), nullable=True)
    website_link = db.Column(db.String(120), nullable=True)
    facebook_link = db.Column(db.String(120), nullable=True)
    seeking_talent = db.Column(db.Boolean, nullable=False)
    seeking_description = db.Column(db.String(500), nullable=True)

    def __repr__(self) -> str:
        return f'''Venues(
                Venue id={self.id}, 
                name={self.name}, 
                city={self.city}, 
                state={self.state}, 
                address={self.address}, 
                phone={self.phone}, 
                genres={self.genres},
                image_link={self.image_link},
                website_link={self.website_link},
                facebook_link={self.facebook_link},
                seeking_talent={self.seeking_talent},
                seeking_description={self.seeking_description}
            )
        '''

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "genres": self.genres,
            "address": self.address,
            "city": self.city,
            "state": self.state,
            "phone": self.phone,
            "website_link": self.website_link,
            "facebook_link": self.facebook_link,
            "seeking_talent": self.seeking_talent,
            "seeking_description": self.seeking_description,
            "image_link": self.image_link
        }

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.String(160), nullable=False)
    image_link = db.Column(db.String(500), nullable=True)
    website_link = db.Column(db.String(120), nullable=True)
    facebook_link = db.Column(db.String(120), nullable=True)
    seeking_venue = db.Column(db.Boolean, nullable=False)
    seeking_description = db.Column(db.String(500), nullable=True)

    def __repr__(self) -> str:
        return f'''Artists(
                Venue id={self.id}, 
                name={self.name}, 
                city={self.city}, 
                state={self.state}, 
                phone={self.phone}, 
                genres={self.genres},
                image_link={self.image_link},
                website_link={self.website_link},
                facebook_link={self.facebook_link},
                seeking_venue={self.seeking_venue},
                seeking_description={self.seeking_description}
            )
        '''

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "genres": self.genres,
            "city": self.city,
            "state": self.state,
            "phone": self.phone,
            "website_link": self.website_link,
            "facebook_link": self.facebook_link,
            "seeking_venue": self.seeking_venue,
            "seeking_description": self.seeking_description,
            "image_link": self.image_link
        }

class Show(db.Model):
    __tablename__ = 'Show'

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id', ondelete='CASCADE'), nullable=False)
    artist = db.relationship('Artist')
    venue = db.relationship('Venue')
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id', ondelete='CASCADE'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)

    def __repr__(self) -> str:
        return f'''Shows(
                Artist ID={self.artist_id},
                Venue ID={self.venue_id},
                Date={self.start_time}
            )
        '''
    
    def to_dict(self):
        return {
            'venue_id': self.venue_id,
            'artist_id': self.artist_id,
            'start_time': str(self.start_time)
        }