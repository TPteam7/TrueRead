
# TrueRead
### By: Trevor Pope, Micheal Callahan, and Mia Zimmerman

TrueRead is a desktop application that captures screenshots or uploads images to convert their content into spoken audio. This application uses PyQt5 for the user interface, Google Text-to-Speech for audio output, MathPix API to process images containing mathematical content, and OpenAI's ChatGPT to interpret mathematical equations in natural language. TrueRead is particularly helpful for individuals with dyslexia to understand complex mathematical equations in audio format.

## Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Installation

### Prerequisites

Ensure Python and pip are installed on your system. This application requires several external libraries and API keys to function properly.

```bash
# Install necessary Python packages
pip install PyQt5 Pillow pygame google-cloud-texttospeech requests
```

### Cloning and Setting Up

Clone the repository and navigate into the project directory:

```bash
git clone https://github.com/yourusername/TrueRead.git
cd TrueRead
```

## Configuration

Before running the application, you need to set up the necessary API keys in your environment:

1. **Google Text-to-Speech API Key**: Follow the instructions [here](https://cloud.google.com/text-to-speech/docs/quickstart-client-libraries) to set up your Google Cloud project and get an API key.

2. **MathPix API Key**: Obtain credentials by signing up at [MathPix](https://mathpix.com).

3. **OpenAI API Key**: If you do not already have an API key, you can request one from [OpenAI](https://beta.openai.com/signup/).

Once you have the keys, set them as environment variables:

```bash
export GOOGLE_APPLICATION_CREDENTIALS='path_to_your_google_credentials.json'
export MATHPIX_APP_ID='your_mathpix_app_id'
export MATHPIX_API_KEY='your_mathpix_api_key'
export OPENAI_API_KEY='your_openai_api_key'
```

## Usage

1. **Take a Screenshot**: Click the 'Take Screenshot' button to select a portion of your screen to capture. The application will minimize, allowing you to select an area on your desktop.
2. **Upload an Image**: You can also upload an image directly by clicking the 'Upload Image' button and selecting an image file.
3. **Play Audio**: Once the image is processed, you can play the audio representation of the image content by pressing the 'Play Audio' button.

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

Please ensure to update tests as appropriate.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Authors

- **Trevor Pope** - *Initial work* - [TPteam7](https://github.com/TPteam7)
- **Micheal Callahan** - *Initial work* - [MichealC03](https://github.com/MichealC03)

## Acknowledgments

- Thanks to all contributors who participate in this project.
- Special thanks to the PyQt5, Google Cloud, MathPix, and OpenAI communities.
