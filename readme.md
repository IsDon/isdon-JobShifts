# isdon-JobShifts
###Contract / Casual Staff Shift Filling application base in Django / React

This is a simple first pass at a tiered list (nested queries) which allows adding Jobs, Shifts per Job, Positions/Roles per Shift and then opening them up (smartphone/email notifications eventually) for Staff to verify Availability then Admin Staff auto-fill or chose which staff to fill each slot (not implemented), built as a few seperate django apps for interchangeability of each part.

## Installation

1. setup files in a directory
2. establish virtual environment <virtualenv> from parent folder recommended
3. in \reactEx project folder:
4. npm install		(install npm packages from package.json)
5. pip install -r requirements.txt  (install pypi packages)
6. replace django.js package url with file contents 'djangojs.replacement.urls.py'
7. python manage.py migrate
8. python mange.py createsuperuser
9. npm run build
10. add host url to ALLOWED_HOSTS
11. python manage.py runserver

## Usage

If you modify js, jsx or css, re-build with webpack, default config file in reactEx folder.    (shortcut is npm run build)
For testing, /forceadmin/ will load admin interface and /forceuser/##/ will load as user (not implemented Apr 2017 - Mock UI for both admin + users coming)

## Contributing

1. At this point this is just an experiment for me - but if you want to take it further or use it for whatever purpose, go for it:   Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request, and I'll see about bringing it back in :D

## History

Apr 2017: Added second app (Responses) for staff to propose Availability/ Unavailable per Role.

Apr 2017: Build basic 3 tier Job/Shift/Role functionality

## Credits

Don Bloomfield

## License

MIT licence for general use (credit), contact me for anything else you need.




