import os

downloads_dir = 'downloads'
print("Checking MP4 files in downloads directory:")
print("-" * 50)

mp4_files = [f for f in os.listdir(downloads_dir) if f.endswith('.mp4')]
for f in mp4_files:
    file_path = os.path.join(downloads_dir, f)
    size = os.path.getsize(file_path)
    if size > 10000:  # Only show files larger than 10KB
        print(f"{f}: {size:,} bytes ({size/1024/1024:.2f} MB)")
    else:
        print(f"{f}: {size} bytes (likely placeholder)")

print("\nChecking for real video content...")
real_videos = [f for f in mp4_files if os.path.getsize(os.path.join(downloads_dir, f)) > 100000]  # >100KB
print(f"Found {len(real_videos)} potential real video files")

if real_videos:
    print("Real video files:")
    for f in real_videos:
        print(f"  - {f}")
else:
    print("No real video files found - all are likely placeholders!")
