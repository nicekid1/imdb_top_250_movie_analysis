IMDb Top 250 Movies Data Analysis
Project Overview

This project focuses on analyzing the IMDb Top 250 Movies dataset.
The data was scraped directly from the web using custom crawlers built with BeautifulSoup (bs4) and Selenium, and then analyzed and visualized using Power BI and Excel dashboards.

The goal of the project is to uncover insights about the top-rated movies, including top actors, directors, genres, and trends across decades.

Tools and Technologies
Purpose	Tool / Library
Web Scraping	BeautifulSoup, Selenium
Data Cleaning	Pandas, Excel
Visualization & Dashboarding	Power BI, Excel Charts
Data Source	IMDb Top 250 Movies Page
Data Collection Process

Web Crawling:

A custom Python crawler was created using BeautifulSoup for static HTML parsing.

Selenium was used for dynamic content extraction (for example, loading additional movie details such as box office, cast, or genres).

Data Export:

The extracted data was cleaned and saved in CSV and Excel formats for visualization.

Dashboard Creation:

The cleaned dataset was imported into Power BI and Excel to build interactive analytical dashboards.

Key Analytical Insights

The dashboards visualize and analyze the following aspects of the dataset:

Top 10 highest-grossing movies

Number of movie ratings

The best movie of every decade

Five most prolific actors

Best-selling movies by genre

Ten writers with the most films on the list

Ten directors with the most films on the list

Number of occurrences of each genre

The highest-grossing movies of each year

Insights Examples

Certain genres such as Drama and Action dominate the Top 250 list.

Directors like Christopher Nolan and Steven Spielberg have multiple entries in the top 10.

The 1990s and 2000s decades contribute the most films to the list.

Several actors appear in multiple top-rated films, showing recurring collaboration trends.
