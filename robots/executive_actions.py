import dbconnect
import mechanize
from twython import Twython
import md5
import re
from robots_settings import settings

URLS = ['https://www.whitehouse.gov/briefing-room/presidential-actions/presidential-memoranda',
		'https://www.whitehouse.gov/briefing-room/presidential-actions/executive-orders', ]

db = dbconnect.db(host=settings.db_host, user=settings.db_user, pwd=settings.db_pass)
br = mechanize.Browser()
tw = Twython(
	settings.twitter_app_key,
	settings.twitter_app_secret,
	settings.twitter_oauth_key,
	settings.twitter_oauth_secret
)

# 1 - Scrape

for url in URLS:
	br.open(url)
	links = br.links(url_regex = 'the-press-office/\d+/\d+/\d+/')
	check_links = []
	for l in links: check_links.append(l)
	
	for l in check_links:
		h = md5.new(l.text).hexdigest()
		print '-> %s' % h
		
		if db.getOne(""" SELECT COUNT(*) AS C
					FROM government.executive_actions
					WHERE h = %s """, (h, )) == 0:
			
			# New record
			br.open(l.url)
			print '   ADDING NEW ORDER'
			html = br.response().read()
			
			html = re.sub('[\r\n]',' ', html)
			
			t = ''
			TXTPATTERN = re.compile('<div class="field-item even"><p class="rtecenter">(.*?)<\/div>', re.IGNORECASE)
			if TXTPATTERN.search(html):
				t = TXTPATTERN.search(html).group(1)
			br.back()
			
			url = 'http://whitehouse.gov' + l.url
			db.run(""" INSERT INTO government.executive_actions(h, title, t, url) VALUES(%s, %s, %s, %s)""",
				( h, l.text, t, url, ))
			
			# Post it
			
			msg = 'JUST POSTED: ' + l.text[:101] + '\n\nhttp://whitehouse.gov' + l.url
			
			tw.update_status(status = msg)
			
			
