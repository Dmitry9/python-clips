import os
import subprocess

def mp4_to_mp3(input_dir, output_dir):
  """
  :param input_dir: Base directory containing episode folders with MP4 files
  :param output_dir: Base directory to save MP3 files
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
    
    for video_file in os.listdir(episode_input_path):
      if not video_file.endswith('.mp4'):
        continue
      
      input_path = os.path.join(episode_input_path, video_file)
      output_path = os.path.join(episode_output_path, os.path.splitext(video_file)[0] + '.mp3')
      
      try:
        # Extract audio from MP4
        subprocess.run([
          'ffmpeg', 
          '-i', input_path,
          '-vn',  # Omit video stream
          output_path
        ], check=True, capture_output=True)
        
        print(f"Converted: {output_path}")
      
      except subprocess.CalledProcessError as e:
        print(f"Error processing {input_path}: {e.stderr.decode()}")

def main():
    # Current working directory
    base_dir = os.getcwd()
    
    # Input and output directories
    input_dir = os.path.join(base_dir, 'clips')
    output_dir = os.path.join(base_dir, 'audio')
    
    # Convert files
    mp4_to_mp3(input_dir, output_dir)

if __name__ == '__main__':
    main()