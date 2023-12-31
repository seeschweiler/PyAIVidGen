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


