This document details the architectural principles and decisions behind this project.

# Core Principles

This project was built with a two core principles in mind.

## Production Ready

Although this project is not 100% deployable to production, it was designed and developed with the same libraries, technologies, and techniques that I would use in a production project.

For example:

1. We use asynchronous workers (celery) to download, parse, and extract information from ZIP files. While it could've been synchronous with a longer request timeout limit, this is the standard way to do long-running tasks.
2. We use Postgresql as the database because it is quite extensible and good for transactional operations such as reading, writing, and updating which is what this project is mostly about.
3. Design patterns to improve extensibility are implemented in various places. For example, the IRS Form parsers are implemented with a Strategy pattern. If we wanted to add another form type, it's just a matter of writing a new, relatively simple subclass with a parsing function and integrating it into the main class. It's as simple as adding the class to an array.

The project itself is not completely deployable in this state. This means you can't just put it up on a server, run `python manage.py runserver` and expect it to run properly. It could, yes, but that's not the recommended way. "Production Ready' in this case means that the developer experience and the deployment experience is not far off from what you would see in an actual live codebase.

## Guided by Experience

The stack I've chosen here is not only a case of, "This is what I'm used to." In fact, some parts of this stack are relatively new to me (Tanstack Query for example). My reasoning for choosing this stack is guided by both good and bad experiences with frameworks I've tried.

For example:

1. Django has been battle-tested by me in the past, and I've found its batteries-included approach is perfect for quickly boostrapping applications while still being able to scale them.
2. I used an SPA because I've had some terrible experiences with using SSR frameworks. In an app like this, some SSR frameworks might actually be good because the pages are mostly static. However, in an app that will eventually become highly dynamic with a lot of routes that won't render in exactly the same way, I thought it best to use an SPA. You'll find more about the tradeoffs below.

# The Stack

## Backend

The backend uses the following. Within each point, I will explain the reasoning for its choice.

1. Django
   - This framework is battle-tested and batteries-included. The latter means that it already includes most things an app would need such as user authentication, an admin panel, and an ORM.
   - Because of this, it's excellent for quickly prototyping applications. However, I've found that the applications are still quite scalable. There are always "opt-outs" or alternative ways to do them that aren't restricted by Django if necessary.
2. Django REST Framework
   - The de facto REST API framework to match with Django. I chose this because it mirrors Django's ORM quite closely, and it even allows you to easily map between ORM types and API data through concepts like `ModelSerializer`.
   - Authentication is also easy to extend. In this case, I used `djangorestframework-api-key` to easily add simply API key authentication to the app. It pretty much worked out of the box with minimal configuration.
3. Celery
   - This is a Python library for managing background and asynchronous tasks. I specifically chose it because it's a very mature library and can accommodate both simple and complex use cases which is important as an application grows.

## Frontend

1. React
   - One of the most popular libraries for frontend web development, but I chose it not because of its popularity but because of the developer experience.
   - It's difficult to use React when you're first getting familiar with it, but once you're used to reading JSX, components, and hooks, state management becomes incredibly easy. Most of the complexity in frontend development, in my opinion, is in state management, and React handles that exceptionally.
   - The tradeoff would be that if someone were not familiar with React, the use of JSX could be offputting and quite foreign so onboarding someone new is not going to be trivial.
   - Another tradeoff is that since React on its own is just a library rather than a framework, it's not as "batteries-included" as Django. There are indeed React frameworks that are more opinionated such as NextJS.
   - I decided to use React on its own in this case because it allows me to structure the frontend in a more flexible way, and even then, with the use of the other libraries below and Vite, there's a good amount of choices that are already made for the developer.
2. Vite

   - I've found Vite to be an incredibly fast build tool. They're not exaggerating when they say it's "blazingly fast". Development server hot reloads take less than a second, and even production builds are very fast as well.
   - To be honest though, this is my first time using a React + Vite set up, so I've yet to see the downsides of this. I see there are plugins for the major libraries and systems that would be used so perhaps this depends on the specific set up that you have.

3. Tanstack Ecosystem (Tanstack Query, Tanstack Table, Tanstack Router)

   - The Tanstack ecosystem of libraries is a bit newer in the developer space (at least for me), but I've had a good experience with using Tanstack Table. Its headless UI approach means that styling the table is incredibly easy as it's easy to align with whatever design system we have in mind. The tradeoff is that it's hard to understand at first because it's a different paradigm.
   - Tanstack Query and Tanstack Router have both been very easy to use. In particular, Tanstack Router somewhat mirrors NextJS's directory/file-based routing approach. I've used NextJS in the past so this was pretty familiar to me.
   - Another BIG reason I used Tanstack is because of its backers. The last thing I would want for the major libraries in a production app is for it to lose support and die. However, Tanstack is backed by big companies like Cloudflare. There's a good chance it'll be safe for a while.

4. Shadcn

   - This is a component library built on top of Radix UI primitives. What I like about this is that it essentially is the "batteries-included" UI kit that React lacks.
   - The React components this provides are very, very customizable and have accessibility in mind so it's good for creating B2C apps.
   - It's also pretty modular. You only take the components you need, and you can build on top of them if needed.
   - One drawback I suppose is that this is NOT a library that you install as a dependency. Shadcn works by you essentially "copy pasting" (in a fancier way) the component's code while including its Radix UI dependency in your `package.json` file. The problem with this is that component fixes on Shadcn's side will require manual implementation or maintenance, but I think the full extensibility and adaptability to any design system is way more important.

## Why a monorepo?

I've found that build, deployments, and CI for monorepos is much, much, much easier compared to split frontend and backend repositories. An example is that when using GraphQL (although it's not used here), it's impossible to have the schemas synchronized between the backend and frontend. This makes zero downtime deployments very difficult to orchestrate.

In the case of this app, we don't use GraphQL, but having a monorepo still makes it easier to orchestrate deployments.

The tradeoff of this is that most developers who will work on the project need to be fullstack or eventually become fullstack. In my opinion though, I think that's pretty much normal and how it should be. Classifying a developer as frontend or backend doesn't quite fit the web development landscape anymore.

# Important Notes

## Out of Scope Items

The following items are out of scope at the moment due to time constraints. I spent a lot of time thinking about how the app should be structured. In the end, I made the mistake of potentially overthinking and not having everything I wanted in the app.

The important thing to note is that each of these items is relatively easy to add. I will indicate in each point how I would add it if I had the time.

1. Key personnel full names and their titles

   - This is simple. It's a matter of inserting the XPath queries for the key personnel inside the individual `XMLParser` strategies. It could be as simple as a few lines of code in the backend, and a simple card component in the frontend.

2. Expenses by category

   - This is a bit more complicated because each Form type has various entries for expenses and they are different across Form types.
   - What I would do is to actually get an annotated form [like this](https://www.irs.gov/pub/irs-tege/2024form990withfieldnames.pdf) and map out each expense record from there.
   - Depending on whether the expense categories are standardized or not, we may need a new `ReturnExpense` model in the backend.
   - Adding the chart is not as hard because it's just a histogram. Most chart libraries have that as a very basic functionality, and the only challenge would be making it mobile responsive. A good library for this is amcharts5.

3. 990T Form Type

   - The parsers for 990PF and 990EZ have been implemented, but I see there's another form type called 990T. It seems to be completely related to taxation and has little information on revenue or expenses so I've decided to leave it alone for now.

4. Staffing Signal and Delta on Employee Headcount
   - As far as I can tell, the 990 returns only have the head count for the current year. If we wanted to implement a previous year comparison, we would need to also get the returns from the previous year.
   - Some form types don't even have a total employee headcount at all. In fact, I don't see this in any form except for 990.

## Parsing Behavior

1. I decided to make the parsing strict, meaning that the XML parser requires an exact match of the key for the data that is being queried. This makes more sense to me at a pre-alpha stage where we want to test whether certain forms have missing fields simply due to incorrect keys or data being inside different keys. In cases where the field cannot be found, a debug log is printed (make sure Celery's log level is set to `DEBUG`).
2. Little to no transformations of the data are performed other than trimming extra whitespace around the value. For example, I don't append `https://` to company website URLs that don't include it and I don't standardize capitalization at the point of parsing the ZIP file. The database of returns that the app has should perfectly mirror what's written on the return as much as possible. Transformations can always be done in the presentation layer, but once a return is stored in the database, we lose the original data if we transform it.
3. This means that transformations on the data occur when the REST API is sending out the values.
4. I use UUIDs as the database primary key to make it harder to guess or enumerate records, improving security.

## Points for Improvement

Other than the items I would've liked to add above:

1. There definitely has to be more robust checking and verification of the data. This application is about data accuracy which means that displaying anything incorrectly would be a nightmare. Automated tests will have to be stringent. I'd love to have automated tests against real XML files or even a real ZIP file to verify that the data is indeed accurate.
2. Some transformations need work. In particular, the transformation to set the mission statement to capital or paragraph case can miss important cases. It will indiscriminately lowercase any acronyms, etc. This is a hard problem to solve and may even require manual verification. Some system needs to be in place to either automatically transform the field data or replace it entirely when presenting it. The database should still keep the original returns data at all times. Perhaps this is something AI can help solve.
3. This app requires more manual testing. I keep seeing and having to handle edge cases regarding how data is displayed in the table and in the details pages. Some intensive manual QA with live data is required to catch as many of these edge cases as possible. Again, automated tests against real XML files would be great as well.
4. The table's implementation is technically not built to handle the future data load of the application. Right now, its searching and sorting are purely client side. This works fine for now where I've got ~40,000 rows because Tanstack is so efficient, but once it starts reaching hundreds of thousands of rows, it will become a problem. The "right" way to do this would be to mix client and server-side searching and pagination. The client will prefetch a large amount of data, and then it will query the server for more records any time some record is not present or if sorting is necessary. Essentially, the client will slowly accumulate more data and query the server less frequently the more the user interacts with the table. It's quite complex to set up which is why I didn't do it here yet.
