import aiohttp
import asyncio
import time
import datetime
from bs4 import BeautifulSoup

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def main():

    async with aiohttp.ClientSession() as session:
        html = await fetch(session, 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=C++&location=Paris,+Île-de-France,+France&geoId=&trk=homepage-jobseeker_jobs-search-bar_search-submit&start=200')
        soup = BeautifulSoup(html, 'html.parser')
        list_jobs = soup.find_all('li')
        #jobs creation array to export to excel 
        jobs = []
        for listing_jobs in list_jobs:
            first_job = listing_jobs
            #first_job = list_jobs[0]
            #print(first_job)
            job_description = first_job.find(class_="base-search-card__title").get_text().strip()
            job_enterprise = first_job.find(class_= "base-search-card__subtitle").get_text().strip()
            job_location = first_job.find(class_="job-search-card__location").get_text().strip()
            date = first_job.find('time');
            
            # print(job_description)
            # print(job_enterprise)
            # print(job_location)
            if date.has_attr('datetime'):
                date_time = date['datetime']
                timestamp = time.mktime(datetime.datetime.strptime(date_time,"%Y-%m-%d").timetuple())
                #print(timestamp)

            job = {
                "title": job_description,
                "company": job_enterprise,
                "location": job_location,
                "timestamp": timestamp
            }

            print(job)
            jobs.append(job)
        
loop = asyncio.get_event_loop()
loop.run_until_complete(main())