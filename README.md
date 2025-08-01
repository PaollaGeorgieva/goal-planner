# Django Project Setup Guide

## 1. Clone the repo

```bash
git clone https://github.com/PaollaGeorgieva/goal-planner.git
cd goal-planner
```

## 2. Create a virtual environment and install dependencies

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 3. Configure environment variables

* Copy `.env.example` to `.env`:

  ```bash
  cp .env.example .env
  ```

* Edit `.env` to add your credentials and a secret key.

### Generating a Django `SECRET_KEY`

You can generate a new secret key by running:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Paste the output into your `.env` file under `DJANGO_SECRET_KEY`.

## 4. Social Authentication Setup

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
    },
    'facebook': {
        'METHOD': 'oauth2',
        'SCOPE': ['email', 'public_profile'],
        'FIELDS': [
            'email',
            'name',
            'first_name',
            'last_name',
            'picture',
        ],
        # To enable Facebook login, uncomment the APP block and ensure your keys are in .env:
        # 'APP': {
        #     'client_id': config('FACEBOOK_CLIENT_ID'),
        #     'secret': config('FACEBOOK_SECRET_KEY'),
        #     'key': ''
        # }
    }
}
```

* **Google**: To enable Google login:
  1. Create a Google Cloud project and configure OAuth 2.0 credentials.
  2. Add your credentials to the .env file as GOOGLE_CLIENT_ID and GOOGLE_SECRET_KEY..
  3. Uncomment the APP block under 'google' in SOCIALACCOUNT_PROVIDERS.
  4. In `templates/accounts/register.html` and `templates/accounts/login.html`, **uncomment** the following block to enable the Google login button:
    ```html
    <a href="{% provider_login_url 'google' %}" class="btn btn-google">
        <span class="google-circle"></span> <span>Google</span>
    </a>
    ```
   **Remove** any unnecessary placeholder buttons like:
    ```html
    <a href="#" class="btn btn-google">
        <span class="google-circle"></span> <span>Google</span>
    </a>
    ```

* **Facebook**: To enable Facebook login:

  1. Create a Facebook App and obtain your App ID & App Secret.
  2. Add them to your `.env` as `FACEBOOK_CLIENT_ID` and `FACEBOOK_SECRET_KEY`.
  3. **Uncomment** the `APP` block under `'facebook'` in `SOCIALACCOUNT_PROVIDERS`.
  4. In `templates/accounts/register.html` and `templates/accounts/login.html`, **uncomment** the following block to enable the Facebook login button:
    ```html
    <a href="{% provider_login_url 'facebook' %}" class="btn btn-facebook">
        <i class="fab fa-facebook-f"></i> <span>Facebook</span>
    </a>
    ```
   **Remove** any unnecessary placeholder buttons like:
    ```html
    <a href="#" class="btn btn-facebook">
        <i class="fab fa-facebook-f"></i> <span>Facebook</span>
    </a>
    ```

* **Disable Facebook**: If you prefer **not** to use Facebook login, **leave the `APP` block commented** or **comment out** the entire `'facebook'` entry:

  ```python
  # 'facebook': {
  #     'METHOD': 'oauth2',
  #     'SCOPE': ['email', 'public_profile'],
  #     'FIELDS': [...],
  #     # 'APP': { ... }
  # },
  ```
  Do the same for Google if you don't intend to use it.



## 5. Run migrations

```bash
python manage.py migrate
```

## 6. Create a superuser (optional)

```bash
python manage.py createsuperuser
```

## 7. Run the development server

```bash
python manage.py runserver
```


