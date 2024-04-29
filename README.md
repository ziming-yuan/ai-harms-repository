# AI Harms Repository

This is a website built with flask and Bootstrap 5. It uses news and reddit apis to fetch Deepfake-related content for research on AI harms.

## Overview

1. Login page:

![image](./res/Login.png)

2. Fetch new data from api endpoint again:

![image](./res/Interface.png)

3. Mannually add entries:

![image](./res/Manual-Add.png)

4. Edit notes of entries:

![image](./res/Edit-Notes.png)

5. Filter contents based on criteria with pagination:

![image](./res/Filter.png)

## Getting started

1. Create a virtual environment and source it:

   ```
   python -m venv .venv
   source .venv/bin/activate
   source .env
   ```

2. Install packages:

   ```
   pip install -r requirements.txt
   ```

3. Running:

   ```
   python manage.py run
   ```

## Notes

User authentication is implemented based on [tutorial](https://www.freecodecamp.org/news/how-to-setup-user-authentication-in-flask/) by Ashutosh Krishna.
