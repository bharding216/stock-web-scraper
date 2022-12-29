# NASDAQ Stock Web Scraper

## Project Description
The purpose of this project is to collect NASDAQ stock information (from https://www.centralcharts.com/), analyze the data, and produce a bar chart of the top 10 companies by trading volume. The program also exports the scraped data to a CSV file for personalized analysis. 

The motivation behind this project was to get some experience using web scraping in combination with the Pandas and Matplotlib libraries. The project is useful because it automatically produces a visual of the top companies by trading volume that was not available on the https://www.centralcharts.com/ website. 

## How to Install & Run the Project
1. Install `virtualenv`. From the command line:
```
python3 -m pip install virtualenv
```
2. Create a folder for the project root directory.
3. Open a terminal in the project root directory and run:
```
virtualenv env
```
4. Then execute the command (for Windows):
```
env\Scripts\activate.bat
```
5. Install the dependencies:
```
(env) python3 -m pip install -r requirements.txt
```
6. Now you are ready to run the program!


## Credits
https://www.centralcharts.com/

## License

