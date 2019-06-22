# IdealSpot

Version - 0.1.0

Trying to plan an outdoor adventure but have too many options? Is researching weather
for all your sweet spots a major pain? Do you know a little bit of Python?

**Problem Solved!**

IdealSpot accesses public data APIs to gather different types of data important
for planning and choosing an ideal location for your outdoor journeys. Data is
gathered, analyzed and transformed to automate scoring and reporting of all
your favorite spots based on your exact needs.

## Features

_In Production_

- **Generate spots using lat / long coordinates**
- **Score each location using customized targets**
- **Weather targets using free OpenWeatherMaps API**
    - Ideal temperature target
    - Ideal wind target
    - Ideal cloud target
    - Rain accumulation target
    - Snow accumulation target
- **Generate score summary report for each spot**

_Future Features_

- **Generate automated forecast reports for spots**
- **Map visualization for scores for spots**
- **Other types of non-weather targets**
    - Campsites / Trails
    - Resort proximity
    - Transportation infrastructure

## Quick Start Guide

Generating scores / data requires three major steps below:

- **Step 0:** Obtain free API key at openweathermap.org by opening a free account
- **Step 1:** Generated Spot classes for each lat / long combination
    - Each Spot should have a string name as an identifier
    - Spot classes can be initialized manually or generated from a pandas DataFrame
- **Step 2:** Build customized WeatherTarget using decorator options
    - Customization is enabled by utilizing a decorator pattern on the
    WeatherTarget base class
- **Step 3:** Utilize static methods of EvaluateSpots class to score spots and
generate reports

Examples can be found in the **examples** folder.
