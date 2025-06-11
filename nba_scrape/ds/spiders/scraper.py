import scrapy
import json
from scrapy_splash import SplashRequest

class ScraperSpider(scrapy.Spider):
    name = "scraper"
    allowed_domains = ["www.nba.com"]
    #start_urls = ["https://www.nba.com/schedule?cal=all&pd=false&region=1&season=Regular%20Season"]


    def start_requests(self):
        url = "https://www.nba.com/schedule?cal=all&pd=false&region=1&season=Regular%20Season"
        yield SplashRequest(url, self.parse, args={'wait': 2})

    def parse(self, response):
        for date_section in response.css('section.ScheduleDate_scheduleDateContainer__Kdyce'):
            date = date_section.css('h2.ScheduleDate_date__f3F3D::text').get()
            
            for game in date_section.css('li.ScheduledGame_gameItem__CRjDf'):
                home_team = game.css('div.TeamLogo_teamName__sQdsc.home div.TeamLogo_teamNameText__P9zxx::text').get()
                away_team = game.css('div.TeamLogo_teamName__sQdsc.away div.TeamLogo_teamNameText__P9zxx::text').get()
                home_score = game.css('div.ScheduledGame_score__AruQh.home::text').get()
                away_score = game.css('div.ScheduledGame_score__AruQh.away::text').get()
                game_status = game.css('span.ScheduledGame_gameStatus__U3lkj::text').get()

                yield {
                    'date': date,
                    'home_team': home_team,
                    'away_team': away_team,
                    'home_score': home_score,
                    'away_score': away_score,
                    'status': game_status,
                }
