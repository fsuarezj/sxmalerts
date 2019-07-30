import scrapy

class ForecastSpider(scrapy.Spider):
    name = "forecast"

    start_urls = [
        'http://www.meteosxm.com/weather/forecast/'
    ]

    def _parse_paragraphs(self, data, i, name):
        result = ''
        if data[i].xpath('.//strong[contains(., "' + name + '")]'):
            # If it's not in the same address block
            if not data[i+1].xpath('./text()').re('\xa0'):
                result = data[i+1].xpath('./text()').get()
                i += 1
            # If it's in the same address block
            else:
                result = data[i].xpath('./text()').get()
            # If it's multiparagraph (multiple address blocks)
            while not data[i+1].xpath('./text()').re('\xa0'):
                i += 1
                result += data[i].xpath('./text()').get()
        return result

    def parse(self, response):
#        print(response.body)
        forecast_info = {}
        data = response.xpath('//div[@class="postcontent"]/address')
        for i in range(len(data)):
            # WEATHER
            summary = self._parse_paragraphs(data, i, "WEATHER")
            if summary: forecast_info['summary'] = summary
            # SURFACE WINDS
            sf_winds = self._parse_paragraphs(data, i, "SURFACE WINDS")
            if sf_winds: forecast_info['sf_winds'] = sf_winds
            # SYNOPSIS
            synopsis = self._parse_paragraphs(data, i, "SYNOPSIS")
            if synopsis: forecast_info['synopsis'] = synopsis
            #if data[i].xpath('.//strong[contains(., "SYNOPSIS")]'):
            #    forecast_info['synopsis'] = ''
            #    while not data[i+1].xpath('./text()').re('\xa0'):
            #        i += 1
            #        forecast_info['synopsis'] += data[i].xpath('./text()').get()
        print(forecast_info)
        return forecast_info
