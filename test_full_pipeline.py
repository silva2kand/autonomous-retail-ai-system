#!/usr/bin/env python3
"""
Test script for full video generation pipeline
"""
import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import VideoPipeline

def test_full_pipeline():
    print("🎬 Testing full video generation pipeline...")
    print("=" * 60)

    # Test the full pipeline
    pipeline = VideoPipeline()

    # Test with simple topics
    topics = ['artificial intelligence', 'machine learning']
    print(f"\n🎯 Testing with topics: {topics}")
    print("⏳ This will generate a complete video (may take several minutes)...")

    try:
        # Generate a short test video
        result = pipeline.process_topics_full(
            topics=topics,
            duration=5,  # 5 minutes
            voice_type='male',
            presenter='none',
            style='educational'
        )

        print("\n📊 Pipeline Results:")
        print(f"  • Status: {result['status']}")
        print(f"  • Topics: {result['topics']}")
        print(f"  • Duration: {result['duration']} minutes")
        print(f"  • Voice: {result['voice_type']}")
        print(f"  • Style: {result['style']}")
        print(f"  • Clips collected: {len(result['clips'])}")
        print(f"  • Script length: {len(result['script'])} characters")

        if result['status'] == 'completed':
            print("\n🎉 SUCCESS: Full pipeline completed!")
            print("📝 Generated components:")

            # Check if files exist
            if os.path.exists(result['video_path']):
                size = os.path.getsize(result['video_path'])
                print(f"  ✅ Final video: {os.path.basename(result['video_path'])} ({size/1024/1024:.2f} MB)")
            else:
                print(f"  ❌ Final video not found: {result['video_path']}")

            if os.path.exists(result['voice']):
                size = os.path.getsize(result['voice'])
                print(f"  ✅ Voice over: {os.path.basename(result['voice'])} ({size/1024:.0f} KB)")
            else:
                print(f"  ❌ Voice over not found: {result['voice']}")

            # Check clips
            real_clips = 0
            for i, clip in enumerate(result['clips']):
                if os.path.exists(clip):
                    size = os.path.getsize(clip)
                    if size > 100000:
                        real_clips += 1
                        print(f"  ✅ Real clip {i}: {os.path.basename(clip)} ({size/1024/1024:.2f} MB)")
                    else:
                        print(f"  ⚠️  Small clip {i}: {os.path.basename(clip)} ({size/1024:.0f} KB)")
                else:
                    print(f"  ❌ Missing clip {i}: {os.path.basename(clip)}")

            print(f"\n📈 Content Summary:")
            print(f"  • Real video clips: {real_clips}/{len(result['clips'])}")
            print(f"  • Script quality: {len(result['script'])} characters")

            if real_clips > 0:
                print("\n🎬 SUCCESS: Generated video with real content!")
                print("💡 The complete pipeline is working correctly!")
            else:
                print("\n⚠️  WARNING: No real video content in final output")
                print("🔧 Check video processing components")

        elif result['status'] == 'error':
            print(f"\n❌ Pipeline failed: {result['message']}")

    except Exception as e:
        print(f"\n❌ Error during pipeline testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_full_pipeline()
