# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#
import sys
import json
from datetime import datetime, timedelta
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object("config")
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# TODO: connect to a local postgresql database

# ----------------------------------------------------------------------------#
# Models.
# ----------------------------------------------------------------------------#


class Venue(db.Model):
    __tablename__ = "venue"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.String(120), nullable=False)
    website = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(500), nullable=False)
    facebook_link = db.Column(db.String(120), nullable=False)
    seeking_talent = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(300), nullable=False)
    shows = db.relationship("Show", cascade="all,delete", backref="venue", lazy=True)
    # TODO: implement any missing fields, as a database migration using Flask-Migrate


class Artist(db.Model):
    __tablename__ = "artist"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.String(120), nullable=False)
    website = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(500), nullable=False)
    facebook_link = db.Column(db.String(120), nullable=False)
    seeking_venue = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(300), nullable=False)
    shows = db.relationship("Show", cascade="all,delete", backref="artist", lazy=True)
    # TODO: implement any missing fields, as a database migration using Flask-Migrate


class Show(db.Model):
    __tablename__ = "show"
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey("artist.id"), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey("venue.id"), nullable=False)


# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#


def format_datetime(value, format="medium"):
    date = dateutil.parser.parse(value)
    if format == "full":
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == "medium":
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


app.jinja_env.filters["datetime"] = format_datetime

# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#


@app.route("/")
def index():
    return render_template("pages/home.html")


#  Venues
#  ----------------------------------------------------------------


@app.route("/venues")
def venues():
    # TODO: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.
    areas = []
    try:
        query = Venue.query.distinct("city", "state").all()

        for item in query:

            venues_query = (
                Venue.query.filter_by(city=item.city, state=item.state)
                .order_by(Venue.name)
                .all()
            )
            venue_data = []
            for item in venues_query:
                data = {"id": item.id, "name": item.name, "num_upcoming_shows": 0}
                venue_data.append(data)
            area = {"city": item.city, "state": item.state, "venues": venue_data}
            areas.append(area)

        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()

    return render_template("pages/venues.html", areas=areas)


@app.route("/venues/search", methods=["POST"])
def search_venues():

    response = {}
    search_term = request.form.get("search_term", "")
    try:
        query = Venue.query.filter(Venue.name.ilike(f"%{search_term}%"))
        venues_count = query.count()
        venues = query.order_by(Venue.name).all()
        data = []
        for venue in venues:
            data.append({"id": venue.id, "name": venue.name})
        response = {"count": venues_count, "data": data}
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return render_template(
        "pages/search_venues.html", results=response, search_term=search_term,
    )


@app.route("/venues/<int:venue_id>")
def show_venue(venue_id):
    data = []
    try:
        venue = Venue.query.get(venue_id)
        records = (
            db.session.query(Show, Artist)
            .join(Artist)
            .filter(Show.venue_id == venue_id)
            .all()
        )

        past_data = []
        upcoming_data = []
        for record in records:

            d = {
                "artist_id": record[1].id,
                "artist_name": record[1].name,
                "artist_image_link": record[1].image_link,
                "start_time": record[0].start_time.strftime("%m/%d/%Y, %H:%M:%S"),
            }

            cutoff_time = datetime.now() - timedelta(hours=3)
            if record[0].start_time <= cutoff_time:
                past_data.append(d)
            else:
                upcoming_data.append(d)

        data = {
            "id": venue.id,
            "name": venue.name,
            "genres": venue.genres.split(","),
            "address": venue.address,
            "city": venue.city,
            "state": venue.state,
            "phone": venue.phone,
            "website": venue.website,
            "facebook_link": venue.facebook_link,
            "seeking_talent": venue.seeking_talent,
            "seeking_description": venue.seeking_description,
            "image_link": venue.image_link,
            "past_shows": past_data,
            "upcoming_shows": upcoming_data,
            "past_shows_count": len(past_data),
            "upcoming_shows_count": len(upcoming_data),
        }
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()

    return render_template("pages/show_venue.html", venue=data)


@app.route("/venues/create", methods=["GET"])
def create_venue_form():
    form = VenueForm(request.form)

    return render_template("forms/new_venue.html", form=form)


@app.route("/venues/create", methods=["POST"])
def create_venue_submission():
    form = VenueForm(request.form)
    if request.method == "POST" and form.validate():

        try:
            genres = str(form.genres.data).strip("[]").replace("'", "").replace(" ", "")
            venue = Venue(
                name=form.name.data,
                city=form.city.data,
                state=form.state.data,
                address=form.address.data,
                phone=form.phone.data,
                genres=genres,
                website=form.website.data,
                image_link=form.image_link.data,
                facebook_link=form.facebook_link.data,
                seeking_talent=form.seeking_talent.data,
                seeking_description=form.seeking_description.data,
            )
            db.session.add(venue)
            db.session.commit()
            flash("Venue " + request.form["name"] + " was successfully listed!")
        except:
            flash(
                "An error occurred. Venue "
                + request.form["name"]
                + " could not be listed."
            )
            db.session.rollback()
            print(sys.exc_info())
        finally:
            db.session.close()

    else:
        flash(
            "An error occurred. Venue " + request.form["name"] + " could not be listed."
        )
    return render_template("pages/home.html", form=form)


@app.route("/venues/<int:venue_id>/edit", methods=["GET", "POST"])
def edit_venue_submission(venue_id):
    form = VenueForm(request.form)
    if request.method == "GET":
        try:
            venue = Venue.query.get(venue_id)

            form.name.data = venue.name
            form.city.data = venue.city
            form.state.data = venue.state
            form.address.data = venue.address
            form.phone.data = venue.phone
            form.website.data = venue.website
            form.image_link.data = venue.image_link
            form.facebook_link.data = venue.facebook_link
            form.seeking_talent.data = venue.seeking_talent
            form.seeking_description.data = venue.seeking_description

            db.session.commit()
        except:
            db.session.rollback()
            print(sys.exc_info())
        finally:
            db.session.close()
        return render_template("forms/edit_venue.html", form=form)

    if request.method == "POST" and form.validate():

        try:
            venue = Venue.query.get(venue_id)
            genres = str(form.genres.data).strip("[]").replace("'", "").replace(" ", "")

            venue.name = form.name.data
            venue.city = form.city.data
            venue.state = form.state.data
            venue.address = form.address.data
            venue.phone = form.phone.data
            venue.genres = genres
            venue.website = form.website.data
            venue.image_link = form.image_link.data
            venue.facebook_link = form.facebook_link.data
            venue.seeking_talent = form.seeking_talent.data
            venue.seeking_description = form.seeking_description.data

            db.session.commit()
            flash("Venue " + form.name.data + " was successfully edited.")
        except:
            flash(
                "An error occurred. Venue " + form.name.data + " could not be edited."
            )
            db.session.rollback()
            print(sys.exc_info())
        finally:
            db.session.close()

    else:
        flash("An error occurred. Venue could not be edited.")
    return render_template("pages/home.html")


@app.route("/venues/<venue_id>/delete", methods=["POST"])
def delete_venue(venue_id):
    query = Venue.query.filter_by(id=venue_id)
    print(query.count())
    if query.count() == 1:
        # show_query = Show.query.filter_by(venue_id=venue_id)
        try:
            venue = db.session.query(Venue).filter_by(id=venue_id).first()
            db.session.delete(venue)

            db.session.commit()
            flash("Venue deleted")
        except:
            db.session.rollback()
            flash("Venue could not be deleted")
        finally:
            db.session.close()

    else:
        flash("Venue could not be deleted")

    return render_template("pages/home.html")


#  Artists
#  ----------------------------------------------------------------


@app.route("/artists")
def artists():

    try:
        artists = Artist.query.order_by(Artist.name).all()

        artist_data = []
        for artist in artists:

            data = {
                "id": artist.id,
                "name": artist.name,
            }
            artist_data.append(data)
            db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()

    return render_template("pages/artists.html", artists=artist_data)


@app.route("/artists/search", methods=["POST"])
def search_artists():
    response = {}
    search_term = request.form.get("search_term", "")
    try:
        query = Artist.query.filter(Artist.name.ilike(f"%{search_term}%"))
        artists_count = query.count()
        artists = query.order_by(Artist.name).all()
        data = []
        for artist in artists:
            data.append({"id": artist.id, "name": artist.name})
        response = {"count": artists_count, "data": data}
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()

    return render_template(
        "pages/search_artists.html", results=response, search_term=search_term,
    )


@app.route("/artists/<int:artist_id>")
def show_artist(artist_id):

    data = {}
    try:
        artist = Artist.query.get(artist_id)
        records = (
            db.session.query(Show, Venue)
            .join(Venue)
            .filter(Show.artist_id == artist_id)
            .all()
        )

        past_data = []
        upcoming_data = []
        for record in records:

            d = {
                "venue_id": record[1].id,
                "venue_name": record[1].name,
                "venue_image_link": record[1].image_link,
                "start_time": record[0].start_time.strftime("%m/%d/%Y, %H:%M:%S"),
            }

            cutoff_time = datetime.now() - timedelta(hours=3)
            if record[0].start_time <= cutoff_time:
                past_data.append(d)
            else:
                upcoming_data.append(d)

        data = {
            "id": artist.id,
            "name": artist.name,
            "genres": artist.genres.split(","),
            "city": artist.city,
            "state": artist.state,
            "phone": artist.phone,
            "website": artist.website,
            "facebook_link": artist.facebook_link,
            "seeking_venue": artist.seeking_venue,
            "seeking_description": artist.seeking_description,
            "image_link": artist.image_link,
            "past_shows": past_data,
            "upcoming_shows": upcoming_data,
            "past_shows_count": len(past_data),
            "upcoming_shows_count": len(upcoming_data),
        }
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()

    return render_template("pages/show_artist.html", artist=data)


@app.route("/artists/create", methods=["GET"])
def create_artist_form():
    form = ArtistForm()
    return render_template("forms/new_artist.html", form=form)


@app.route("/artists/create", methods=["POST"])
def create_artist_submission():

    form = ArtistForm(request.form)
    if form.validate():
        try:
            genres = str(form.genres.data).strip("[]").replace("'", "").replace(" ", "")

            artist = Artist(
                name=form.name.data,
                city=form.city.data,
                state=form.state.data,
                phone=form.phone.data,
                genres=genres,
                website=form.website.data,
                image_link=form.image_link.data,
                facebook_link=form.facebook_link.data,
                seeking_venue=form.seeking_venue.data,
                seeking_description=form.seeking_description.data,
            )
            db.session.add(artist)
            db.session.commit()
            flash("Artist " + request.form["name"] + " was successfully listed!")
        except:
            flash(
                "An error occurred. Artist "
                + request.form["name"]
                + " could not be listed."
            )
            db.session.rollback()
            print(sys.exc_info())
        finally:
            db.session.close()

    else:
        flash(
            "An error occurred. Artist "
            + request.form["name"]
            + " could not be listed."
        )

    return render_template("pages/home.html")


@app.route("/artists/<int:artist_id>/edit", methods=["GET", "POST"])
def edit_artist_submission(artist_id):

    form = ArtistForm(request.form)
    if request.method == "GET":
        try:
            artist = Artist.query.get(artist_id)

            form.name.data = artist.name
            form.city.data = artist.city
            form.state.data = artist.state
            form.phone.data = artist.phone
            form.website.data = artist.website
            form.image_link.data = artist.image_link
            form.facebook_link.data = artist.facebook_link
            form.seeking_venue.data = artist.seeking_venue
            form.seeking_description.data = artist.seeking_description

            db.session.commit()
        except:
            db.session.rollback()
            print(sys.exc_info())
        finally:
            db.session.close()
        return render_template("forms/edit_artist.html", form=form)

    if request.method == "POST" and form.validate():

        try:
            artist = Artist.query.get(artist_id)
            genres = str(form.genres.data).strip("[]").replace("'", "").replace(" ", "")

            artist.name = form.name.data
            artist.city = form.city.data
            artist.state = form.state.data
            artist.phone = form.phone.data
            artist.genres = genres
            artist.website = form.website.data
            artist.image_link = form.image_link.data
            artist.facebook_link = form.facebook_link.data
            artist.seeking_venue = form.seeking_venue.data
            artist.seeking_description = form.seeking_description.data

            db.session.commit()
            flash("Artist " + form.name.data + " was successfully edited.")
        except:
            flash(
                "An error occurred. Artist " + form.name.data + " could not be edited."
            )
            db.session.rollback()
            print(sys.exc_info())
        finally:
            db.session.close()

    else:
        flash("An error occurred. Artist could not be edited.")
    return render_template("pages/home.html")


@app.route("/artists/<artist_id>/delete", methods=["POST"])
def delete_artist(artist_id):
    query = Artist.query.filter_by(id=artist_id)
    print(query.count())
    if query.count() == 1:
        try:
            artist = db.session.query(Artist).filter_by(id=artist_id).first()
            db.session.delete(artist)
            db.session.commit()
            flash("Artist deleted")
        except:
            db.session.rollback()
            flash("Artist could not be deleted")
        finally:
            db.session.close()

    else:
        flash("Artist could not be deleted")

    return render_template("pages/home.html")


#  Shows
#  ----------------------------------------------------------------


@app.route("/shows")
def shows():
    shows_data = []
    try:
        query = db.session.query(Show, Artist, Venue).join(Artist).join(Venue)
        records = query.all()

        for record in records:

            data1 = {
                "venue_id": record[2].id,
                "venue_name": record[2].name,
                "artist_id": record[1].id,
                "artist_name": record[1].name,
                "artist_image_link": record[1].image_link,
                "start_time": record[0].start_time.strftime("%m/%d/%Y, %H:%M:%S"),
            }

            shows_data.append(data1)
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()

    return render_template("pages/shows.html", shows=shows_data)


@app.route("/shows/create")
def create_shows():
    # Render form
    form = ShowForm()
    return render_template("forms/new_show.html", form=form)


@app.route("/shows/create", methods=["POST"])
def create_show_submission():
    form = ShowForm()
    if form.validate():
        try:

            show = Show(
                artist_id=form.artist_id.data,
                venue_id=form.venue_id.data,
                start_time=form.start_time.data,
            )
            db.session.add(show)
            db.session.commit()
            flash("Show was successfully listed!")
        except:
            flash("An error occurred. Show could not be listed.")
            db.session.rollback()
            print(sys.exc_info())
        finally:
            db.session.close()

    else:
        flash("An error occurred. Show could not be listed.")

    return render_template("pages/home.html")


@app.errorhandler(404)
def not_found_error(error):
    return render_template("errors/404.html"), 404


@app.errorhandler(500)
def server_error(error):
    return render_template("errors/500.html"), 500


if not app.debug:
    file_handler = FileHandler("error.log")
    file_handler.setFormatter(
        Formatter("%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]")
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info("errors")

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
if __name__ == "__main__":
    app.run()

# Or specify port manually:
"""
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
"""
