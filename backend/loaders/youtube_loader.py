from youtube_transcript_api import YouTubeTranscriptApi

def load_youtube(video_id: str) -> str:
    try:
        # Clean video ID if user pastes full URL params
        video_id = video_id.strip().split("&")[0]

        api = YouTubeTranscriptApi()
        transcript_list = api.list(video_id)

        # Try manual English first, fall back to auto-generated
        try:
            transcript = transcript_list.find_transcript(["en"])
        except Exception:
            transcript = transcript_list.find_generated_transcript(["en"])

        data = transcript.fetch()

        # Join all transcript segments into one clean string
        text = " ".join(segment.text.strip() for segment in data)

        return text

    except Exception as e:
        print(f"❌ YouTube loader error: {e}")
        return ""