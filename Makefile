dc_app = docker-compose -f docker-compose.yml

up:
	${dc_app} up -d
down:
	${dc_app} down
logs:
	${dc_app} logs -f
heroku_deploy:
	heroku create job-checker-app
	heroku container:push job_checker
	heroku container:release job_checker 
	heroku ps:scale job_checker=1
heroku_destroy:
	heroku apps:destroy --app job-checker-app --confirm job-checker-app
	heroku container:rm job-checker-app