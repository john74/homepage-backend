# Thikee Backend

Welcome to the backend repository of Thikee. This repository contains the django-based backend code responsible for creating a personalized homepage with bookmark management and weather data integration.

## Project Overview

Thikee allows users to:
- Search the web using predefined search engines or add new search engines.
- Organize bookmarks into categories.
- Create shortcuts for quick access to bookmarks.
- Access current weather data and forecasts.

## Todo List

1. Refactor the codebase for better maintainability.
2. Add docstrings and unit tests
3. Implement a notes app allowing users to create personal notes, with the capability to set email notifications for specific times.
4. Develop a news aggregator app enabling users to consolidate articles from their favorite websites in a single location.
5. Build a social media aggregator app allowing users to view the latest posts from their favorite accounts in a centralized feed.

## How to Run

Follow these steps to set up and run the project locally:

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt

2. **Run migrations:**
   ```bash
   python manage.py migrate

3. **Create a superuser:**
   ```bash
   python manage.py createsuperuser

4. **Run the server:**
   ```bash
   python manage.py runserver

Open your web browser and navigate to http://localhost:8000/admin to access the admin area