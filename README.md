# What is this app?

This app analyzes public filings to the IRS of non-profit companies in the US.

# How do I set this up?

There are many ways to set up Django + Vite/React apps. The approach below details what I've found works consistently. If there are any issues, please let me know!

## Prerequisites

- `python` 3.14.2
- `nodejs` 24.12.0 with `npm`
- `poetry` 2.2.1
- `postgresql` 17
- Redis with `redis-server` 8.2.2

You'll notice that there are other tools included in `.tool-versions` like `just`. Overmind files are also present in the codebase. Those are just for developer experience purposes and are not required to set up the app.

> 📝 Commands below are written for `zsh` shells. Consult your terminal documentation for equivalent commands.

> 📝 Commands below assume the use of a Linux or macOS system. Consult Windows documentation for equivalents.

> 🚨 **IMPORTANT**: The backend and frontend servers should be running in separate terminals at the same time while accessing the app.

## Set up the backend

The backend is built with a combination of Django and Django REST Framework to serve the API. There are a few associated libraries, but these are the main frameworks. I prefer using `poetry` for dependency management, but the project is generally agnostic. What matters is you can install `python` libraries with no conflicts and run `python` commands that can see those libraries.

The API uses `celery` to run asynchronous tasks such as downloading ZIP files. You will need `redis` in order to get this to work so please make sure you have it installed in your platform.

1. Go to the backend app's directory.

```zsh
% cd irs_returns/
```

2. Create a new virtual environment and install the python dependences

```zsh
% poetry install  # This will create a virtual environment and install dependencies at once
```

3. `poetry install` will also automatically activate the virtual environment. If it doesn't for some reason, you can run the command returned by `poetry env activate`.

```zsh
% poetry env activate
source /your/absolute/path/to/the/environment/irs-tax-exempt-filing-analyzer/.venv/bin/activate

# Copy paste the above and execute it.
% source /your/absolute/path/to/the/environment/irs-tax-exempt-filing-analyzer/.venv/bin/activate
```

Alternatively, you can shorten it to this (note: this is for `zsh` shells).

```zsh
% eval $(poetry env activate)
```

4. Create a `.env` from the `.env.example` file and fill in the required environment variables

```zsh
cp .env.example .env
```

📝 Notes:

- You likely don't need to touch the `OVERMIND_PROCFILE` env var if it's indicated in the `.env` file.
- The `DATABASE_URL` should be the connection string of your Postgres database.
- If you need a `DJANGO_SECRET_KEY`, you can go to [https://djecrety.ir/](https://djecrety.ir/) to quickly generate one.

5. Run the Django migrations

```zsh
% python manage.py migrate
```

6. Create a super user so you can generate an API key in the admin panel

```zsh
% python manage.py createsuperuser
# Follow the instructions...
```

7. Run the server!

```zsh
% python manage.py runserver
```

8. Set up an API key by going to `localhost:8000/admin/`. Log in with the user you created in step 6. On the page that appears, click on the "+ Add" button beside "API Key Permissions" > "Api Keys". Fill up the form. Once it's saved, you will be redirected back to the list page _with your API key listed at the top. You MUST copy this now or else you'll never see it again._

9. In another terminal, activate the virtual environment again and run `celery`. This runs the downloading and parsing of ZIP files in an asynchronous task as this process can take a while.

```zsh
# In another terminal
% eval $(poetry env activate)
% celery -A core worker -l INFO
```

You may set `-l` to `DEBUG` if you need more verbosity in the messages.

## Set up the frontend

1. Set up `nodejs` if you haven't yet. The easiest way to set this up is using `nvm` or `asdf`. You can also just install it directly from [the NodeJS webpage](https://nodejs.org/en/download). Make sure you use the right version as indicated in the prerequisites above.

> [Here](https://github.com/nvm-sh/nvm) are the `nvm` docs for setting it up using NVM. [Here](https://asdf-vm.com/guide/getting-started.html) are `asdf` docs for setting it up using asdf.

2. In another terminal, go to the frontend directory.

```zsh
# If coming from the backend
% cd ../irs-returns-frontend

# If from the root directory
% cd irs-returns-frontend/
```

3. Install the dependencies using `npm`

```zsh
% npm install
```

4. Run the server

```
npm run dev
```

# General Information

To make requests to the API, you can use an app like Postman or just use cURL. I recommend using Postman so you can easily introspect the response as it formats it for you.

**Endpoints:**

1. GET localhost:8000/companies (public)
2. GET localhost:8000/companies/<:uuid> (public)
3. POST localhost:8000/dataset (requires an API key)
   - Body params: `zip_url`

**Using an API key:**

With the API key you got in the backend set up, you can use it by including it as a request header. The key should be `Authorization` and the value should be `Api-Key <your api key>`. DO NOT FORGET THE "Api-Key" in front of your actual API key value.

**Other Notes:**

When downloading and analyzing a ZIP file from the IRS, you will see a lot of messages related to Skipping XML files in the celery terminal. **This is normal and expected.** That's because not all the form types have been implemented yet, but the scaffold for implementing them is there. More information can be found in the SOLUTION.md file in this repository.
