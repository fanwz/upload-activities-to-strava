# Strava API Token Manager and Activity Uploader

This Python script provides a structured approach for managing access tokens and uploading activities to the Strava API.

## Overview

- **TokenManager**: Manages the access token and refresh token for Strava API.
- **ActivityUploader**: Allows for uploading activities to the Strava API.

## Features

### TokenManager

TokenManager can be used to manage your Strava API access token.

The first time you run the script, it will open a local server for user authorization to obtain access token and refresh token.

After the first run, the script will automatically refresh your access token when needed.

TokenManager provides the following features:

- **Check Token Expiry**: Easily verify if your access token has expired.
- **Refresh Token**: Automatically refresh your access token when needed.
- **Save and Load Token Data**: Save your token data to a file and load it back when required.
- **User Authorization for Token**: Opens a local server for user authorization to obtain access token.

#### About Strava API Token

read more about Strava API token [here](https://developers.strava.com/docs/authentication/)

### ActivityUploader

- **Upload Activity**: Upload your activities to Strava with ease. Provide file path, data type, activity type, name, and description.

## Getting Started

1. Clone the repository:

```bash
git clone <repository_url>
```

2. Navigate to the cloned directory:

```bash
cd <repository_directory>
```

3. Replace the placeholder values of `CLIENT_ID` and `CLIENT_SECRET` in the script with your own Strava API credentials.

4. Use the script as described in the "Usage" section below.

## Usage

1. Create an instance of `TokenManager`:

```python
token_manager = TokenManager()
```

2. Use the access_token attribute from the TokenManager instance to create an instance of ActivityUploader:

```python
uploader = ActivityUploader(token_manager.access_token)
```

3. Use the upload_activity method of the ActivityUploader class to upload activities to Strava:

```python
uploader.upload_activity(file_path, data_type, activity_type, name, description)
```

## Prerequisites

You need to have a valid Strava API client ID and client secret. Register your application on the Strava developers' portal to obtain these credentials.
Install required libraries:

```
Flask==2.3.2
requests==2.31.0
stravalib==1.4
```

## Contributing

Feel free to fork the repository and submit pull requests. For major changes, please open an issue first to discuss the proposed changes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
