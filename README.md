# EasyGatherContact
This project scrapes LinkedIn names using a Google search and generates email addresses in a specified format.

EasyGatherContact is a Python script to gather LinkedIn profiles and generate email addresses based on specified formats. This script uses Selenium webdrivers to perform Google searches and parse the results to curate the list of emails for input organization names.

## Features

- Automatically scrolls through Google search results to gather all profiles.
- Generates email addresses based on the collected names and specified format.
- Supports multiple email formats.
- Outputs results into specified directories.
- Utilizes Google Dorks for LinkedIn and RocketReach.

## Prerequisites

- Python 3.7+
- Google Chrome browser
- ChromeDriver 

### [!] make sure the ChromeDriver version matches your Google Chrome version

## Installation

1. Clone this repository:
    ```sh
    git clone https://github.com/m4xx101/EasyGatherContact.git
    cd EasyGatherContact
    ```

2. Install required Python packages:
    ```sh
    pip install -r requirements.txt
    ```

3. Download and install the ChromeDriver. Ensure the version matches your installed version of Google Chrome. You can download ChromeDriver from [here](https://sites.google.com/a/chromium.org/chromedriver/downloads).

## Usage

To run the script, use the following command:

```sh
$ python3 gather_contact5.py [-h] --domain DOMAIN [--email_format {1,2,3,4}] [--output_directory OUTPUT_DIRECTORY] [--chrome_driver_path CHROME_DRIVER_PATH] company [company ...]

  -h, --help            show this help message and exit
  --domain DOMAIN, -d DOMAIN
                        The domain (e.g., company.com) for email creation
  --email_format {1,2,3,4}, -ef {1,2,3,4}
                        Email format (1, 2, 3, or 4). Examples: 1. flastname@domain.com, 2. firstname.lastname@domain.com, 3. lastnamef@domain.com, 4. firstnamel@domain.com
  --output_directory OUTPUT_DIRECTORY, -o OUTPUT_DIRECTORY
                        The output directory to create and store the results
  --chrome_driver_path CHROME_DRIVER_PATH, -cdp CHROME_DRIVER_PATH
                        The path to the ChromeDriver executable
```

## Example

```sh
python3 gather_contact.py "Company Name" -d comapny-domain.com -ef 2 -o <output-dir-to-save-results>
```

## Notes:

Make sure your ChromeDriver version matches your Google Chrome version to avoid compatibility issues.
If you encounter any issues or have suggestions, feel free to open an issue or a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Credits:
Inspired by the work of gathercontacts burp extension (Credit: @OrOneEqualsOne).
