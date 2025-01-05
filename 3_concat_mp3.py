import sys
import os
import subprocess

def concat_mp3(input_dir, output_dir, silence_path):
    """
    Changes playback speed of MP3.
    
    :param input_dir: Base directory containing episode folders with MP4 files
    :param output_dir: Base directory to save MP3 files
    :param silence_path location of a file with silience
    """
     # Ensure all input directories exist
    if not os.path.exists(silence_path):
        raise ValueError(f"{silence_path} does not exist")
    if not os.path.exists(input_dir):
        raise ValueError(f"{input_dir} does not exist")

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Iterate through episode folders
    for episode in os.listdir(input_dir):
        episode_input_path = os.path.join(input_dir, episode)
        episode_output_path = os.path.join(output_dir, episode)
        
        # Skip if not a directory
        if not os.path.isdir(episode_input_path):
            continue
        
        # Create output episode directory
        os.makedirs(episode_output_path, exist_ok=True)
        
        # Process each MP4 file
        for audio_file in os.listdir(episode_input_path):
            if not audio_file.endswith('.mp3'):
                continue
            
            # Full input and output paths
            input_path = os.path.join(episode_input_path, audio_file)
            output_path = os.path.join(episode_output_path, audio_file)
            
            try:
                # Extract audio from MP4
                subprocess.run([
                    'ffmpeg',
                    '-i', f"concat:{input_path}|{silence_path}",
                    output_path
                ], check=True, capture_output=True)
                
                print(f"Concated: {output_path}")
            
            except subprocess.CalledProcessError as e:
                print(f"Error processing {input_path}: {e.stderr.decode()}")

def main():
    # Get optional silence file argument from command line
    silence_file = 'silience.mp3'
    if len(sys.argv) > 1:
      silence_file = sys.argv[1]
      
    # Current working directory
    base_dir = os.getcwd()
    
    # Input and output directories
    input_dir = os.path.join(base_dir, 'slow')
    output_dir = os.path.join(base_dir, 'with_silience')
    silience_dir = os.path.join(base_dir, silence_file)
    
    # Convert files
    concat_mp3(input_dir, output_dir, silience_dir)

if __name__ == '__main__':
    main()