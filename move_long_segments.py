import os
import subprocess

def get_video_duration(video_path):
    """
    Get video duration using ffprobe.
    
    :param video_path: Path to the video file
    :return: Duration of the video in seconds
    """
    try:
        # Run ffprobe command to get duration
        result = subprocess.run([
            'ffprobe', 
            '-v', 'error', 
            '-show_entries', 'format=duration', 
            '-of', 'default=noprint_wrappers=1:nokey=1', 
            video_path
        ], capture_output=True, text=True)
        
        # Convert duration to float
        return float(result.stdout.strip())
    except Exception as e:
        print(f"Error getting duration for {video_path}: {e}")
        return 0

def move_long_segments(phrases_dir, long_dir, duration_threshold=30):
    """
    Move video files longer than the threshold to a 'long' directory.
    
    :param phrases_dir: Base directory with episode phrase folders
    :param long_dir: Directory to move long segments
    :param duration_threshold: Minimum duration (in seconds) to be considered 'long'
    """
    # Ensure long directory exists
    os.makedirs(long_dir, exist_ok=True)
    
    # Iterate through episodes
    for episode in os.listdir(phrases_dir):
        episode_path = os.path.join(phrases_dir, episode)
        
        # Skip if not a directory
        if not os.path.isdir(episode_path):
            continue
        
        # Create corresponding long episode directory
        long_episode_path = os.path.join(long_dir, episode)
        os.makedirs(long_episode_path, exist_ok=True)
        
        # Check each segment
        for segment in os.listdir(episode_path):
            if not segment.endswith('.mp4'):
                continue
            
            full_segment_path = os.path.join(episode_path, segment)
            duration = get_video_duration(full_segment_path)
            
            # Move long segments
            if duration > duration_threshold:
                dest_path = os.path.join(long_episode_path, segment)
                os.rename(full_segment_path, dest_path)
                print(f"Moved long segment: {full_segment_path} (Duration: {duration:.2f}s)")

def main():
    # Current working directory
    base_dir = os.getcwd()
    
    # Directories
    phrases_dir = os.path.join(base_dir, 'phrases')
    long_dir = os.path.join(base_dir, 'long')
    
    # Move long segments
    move_long_segments(phrases_dir, long_dir)

if __name__ == '__main__':
    main()