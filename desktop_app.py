import sys
import os
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
                             QSpinBox, QComboBox, QPushButton, QTextEdit, QProgressBar, QGroupBox,
                             QListWidget, QListWidgetItem, QCheckBox)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt

# Import the classes from main.py
from main import VideoPipeline, NotebookMemory

class TopicProcessor:
    """Process natural language input and suggest subtopics"""
    
    def __init__(self):
        self.subtopic_map = {
            'news': ['politics', 'technology', 'sports', 'business', 'health', 'entertainment', 'world news', 'local news'],
            'technology': ['artificial intelligence', 'machine learning', 'blockchain', 'cybersecurity', 'mobile apps', 'web development', 'cloud computing'],
            'science': ['physics', 'biology', 'chemistry', 'astronomy', 'climate change', 'medical research', 'space exploration'],
            'business': ['finance', 'marketing', 'entrepreneurship', 'startups', 'e-commerce', 'corporate strategy', 'leadership'],
            'health': ['fitness', 'nutrition', 'mental health', 'medical breakthroughs', 'disease prevention', 'wellness', 'healthcare'],
            'sports': ['football', 'basketball', 'tennis', 'olympics', 'athletes', 'training', 'sports medicine'],
            'entertainment': ['movies', 'music', 'gaming', 'celebrities', 'streaming', 'social media', 'pop culture'],
            'education': ['online learning', 'STEM education', 'higher education', 'skill development', 'teaching methods', 'educational technology']
        }
    
    def process_natural_language(self, input_text: str) -> dict:
        """Process natural language input to extract topics and details"""
        input_lower = input_text.lower()
        
        # Extract duration if mentioned
        duration = 5  # default
        if 'minute' in input_lower or 'min' in input_lower:
            import re
            duration_match = re.search(r'(\d+)\s*min', input_lower)
            if duration_match:
                duration = int(duration_match.group(1))
                duration = max(5, min(45, duration))  # clamp to valid range
        
        # Extract voice type
        voice_type = 'male'  # default
        if 'female' in input_lower or 'woman' in input_lower:
            voice_type = 'female'
        
        # Extract style
        style = 'cinematic'  # default
        if 'news' in input_lower:
            style = 'news'
        elif 'documentary' in input_lower:
            style = 'documentary'
        
        # Extract main topics
        topics = []
        
        # Check for explicit topic mentions
        for category, subtopics in self.subtopic_map.items():
            if category in input_lower:
                topics.append(category)
                # Add some related subtopics
                topics.extend(subtopics[:3])  # Add up to 3 related subtopics
                break
        
        # If no specific category found, try to extract keywords
        if not topics:
            words = input_text.split()
            # Look for noun-like words (simple heuristic)
            potential_topics = []
            for word in words:
                word = word.strip('.,!?').lower()
                if len(word) > 3 and word not in ['create', 'make', 'video', 'about', 'want', 'need', 'please', 'show', 'tell']:
                    potential_topics.append(word)
            
            topics = potential_topics[:5]  # Limit to 5 topics
        
        return {
            'topics': topics,
            'duration': duration,
            'voice_type': voice_type,
            'style': style,
            'original_input': input_text
        }
    
    def suggest_subtopics(self, main_topic: str) -> list:
        """Suggest subtopics for a given main topic"""
        main_topic_lower = main_topic.lower()
        
        # Direct match
        if main_topic_lower in self.subtopic_map:
            return self.subtopic_map[main_topic_lower]
        
        # Fuzzy match
        for category in self.subtopic_map:
            if category in main_topic_lower or main_topic_lower in category:
                return self.subtopic_map[category]
        
        # Default suggestions
        return ['latest developments', 'key insights', 'future trends', 'expert analysis', 'real-world applications']

class VideoGeneratorThread(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)

    def __init__(self, topics, duration, voice_type, presenter, style):
        super().__init__()
        self.topics = topics
        self.duration = duration
        self.voice_type = voice_type
        self.presenter = presenter
        self.style = style
        self.pipeline = VideoPipeline()

    def run(self):
        try:
            self.progress.emit(0)  # Initializing
            print("🚀 Starting video generation pipeline...")
            
            self.progress.emit(10)  # Generating script
            print("📝 Generating script...")
            script = self.pipeline.script_agent.generate_script(self.topics, self.duration, self.style)
            
            self.progress.emit(20)  # Searching for clips
            print("🎬 Searching for video clips...")
            num_clips = max(2, self.duration // 2)  # Fewer clips for speed
            clips = self.pipeline.media_agent.search_and_download_clips(self.topics, num_clips)
            
            self.progress.emit(60)  # Creating voice
            print("🎤 Creating voice-over...")
            voice_path = self.pipeline.voice_agent.generate_voice_over(script, self.voice_type)
            
            self.progress.emit(80)  # Assembling video
            print("🎞️ Assembling video...")
            output_path = self.pipeline.video_editor.assemble_video(clips, voice_path, script, self.duration, self.style, self.presenter)
            
            self.progress.emit(100)  # Complete
            print("✅ Video generation complete!")
            
            result = {
                "status": "completed",
                "script": script,
                "clips": clips,
                "voice": voice_path,
                "video_path": output_path,
                "topics": self.topics,
                "duration": self.duration,
                "voice_type": self.voice_type,
                "presenter": self.presenter,
                "style": self.style,
                "progress": 100
            }
            
            self.pipeline.notebook.log("VideoPipeline", "process_topics_full", result)
            self.finished.emit(result)
            
        except Exception as e:
            print(f"❌ Error during video generation: {e}")
            self.error.emit(str(e))

class DesktopApp(QWidget):
    def __init__(self):
        super().__init__()
        self.topic_processor = TopicProcessor()
        self.initUI()
        self.thread = None

    def initUI(self):
        self.setWindowTitle('AI Video Remaker - Desktop Version')
        self.setGeometry(100, 100, 900, 700)

        layout = QVBoxLayout()

        # Natural Language Input section
        nl_group = QGroupBox("Natural Language Input")
        nl_layout = QVBoxLayout()
        
        nl_layout.addWidget(QLabel("Describe your video in natural language:"))
        self.nl_input = QTextEdit()
        self.nl_input.setPlaceholderText("Example: Create a 10-minute video about the latest developments in artificial intelligence and machine learning")
        self.nl_input.setMaximumHeight(80)
        nl_layout.addWidget(self.nl_input)
        
        self.process_nl_btn = QPushButton("Process Input")
        self.process_nl_btn.clicked.connect(self.process_natural_language)
        nl_layout.addWidget(self.process_nl_btn)
        
        nl_group.setLayout(nl_layout)
        layout.addWidget(nl_group)

        # Input section
        input_group = QGroupBox("Video Configuration")
        input_layout = QVBoxLayout()

        # Topics
        topics_layout = QHBoxLayout()
        topics_layout.addWidget(QLabel("Topics (comma-separated):"))
        self.topics_input = QLineEdit("artificial intelligence, machine learning")
        topics_layout.addWidget(self.topics_input)
        input_layout.addLayout(topics_layout)

        # Subtopic suggestions
        subtopic_layout = QHBoxLayout()
        subtopic_layout.addWidget(QLabel("Suggested Subtopics:"))
        self.subtopic_list = QListWidget()
        self.subtopic_list.setMaximumHeight(100)
        self.subtopic_list.itemClicked.connect(self.add_subtopic)
        subtopic_layout.addWidget(self.subtopic_list)
        input_layout.addLayout(subtopic_layout)

        # Duration
        duration_layout = QHBoxLayout()
        duration_layout.addWidget(QLabel("Duration (minutes):"))
        self.duration_spin = QSpinBox()
        self.duration_spin.setRange(5, 45)
        self.duration_spin.setValue(5)
        duration_layout.addWidget(self.duration_spin)
        input_layout.addLayout(duration_layout)

        # Voice type
        voice_layout = QHBoxLayout()
        voice_layout.addWidget(QLabel("Voice Type:"))
        self.voice_combo = QComboBox()
        self.voice_combo.addItems(["male", "female"])
        voice_layout.addWidget(self.voice_combo)
        input_layout.addLayout(voice_layout)

        # Presenter
        presenter_layout = QHBoxLayout()
        presenter_layout.addWidget(QLabel("Presenter:"))
        self.presenter_combo = QComboBox()
        self.presenter_combo.addItems(["none", "expert", "narrator"])
        presenter_layout.addWidget(self.presenter_combo)
        input_layout.addLayout(presenter_layout)

        # Style
        style_layout = QHBoxLayout()
        style_layout.addWidget(QLabel("Style:"))
        self.style_combo = QComboBox()
        self.style_combo.addItems(["cinematic", "documentary", "news"])
        style_layout.addWidget(self.style_combo)
        input_layout.addLayout(style_layout)

        input_group.setLayout(input_layout)
        layout.addWidget(input_group)

        # Generate button
        self.generate_btn = QPushButton("Generate Video")
        self.generate_btn.clicked.connect(self.generate_video)
        layout.addWidget(self.generate_btn)

        # Progress bar
        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        # Status
        self.status_label = QLabel("Ready")
        layout.addWidget(self.status_label)

        # Results
        results_group = QGroupBox("Results")
        results_layout = QVBoxLayout()
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        results_layout.addWidget(self.results_text)
        results_group.setLayout(results_layout)
        layout.addWidget(results_group)

        # Video preview
        preview_group = QGroupBox("Video Preview")
        preview_layout = QVBoxLayout()
        self.preview_label = QLabel("Video preview will appear here after generation")
        self.open_video_btn = QPushButton("Open Generated Video")
        self.open_video_btn.clicked.connect(self.open_video)
        self.open_video_btn.setEnabled(False)
        preview_layout.addWidget(self.preview_label)
        preview_layout.addWidget(self.open_video_btn)
        preview_group.setLayout(preview_layout)
        layout.addWidget(preview_group)

        self.setLayout(layout)

    def process_natural_language(self):
        """Process natural language input and update form fields"""
        input_text = self.nl_input.toPlainText().strip()
        if not input_text:
            return
        
        # Process the input
        result = self.topic_processor.process_natural_language(input_text)
        
        # Update form fields
        if result['topics']:
            self.topics_input.setText(', '.join(result['topics']))
        
        self.duration_spin.setValue(result['duration'])
        
        if result['voice_type'] == 'female':
            self.voice_combo.setCurrentText('female')
        else:
            self.voice_combo.setCurrentText('male')
        
        if result['style'] in ['cinematic', 'documentary', 'news']:
            self.style_combo.setCurrentText(result['style'])
        
        # Show subtopic suggestions
        self.update_subtopic_suggestions(result['topics'][0] if result['topics'] else "")

    def update_subtopic_suggestions(self, main_topic: str):
        """Update the subtopic suggestions list"""
        self.subtopic_list.clear()
        
        if main_topic:
            suggestions = self.topic_processor.suggest_subtopics(main_topic)
            for suggestion in suggestions:
                item = QListWidgetItem(suggestion)
                item.setCheckState(Qt.CheckState.Unchecked)
                self.subtopic_list.addItem(item)

    def add_subtopic(self, item):
        """Add selected subtopic to topics list"""
        current_topics = self.topics_input.text()
        if current_topics:
            new_topics = current_topics + ', ' + item.text()
        else:
            new_topics = item.text()
        self.topics_input.setText(new_topics)

    def generate_video(self):
        topics_text = self.topics_input.text()
        topics = [t.strip() for t in topics_text.split(',') if t.strip()]
        
        if not topics:
            self.status_label.setText("Error: Please enter at least one topic")
            return

        duration = self.duration_spin.value()
        voice_type = self.voice_combo.currentText()
        presenter = self.presenter_combo.currentText()
        style = self.style_combo.currentText()

        self.generate_btn.setEnabled(False)
        self.status_label.setText("🚀 Starting fast video generation...")
        self.progress_bar.setValue(0)
        self.results_text.clear()

        self.thread = VideoGeneratorThread(topics, duration, voice_type, presenter, style)
        self.thread.progress.connect(self.update_progress_with_message)
        self.thread.finished.connect(self.on_generation_finished)
        self.thread.error.connect(self.on_generation_error)
        self.thread.start()

    def update_progress_with_message(self, progress_value):
        """Update progress bar with descriptive messages"""
        messages = {
            0: "🚀 Initializing...",
            10: "📝 Generating script...",
            20: "🎬 Searching for video clips...",
            40: "📥 Downloading clips...",
            60: "🎤 Creating voice-over...",
            80: "🎞️ Assembling video...",
            90: "💾 Finalizing video...",
            100: "✅ Complete!"
        }
        
        message = messages.get(progress_value, f"Processing... {progress_value}%")
        self.status_label.setText(message)
        self.progress_bar.setValue(progress_value)

    def on_generation_finished(self, result):
        self.generate_btn.setEnabled(True)
        self.status_label.setText("Video generation completed!")
        self.results_text.setPlainText(f"Status: {result.get('status', 'unknown')}\n"
                                       f"Video Path: {result.get('video_path', 'N/A')}\n"
                                       f"Topics: {', '.join(result.get('topics', []))}\n"
                                       f"Duration: {result.get('duration', 0)} minutes\n"
                                       f"Voice: {result.get('voice_type', 'N/A')}\n"
                                       f"Style: {result.get('style', 'N/A')}")

        # Update preview
        video_path = result.get('video_path')
        if video_path and os.path.exists(video_path):
            self.preview_label.setText(f"Video generated: {video_path}")
            self.open_video_btn.setEnabled(True)
            self.video_path = video_path
            
            # Auto-play the video
            self.auto_play_video(video_path)
        else:
            self.preview_label.setText("Video file not found")
            self.open_video_btn.setEnabled(False)

    def auto_play_video(self, video_path):
        """Auto-play the generated video"""
        try:
            print(f"Auto-playing video: {video_path}")
            os.startfile(video_path)  # Windows-specific, opens with default player
        except Exception as e:
            print(f"Could not auto-play video: {e}")

    def open_video(self):
        if hasattr(self, 'video_path') and self.video_path:
            os.startfile(self.video_path)  # Windows-specific, opens with default player

    def on_generation_error(self, error_msg):
        self.generate_btn.setEnabled(True)
        self.status_label.setText("Error occurred")
        self.results_text.setPlainText(f"Error: {error_msg}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DesktopApp()
    ex.show()
    sys.exit(app.exec_())