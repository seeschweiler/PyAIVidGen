<img src="logo.png" align="left" height="150">

# PyAIVidGen


**PyAIVidGen** is a Python-based tool designed to automate the generation and uploading of AI-driven YouTube videos. Utilizing OpenAI's GPT-4 and DALL-E models, it crafts engaging content, from generating meditation scripts and corresponding images to transforming text into speech and seamlessly uploading the final video to YouTube.

## Features

- **Text Generation**: Utilizes GPT-4 for generating guided meditation scripts.
- **Text-to-Speech Transformation**: Converts generated text into spoken narration.
- **Image Generation**: Leverages DALL-E for creating images matching the script.
- **Video Assembly**: Compiles the narration and images into a complete video.
- **YouTube Upload**: Automated YouTube upload with SEO-optimized video details

## Installation

To install PyAIVidGen, clone this repository and install the required packages.

```bash
git clone https://github.com/seeschweiler/PyAiVidGen
cd PyAIVidGen
pip install -r requirements.txt
```

## Environment Setup

To run PyAIVidGen, you need to set up your OpenAI API key in an `.env` file. This API key is used to authenticate your requests to OpenAI's services.

### Retrieving the OpenAI API Key

1. Sign up or log in to your account on [OpenAI's platform](https://platform.openai.com/signup).
2. Navigate to the API section and create an API key.
3. Copy the generated API key.

### Configuring the .env File

1. In the root directory of PyAIVidGen, create a file named `.env`.
2. Add the following line to the `.env` file:

   ```
   OPENAI_API_KEY=Your_OpenAI_API_Key
   ```

   Replace `Your_OpenAI_API_Key` with the key you copied from the OpenAI platform.

This `.env` file will be automatically read by PyAIVidGen to authenticate API requests.

## Setting Up YouTube API Access

To enable the YouTube upload functionality in PyAIVidGen, you need to set up a `client_secret.json` file. This file contains the credentials required to authenticate with the YouTube Data API. Here are the steps to configure this file:

1. **Rename the Template File**:
   PyAIVidGen includes a template file named `client_secret-TEMPLATE.json`. Rename this file to `client_secret.json`.

2. **Create a Project in Google Cloud Platform**:
   - Visit the [Google Cloud Console](https://console.cloud.google.com/).
   - Create a new project or select an existing one.
   - Navigate to "APIs & Services" > "Dashboard" and enable the YouTube Data API v3 for your project.

3. **Create Credentials**:
   - In the Google Cloud Console, go to "APIs & Services" > "Credentials".
   - Click on "Create Credentials" and choose "OAuth client ID".
   - Set the application type to "Desktop app" and give it a name.
   - Upon creation, you will receive your `client_id` and `client_secret`.

4. **Update `client_secret.json` File**:
   - Open your `client_secret.json` file in a text editor.
   - Replace `INSERT YOUR CLIENT ID` with the `client_id` obtained from the Google Cloud Console.
   - Replace `INSERT YOUR CLIENT SECRET` with the `client_secret`.

5. **Authenticate Your Application**:
   - When you run PyAIVidGen for the first time with YouTube upload enabled, it will prompt you to authenticate via a web browser.
   - Log in with your Google account and grant the necessary permissions.
   - This will generate a token file that allows PyAIVidGen to upload videos to your YouTube channel.

Ensure that the `client_secret.json` file is kept secure and is not shared publicly, as it contains sensitive information regarding your Google API credentials.

## Configuration with settings.json

`settings.json` provides a flexible way to configure the default behavior of PyAIVidGen. If not provided, the program will use the hard-coded default settings.

### Structure of settings.json

The `settings.json` file includes the following settings:

- `user_message`: Default text prompt for meditation script generation.
- `default_num_images`: Default number of images to generate.
- `max_num_images`: Maximum number of images allowed to generate.
- `default_output_file`: Default name for the output video file.
- `default_music_file`: Default background music file.
- `default_image_output_folder`: Default folder for saving generated images.
- `text_output_file`: Default name for the text output file.
- `zoom_intensity`: Intensity of zoom effect in the video (0.2 is standard).
- `transition_time`: Duration of transition between images in the video (in seconds).
- `video_details_file`: Default file path for storing video title, description, and keywords. If not present, default values are used.


### Default Configuration

If `settings.json` is not used, PyAIVidGen will apply the following defaults:

- Text for meditation script generation will be taken from the command line argument.
- One image will be generated (`default_num_images` = 1).
- The output video will be named `vid_output.mp4`.
- No background music will be added if not specified.
- Images will be saved in a folder named `image_output`.
- Text output file will be `custom_text_output.txt`.
- Zoom intensity for video images will be 0.2.
- Transition time between images will be 3 seconds.
- Video title, description, and keywords details will be generated automatically unless a `video_details.json` file is specified.

To use custom settings, create a `settings.json` file in the root directory with your desired configuration.


## Usage

Run `pyaividgen.py` with the necessary arguments. For example:

```bash
python pyaividgen.py --text-file your_text.txt --music-file background_music.mp3
```

### Command Line Arguments

PyAIVidGen supports several command line arguments to customize the video generation process:

- `-t`, `--text-file`: Path to the text file for voice conversion. If not provided, the default text file specified in `settings.json` will be used.
- `-m`, `--music-file`: Path to the background music file. If not provided, the default music file specified in `settings.json` will be used.
- `-n`, `--num-images`: Number of images to be generated. Overrides the default number set in `settings.json`.
- `-i`, `--image-output-folder`: Path for the folder where images will be saved. Overrides the default folder set in `settings.json`.
- `-o`, `--output-file`: Path for the output video file. Overrides the default output file set in `settings.json`.
- `-v`, `--video-details-file`: Path to the JSON file containing video title, description, and keywords. If not provided, PyAIVidGen will use the default file specified in `settings.json` or generate these details automatically.

These arguments provide flexibility and control over the video generation process, allowing for customization and automation as per user requirements.


## Configuration

Customize the behavior of PyAIVidGen through `settings.json`. Set default paths, number of images, zoom intensity, and more.

## Contributing

Contributions to PyAIVidGen are welcome! Please read our contributing guidelines for more information.

## License

PyAIVidGen is released under the MIT License. See [LICENSE](LICENSE) for details.

## Acknowledgements

This project utilizes OpenAI's GPT-4 and DALL-E models. Special thanks to the OpenAI team for their incredible work.


