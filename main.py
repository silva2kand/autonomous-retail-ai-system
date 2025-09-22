import os
from typing import List, Dict, Any
import json
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    # dotenv is optional; proceed if not installed
    pass

from flask import Flask, request, render_template_string, send_file

# Configuration
# Video pipeline configuration
DOWNLOAD_DIR = os.environ.get("DOWNLOAD_DIR", "downloads")
OUTPUT_DIR = os.environ.get("OUTPUT_DIR", "output")
ASSETS_DIR = os.environ.get("ASSETS_DIR", "assets")

# Ensure directories exist
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(ASSETS_DIR, exist_ok=True)

app = Flask(__name__)
pipeline = None

class NotebookMemory:
    def __init__(self):
        self.logs = []

    def log(self, agent_name: str, action: str, result: Any):
        entry = {
            "agent": agent_name,
            "action": action,
            "result": str(result),
            "timestamp": "2025-09-15"  # Placeholder
        }
        self.logs.append(entry)
        print(f"Logged: {entry}")

    def get_history(self):
        return self.logs

notebook = NotebookMemory()

class VideoPipeline:
    def __init__(self):
        self.notebook = notebook
        self.script_agent = ScriptAgent()
        self.media_agent = MediaAgent()
        self.voice_agent = VoiceAgent()
        self.video_editor = VideoEditor()
        self.ai_generator = AIVideoGenerator()

    def process_topics(self, topics: List[str]) -> Dict[str, Any]:
        """Process topics and generate video pipeline (legacy method)"""
        return self.process_topics_full(topics, 5, 'male', 'none', 'cinematic')

    def process_topics_full(self, topics: List[str], duration: int, voice_type: str, presenter: str, style: str) -> Dict[str, Any]:
        """Process topics and generate video pipeline with full options"""
        print(f"Processing topics: {topics}, duration: {duration}min, voice: {voice_type}, style: {style}")
        
        try:
            # Generate script
            script = self.script_agent.generate_script(topics, duration, style)
            
            # Calculate how many clips we need (10-45 seconds each for 5-45 min videos)
            total_seconds = duration * 60
            clip_duration_range = (10, 45)
            # Ensure we have enough clips for longer videos
            min_clips = max(5, duration // 3)  # At least 5 clips, more for longer videos
            num_clips = max(min_clips, total_seconds // 30)  # More clips for longer duration
            
            # Search and download media
            clips = self.media_agent.search_and_download_clips(topics, num_clips, clip_duration_range)
            
            # Generate voice over
            voice_path = self.voice_agent.generate_voice_over(script, voice_type)
            
            # Assemble video
            output_path = self.video_editor.assemble_video(clips, voice_path, script, duration, style, presenter)
            
            result = {
                "status": "completed",
                "script": script,
                "clips": clips,
                "voice": voice_path,
                "video_path": output_path,
                "topics": topics,
                "duration": duration,
                "voice_type": voice_type,
                "presenter": presenter,
                "style": style,
                "progress": 100
            }
            
            self.notebook.log("VideoPipeline", "process_topics_full", result)
            return result
            
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "topics": topics,
                "duration": duration,
                "voice_type": voice_type
            }

class ScriptAgent:
    def generate_script(self, topics: List[str], duration: int = 5, style: str = 'cinematic') -> str:
        """Generate narrative script from topics with duration and style"""
        print(f"Generating {style} script for topics: {topics}, duration: {duration}min")
        
        # Calculate word count based on duration (roughly 120-150 words per minute for video narration)
        if duration <= 10:
            target_words = duration * 120
        elif duration <= 20:
            target_words = duration * 130
        else:
            target_words = duration * 140  # Slower pace for longer videos
        
        # Create a structured script based on style
        if style == 'cinematic':
            if duration <= 10:
                script = f"""Welcome to this cinematic exploration of {', '.join(topics)}.

In this {duration}-minute journey, we'll dive deep into the fascinating world of {topics[0]}.

[Scene transition with dramatic music]

The evolution of {topics[0]} has revolutionized how we understand {topics[1] if len(topics) > 1 else 'technology'}.

[Visual effects: slow motion footage]

Experts predict that {topics[0]} will continue to transform our society in unprecedented ways.

[Closing scene with inspiring music]

Thank you for joining us on this cinematic adventure through {', '.join(topics)}."""
            else:
                script = f"""Welcome to this comprehensive cinematic exploration of {', '.join(topics)}.

In this {duration}-minute cinematic journey, we embark on a profound exploration of {topics[0]} and its transformative impact on our world.

[Opening montage with epic music]

Chapter 1: The Genesis
The story begins with the fundamental principles of {topics[0]}. From its earliest conceptualizations to breakthrough discoveries, we'll trace the historical development that brought us to where we are today.

[Scene transition - documentary footage]

Chapter 2: Current Landscape
Today, {topics[0]} intersects with {topics[1] if len(topics) > 1 else 'every aspect of modern life'}. We'll examine real-world applications, cutting-edge research, and the practical implications for businesses and society.

[Visual effects: data visualization and expert interviews]

Chapter 3: Future Horizons
Looking ahead, the future of {topics[0]} promises unprecedented possibilities. We'll explore emerging trends, potential challenges, and the ethical considerations that will shape its development.

[Closing sequence with reflective music]

As we conclude this {duration}-minute exploration, one thing becomes clear: {topics[0]} is not just a technology—it's a catalyst for human progress and innovation.

Thank you for joining us on this cinematic journey through {', '.join(topics)}."""
        
        elif style == 'documentary':
            if duration <= 10:
                script = f"""Documentary: Understanding {', '.join(topics)}

This {duration}-minute documentary examines the critical role of {topics[0]} in modern society.

Through expert interviews and real-world examples, we'll explore how {topics[0]} intersects with {topics[1] if len(topics) > 1 else 'contemporary issues'}.

The implications for our future are profound and far-reaching."""
            else:
                script = f"""Documentary Series: Deep Dive into {', '.join(topics)}

This comprehensive {duration}-minute documentary series provides an in-depth examination of {topics[0]} and its multifaceted impact on our world.

[Opening credits with investigative music]

Part 1: Foundations and Origins
We begin by exploring the historical context and fundamental principles that gave rise to {topics[0]}. Through archival footage and expert analysis, we'll understand the key developments that shaped its evolution.

[Interviews with pioneers in the field]

Part 2: Current Applications and Challenges
Today, {topics[0]} is transforming industries and societies across the globe. We'll examine real-world implementations, success stories, and the challenges that accompany rapid technological advancement.

[Case studies and data analysis]

Part 3: Societal Impact and Future Outlook
As we look to the future, {topics[0]} presents both opportunities and challenges. We'll explore the ethical considerations, regulatory frameworks, and societal implications that will define its role in tomorrow's world.

[Closing reflections with contemplative music]

This documentary series has explored the profound impact of {', '.join(topics)} on our present and future. The journey continues..."""
        
        elif style == 'news':
            script = f"""Breaking News: Latest Developments in {', '.join(topics)}

In today's news briefing, we examine the latest breakthroughs in {topics[0]}.

Industry experts are calling this a turning point for {topics[1] if len(topics) > 1 else 'innovation'}.

Stay tuned for more updates on this developing story."""
        
        else:  # educational
            if duration <= 10:
                script = f"""Educational Series: {', '.join(topics)}

Welcome to our educational exploration of {topics[0]}.

In this {duration}-minute lesson, we'll cover:
- The fundamentals of {topics[0]}
- Real-world applications
- Future implications

By the end of this video, you'll have a comprehensive understanding of {', '.join(topics)}."""
            else:
                script = f"""Educational Course: Mastering {', '.join(topics)}

Welcome to this comprehensive {duration}-minute educational course on {topics[0]}. This series is designed to provide you with a complete understanding of the subject matter.

[Course introduction with engaging graphics]

Module 1: Introduction and Fundamentals
We'll start with the basic concepts and principles of {topics[0]}. Understanding these foundations is crucial for grasping the more advanced topics we'll cover later.

[Interactive diagrams and explanations]

Module 2: Core Concepts and Theory
Building on the fundamentals, we'll explore the theoretical framework that underlies {topics[0]}. This includes key principles, methodologies, and the scientific basis for the field.

[Visual demonstrations and examples]

Module 3: Practical Applications
Theory meets practice as we examine real-world applications of {topics[0]}. We'll look at case studies, industry implementations, and the practical benefits of these concepts.

[Real-world examples and demonstrations]

Module 4: Advanced Topics and Future Directions
For those ready to dive deeper, we'll explore cutting-edge developments and emerging trends in {topics[0]}. This includes future possibilities and ongoing research.

[Expert interviews and research highlights]

Module 5: Conclusion and Next Steps
We'll wrap up our comprehensive exploration by reviewing key concepts and discussing how you can apply this knowledge in your own work or studies.

[Course summary and resources]

Thank you for completing this educational journey through {', '.join(topics)}. Remember, learning is a continuous process—keep exploring and applying these concepts in your own projects."""
        
        notebook.log("ScriptAgent", "generate_script", f"Generated {len(script)} character script")
        return script

class MediaAgent:
    def search_and_download_clips(self, topics: List[str], num_clips: int = 3, duration_range: tuple = (10, 45)) -> List[str]:
        """Search for and download relevant video clips from multiple sources - IMPROVED VERSION"""
        print(f"Searching for {num_clips} clips about: {topics}")

        clips = []

        try:
            import yt_dlp
            import random
            import time

            # Enhanced search queries for better results
            search_queries = []
            for topic in topics:
                search_queries.extend([
                    f"{topic} educational video",
                    f"{topic} tutorial",
                    f"{topic} explanation",
                    f"{topic} documentary clip",
                    f"{topic} news report",
                    f"{topic} overview",
                    f"{topic} guide",
                    f"{topic} introduction"
                ])

            # Improved download options for reliability
            ydl_opts = {
                'format': 'best[height<=720][ext=mp4]',  # Better quality but still reasonable
                'outtmpl': os.path.join(DOWNLOAD_DIR, 'temp_clip_%(id)s.%(ext)s'),
                'quiet': False,  # Show progress for debugging
                'no_warnings': False,
                'extract_flat': False,
                'download_ranges': lambda info_dict, ydl: [{'start_time': 0, 'end_time': 45}],  # Download up to 45 seconds
                'socket_timeout': 30,  # Timeout for slow connections
                'retries': 3,  # Retry failed downloads
                'fragment_retries': 3,
                'skip_unavailable_fragments': True,
                'ignoreerrors': False,  # Don't ignore errors
                'restrictfilenames': True,
                'windowsfilenames': True,
            }

            downloaded_count = 0
            max_attempts = min(num_clips * 3, len(search_queries))  # More attempts per clip
            used_queries = set()  # Track used queries to avoid duplicates

            for i in range(max_attempts):
                if downloaded_count >= num_clips:
                    break

                try:
                    # Get a unique query we haven't used yet
                    available_queries = [q for q in search_queries if q not in used_queries]
                    if not available_queries:
                        used_queries.clear()  # Reset if we've used all queries
                        available_queries = search_queries[:]

                    query = random.choice(available_queries)
                    used_queries.add(query)
                    print(f"Search attempt {i+1}/{max_attempts}: {query}")

                    # Search for multiple results to have better options
                    with yt_dlp.YoutubeDL({'quiet': True, 'extract_flat': True, 'max_downloads': 3}) as ydl:
                        search_results = ydl.extract_info(f"ytsearch3:{query}", download=False)

                        if 'entries' in search_results and search_results['entries']:
                            # Try each video in the search results
                            for video in search_results['entries']:
                                if downloaded_count >= num_clips:
                                    break

                                try:
                                    video_url = video['url']
                                    print(f"  Trying video: {video.get('title', 'Unknown title')}")

                                    # Download with improved options
                                    download_opts = ydl_opts.copy()
                                    download_opts['outtmpl'] = os.path.join(DOWNLOAD_DIR, f"clip_{downloaded_count}.%(ext)s")

                                    with yt_dlp.YoutubeDL(download_opts) as ydl_download:
                                        info = ydl_download.extract_info(video_url, download=True)
                                        filename = ydl_download.prepare_filename(info)

                                        # Enhanced validation
                                        if os.path.exists(filename):
                                            file_size = os.path.getsize(filename)
                                            print(f"    Downloaded: {os.path.basename(filename)} ({file_size/1024/1024:.2f} MB)")

                                            if file_size > 100000:  # At least 100KB for real content
                                                clips.append(filename)
                                                downloaded_count += 1
                                                print(f"✅ Successfully downloaded clip {downloaded_count}: {os.path.basename(filename)}")
                                                break  # Success, move to next clip
                                            else:
                                                print(f"    File too small ({file_size} bytes), trying next video...")
                                                if os.path.exists(filename):
                                                    os.remove(filename)
                                        else:
                                            print("    File not found after download")

                                except Exception as dl_error:
                                    print(f"    Download failed: {dl_error}")
                                    continue

                        else:
                            print(f"  No search results for: {query}")

                except Exception as e:
                    print(f"Search attempt {i+1} failed: {e}")
                    time.sleep(1)  # Brief pause before retry
                    continue

        except ImportError:
            print("yt-dlp not available, will create placeholder clips")
        except Exception as e:
            print(f"MediaAgent error: {e}")

        # If we don't have enough real clips, try alternative sources or create better placeholders
        if len(clips) < num_clips:
            print(f"Only got {len(clips)}/{num_clips} real clips, attempting alternative methods...")

            # Try alternative search approach
            alt_clips = self._try_alternative_downloads(topics, num_clips - len(clips))
            clips.extend(alt_clips)

        # Final fallback: create minimal placeholders only if we have no real content
        if not clips:
            print("No real clips obtained, creating minimal placeholders...")
            clips = self._create_minimal_placeholders(num_clips, topics)

        print(f"Total clips ready: {len(clips)} (real: {len([c for c in clips if os.path.getsize(c) > 100000])})")
        notebook.log("MediaAgent", "search_and_download_clips", f"Downloaded {len(clips)} clips")
        return clips

    def _create_fast_placeholders(self, num_clips: int, topics: List[str]) -> List[str]:
        """Create fast, simple placeholder videos without text (no ImageMagick required)"""
        clips = []
        try:
            from moviepy.editor import ColorClip

            for i in range(num_clips):
                clip_path = os.path.join(DOWNLOAD_DIR, f"clip_{i}_placeholder.mp4")

                # Create a simple colored background (no text to avoid ImageMagick dependency)
                colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255)]
                bg_color = colors[i % len(colors)]

                # Create simple color clip
                background = ColorClip(size=(1280, 720), color=bg_color, duration=10)

                # Fast encoding with minimal settings
                background.write_videofile(
                    clip_path,
                    fps=24,
                    codec='libx264',
                    audio_codec='aac',
                    bitrate='800k',
                    verbose=False,
                    logger=None,
                    threads=2
                )

                background.close()
                clips.append(clip_path)
                print(f"Created simple placeholder: {os.path.basename(clip_path)}")

        except Exception as e:
            print(f"Failed to create video placeholders: {e}")
            # Fallback to text files
            for i in range(num_clips):
                clip_path = os.path.join(DOWNLOAD_DIR, f"clip_{i}_placeholder.mp4")
                with open(clip_path.replace('.mp4', '.txt'), 'w') as f:
                    topic_text = topics[i % len(topics)] if topics else "Topic"
                    f.write(f"Placeholder for {topic_text}")
                clips.append(clip_path)

        return clips

    def _try_alternative_downloads(self, topics: List[str], num_clips: int) -> List[str]:
        """Try alternative download methods when primary method fails"""
        print(f"Trying alternative download methods for {num_clips} clips...")
        clips = []

        try:
            import yt_dlp

            # Alternative search queries - more specific and educational
            alt_queries = []
            for topic in topics:
                alt_queries.extend([
                    f"{topic} educational content",
                    f"learn about {topic}",
                    f"{topic} basics tutorial",
                    f"{topic} fundamentals",
                    f"{topic} course preview"
                ])

            # Simplified download options for alternative method
            alt_opts = {
                'format': 'best[height<=480][ext=mp4]',
                'outtmpl': os.path.join(DOWNLOAD_DIR, f"alt_clip_%(autonumber)s.%(ext)s"),
                'quiet': True,
                'no_warnings': True,
                'socket_timeout': 20,
                'retries': 2,
            }

            for i in range(min(num_clips * 2, len(alt_queries))):
                if len(clips) >= num_clips:
                    break

                try:
                    query = alt_queries[i % len(alt_queries)]
                    print(f"  Alternative search: {query}")

                    with yt_dlp.YoutubeDL({'quiet': True, 'extract_flat': True, 'max_downloads': 1}) as ydl:
                        search_results = ydl.extract_info(f"ytsearch1:{query}", download=False)

                        if 'entries' in search_results and search_results['entries']:
                            video = search_results['entries'][0]
                            video_url = video['url']

                            with yt_dlp.YoutubeDL(alt_opts) as ydl_download:
                                info = ydl_download.extract_info(video_url, download=True)
                                filename = ydl_download.prepare_filename(info)

                                if os.path.exists(filename) and os.path.getsize(filename) > 50000:
                                    clips.append(filename)
                                    print(f"  ✅ Alternative download successful: {os.path.basename(filename)}")
                                else:
                                    if os.path.exists(filename):
                                        os.remove(filename)

                except Exception as e:
                    print(f"  Alternative download attempt {i+1} failed: {e}")
                    continue

        except Exception as e:
            print(f"Alternative download method failed: {e}")

        return clips

    def _create_minimal_placeholders(self, num_clips: int, topics: List[str]) -> List[str]:
        """Create minimal placeholder files when all download methods fail"""
        clips = []

        for i in range(num_clips):
            clip_path = os.path.join(DOWNLOAD_DIR, f"clip_{i}_minimal.mp4")

            # Create a simple text file indicating the content that should be there
            with open(clip_path.replace('.mp4', '.txt'), 'w') as f:
                topic_text = topics[i % len(topics)] if topics else "Topic"
                f.write(f"Minimal placeholder for: {topic_text}\n")
                f.write("This indicates that real video content could not be downloaded.\n")
                f.write("To fix: Check internet connection, YouTube availability, and yt-dlp installation.")

            # Create a tiny video file if possible
            try:
                from moviepy.editor import ColorClip
                background = ColorClip(size=(640, 360), color=(50, 50, 50), duration=5)
                background.write_videofile(clip_path, fps=10, codec='libx264', verbose=False, logger=None)
                background.close()
                clips.append(clip_path)
                print(f"Created minimal placeholder: {os.path.basename(clip_path)}")
            except:
                clips.append(clip_path.replace('.mp4', '.txt'))

        return clips

    def _trim_video(self, video_path: str, duration: int):
        """Trim video to specified duration"""
        try:
            from moviepy.editor import VideoFileClip
            clip = VideoFileClip(video_path)
            if clip.duration > duration:
                trimmed = clip.subclip(0, duration)
                trimmed.write_videofile(video_path, fps=24, codec='libx264', verbose=False, logger=None)
                clip.close()
                trimmed.close()
        except:
            pass  # Skip trimming if fails

class VoiceAgent:
    def generate_voice_over(self, script: str, voice_type: str = 'male') -> str:
        """Generate voice over from script with specified voice type - FAST VERSION"""
        print(f"Fast generating {voice_type} voice over ({len(script)} chars)")

        voice_path = os.path.join(OUTPUT_DIR, f"voiceover_{voice_type}.mp3")

        try:
            from gtts import gTTS

            # Limit text for faster generation and split if too long
            max_chars = 1000  # Shorter for speed
            text_to_speak = script[:max_chars]

            # Create TTS with optimized settings
            tts = gTTS(
                text=text_to_speak,
                lang='en',
                slow=False,  # Faster speech
                tld='com'    # Use .com domain for faster response
            )

            # Save the audio
            tts.save(voice_path)

            # Quick validation
            if os.path.exists(voice_path) and os.path.getsize(voice_path) > 1000:
                print(f"✅ Voice over saved: {voice_path} ({os.path.getsize(voice_path)} bytes)")
                return voice_path
            else:
                raise Exception("Voice file too small or missing")

        except ImportError:
            print("gTTS not available, creating silent audio placeholder")
            return self._create_silent_audio(voice_path)
        except Exception as e:
            print(f"Voice generation failed: {e}, creating silent audio")
            return self._create_silent_audio(voice_path)

    def _create_silent_audio(self, audio_path: str) -> str:
        """Create a silent audio file as fallback"""
        try:
            from moviepy.editor import AudioClip

            # Create 10 seconds of silence
            silent_audio = AudioClip(lambda t: 0, duration=10)
            silent_audio.write_audiofile(audio_path, verbose=False, logger=None)
            silent_audio.close()

            if os.path.exists(audio_path):
                print(f"✅ Created silent audio: {audio_path}")
                return audio_path

        except:
            pass

        # Last resort - create text file
        text_path = audio_path.replace('.mp3', '.txt')
        with open(text_path, 'w') as f:
            f.write("# Silent audio placeholder")
        return text_path

class VideoEditor:
    def assemble_video(self, clips: List[str], voice: str, script: str, duration: int = 5, style: str = 'cinematic', presenter: str = 'none') -> str:
        """Assemble final video - SIMPLIFIED VERSION without MoviePy dependency"""
        print(f"Simple assembling {style} video, duration: {duration}min")

        output_path = os.path.join(OUTPUT_DIR, f"final_video_{style}_{duration}min.mp4")

        # Try MoviePy first, fallback to simple method
        try:
            return self._try_moviepy_assembly(clips, voice, script, duration, style, output_path)
        except Exception as e:
            print(f"MoviePy failed: {e}, using simple method")
            return self._create_simple_output(script, duration, style, output_path)

    def _try_moviepy_assembly(self, clips: List[str], voice: str, script: str, duration: int, style: str, output_path: str) -> str:
        """Try to assemble video using MoviePy"""
        from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip, concatenate_videoclips

        # Quick voice validation
        voice_clip = None
        if os.path.exists(voice) and os.path.getsize(voice) > 1000:
            try:
                voice_clip = AudioFileClip(voice)
                target_duration = duration * 60
                if voice_clip.duration > target_duration:
                    voice_clip = voice_clip.subclip(0, target_duration)
            except:
                voice_clip = None

        # Process video clips
        video_clips = []
        available_clips = [c for c in clips if os.path.exists(c) and os.path.getsize(c) > 10000]

        if not available_clips:
            raise Exception("No valid clips found")

        # Load and process clips quickly
        target_clip_duration = min(15, (duration * 60) / len(available_clips))

        for clip_path in available_clips[:min(len(available_clips), 2)]:  # Max 2 clips for speed
            try:
                clip = VideoFileClip(clip_path)
                if clip.size[0] > 1280:
                    clip = clip.resize(width=1280)
                if clip.duration > target_clip_duration:
                    clip = clip.subclip(0, target_clip_duration)
                video_clips.append(clip)
            except:
                continue

        if not video_clips:
            raise Exception("No clips could be processed")

        # Quick concatenation
        if len(video_clips) == 1:
            final_clip = video_clips[0]
        else:
            final_clip = concatenate_videoclips(video_clips, method="compose")

        # Adjust duration
        target_duration = duration * 60
        if final_clip.duration < target_duration:
            final_clip = final_clip.loop(duration=target_duration)
        elif final_clip.duration > target_duration:
            final_clip = final_clip.subclip(0, target_duration)

        # Add voice if available
        if voice_clip:
            final_clip = final_clip.set_audio(voice_clip)

        # Fast export
        final_clip.write_videofile(
            output_path,
            fps=24,
            codec='libx264',
            audio_codec='aac',
            bitrate='1000k',
            preset='fast',
            verbose=False,
            logger=None,
            threads=4
        )

        # Cleanup
        final_clip.close()
        for clip in video_clips:
            clip.close()
        if voice_clip:
            voice_clip.close()

        print(f"✅ Video assembled with MoviePy: {output_path}")
        return output_path

    def _create_simple_output(self, script: str, duration: int, style: str, output_path: str) -> str:
        """Create a simple output file when video processing fails"""
        try:
            # Try ffmpeg if available
            import ffmpeg

            # Create a simple video with solid color and text overlay
            text = script[:200] + "..." if len(script) > 200 else script

            (
                ffmpeg
                .input(f'color=c=black:s=1280x720:d={duration*60}', f='lavfi')
                .filter('drawtext', text=text, fontsize=50, fontcolor='white', x='(w-text_w)/2', y='(h-text_h)/2')
                .output(output_path, vcodec='libx264', acodec='aac', preset='fast')
                .run(quiet=True)
            )

            if os.path.exists(output_path):
                print(f"✅ Created video with ffmpeg: {output_path}")
                return output_path

        except:
            pass

        # Fallback: Create an HTML file that can display the content
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>AI Generated Video - {style.title()}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-align: center;
            padding: 50px;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
            background: rgba(255,255,255,0.1);
            padding: 30px;
            border-radius: 10px;
        }}
        .script {{
            background: rgba(0,0,0,0.3);
            padding: 20px;
            border-radius: 5px;
            margin: 20px 0;
            text-align: left;
            white-space: pre-wrap;
        }}
        .play-button {{
            background: #4CAF50;
            color: white;
            padding: 15px 30px;
            border: none;
            border-radius: 5px;
            font-size: 18px;
            cursor: pointer;
            margin: 20px 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🎬 AI Generated Video</h1>
        <p><strong>Style:</strong> {style.title()}</p>
        <p><strong>Duration:</strong> {duration} minutes</p>

        <button class="play-button" onclick="alert('Video processing libraries not available. Please install ffmpeg and MoviePy for full video generation.')">
            ▶️ Play Video
        </button>

        <div class="script">
            <h3>📝 Generated Script:</h3>
            {script}
        </div>

        <p>⚠️ Full video file could not be created due to missing video processing libraries.</p>
        <p>🔧 To fix: Install ffmpeg and ensure MoviePy is working properly.</p>
    </div>
</body>
</html>
"""

        # Save as HTML file
        html_path = output_path.replace('.mp4', '.html')
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"✅ Created HTML video page: {html_path}")
        return html_path

class AIVideoGenerator:
    def generate_ai_video(self, prompt: str, duration: int = 5) -> str:
        """Generate video using AI models"""
        print(f"Generating AI video for prompt: {prompt}")
        
        # In real implementation, this would use models like:
        # - Stable Diffusion for images
        # - AI video generation models
        # - Animation tools
        
        output_path = os.path.join(OUTPUT_DIR, f"ai_generated_{duration}min.mp4")
        
        # Create placeholder
        with open(output_path, 'w') as f:
            f.write(f"# AI Generated Video: {prompt}")
        
        notebook.log("AIVideoGenerator", "generate_ai_video", f"Generated AI video: {output_path}")
        return output_path
        """Add background music based on style"""
        # Create placeholder music file path
        music_path = os.path.join(ASSETS_DIR, f"bg_music_{style}.mp3")
        
        # In real implementation, this would download or generate music
        # For now, create placeholder
        if not os.path.exists(music_path):
            with open(music_path, 'w') as f:
                f.write("# Placeholder background music")
        
        return music_path
        """Assemble final video with effects, subtitles, watermarks"""
        print(f"Assembling {style} video with {len(clips)} clips, duration: {duration}min")
        
        output_path = os.path.join(OUTPUT_DIR, f"final_video_{style}_{duration}min.mp4")
        
        try:
            from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip, concatenate_videoclips
            import random
            
            # Check if voice file exists and is valid
            if os.path.exists(voice) and os.path.getsize(voice) > 100:
                voice_clip = AudioFileClip(voice)
                target_duration = duration * 60
                voice_duration = voice_clip.duration
                
                # If voice is shorter than target, loop or extend
                if voice_duration < target_duration:
                    # Loop the voice or add silence
                    voice_clip = voice_clip.loop(duration=target_duration)
                elif voice_duration > target_duration:
                    voice_clip = voice_clip.subclip(0, target_duration)
            else:
                # Create silent audio if voice file is invalid
                from moviepy.editor import AudioClip
                voice_clip = AudioClip(lambda t: 0, duration=duration*60)
            
            # Process video clips
            video_clips = []
            available_clips = [c for c in clips if os.path.exists(c)]
            
            if not available_clips:
                # Create a placeholder video if no clips available
                from moviepy.editor import ColorClip
                placeholder = ColorClip(size=(1920, 1080), color=(0, 0, 0), duration=duration*60)
                text_clip = TextClip("Video Clips Not Available", fontsize=70, color='white').set_position('center').set_duration(duration*60)
                final_clip = CompositeVideoClip([placeholder, text_clip])
                final_clip = final_clip.set_audio(voice_clip)
                final_clip.write_videofile(output_path, fps=24, codec='libx264', audio_codec='aac')
                return output_path
            
            # Load and process available clips
            for clip_path in available_clips[:min(len(available_clips), 5)]:  # Max 5 clips
                try:
                    clip = VideoFileClip(clip_path)
                    # Resize to 1920x1080
                    clip = clip.resize(height=1080)
                    if clip.w > 1920:
                        clip = clip.resize(width=1920)
                    
                    # Apply style-specific effects
                    if style == 'cinematic':
                        # Add slight color grading
                        clip = clip.fx(lambda c: c.colorx(1.1).lum_contrast(0, 0.1, 1.1))
                    
                    video_clips.append(clip)
                except Exception as e:
                    print(f"Error loading clip {clip_path}: {e}")
                    continue
            
            if not video_clips:
                # Fallback to placeholder
                from moviepy.editor import ColorClip
                placeholder = ColorClip(size=(1920, 1080), color=(0, 0, 0), duration=duration*60)
                final_clip = placeholder.set_audio(voice_clip)
                final_clip.write_videofile(output_path, fps=24, codec='libx264', audio_codec='aac')
                return output_path
            
            # Concatenate clips
            if len(video_clips) == 1:
                final_clip = video_clips[0]
            else:
                final_clip = concatenate_videoclips(video_clips, method="compose")
            
            # Adjust duration
            target_duration = duration * 60
            if final_clip.duration < target_duration:
                # Loop the video if too short
                final_clip = final_clip.loop(duration=target_duration)
            elif final_clip.duration > target_duration:
                final_clip = final_clip.subclip(0, target_duration)
            
            # Add background music
            bg_music_path = self.add_background_music(duration, style)
            if bg_music_path and os.path.exists(bg_music_path):
                from moviepy.editor import AudioFileClip
                bg_music = AudioFileClip(bg_music_path).subclip(0, target_duration).set_volume(0.3)
                # Mix voice with background music
                final_audio = voice_clip.overlay(bg_music)
                final_clip = final_clip.set_audio(final_audio)
            
            # Add text overlays based on presenter choice
            if presenter == 'text':
                # Add title text
                title_text = f"{', '.join([c.split('_')[-1] for c in clips[:1]]).replace('_', ' ').title()}"
                title_clip = TextClip(title_text, fontsize=50, color='white', bg_color='black', size=(1920, 100))
                title_clip = title_clip.set_position(('center', 50)).set_duration(min(10, final_clip.duration))
                
                # Add watermark
                watermark = TextClip("AI Generated Video", fontsize=30, color='white', bg_color='rgba(0,0,0,0.5)')
                watermark = watermark.set_position(('right', 'bottom')).set_duration(final_clip.duration)
                
                final_clip = CompositeVideoClip([final_clip, title_clip, watermark])
            
            # Add subtitles from script (simplified)
            if len(script) > 100:
                # Create simple subtitle clips
                subtitle_clips = []
                words = script.split()
                subtitle_duration = min(5, final_clip.duration / 10)
                
                for i in range(0, min(len(words), 50), 10):  # Show 10 words at a time
                    subtitle_text = ' '.join(words[i:i+10])
                    sub_clip = TextClip(subtitle_text, fontsize=40, color='white', bg_color='rgba(0,0,0,0.7)', size=(1800, 100))
                    sub_clip = sub_clip.set_position(('center', 900)).set_start(i * subtitle_duration / 10).set_duration(subtitle_duration)
                    subtitle_clips.append(sub_clip)
                
                final_clip = CompositeVideoClip([final_clip] + subtitle_clips)
            
            # Export final video
            print(f"Exporting video to: {output_path}")
            final_clip.write_videofile(output_path, fps=24, codec='libx264', audio_codec='aac', verbose=False, logger=None)
            
            # Clean up
            final_clip.close()
            for clip in video_clips:
                clip.close()
            voice_clip.close()
            
        except ImportError:
            print("MoviePy not available, creating placeholder video file")
            # Create placeholder file
            with open(output_path, 'w') as f:
                f.write("# Placeholder video file")
        
        notebook.log("VideoEditor", "assemble_video", f"Assembled {style} video: {output_path}")
        return output_path

def main():
    global pipeline
    pipeline = VideoPipeline()
    topics = ["artificial intelligence", "machine learning"]
    
    # Process pipeline
    result = pipeline.process_topics(topics)
    print(f"Pipeline result: {result}")

@app.route('/', methods=['GET', 'POST'])
def index():
    global pipeline
    if pipeline is None:
        pipeline = VideoPipeline()
        
    if request.method == 'POST':
        action = request.form.get('action')
        topics = request.form.get('topics', '').split(',')
        topics = [t.strip() for t in topics if t.strip()]
        
        if not topics:
            return render_template_string(HTML_TEMPLATE, result={"status": "error", "message": "Please enter at least one topic"}, topics=[])
        
        duration = int(request.form.get('duration', 5))
        if duration < 5 or duration > 45:
            return render_template_string(HTML_TEMPLATE, result={"status": "error", "message": "Duration must be between 5 and 45 minutes"}, topics=topics)
        voice_type = request.form.get('voice_type', 'male')
        presenter = request.form.get('presenter', 'none')
        style = request.form.get('style', 'cinematic')
        
        if action == 'preview':
            # Preview script only
            script = pipeline.script_agent.generate_script(topics, duration, style)
            return render_template_string(HTML_TEMPLATE, result={
                "status": "completed",
                "script": script,
                "topics": topics,
                "duration": duration,
                "voice_type": voice_type,
                "clips": [],
                "video_path": None
            }, topics=topics)
        
        elif action == 'generate':
            try:
                # Full video generation
                result = pipeline.process_topics_full(topics, duration, voice_type, presenter, style)
                return render_template_string(HTML_TEMPLATE, result=result, topics=topics)
            except Exception as e:
                return render_template_string(HTML_TEMPLATE, result={"status": "error", "message": str(e)}, topics=topics)
    
    return render_template_string(HTML_TEMPLATE, result=None, topics=[])

@app.route('/upload/<platform>', methods=['POST'])
def upload_to_platform(platform):
    """Handle social media uploads"""
    video_path = request.form.get('video_path')
    if not video_path or not os.path.exists(video_path):
        return {"status": "error", "message": "Video file not found"}
    
    # Placeholder for social media uploads
    if platform == 'youtube':
        # Implement YouTube API upload
        return {"status": "success", "message": "YouTube upload placeholder"}
    elif platform == 'twitter':
        # Implement Twitter API upload
        return {"status": "success", "message": "Twitter upload placeholder"}
    elif platform == 'facebook':
        # Implement Facebook API upload
        return {"status": "success", "message": "Facebook upload placeholder"}
    
    return {"status": "error", "message": f"Unknown platform: {platform}"}

@app.route('/livestream', methods=['POST'])
def start_livestream():
    """Start live streaming"""
    video_path = request.form.get('video_path')
    platform = request.form.get('platform', 'youtube')

    # Placeholder for live streaming
    return {"status": "success", "message": f"Live stream to {platform} placeholder"}

@app.route('/video/<filename>')
def serve_video(filename):
    """Serve generated video files"""
    try:
        # Serve from output directory
        video_path = os.path.join(OUTPUT_DIR, filename)
        if os.path.exists(video_path):
            return send_file(video_path, mimetype='video/mp4')

        # Also check downloads directory for clips
        clip_path = os.path.join(DOWNLOAD_DIR, filename)
        if os.path.exists(clip_path):
            return send_file(clip_path, mimetype='video/mp4')

        return {"status": "error", "message": "Video file not found"}, 404
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>AI Video Remaker</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 1000px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        h1 { color: #333; text-align: center; }
        .form-group { margin: 15px 0; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        input[type="text"], input[type="number"], select { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }
        .input-row { display: flex; gap: 10px; }
        .input-row > div { flex: 1; }
        button { padding: 12px 25px; background: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }
        button:hover { background: #0056b3; }
        .result { margin-top: 30px; padding: 20px; border: 1px solid #ddd; border-radius: 5px; background: #f9f9f9; }
        .progress { margin: 10px 0; }
        .progress-bar { width: 100%; height: 20px; background: #f0f0f0; border-radius: 10px; overflow: hidden; }
        .progress-fill { height: 100%; background: #007bff; width: 0%; transition: width 0.3s; }
        video { max-width: 100%; margin-top: 10px; border-radius: 5px; }
        .status { padding: 10px; margin: 10px 0; border-radius: 5px; }
        .status.info { background: #d1ecf1; color: #0c5460; }
        .status.success { background: #d4edda; color: #155724; }
        .status.error { background: #f8d7da; color: #721c24; }
        .social-btn { margin: 5px; padding: 8px 15px; background: #dc3545; color: white; border: none; border-radius: 3px; cursor: pointer; }
        .social-btn.youtube { background: #ff0000; }
        .social-btn.twitter { background: #1da1f2; }
        .social-btn.facebook { background: #1877f2; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 AI Video Remaker & Generator</h1>
        <form method="post">
            <div class="form-group">
                <label for="topics">Topics (comma-separated):</label>
                <input type="text" id="topics" name="topics" placeholder="e.g., artificial intelligence, machine learning, future technology" required>
            </div>
            
            <div class="input-row">
                <div class="form-group">
                    <label for="duration">Video Duration (5-45 minutes):</label>
                    <input type="number" id="duration" name="duration" min="5" max="45" value="5" required>
                </div>
                <div class="form-group">
                    <label for="voice_type">Voice Type:</label>
                    <select id="voice_type" name="voice_type">
                        <option value="male">Male</option>
                        <option value="female">Female</option>
                        <option value="mixed">Mixed</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="presenter">Presenter:</label>
                    <select id="presenter" name="presenter">
                        <option value="avatar">AI Avatar</option>
                        <option value="text">Text Overlay</option>
                        <option value="none">None</option>
                    </select>
                </div>
            </div>
            
            <div class="form-group">
                <label for="style">Video Style:</label>
                <select id="style" name="style">
                    <option value="cinematic">Cinematic</option>
                    <option value="documentary">Documentary</option>
                    <option value="news">News Style</option>
                    <option value="educational">Educational</option>
                </select>
            </div>
            
            <button type="submit" name="action" value="generate">🎬 Generate Video</button>
            <button type="submit" name="action" value="preview">👁️ Preview Script Only</button>
            <button type="submit" name="action" value="ai_generate">🤖 AI Generate Video</button>
        </form>
        
        {% if result %}
        <div class="result">
            <h2>🎯 Generation Results</h2>
            
            {% if result.status == 'processing' %}
            <div class="status info">
                <h3>🔄 Processing...</h3>
                <div class="progress">
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: {{ result.progress }}%"></div>
                    </div>
                </div>
                <p>{{ result.message }}</p>
            </div>
            {% endif %}
            
            {% if result.status == 'completed' %}
            <div class="status success">
                <h3>✅ Video Generated Successfully!</h3>
                <p><strong>Topics:</strong> {{ result.topics|join(', ') }}</p>
                <p><strong>Duration:</strong> {{ result.duration }} minutes</p>
                <p><strong>Voice:</strong> {{ result.voice_type }}</p>
                <p><strong>Clips collected:</strong> {{ result.clips|length }}</p>
                <p><strong>Script length:</strong> {{ result.script|length }} characters</p>
            </div>
            
            {% if result.video_path %}
            <h3>🎥 Final Video Preview:</h3>
            <video controls>
                <source src="/video/{{ result.video_path.split('/')[-1] }}" type="video/mp4">
                Your browser does not support the video tag.
            </video>
            
            <h3>📤 Share Options:</h3>
            <button class="social-btn youtube" onclick="uploadToYouTube()">📺 Upload to YouTube</button>
            <button class="social-btn twitter" onclick="uploadToTwitter()">🐦 Share on Twitter</button>
            <button class="social-btn facebook" onclick="uploadToFacebook()">📘 Share on Facebook</button>
            <button class="social-btn" onclick="startLiveStream()">🔴 Start Live Stream</button>
            {% endif %}
            
            {% endif %}
            
            {% if result.status == 'error' %}
            <div class="status error">
                <h3>❌ Error Occurred</h3>
                <p>{{ result.message }}</p>
            </div>
            {% endif %}
        </div>
        {% endif %}
    </div>

    <script>
        async function uploadToYouTube() {
            const videoPath = document.querySelector('video source').src.split('/').pop();
            const response = await fetch('/upload/youtube', {
                method: 'POST',
                headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                body: `video_path=output/${videoPath}`
            });
            const result = await response.json();
            alert(result.message);
        }
        
        async function uploadToTwitter() {
            const videoPath = document.querySelector('video source').src.split('/').pop();
            const response = await fetch('/upload/twitter', {
                method: 'POST',
                headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                body: `video_path=output/${videoPath}`
            });
            const result = await response.json();
            alert(result.message);
        }
        
        async function uploadToFacebook() {
            const videoPath = document.querySelector('video source').src.split('/').pop();
            const response = await fetch('/upload/facebook', {
                method: 'POST',
                headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                body: `video_path=output/${videoPath}`
            });
            const result = await response.json();
            alert(result.message);
        }
        
        async function startLiveStream() {
            const videoPath = document.querySelector('video source').src.split('/').pop();
            const response = await fetch('/livestream', {
                method: 'POST',
                headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                body: `video_path=output/${videoPath}&platform=youtube`
            });
            const result = await response.json();
            alert(result.message);
        }
    </script>
</body>
</html>
"""

if __name__ == "__main__":
    main()
    print("Starting web interface at http://localhost:5000")
    app.run(debug=True)
