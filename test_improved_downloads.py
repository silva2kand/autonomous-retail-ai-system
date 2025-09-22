#!/usr/bin/env python3
"""
Test script for improved video download functionality
"""
import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import MediaAgent

def test_improved_downloads():
    print("🧪 Testing improved video download functionality...")
    print("=" * 60)

    # Test the improved MediaAgent
    agent = MediaAgent()
    print("Testing improved video download functionality...")

    # Test with a simple topic
    topics = ['artificial intelligence']
    print(f"\n🎯 Testing with topics: {topics}")
    print("⏳ This may take a few minutes as it searches for real videos...")

    try:
        clips = agent.search_and_download_clips(topics, num_clips=2)

        print(f"\n📊 Results:")
        print(f"Found {len(clips)} clips")

        real_clips = 0
        for i, clip in enumerate(clips):
            if os.path.exists(clip):
                size = os.path.getsize(clip)
                size_mb = size / 1024 / 1024
                if size > 100000:  # Real content
                    real_clips += 1
                    print(f"  ✅ Clip {i}: {os.path.basename(clip)} - {size:,} bytes ({size_mb:.2f} MB) - REAL CONTENT")
                else:
                    print(f"  ⚠️  Clip {i}: {os.path.basename(clip)} - {size:,} bytes ({size_mb:.2f} MB) - PLACEHOLDER")
            else:
                print(f"  ❌ Clip {i}: {os.path.basename(clip)} - FILE NOT FOUND")

        print(f"\n📈 Summary:")
        print(f"  • Total clips: {len(clips)}")
        print(f"  • Real content clips: {real_clips}")
        print(f"  • Placeholder clips: {len(clips) - real_clips}")

        if real_clips > 0:
            print("\n🎉 SUCCESS: Found real video content!")
            print("💡 The improved download system is working!")
        else:
            print("\n⚠️  WARNING: No real content found, still getting placeholders")
            print("🔧 May need to check internet connection or YouTube availability")

    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_improved_downloads()
