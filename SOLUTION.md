**🚧 UNDER CONSTRUCTION**

Sections to Detail:

Stack

1. Django + Django REST Framework
2. React + Vite + TS
3. Procfile + Overmind (Don't want to limit it to Heroku) for convenience
4. Why a monorepo?
5. What is just for?
6. Why is `rest_api` a separate package?
7. Why do we use UUIDs instead of sequential integer IDs?
8. Why a strategy pattern?
9. Why is the XML parsing strict?

- Can use Sentry in the future to detect new formats.

10. Why are there no transformations of data from the return itself? For example,
    the app doesn't standardize the URL to something like WWW.JUSTICEFUNDERS.ORG -> "https://www.justicefunders.org"

- We should be able to refer to our own Database any time we want to get the value
  of the return AS WRITTEN. That way, the database is a source of truth for the return.
- We want to store the EXACT return information without making assumptions about its
  correctness or intended format.
- We can always create a presentation layer that changes the data, but transforming
  and storing it already "dirties up" the data.
