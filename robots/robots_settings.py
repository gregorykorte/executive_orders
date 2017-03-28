
class settings:

	# Scrape settings
	multitask = False					# Use multiprocessing for scraping RSS?
	multitask_threads = 5
	http_timeout = 30.0					# How long to wait for http requests
	file_temp_path = ''					# Set a temporary path for working with PDFs (i.e., /data/pacer)
	file_archive_path = ''				# Set a folder to archive downloaded PDFs (i.e., /data/pacer/archive)
	max_files_to_scrape = 10

	# Database settings (MySQL server)
	db_host = ''						# MySQL host name
	db_user = ''						# MySQL username
	db_pass = ''						# MySQL password
	db_port = 3306						# MySQL port

	
	# Twitter credentials
	twitter_app_key = ''
	twitter_app_secret = ''
	twitter_oauth_key = ''
	twitter_oauth_secret = ''

