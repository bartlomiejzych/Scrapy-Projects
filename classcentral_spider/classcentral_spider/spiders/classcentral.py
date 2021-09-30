from scrapy import Spider
from scrapy.http import Request
from time import sleep
from selenium import webdriver
from scrapy.selector import Selector


class ClasscentralSpider(Spider):
    name = 'classcentral'
    allowed_domains = ['classcentral.com']
    start_urls = ['https://www.classcentral.com/subjects']

    def __init__(self, subject=None):
        self.subject = subject
        self.driver = webdriver.Chrome("D:/ScrapyProjects/chromedriver_win32/chromedriver.exe")

    def parse(self, response):
        if self.subject:
            subject_url = response.xpath('//a[contains(@title, "' + self.subject + '")]/@href').extract_first()
            absolute_subject_url = response.urljoin(subject_url)
            yield Request(
                absolute_subject_url,
                callback=self.parse_subject,
                )
        else:
            self.log('Scraping all pages')
            subject_urls = response.xpath('//h3/a[1]/@href').extract()
            for subject_url in subject_urls:
                absolute_subject_url = response.urljoin(subject_url)
                yield Request(
                    absolute_subject_url,
                    callback=self.parse_subject,
                    )

    def parse_subject(self, response):
        self.driver.get(response.url)
        sleep(5)
 
        while True:
            try:
                self.driver.find_element_by_xpath('//button[@data-name="LOAD_MORE"]').click()
                sleep(5)
            except:
                self.log('No more pages to load.')
                break

        sel = Selector(text=self.driver.page_source)

        subject_name = sel.xpath('//h1/text()').extract_first()

        courses = sel.xpath('//*[@class="color-charcoal course-name"]')
        for course in courses:
            course_name = course.xpath('.//*[@itemprop="name"]/text()').extract_first()
            course_url = course.xpath('./@href').extract_first()
            absolute_course_url = response.urljoin(course_url)

            yield{
                'subject_name': subject_name,
                'course_name': course_name,
                'course_url': absolute_course_url,
            }
  

