import argparse
import os
import json
from openai import OpenAI
import colorama
from colorama import Fore, Style
from dotenv import load_dotenv

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
    with open('text_output.txt', 'w') as file:
        file.write(text)

def ask_user_for_text_generation():
    response = input("Do you want to generate text? [Y/n]: ").strip().lower()
    return response in ['', 'y', 'yes']

def main(args):
    if args.text_file:
        print_green_bold("Using provided text file.")
    else:
        if ask_user_for_text_generation():
            print_green_bold("Generating text using OpenAI.")
            generated_text = generate_text_with_openai()
            if generated_text:
                save_generated_text(generated_text)
                args.text_file = 'text_output.txt'
        else:
            print("Text generation skipped.")
            return  # Or handle this case as needed

    # Rest of your main function logic

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='PyAIVidGen: A tool to generate YouTube videos using OpenAI APIs')

    parser.add_argument('-t', '--text-file', type=str, help='Path to the text file (txt) for voice conversion', required=False)
    parser.add_argument('-m', '--music-file', type=str, help='Path to the background music file (mp3)', default=settings.get('default_music_file'))
    parser.add_argument('-n', '--num-images', type=int, help='Number of images to be generated', default=settings.get('default_num_images', 5))
    parser.add_argument('-o', '--output-file', type=str, help='Path for the output video file', default=settings.get('default_output_file'))

    args = parser.parse_args()
    main(args)
