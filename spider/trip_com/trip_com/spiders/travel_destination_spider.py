import json
import scrapy
from scrapy.spiders import CrawlSpider

"""
command: scrapy crawl TravelDestinationSpider -o trip_data.json
"""


class TravelDestinationSpider(CrawlSpider):
    name = "TravelDestinationSpider"
    custom_settings = {'HTTPERROR_ALLOW_ALL': True}

    def start_requests(self):

        url = "https://www.trip.com/travel-guide/inspiration-list/"
        yield scrapy.Request(url, self.inspiration_parser)

        # url = "https://www.trip.com/travel-guide/toplist-569/"
        # yield scrapy.Request(url, self.toplist_parser)

        # url = "https://www.trip.com/travel-guide/takamatsu-56911/"
        # url = "https://www.trip.com/travel-guide/margaret-river-1606/"
        # yield scrapy.Request(url, self.destination_parser)

        # url = "https://www.trip.com/travel-guide/margaret-river-1606/tourist-attractions/"
        # yield scrapy.Request(url, self.attractions_parser)

        # url = "https://www.trip.com/travel-guide/margaret-river/margaret-river-80816/"
        # yield scrapy.Request(url, self.attraction_parser)

    def inspiration_parser(self, response, **kwargs):

        toplists = response.css('[class="jsx-3344324880 toplist-content"]')
        toplist_items = list()
        for cur_toplist in toplists:
            name = cur_toplist.css('[class="jsx-3344324880 title"]')\
                .css('a.jsx-3344324880::text').get()
            link = cur_toplist.css('[class="jsx-3344324880 more-icon"]')\
                .css("a.jsx-3344324880::attr(href)").get()
            toplist_info = {"name": name, "link": link}
            toplist_items.append(toplist_info)
            yield scrapy.Request(link, self.toplist_parser, meta={"inspiration": name})

        yield {"inspirations": toplist_items, "type": "inspirations"}

    def toplist_parser(self, response, **kwargs):

        res = dict()
        res["type"] = "toplists"
        res["inspiration"] = response.meta["inspiration"]
        res["destinations"] = list()
        destination_list = response.css('[class="jsx-946890623 item"]')

        for cur_destination in destination_list:

            cur_destination_info = dict()

            cur_destination_name = cur_destination.css('[class="jsx-946890623 content-title"]')\
                .css("a.jsx-946890623::attr(title)").get()

            cur_destination_link = cur_destination.css('[class="jsx-946890623 content-title"]') \
                .css("a.jsx-946890623::attr(href)").get()

            cur_destination_description = cur_destination.css('[class="jsx-946890623 content-p"]::text').getall()

            cur_destination_info["name"] = cur_destination_name
            cur_destination_info["link"] = cur_destination_link
            cur_destination_info["description"] = cur_destination_description

            res["destinations"].append(cur_destination_info)

            yield scrapy.Request(cur_destination_info["link"], callback=self.destination_parser,
                                 meta={"toplist": res["inspiration"]})

        yield res

    def destination_parser(self, response, **kwargs):
        destination = dict()
        destination["type"] = "destination"
        destination["toplist"] = response.meta["toplist"]

        loc_items = response.css('[class="gl-component-bread-crumb_item"]')
        loc_list_tmp = list()
        for item in loc_items:
            if item.css("a.gl-component-bread-crumb_item::text").get():
                loc_list_tmp.append(item.css("a.gl-component-bread-crumb_item::text").get())
            elif item.css('[class="gl-component-bread-crumb_item"]::text').get():
                loc_list_tmp.append(item.css('[class="gl-component-bread-crumb_item"]::text').get())
        loc_tags = ", ".join(loc_list_tmp[2:])
        destination["name"] = loc_list_tmp[-1]
        destination["loc_tags"] = loc_tags
        nav_modules = response.css('[class="nav-a-module"]')
        navigation = dict()

        for cur_nav in nav_modules:
            cur_nav_name = cur_nav.css("::attr(title)").get()
            cur_nav_link = "https://www.trip.com" + cur_nav.css("::attr(href)").get()
            navigation[cur_nav_name] = cur_nav_link

        destination["navigation"] = navigation

        yield scrapy.Request(navigation["Attractions"], self.attractions_parser, meta={"destination": destination["name"]})

        yield destination

    def attractions_parser(self, response, **kwargs):
        attractions_list = response.css('[class="burited_point "]')
        attractions = dict()
        attractions["type"] = "attractions"
        attractions["attractions"] = list()
        attractions["destination"] = response.meta["destination"]
        for cur_attraction in attractions_list:
            if not cur_attraction.css("[class='mt16']::attr(title)").get():
                continue
            name = cur_attraction.css("[class='mt16']::attr(title)").get()
            link = cur_attraction.css("[class='mt16']::attr(href)").get()
            attractions["attractions"].append({"name": name, "link": link})
            yield scrapy.Request(link, self.attraction_parser, meta={"destination": attractions["destination"]})

        yield attractions

    def attraction_parser(self, response, **kwargs):
        loc_items = response.css('[class="gl-component-bread-crumb_item"]')
        loc_list_tmp = list()
        for item in loc_items:
            if item.css("a.gl-component-bread-crumb_item::text").get():
                loc_list_tmp.append(item.css("a.gl-component-bread-crumb_item::text").get())
            elif item.css('[class="gl-component-bread-crumb_item"]::text').get():
                loc_list_tmp.append(item.css('[class="gl-component-bread-crumb_item"]::text').get())
        loc_tags = ", ".join(loc_list_tmp[2:])
        name = response.css('[class="poi-page-title"]::text').get()
        open_status = response.css('[class="POITopInfo-sc-1jsox87-12 hYTUea clickable"]')\
            .css("div.one-line")\
            .css("span.field::text").get()
        recommended_sightseeing_time, phone = response.css('[class="POITopInfo-sc-1jsox87-12 hYTUea"]')\
            .css("div.one-line")\
            .css("span.field::text").getall()
        address = response.css('[class="address"]').css("div.one-line").css("span.field::text").get()

        reviews = response.css('[class="TripReviewItemContainer-mgadbi-0 fizkZA review-item"]')
        reviews_list = [cur_review.css("div.gl-poi-detail_comment-content").css("a").css("p::text").get()
                        for cur_review in reviews]

        attraction_info = {
            "type": "attraction",
            "destination": response.meta["destination"],
            "loc_tags": loc_tags,
            "name": name,
            "open_status": open_status,
            "recommended_sightseeing_time": recommended_sightseeing_time,
            "phone": phone,
            "address": address,
            "reviews": reviews_list
        }

        yield attraction_info
