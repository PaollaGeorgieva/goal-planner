# Goal Planner


**Goal Planner** is a web application for creating personal goals, organizing the steps needed to achieve them and tracking progress over time.

The application supports two types of goals:

* **Target goals** — goals with a specific end date that can be divided into smaller steps.
* **Habit goals** — recurring activities tracked through daily or weekly check-ins.

## Features

### Goal Management

* Create, edit and delete personal goals
* Organize goals into custom categories
* Search and filter goals
* Mark goals as completed
* Track goal progress

### Target Goals

* Set a start date and an end date
* Divide a goal into smaller steps
* Add, edit, complete and delete steps
* Calculate progress based on completed steps

### Habit Goals

* Set daily or weekly targets
* Record habit check-ins
* Track progress for the current period
* Follow the current activity streak

### Notes

* Add notes to both target goals and habits
* Attach images to notes
* Edit and delete existing notes

### User Accounts

* Registration and login with email
* Personal user profiles
* Profile picture and personal information
* Password management
* Optional Google authentication

### REST API

The project also provides API endpoints for working with goals, habits and goal steps through Django REST Framework.

## Technology Stack

* **Python**
* **Django**
* **Django REST Framework**
* **PostgreSQL**
* **Django Allauth**
* **HTML**
* **CSS**
* **JavaScript**
* **Pillow**

## Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/PaollaGeorgieva/goal-planner.git
cd goal-planner
```

### 2. Create a virtual environment and install dependencies

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure environment variables

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Edit `.env` to add your credentials and a secret key.

#### Generating a Django `SECRET_KEY`

You can generate a new secret key by running:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Paste the output into your `.env` file under `DJANGO_SECRET_KEY`.

### 4. Social Authentication Setup

In your Django settings file (e.g., `settings.py`), locate and configure the following provider section (note that the `APP` blocks are commented out by default):

```python
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
        # Uncomment the APP block below to enable Google login:
        # 'APP': {
        #     'client_id': config('GOOGLE_CLIENT_ID'),
        #     'secret': config('GOOGLE_SECRET_KEY'),
        #     'key': ''
        # }
    }
}
```

#### Google

To enable Google login:

1. Create a Google Cloud project and configure OAuth 2.0 credentials.
2. Add your credentials to `.env` as `GOOGLE_CLIENT_ID` and `GOOGLE_SECRET_KEY`.
3. Uncomment the `APP` block under `google` in `SOCIALACCOUNT_PROVIDERS`.
4. In `templates/accounts/register.html` and `templates/accounts/login.html`, uncomment:

```html
<a href="{% provider_login_url 'google' %}" class="btn btn-google">
    <span class="google-circle"></span>
    <span>Google</span>
</a>
```

Remove any unnecessary placeholder buttons such as:

```html
<a href="#" class="btn btn-google">
    <span class="google-circle"></span>
    <span>Google</span>
</a>
```


### 5. Run migrations

```bash
python manage.py migrate
```

### 6. Create a superuser (optional)

```bash
python manage.py createsuperuser
```

### 7. Run the development server

```bash
python manage.py runserver
```

## Project Structure

```text
goal-planner/
├── accounts/       # User accounts and profiles
├── api/            # REST API endpoints
├── common/         # Landing page and shared functionality
├── goals/          # Target goals, habits and categories
├── notes/          # Notes and image attachments
├── steps/          # Target goal steps
├── templates/      # Django HTML templates
├── static/         # CSS, JavaScript and images
├── GoalPlanner/    # Main project configuration
├── manage.py
└── requirements.txt
```



