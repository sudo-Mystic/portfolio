"""Public project files and contact links."""

GITHUB = "https://github.com/sudo-Mystic"
LINKEDIN = "https://www.linkedin.com/in/rishabh-b-90303b245"
EMAIL = "mrmysticuniverse@gmail.com"
HOME_ASSISTANT_PR = "https://github.com/home-assistant/core/pull/183175"

PROJECTS = (
    {
        "slug": "scoot",
        "file": "scoot.dart",
        "language": "Dart",
        "name": "Scoot",
        "intro": "Android companion for compatible TVS SmartXonnect scooters.",
        "tags": ("Flutter", "Dart", "Bluetooth LE"),
        "links": (("Download Scoot", "https://sudo-mystic.github.io/Scoot-releases/"),),
        "details": (
            ("Dashboard", "Live telemetry, trip history and parked location on your phone."),
            ("Instrument cluster", "Turn-by-turn directions and call alerts over Bluetooth."),
            ("Compatibility", "Jupiter 110/125 SmartXonnect, partial Ntorq support and experimental Zest telemetry. See the download page for current support."),
        ),
    },
    {
        "slug": "esp-reddit",
        "file": "esp_reddit.cpp",
        "language": "C++",
        "name": "esp-reddit",
        "intro": "A lightweight C++ Reddit API client for ESP32.",
        "tags": ("ESP32", "C++", "ArduinoJson"),
        "links": (("View source", f"{GITHUB}/esp-reddit"),),
        "details": (
            ("API", "Listings, posts and comments, with OAuth token refresh and rate-limit backoff."),
            ("Memory", "Streaming JSON, field filters and capped page sizes."),
            ("Testing", "A separate ESP32 transport lets the client logic run in host tests."),
        ),
    },
    {
        "slug": "exam-eval",
        "file": "exam_eval.md",
        "language": "Markdown",
        "name": "Exam Evaluation",
        "intro": "AI-assisted grading for handwritten exam papers, with faculty review.",
        "tags": ("Next.js", "PostgreSQL", "Gemini"),
        "links": (("View source", f"{GITHUB}/exam-eval-platform"),),
        "details": (
            ("Grading", "Capture answer sheets and draft question-level marks against a rubric."),
            ("Review", "Faculty check the evidence, adjust marks and publish reports."),
            ("Pipeline", "A PostgreSQL job queue and separate worker run the Gemini stages."),
        ),
    },
    {
        "slug": "detroit-jev",
        "file": "detroit_jev.py",
        "language": "Python",
        "name": "detroit-jev",
        "intro": "An experiment in how AI decisions hold together across a branching story.",
        "tags": ("Python", "LLMs", "Story graphs"),
        "links": (),
        "details": (
            ("Story graph", "The narrative is represented as choices and consequences."),
            ("Decision trace", "The runner records the model’s choices so a playthrough can be reviewed."),
        ),
    },
)
