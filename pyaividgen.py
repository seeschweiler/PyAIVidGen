import argparse
import os
import json
import requests
import shutil
from openai import OpenAI
import colorama
from colorama import Fore, Style
from dotenv import load_dotenv
from moviepy.editor import ImageClip, concatenate_audioclips, concatenate_videoclips, AudioFileClip, CompositeAudioClip, AudioClip

from youtube_uploader import upload_video

colorama.init(autoreset=True)
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    print("Error: OpenAI API key not found. Please check your .env file.")
    exit(1)

client = OpenAI(api_key=openai_api_key)

def print_green_bold(text):
    print(Fore.GREEN + Style.BRIGHT + text + Style.RESET_ALL)

def read_settings():
    try:
        with open('settings.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print("settings.json file not found.")
        return None

settings = read_settings()
if settings is None:
    exit(1)

def generate_text_with_openai():
    user_message = settings.get('user_message', '')
    try:
        response = client.chat.completions.create(model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant which is able to generate guided meditations as text."},
            {"role": "user", "content": user_message}
        ],
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error while generating text with OpenAI: {e}")
        return None

def save_generated_text(text):
    text_output_file = settings.get('text_output_file', 'text_output.txt')
    with open(text_output_file, 'w') as file:
        file.write(text)

def ask_user_for_text_generation():
    response = input("Do you want to generate text? [Y/n]: ").strip().lower()
    return response in ['', 'y', 'yes']

def ask_user_for_text_to_speech_transformation():
    response = input("Do you want to proceed with Text-to-Speech transformation? [Y/n]: ").strip().lower()
    return response in ['', 'y', 'yes']

def perform_text_to_speech_transformation(text_file):
    try:
        with open(text_file, 'r') as file:
            text = file.read()
            
            mp3_output_file = text_file.replace('.txt', '.mp3')
            response = client.audio.speech.create(
                model="tts-1",
                voice="nova",
                speed=0.75,
                input=text
            )
            response.stream_to_file(mp3_output_file)
            print_green_bold(f"Text-to-Speech output written to file {mp3_output_file}.")

    except Exception as e:
        print(f"Error during Text-to-Speech transformation: {e}")

def ask_user_for_image_generation():
    response = input("Do you want to start the image generation process? [Y/n]: ").strip().lower()
    return response in ['', 'y', 'yes']

def generate_image_prompts(text, num_prompts):
    prompts = []
    try:
        for _ in range(num_prompts):
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant who is able to generate perfect DallE 3 image generation prompts. Those prompts should be perfect for generating images to accompany the spoken text in a video. Please only output the prompt for the text the user is providing. Please do not include any further instructions or explainations in your answer, only the prompt text."},
                    {"role": "user", "content": text}
                ],
                temperature=1.4
            )
            prompt = response.choices[0].message.content.strip()
            prompts.append(prompt)
    except Exception as e:
        print(f"Error while generating image prompts with OpenAI: {e}")
    
    return prompts

def generate_and_save_images(prompts, image_output_folder):
    # Empty the image output folder first
    empty_directory(image_output_folder)
   
    for i, prompt in enumerate(prompts, 1):
        try:
            response = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1792x1024",
                quality="standard",
                n=1,
            )
            # Assuming the API returns the image URL
            image_url = response.data[0].url

            # Call download_image function
            image_file_path = os.path.join(image_output_folder, f"image_{i}.png")
            download_image(image_url, image_file_path)

            print_green_bold(f"Image {i} generated and saved in {image_output_folder}")

        except Exception as e:
            print(f"Error during image generation for prompt {i}: {e}")

def download_image(image_url, file_path):
    try:
        response = requests.get(image_url)
        response.raise_for_status()

        with open(file_path, 'wb') as file:
            file.write(response.content)

        print_green_bold(f"Image downloaded and saved to {file_path}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading image: {e}")

def empty_directory(folder_path):
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isfile(item_path):
            os.remove(item_path)
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)

def ask_user_for_video_generation():
    response = input("Do you want to start the video generation process? [Y/n]: ").strip().lower()
    return response in ['', 'y', 'yes']

def create_animated_clip(img_path, duration, zoom_intensity):
    # Create a clip from an image with zoom-in and zoom-out effect
    clip = ImageClip(img_path).resize(height=1080)  # Resize for consistency
    clip = clip.set_duration(duration)

    # Define zoom-in and zoom-out effects
    zoom_factor = 1 + zoom_intensity
    zoom_in = lambda t: min(1 + zoom_intensity * (t / (duration / 2)), zoom_factor) if t < duration / 2 else zoom_factor
    zoom_out = lambda t: zoom_factor if t < duration / 2 else max(zoom_factor - zoom_intensity * ((t - duration / 2) / (duration / 2)), 1)

    # Apply zoom-in and zoom-out effect
    clip = clip.fl_time(lambda t: zoom_in(t) if t < duration / 2 else zoom_out(t))
    clip = clip.resize(lambda t: zoom_in(t) if t < duration / 2 else zoom_out(t))

    return clip

def generate_video(images_folder, audio_file, music_file, output_file, total_duration, zoom_intensity, transition_time):
    # Load all images and create animated clips
    image_files = [os.path.join(images_folder, f) for f in sorted(os.listdir(images_folder)) if f.endswith('.png')]
    duration_per_image = total_duration / len(image_files)
    clips = [create_animated_clip(img, duration_per_image, zoom_intensity) for img in image_files]

    # Apply crossfade transition between clips
    final_clips = [clips[0]]
    for clip in clips[1:]:
        final_clips.append(clip.crossfadein(transition_time))

    # Concatenate all clips together
    video_clip = concatenate_videoclips(final_clips, method="compose")

    # Load the voiceover audio
    voice_clip = AudioFileClip(audio_file).audio_fadein(1).audio_fadeout(1)

    # Create a silent audio clip for padding
    silence = AudioClip(lambda t: 0, duration=5, fps=44100)

    # Combine voice clip with silence padding
    padded_voice_clip = concatenate_audioclips([silence, voice_clip, silence])

    # Combine audio tracks if background music is available
    if music_file:
        music_clip = AudioFileClip(music_file).volumex(0.5)  # Reduce music volume
        final_audio = CompositeAudioClip([padded_voice_clip, music_clip.set_duration(video_clip.duration)])
    else:
        final_audio = padded_voice_clip

    # Set the audio to the video
    final_video = video_clip.set_audio(final_audio)

    # Write the final video file
    final_video.write_videofile(output_file, fps=24)

def ask_user_for_youtube_upload():
    response = input("Do you want to automatically upload the generated video to YouTube? [Y/n]: ").strip().lower()
    return response in ['', 'y', 'yes']

# Function to handle preparation for YouTube video upload
def upload_video_to_youtube(video_file_path, video_text):
    generate_video_details = ask_for_video_details_generation()
    video_details_file = args.video_details_file if args.video_details_file else settings.get('video_details_file', 'video_details.json')

    if generate_video_details:
        # Generate video details (title, description, keywords)
        # Use OpenAI Chat Completion API to generate video details
        try:
            system_message = "You are an assistant which is able to generate for a given text of a YouTube video great seo-optimized and engaging video title (title), video description (description) and keywords (keywords). Please output in JSON format only."

            completion = client.chat.completions.create(
                model="gpt-3.5-turbo-1106",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": video_text}
                ],
                response_format={"type": "json_object"}
            )

            video_details_str = completion.choices[0].message.content
            video_details = json.loads(video_details_str)  # Converting string to JSON object

            if 'title' in video_details and 'description' in video_details and 'keywords' in video_details:
                # Convert comma-separated keywords string to a list
                keywords_list = [keyword.strip() for keyword in video_details['keywords'].split(',')]

                # Update the video_details with the list of keywords
                video_details['keywords'] = keywords_list

                # Write updated video details to the file
                with open(video_details_file, 'w') as file:
                    json.dump(video_details, file, indent=4)

                print(f"New video details written to {video_details_file}")

                title = video_details['title']
                description = video_details['description']
                keywords = video_details['keywords']

                print("Video details generated.")
            else:
                print("Error: Received invalid video details format.")
                print("Use default video details ... ")
                title = "Default Video Title"
                description = "Default video description."
                keywords = ["Default", "Video", "Keywords"]
                print("Default video details set.")
        
        except Exception as e:
            print(f"Error generating video details: {e}")

        
    elif os.path.exists(video_details_file):
        # Read video details from file
        print(f"Trying to retrieve video details from file {video_details_file}")
        video_details = read_video_details(video_details_file)
        title = video_details.get('title', 'Default Title')
        description = video_details.get('description', 'Default Description')
        keywords = video_details.get('keywords', ['Default', 'Keywords'])
        print("Video details retrieved successfully.")
    else:
        # Use default video details
        print("Use default video details ... ")
        title = "Default Video Title"
        description = "Default video description."
        keywords = ["Default", "Video", "Keywords"]
        print("Default video details set.")

    print("-------------------------------")
    print(f"- Video Details - Title: {title}")
    print(f"- Video Details - Description: {description}")
    print(f"- Video Details - Keywords: {keywords}")
    print("-------------------------------")

    print_green_bold("Uploading to YouTube...")
    category = "22"  # Category ID (e.g., "22" for People & Blogs)
    tags = keywords

    # Perform upload
    upload_response = upload_video(video_file_path, title, description, category, tags)
    print_green_bold(f"Video uploaded successfully: {upload_response.get('id')}")

def ask_for_video_details_generation():
    response = input("Do you want to generate video title, description, and keywords? [Y/n]: ").strip().lower()
    return response in ['', 'y', 'yes']

def read_video_details(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error reading video details file: {e}")
        return None

def main(args):
    # Determine the music file to use
    music_file = args.music_file if args.music_file else settings.get('default_music_file')
    
    # Check if the music file exists
    if music_file and os.path.exists(music_file):
        print_green_bold(f"Background music file to be used: {music_file}")
    else:
        print("No background music file provided or file not found. No background music will be added to the video.")
        music_file = None
    
    text_file_available = False
    mp3_file_exists = False

    # Determine the text output file
    text_output_file = args.text_file if args.text_file else settings.get('text_output_file', 'text_output.txt')

    # Check if the text file exists
    if os.path.exists(text_output_file):
        print_green_bold(f"Using existing text file: {text_output_file}")
        text_file_available = True
    else:
        if ask_user_for_text_generation():
            print_green_bold("Generating text using OpenAI.")
            generated_text = generate_text_with_openai()
            if generated_text:
                save_generated_text(generated_text)
                text_file_available = True
        else:
            print("Text generation skipped.")
    

    # Check if corresponding MP3 file exists or generate new MP3
    mp3_output_file = text_output_file.replace('.txt', '.mp3')
    
    # Check if the MP3 file exists
    if os.path.exists(mp3_output_file):
        print_green_bold(f"Corresponding voice MP3 file found: {mp3_output_file}. It will be used.")
        mp3_file_exists = True
    elif text_file_available:
        if ask_user_for_text_to_speech_transformation():
            print_green_bold("Text-to-Speech transformation selected.")
            perform_text_to_speech_transformation(text_output_file)
            mp3_file_exists = True
        else:
            print("Text-to-Speech transformation skipped.")

    # Image output folder handling
    image_output_folder = args.image_output_folder if args.image_output_folder else settings.get('default_image_output_folder', 'image_output')
    print_green_bold(f"Images will be saved in the folder: {image_output_folder}")

    # Ensure the output folder exists
    os.makedirs(image_output_folder, exist_ok=True)

    # Ask user for image generation
    if ask_user_for_image_generation():
        print_green_bold("Image generation process selected.")

        # Read the maximum number of images from settings
        max_num_images = settings.get('max_num_images', 5)

        # Determine the actual number of images to generate
        num_images = min(args.num_images if args.num_images else settings.get('default_num_images', 5), max_num_images)

        # Read the text from the output file
        try:
            with open(text_output_file, 'r') as file:
                text_content = file.read()
        except FileNotFoundError:
            print(f"Error: Text output file {text_output_file} not found.")
            return

        image_prompts = generate_image_prompts(text_content, num_images)
        
        # Output image prompts array to the console
        print_green_bold("Generated Image Prompts:")
        for i, prompt in enumerate(image_prompts, 1):
            print(f"Prompt {i}: {prompt}")
        
        # Generate and save images
        generate_and_save_images(image_prompts, image_output_folder)
    else:
        print("Image generation process skipped.")

    # Ask user if video generation should be started
    if ask_user_for_video_generation():
        print_green_bold("Video generation process selected.")

        # Determine the video output file
        video_output_file = args.output_file if args.output_file else settings.get('default_output_file')
        if video_output_file:
            print_green_bold(f"Video output file to be used: {video_output_file}")
        else:
            print("No video output file specified. Ending program.")
            return

        print(f"Text File Available: {text_file_available}, MP3 File Exists: {mp3_file_exists}")

        # Read zoom intensity and transition time from settings
        zoom_intensity = settings.get('zoom_intensity', 0.05)  # Default value if not specified
        transition_time = settings.get('transition_time', 1)   # Default value if not specified

        # Video generation
        if text_file_available and mp3_file_exists:
            try:
                generate_video(image_output_folder, mp3_output_file, music_file, video_output_file, AudioFileClip(mp3_output_file).duration, zoom_intensity, transition_time)
                print("Video generation completed successfully.")

                if ask_user_for_youtube_upload():
                    # Read the text from the output file
                    try:
                        with open(text_output_file, 'r') as file:
                            text_content = file.read()
                            upload_video_to_youtube(video_output_file, text_content)
                    except FileNotFoundError:
                        print(f"Error: Text output file {text_output_file} not found.")
                        return
                else:
                    print("Automatic YouTube upload skipped.")

            except Exception as e:
                print(f"Error during video generation: {e}")
        else:
            print("Skipping video generation due to missing text or MP3 file.")
    else:
        # Check if the video file exists for YouTube upload
        video_output_file = args.output_file if args.output_file else settings.get('default_output_file')
        if os.path.exists(video_output_file):
            print_green_bold(f"Found existing video file: {video_output_file}")
            if ask_user_for_youtube_upload():
                # Read the text from the output file
                try:
                    with open(text_output_file, 'r') as file:
                        text_content = file.read()
                        upload_video_to_youtube(video_output_file, text_content)
                except FileNotFoundError:
                    print(f"Error: Text output file {text_output_file} not found.")
                    return
            else:
                print("Automatic YouTube upload skipped.")
        else:
            print("No existing video file found. Ending program.")

    # Rest of your main function logic

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='PyAIVidGen: A tool to generate YouTube videos using AI')

    parser.add_argument('-t', '--text-file', type=str, help='Path to the text file (txt) for voice conversion', required=False)
    parser.add_argument('-m', '--music-file', type=str, help='Path to the background music file (mp3)', default=settings.get('default_music_file'))
    parser.add_argument('-n', '--num-images', type=int, help='Number of images to be generated', default=settings.get('default_num_images', 5))
    parser.add_argument('-i', '--image-output-folder', type=str, help='Path for the folder where images will be saved', default=settings.get('default_image_output_folder', 'image_output'))
    parser.add_argument('-o', '--output-file', type=str, help='Path for the output video file', default=settings.get('default_output_file'))
    parser.add_argument('-v', '--video-details-file', type=str, help='Path to the video details JSON file', required=False)

    args = parser.parse_args()
    main(args)
