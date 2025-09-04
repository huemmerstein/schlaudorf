# Village Chat (Django Edition)

This project provides a simple community chat platform built with the
[Django](https://www.djangoproject.com/) web framework and styled with
[Bootstrap&nbsp;5](https://getbootstrap.com/).  It offers a public chat room for the
whole village and one‑to‑one direct messages that are automatically deleted
after two days.

## Features

- ✅ Open source under the MIT license
- ✅ User registration and login using Django's authentication system
- ✅ Village‑wide chat room
- ✅ Direct messages that expire after 48 hours
- ✅ Responsive interface thanks to Bootstrap 5
- ✅ Real‑time updates via WebSockets (Django Channels)
- ✅ Browser notifications for new direct messages
- ✅ Message search and filtering
- ✅ Neighborhood help offers on an interactive map
- ✅ Share offers directly in the chat
- ✅ User profiles with optional avatars, bio and contact info
- ✅ Automated tests and GitHub Actions CI
- ✅ Admin approval required before posting
- ✅ Encrypted direct messages and profile data
- ✅ Customizable help offer categories via `OFFER_CATEGORIES`

## Installation on Ubuntu

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd schlaudorf
   ```
2. **Run the installation script**
   ```bash
   bash install.sh
   ```
3. **Start the development server**
   ```bash
   source venv/bin/activate
   python manage.py runserver
   ```
4. Open <http://127.0.0.1:8000> in your browser and register a user.

The default configuration uses SQLite for easy local development.  To deploy
with MariaDB (social features) and PostgreSQL/PostGIS (geodata), set the
environment variable `USE_SQLITE=0` and provide database credentials via the
`MYSQL_*` and `POSTGRES_*` environment variables.  Direct messages and profile
fields are encrypted using a key derived from `SECRET_KEY`.

To adapt the list of help categories for your village, edit the
`OFFER_CATEGORIES` setting in `village/settings.py`.

## Managing Content

- Visit <http://127.0.0.1:8000/admin/> to access Django's admin interface.
  Create a superuser with `python manage.py createsuperuser` for full access.
  New users must be marked as approved in the Profile section before they can
  post in chat or create offers.
- Messages older than two days are cleaned up automatically each time the
  direct message view is accessed.
- Create help offers via the Offers page and share them in chat.

## Development Notes

The code is heavily commented to help newcomers.  Key files:

- `chat/models.py` – database models for public and private messages
- `chat/views.py` – view logic for chat interactions and user registration
- `templates/` – Bootstrap‑based HTML templates

## Ideas for Improvement

- WebSocket chat rooms beyond the global room
- Offline storage for messages in the browser
- Better moderation tools

Contributions are welcome!  Feel free to open issues or pull requests to help
make the project better.
