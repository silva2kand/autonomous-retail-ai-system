# AI Video Remaker - Desktop Version

This is the desktop version of the AI Video Remaker application, built with PyQt5.

## Features

✅ **Complete GUI Interface** - Built with PyQt5 featuring:
- Natural language input processing
- Auto subtopic suggestions
- Input fields for topics, duration (5-45 min), voice type, presenter, and style
- Generate button to start video creation
- Real-time progress bar during processing
- Results display with generation details
- Video preview with "Open Generated Video" button
- **Auto-play video** when generation completes

✅ **Natural Language Processing** - Smart input processing:
- Type naturally: "Create a 10-minute video about AI developments"
- Automatically extracts topics, duration, voice preferences
- Suggests relevant subtopics based on main topics

✅ **Auto Subtopic Suggestions** - For example:
- Input "news" → suggests politics, technology, sports, business, etc.
- Input "technology" → suggests AI, blockchain, cybersecurity, etc.

✅ **Seamless Integration** - Uses the same backend logic as your web version:
- All agents (ScriptAgent, MediaAgent, VoiceAgent, VideoEditor, AIVideoGenerator)
- Same video pipeline and processing workflow
- Identical output quality and features

✅ **Real Media Downloads** - Downloads actual YouTube clips using yt-dlp
✅ **Voice Generation** - Creates voice-over using Google Text-to-Speech
✅ **Video Assembly** - Combines clips with effects and transitions

## Requirements

- Python 3.8+
- All packages listed in requirements.txt

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Desktop App

```bash
python desktop_app.py
```

Or with virtual environment:
```bash
C:/Users/Siva/Documents/GitHub/ai-thatsilva/.venv/Scripts/python.exe desktop_app.py
```

## Usage

### Natural Language Input
1. Use the "Natural Language Input" section
2. Type naturally: "Create a 15-minute documentary about climate change with female narrator"
3. Click "Process Input" - the system will automatically:
   - Extract topics (climate change)
   - Set duration (15 minutes)
   - Set voice type (female)
   - Set style (documentary)
   - Suggest relevant subtopics

### Manual Configuration
1. Enter topics (comma-separated) or use suggestions
2. Select duration (5-45 minutes)
3. Choose voice type (male/female)
4. Select presenter style
5. Choose video style
6. Click "Generate Video"

### Auto-Play Feature
- When video generation completes, the video automatically opens in your default media player
- You can also manually open it using the "Open Generated Video" button

## Examples

### Example 1: Natural Language
Input: "Make a 10-minute video about artificial intelligence and machine learning"
- Automatically sets: Topics, 10min duration, cinematic style
- Suggests subtopics: neural networks, deep learning, applications, etc.

### Example 2: Topic-Based Suggestions
Input topic: "news"
- Suggests: politics, technology, sports, business, health, entertainment

### Example 3: Complex Request
Input: "Create a 20-minute documentary about space exploration with expert narration"
- Extracts: space exploration topic, 20 minutes, documentary style, expert presenter

## Output

- Generated videos saved in `output/` directory
- Voice-over files in MP3 format
- Downloaded clips in `downloads/` directory
- Video files named: `final_video_[style]_[duration]min.mp4`

## Notes

- The app runs video generation in a separate thread to keep the UI responsive
- Videos are automatically played when generation completes
- Real YouTube clips are downloaded and used in the video
- Voice-over is generated using Google Text-to-Speech
- Supports 5-45 minute videos with appropriate content scaling
- Generated videos are saved in the `output/` directory
- Media clips are downloaded to the `downloads/` directory