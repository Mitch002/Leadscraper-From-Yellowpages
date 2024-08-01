# Leadscraper From Yellowpages

## Description

Leadscraper From Yellowpages is a Python-based web scraping tool designed to extract business leads from Yellowpages. This tool fetches business information such as names, addresses, phone numbers, and websites to help users collect valuable data for their marketing and business development efforts.

## Features

- Scrape business leads from Yellowpages
- Extract business name, address, phone number, and website
- Save extracted data into a CSV file for easy access and organization

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/Mitch002/Leadscraper-From-Yellowpages.git
    ```
2. Navigate to the project directory:
    ```sh
    cd Leadscraper-From-Yellowpages
    ```
3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Run the scraper script:
    ```sh
    python leadscraper.py
    ```
2. Follow the on-screen instructions to enter the search keyword and the location for scraping.
3. The extracted data will be saved to a CSV file named `leads.csv`.

## Files

- `leadscraper.py`: Main script to run the web scraper.
- `requirements.txt`: List of dependencies required to run the project.
- `README.md`: Project documentation.

## Dependencies

- Python 3.x
- Requests
- BeautifulSoup4
- Pandas

## Contributing

Contributions are welcome! Please fork this repository and submit a pull request for any improvements or bug fixes.

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Create a new pull request
