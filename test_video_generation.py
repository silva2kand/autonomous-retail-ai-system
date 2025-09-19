#!/usr/bin/env python3
"""
Test script for the AI Video Remaker desktop app
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import VideoPipeline

def test_video_generation():
    """Test the video generation pipeline"""
    print("Testing AI Video Remaker...")

    # Create pipeline
    pipeline = VideoPipeline()

    # Test parameters
    topics = ["artificial intelligence", "machine learning"]
    duration = 5
    voice_type = "male"
    presenter = "expert"
    style = "cinematic"

    print(f"Generating video with topics: {topics}")
    print(f"Duration: {duration} minutes")
    print(f"Voice: {voice_type}")
    print(f"Style: {style}")

    try:
        # Generate video
        result = pipeline.process_topics_full(topics, duration, voice_type, presenter, style)

        print("\n=== Generation Results ===")
        print(f"Status: {result.get('status')}")
        print(f"Video Path: {result.get('video_path')}")
        print(f"Topics: {result.get('topics')}")
        print(f"Duration: {result.get('duration')} minutes")
        print(f"Voice Type: {result.get('voice_type')}")
        print(f"Style: {result.get('style')}")

        # Check if video file exists
        video_path = result.get('video_path')
        if video_path and os.path.exists(video_path):
            file_size = os.path.getsize(video_path)
            print(f"✅ Video file created successfully: {video_path}")
            print(f"File size: {file_size} bytes")
        else:
            print("❌ Video file not found")

        return True

    except Exception as e:
        print(f"❌ Error during video generation: {e}")
        return False

if __name__ == "__main__":
    success = test_video_generation()
    if success:
        print("\n🎉 Test completed successfully!")
    else:
        print("\n💥 Test failed!")
        sys.exit(1)