# PyAIVidGen

PyAIVidGen is a Python command-line tool designed to automate the creation of YouTube videos using OpenAI's APIs. This tool leverages the power of AI to transform texts into voice narrations, integrates background music, and utilizes OpenAI's DALL-E API to generate relevant images, culminating in a complete video package.

## Features

- **Text to Speech**: Converts provided text (like meditation scripts or poems) into voice audio using OpenAI's text-to-speech transformation.
- **Background Music Integration**: Allows the addition of background music to the video, enhancing the auditory experience.
- **Image Generation**: Uses OpenAI's DALL-E API to generate images that are displayed throughout the video.
- **Automated Video Assembly**: Determines the length of the video based on the voice audio and displays images in a sequential order, with each image appearing for an equal duration.

## Getting Started

### Prerequisites

- Python 3.x
- OpenAI API key (see [OpenAI API documentation](https://openai.com/api/))

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/seeschweiler/PyAiVidGen.git
   ```
2. Navigate to the project directory:
   ```
   cd PyAiVidGen
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

### Usage

Run the program using the following command:

```
python pyaividge.py --text-file <path-to-text-file> --music-file <path-to-music-file> --num-images <number-of-images> --output-file <output-video-file>
```

Optional arguments:
- `--text-file`: Path to the text file for voice conversion (optional if you want to use OpenAI's text generation).
- `--music-file`: Path to the background music file (MP3 format).
- `--num-images`: Number of images to generate via DALL-E.
- `--output-file`: Path for the output video file (default is `vid_output.mp4`).

### Example

```
python pyaividge.py --num-images 5 --text-file example.txt --music-file background.mp3 --output-file my_video.mp4
```

## Contributing

Contributions are welcome! Please feel free to submit pull requests.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

- OpenAI for providing the APIs used in this project.
- Contributors and supporters of the PyAIVidGen project.

---

Note: This tool is in its early stages of development and may undergo significant changes. Feedback and contributions are highly appreciated.
