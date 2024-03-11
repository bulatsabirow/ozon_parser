# Ozone phones parser
## Project requirements
1. [Python >= 3.10](https://python.org/downloads/)
2. [Poetry](https://pypi.org/project/poetry/) 
## Project Setup
1. Enter the virtual environment:
    ```shell
   Poetry shell
   ```
2. Install required dependencies:
   ```shell
   Poetry install
   ```
3. To run the scrapy crawler, enter the following command:
   ```shell
   cd phones_parser && scrapy crawl ozon_phones
   ```