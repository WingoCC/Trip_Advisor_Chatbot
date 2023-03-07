import re
import json
import mysql.connector

INSERT_INTO_TOPLIST_TEMPLATE = "INSERT INTO toplist (name, link) VALUES (%s, %s)"
INSERT_INTO_TandD_TEMPLATE = "INSERT INTO toplist_and_destination (toplist_id, destination_id) VALUES (%d, %d)"
INSERT_INTO_DESTINATION_TEMPLATE = "INSERT INTO destination (name, link, description, location_tags, attractions_link, restaurants_link, tours_link, trip_moments_link) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
INSERT_INTO_DandA_TEMPLATE = "INSERT INTO destination_and_attraction (destination_id, attraction_id) VALUES (%d, %d)"
INSERT_INTO_ATTRACTION_TEMPLATE = "INSERT INTO attraction (name, link, location_tags, open_status, recommended_sightseeing_time, phone, address) VALUES (%s, %s, %s, %s, %s, %s, %s)"
INSERT_INTO_AandR_TEMPLATE = "INSERT INTO attraction_and_review (attraction_id, review_id) VALUES (%d, %d)"
INSERT_INTO_REVIEW_TEMPLATE = "INSERT INTO review (content) VALUES (%s)"


def read_json_as_dict(data_path):
    with open(data_path, "r") as fp:
        return json.load(fp)


def insert_toplist_return_id(toplist_item, mycursor, db_connector):
    toplist_name = toplist_item["name"]
    toplist_link = toplist_item["link"]

    # Judge if cur toplist is already in toplist table
    mycursor.execute('SELECT id FROM toplist WHERE name = "%s"' % toplist_name)
    toplist_id = mycursor.fetchone()

    if toplist_id is None:
        mycursor.execute(INSERT_INTO_TOPLIST_TEMPLATE, (toplist_name, toplist_link))
        db_connector.commit()

        mycursor.execute('SELECT id FROM toplist WHERE name = "%s"' % toplist_name)
        toplist_id = mycursor.fetchone()

    return toplist_id[0]


def insert_destination_return_id(destination_item, mycursor, db_connector):
    name = destination_item["name"]
    link = destination_item["link"]

    try:
        description = "".join(destination_item["description"])
    except KeyError:
        description = ""
    try:
        location_tags = destination_item["loc_tags"]
    except KeyError:
        location_tags = ""
    try:
        attractions_link = destination_item["navigation"]["Attractions"]
    except KeyError:
        attractions_link = ""
    try:
        restaurants_link = destination_item["navigation"]["Restaurants"]
    except KeyError:
        restaurants_link = ""
    try:
        tours_link = destination_item["navigation"]["Tours/Tickets"]
    except KeyError:
        tours_link = ""
    try:
        trip_moments_link = destination_item["navigation"]["Trip Moments"]
    except KeyError:
        trip_moments_link = ""

    # Judge if cur toplist is already in destination table
    mycursor.execute('SELECT id FROM destination WHERE name = "%s"' % name)
    destination_id = mycursor.fetchone()

    if destination_id is None:
        mycursor.execute(INSERT_INTO_DESTINATION_TEMPLATE,
                         (name,
                          link,
                          description,
                          location_tags,
                          attractions_link,
                          restaurants_link,
                          tours_link,
                          trip_moments_link))
        db_connector.commit()

        mycursor.execute('SELECT id FROM destination WHERE name = "%s"' % name)
        destination_id = mycursor.fetchone()
    return destination_id[0]


def insert_attraction_return_id(attraction_item, mycursor, db_connector):
    name = attraction_item["name"].replace('"', "")
    link = attraction_item["link"]
    try:
        location_tags = attraction_item["loc_tags"]
    except KeyError:
        location_tags = ""
    try:
        open_status = attraction_item["open_status"]
    except KeyError:
        open_status = ""
    try:
        recommended_sightseeing_time = attraction_item["recommended_sightseeing_time"]
    except KeyError:
        recommended_sightseeing_time = ""
    try:
        phone = attraction_item["phone"]
    except KeyError:
        phone = ""
    try:
        address = attraction_item["address"]
    except KeyError:
        address = ""

    # Judge if cur toplist is already in destination table
    mycursor.execute('SELECT id FROM attraction WHERE name = "%s"' % name)
    attraction_id = mycursor.fetchone()

    if attraction_id is None:
        mycursor.execute(INSERT_INTO_ATTRACTION_TEMPLATE,
                         (name,
                          link,
                          location_tags,
                          open_status,
                          recommended_sightseeing_time,
                          phone,
                          address))
        db_connector.commit()

        mycursor.execute('SELECT id FROM attraction WHERE name = "%s"' % name)
        attraction_id = mycursor.fetchone()

    return attraction_id[0]


def insert_reviews_return_id(review_, mycursor, db_connector):
    review = re.sub(r'[^A-Za-z0-9 ]+', '', review_)

    mycursor.execute('SELECT id FROM review WHERE content = "%s"' % review)
    review_id = mycursor.fetchone()

    if review_id is None:
        mycursor.execute(INSERT_INTO_REVIEW_TEMPLATE, (review,))
        db_connector.commit()

        mycursor.execute('SELECT id FROM review WHERE content = "%s"' % review)
        review_id = mycursor.fetchone()

    return review_id[0]


def database_init(db_connector, trip_info):
    mycursor = db_connector.cursor()

    for cur_toplist in trip_info:
        toplist_id = insert_toplist_return_id(cur_toplist, mycursor, db_connector)
        for cur_destination in cur_toplist["destinations"]:
            destination_id = insert_destination_return_id(cur_destination, mycursor, db_connector)

            mycursor.execute(INSERT_INTO_TandD_TEMPLATE % (toplist_id, destination_id))
            db_connector.commit()

            if "attractions" in cur_destination.keys():
                for cur_attraction in cur_destination["attractions"]:
                    attraction_id = insert_attraction_return_id(cur_attraction, mycursor, db_connector)

                    mycursor.execute(INSERT_INTO_DandA_TEMPLATE % (destination_id, attraction_id))
                    db_connector.commit()

                    if "reviews" in cur_attraction.keys():
                        for cur_review in cur_attraction["reviews"]:
                            review_id = insert_reviews_return_id(cur_review, mycursor, db_connector)

                            mycursor.execute(INSERT_INTO_AandR_TEMPLATE % (attraction_id, review_id))
                            db_connector.commit()


if __name__ == "__main__":
    mydb = mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        passwd="chatbot5125",
        database="trip_info"
    )

    trip_info = read_json_as_dict("./dataset.json")
    database_init(mydb, trip_info)
