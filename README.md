# Global Neighbor

A CMS (currently, a blog with comments, forum, and a Bluesky ticker on the homepage) for use by communities. WCAG-compliant for accessibility.

You'll need an `.env` file in the root directory, containing the following:

```bash
DEBUG=True  # False for production
SECRET_KEY=
BASE_URL=http://localhost:8000  # Change for production
PATH_TO_GIT_REPO=/path/to/Global-Neighbor
ALLOWED_HOSTS=localhost,localhost:8000,127.0.0.0:8000  # Add production hosts
EMAIL_BACKEND='django.core.mail.backends.filebased.EmailBackend'  # Change filebased to smtp on production
EMAIL_HOST="smtp.example.com"  # Replace with your SMTP server
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER="your-email@example.com"
EMAIL_HOST_PASSWORD="your-password"
EMAIL_FILE_PATH="./backup/email_dump"
DEFAULT_FROM_EMAIL="Global Neighbor <no-reply@example.com>"
BLUESKY_USERNAME=your-bluesky-username
BLUESKY_PASSWORD=your-bluesky-password

# database configuration
DATABASE_PASSWORD=your-database-password
DATABASE_USER=your-database-owner
DATABASE_NAME=your-database-name
DATABASE_HOST=localhost  # Change for production
DATABASE_URL=postgres://localhost:5432/your-database-name  # Change for production or if using MySQL
DATABASE_PORT=5432  # Change for production or if using MySQL
```
