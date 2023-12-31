<img src="logo.png" align="left" height="150">

# PyAIVidGen


**PyAIVidGen** is a sophisticated tool designed to leverage AI capabilities for generating YouTube videos. This program uniquely combines OpenAI's GPT-4 and DALL-E models to generate video scripts, voice narrations, and corresponding visual content.

## Features

- **Text Generation**: Utilizes GPT-4 for generating guided meditation scripts.
- **Text-to-Speech Transformation**: Converts generated text into spoken narration.
- **Image Generation**: Leverages DALL-E for creating images matching the script.
- **Video Assembly**: Compiles the narration and images into a complete video.

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

---

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

To use custom settings, create a `settings.json` file in the root directory with your desired configuration.

## Usage

Run `pyaividgen.py` with the necessary arguments. For example:

```bash
python pyaividgen.py --text-file your_text.txt --music-file background_music.mp3
```

### Command Line Arguments

- `-t`, `--text-file`: Path to the text file for voice conversion.
- `-m`, `--music-file`: Path to the background music file.
- `-n`, `--num-images`: Number of images to be generated.
- `-i`, `--image-output-folder`: Path for the folder where images will be saved.
- `-o`, `--output-file`: Path for the output video file.

## Configuration

Customize the behavior of PyAIVidGen through `settings.json`. Set default paths, number of images, zoom intensity, and more.

## Contributing

Contributions to PyAIVidGen are welcome! Please read our contributing guidelines for more information.

## License

PyAIVidGen is released under the MIT License. See [LICENSE](LICENSE) for details.

## Acknowledgements

This project utilizes OpenAI's GPT-4 and DALL-E models. Special thanks to the OpenAI team for their incredible work.


