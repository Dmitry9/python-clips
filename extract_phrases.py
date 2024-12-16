import os
import webvtt
import ffmpeg
import re

def parse_vtt_file(vtt_path):
    """
    Parse VTT file and extract segments, merging those within 1 second of each other.
    
    :param vtt_path: Path to the VTT file
    :return: List of merged segments with start and end times
    """
    segments = []
    
    # Parse VTT file
    for caption in webvtt.read(vtt_path):
        # Convert timestamp to seconds
        start = timestamp_to_seconds(caption.start)
        end = timestamp_to_seconds(caption.end)
        
        # If first segment or gap is more than 1 second
        if not segments or start - segments[-1]['end'] > 1:
            segments.append({
                'start': start,
                'end': end,
                'text': caption.text
            })
        else:
            # Merge segments
            segments[-1]['end'] = end
    
    return segments

def timestamp_to_seconds(timestamp):
    """
    Convert WebVTT timestamp to seconds.
    
    :param timestamp: WebVTT timestamp string
    :return: Float representing time in seconds
    """
    # Remove potential milliseconds for clean parsing
    timestamp = timestamp.split('.')[0]
    h, m, s = map(float, timestamp.split(':'))
    return h * 3600 + m * 60 + s

def extract_phrases(mp4_dir, vtt_dir, output_base_dir):
    """
    Extract phrase segments from MP4 files based on VTT timestamps.
    
    :param mp4_dir: Directory containing MP4 files
    :param vtt_dir: Directory containing VTT files
    :param output_base_dir: Base directory for storing extracted phrases
    """
    # Ensure all input directories exist
    if not os.path.exists(mp4_dir) or not os.path.exists(vtt_dir):
        raise ValueError("MP4 or VTT directory does not exist")
    
    # Get sorted list of files to ensure matching
    mp4_files = sorted([f for f in os.listdir(mp4_dir) if f.endswith('.mp4')])
    vtt_files = sorted([f for f in os.listdir(vtt_dir) if f.endswith('.vtt')])
    
    # Validate file matching
    if len(mp4_files) != len(vtt_files):
        raise ValueError(f"Mismatch in number of MP4 ({len(mp4_files)}) and VTT ({len(vtt_files)}) files")
    
    # Process each episode
    for mp4_file, vtt_file in zip(mp4_files, vtt_files):
        # Remove file extension for consistent naming
        episode_name = os.path.splitext(mp4_file)[0]
        
        # Full paths
        mp4_path = os.path.join(mp4_dir, mp4_file)
        vtt_path = os.path.join(vtt_dir, vtt_file)
        
        # Create output directory for this episode
        episode_output_dir = os.path.join(output_base_dir, episode_name)
        os.makedirs(episode_output_dir, exist_ok=True)
        
        # Parse VTT segments
        segments = parse_vtt_file(vtt_path)
        
        # Extract each segment
        for i, segment in enumerate(segments, 1):
            output_path = os.path.join(episode_output_dir, f'segment-{i:03d}.mp4')
            
            try:
                # Use ffmpeg-python to trim the video
                (
                    ffmpeg
                    .input(mp4_path, ss=segment['start'], to=segment['end'])
                    .output(output_path, c='copy')
                    .overwrite_output()
                    .run(capture_stdout=True, capture_stderr=True)
                )
                print(f"Extracted {output_path}")
            except ffmpeg.Error as e:
                print(f"Error extracting segment {i} from {mp4_file}: {e.stderr.decode()}")

def main():
    # Base directories
    base_dir = os.getcwd()
    mp4_dir = os.path.join(base_dir, 'mp4')
    vtt_dir = os.path.join(base_dir, 'vtt')
    phrases_dir = os.path.join(base_dir, 'phrases')
    
    # Create phrases directory if it doesn't exist
    os.makedirs(phrases_dir, exist_ok=True)
    
    # Run extraction
    extract_phrases(mp4_dir, vtt_dir, phrases_dir)

if __name__ == '__main__':
    main()