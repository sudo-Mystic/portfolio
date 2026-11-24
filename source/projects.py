"""Public portfolio content, ordered by its position on the homepage."""

GITHUB = "https://github.com/sudo-Mystic"
LINKEDIN = "https://www.linkedin.com/in/rishabh-b-90303b245"
EMAIL = "mrmysticuniverse@gmail.com"
SCOOT_SITE = "https://sudo-mystic.github.io/Scoot-releases/"
HOME_ASSISTANT_PR = "https://github.com/home-assistant/core/pull/183175"

PROJECTS = (
    {
        "slug": "scoot",
        "name": "Scoot",
        "category": "Mobile / Embedded",
        "status": "Available for Android",
        "intro": "An Android companion for TVS scooters that brings ride data to your phone and puts the next turn on the scooter’s display.",
        "tags": ("Flutter", "Dart", "Bluetooth LE"),
        "links": (("Get Scoot", SCOOT_SITE), ("Open the cluster simulator", f"{SCOOT_SITE}sim/")),
        "sections": (
            ("The two screens have different jobs",
             "The scooter’s instrument cluster is where a rider can glance at a turn or call alert. The phone is where the same rider can review their route, look back through trips and find where they parked. Scoot uses Bluetooth Low Energy to connect the two."),
            ("Where model support gets tricky",
             "The Bluetooth connection alone tells you very little about what a particular cluster can show. Scoot supports compatible Jupiter SmartXonnect clusters, with partial Ntorq support and experimental speed and odometer telemetry for Zest. The release page lists the current compatibility details."),
            ("Try it with or without a scooter",
             "The browser simulator gives you an instrument cluster to explore before installing the app. If you download the Android APK, the release page can also check the file’s SHA-256 checksum locally in your browser."),
        ),
    },
    {
        "slug": "esp-reddit",
        "name": "esp-reddit",
        "category": "Embedded / Open source",
        "status": "Public library",
        "intro": "A C++ Reddit API client for ESP32 that works within the memory limits of a microcontroller.",
        "tags": ("ESP32", "C++", "ArduinoJson"),
        "links": (("View source", f"{GITHUB}/esp-reddit"),),
        "sections": (
            ("Keep the response small",
             "The client fetches listings and comment trees, with OAuth token refresh and rate-limit backoff. Streaming JSON parsing, field filters and page-size limits keep large responses from consuming more memory than the ESP32 can spare."),
            ("Separate HTTP from the board",
             "The ESP32 network transport handles the hardware-specific work. The rest of the library can run on a host, which makes it possible to test pagination, token refresh and rate-limit behavior without flashing a board."),
            ("Start with a listing",
             "The repository includes a PlatformIO setup and examples for reading a feed, authenticating and working with posts and comments."),
        ),
    },
    {
        "slug": "exam-eval",
        "name": "Exam Evaluation",
        "category": "Web / Applied AI",
        "status": "MVP complete",
        "intro": "A rubric-driven review workflow for grading handwritten exam papers, question by question.",
        "tags": ("Next.js", "PostgreSQL", "Gemini"),
        "links": (("View source", f"{GITHUB}/exam-eval-platform"),),
        "sections": (
            ("Give each grade a source",
             "Faculty upload an exam and marking scheme, review a draft rubric and capture handwritten answer sheets. The grading pipeline works question by question so each proposed mark can be reviewed against its rubric and the corresponding answer."),
            ("Leave the decision with faculty",
             "The review workflow lets faculty inspect the evidence, override marks and publish reports. Exam and class analytics follow from the reviewed results."),
            ("Run grading in the background",
             "A PostgreSQL-backed job queue handles the AI stages. The application uses Next.js and a separate worker, and the live grading stages require configured Gemini credentials."),
        ),
    },
    {
        "slug": "detroit-jev",
        "name": "detroit-jev",
        "category": "Applied AI / Experiment",
        "status": "In progress",
        "intro": "An experiment in keeping AI decisions coherent across a long, branching story.",
        "tags": ("Python", "LLMs", "Story graphs"),
        "links": (),
        "sections": (
            ("Follow a branching narrative",
             "Inspired by Detroit: Become Human, this experiment treats the story as a graph. Each decision advances the run to a new node, so the choices that came before shape what is possible next."),
            ("Make each decision inspectable",
             "The interesting part is seeing why a model chooses one branch and how that choice holds up later. A decision trace makes a run easier to follow and gives each choice context."),
        ),
    },
)
