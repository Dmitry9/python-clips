import os
import subprocess

def change_playback_speed(input_dir, output_dir, playback_speed=0.75):
    """
    Changes playback speed of MP3.
    
    :param input_dir: Base directory containing episode folders with MP4 files
    :param output_dir: Base directory to save MP3 files
    :param playback_speed: (doble)
    """
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
                    '-i', input_path,
                    '-af', f"atempo={playback_speed}",
                    output_path
                ], check=True, capture_output=True)
                
                print(f"Converted: {output_path}")
            
            except subprocess.CalledProcessError as e:
                print(f"Error processing {input_path}: {e.stderr.decode()}")

def main():
    # Current working directory
    base_dir = os.getcwd()
    
    # Input and output directories
    input_dir = os.path.join(base_dir, 'audio')
    output_dir = os.path.join(base_dir, 'slow')
    
    # Convert files
    change_playback_speed(input_dir, output_dir)

if __name__ == '__main__':
    main()