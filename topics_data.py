import re
from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class Topic:
    id: str
    title: str
    short_description: str
    details: str
    tags: List[str] = field(default_factory=list)
    example_questions: List[str] = field(default_factory=list)
    links: List[Dict[str, str]] = field(default_factory=list)


TOPICS: List[Topic] = [
    Topic(
        id="accounts-and-logins",
        title="Metropolia Accounts & Logins",
        short_description="How to activate your Metropolia account, access email and other services.",
        details=(
            "As a new student, you will receive a Metropolia username which is used for logging into "
            "most services (Oma, email, Wi-Fi, computers, etc.).\n\n"
            "Typical steps:\n"
            "1. Activate your account using the instructions from your admission email.\n"
            "2. Set a strong password and enable multi-factor authentication if available.\n"
            "3. Use your Metropolia email for all official communication.\n\n"
            "If you forget your password, you can reset it through the self-service portal or contact IT support."
        ),
        tags=["account", "login", "password", "email", "user id", "metropolia account", "office 365"],
        example_questions=[
            "How do I activate my Metropolia account?",
            "Where do I find my student email?",
            "I forgot my password, what do I do?",
        ],
        links=[
            {"label": "Account activation / password reset (IT services)", "url": "https://metropolia.fi"},
            {"label": "Metropolia webmail / Microsoft 365 login", "url": "https://portal.office.com"},
        ],
    ),
    Topic(
        id="oma-and-study-tools",
        title="Oma Portal & Study Tools",
        short_description="Where to see courses, grades and study information.",
        details=(
            "Oma is the central portal where you see your studies, announcements and many useful links. "
            "From Oma you usually access:\n\n"
            "- Course registrations\n"
            "- Your study plan\n"
            "- Links to learning environments (like Moodle / other platforms)\n"
            "- Important messages from staff\n\n"
            "Check Oma regularly – many teachers assume you read announcements there."
        ),
        tags=["oma", "study portal", "grades", "course registration", "study info", "schedule"],
        example_questions=[
            "Where do I see my grades?",
            "Where do I register for courses?",
            "What is Oma?",
        ],
        links=[
            {"label": "Oma portal", "url": "https://oma.metropolia.fi"},
        ],
    ),
    Topic(
        id="schedule-and-tuudo",
        title="Schedule & Tuudo",
        short_description="How to find your timetable and classroom locations.",
        details=(
            "Your weekly timetable can usually be checked via the timetable system and the Tuudo app. "
            "In Tuudo you can:\n\n"
            "- See your weekly schedule\n"
            "- Check classroom locations\n"
            "- View upcoming exams\n"
            "- See some announcements\n\n"
            "At the start of the semester, double-check that you are looking at the correct group code "
            "and campus in the timetable."
        ),
        tags=["schedule", "timetable", "tuudo", "classes", "classroom", "room", "where is my class"],
        example_questions=[
            "Where can I see my schedule?",
            "How do I know what classroom I have?",
            "What is Tuudo and how do I use it?",
        ],
        links=[
            {"label": "Tuudo info", "url": "https://www.tuudo.fi"},
        ],
    ),
    Topic(
        id="it-support",
        title="IT Support & Helpdesk",
        short_description="Where to get help if something technical doesn't work.",
        details=(
            "If you have issues with logins, Wi-Fi, software or other technical problems, contact IT support. "
            "First, check if there is a known outage or FAQ in Oma or on the IT pages.\n\n"
            "Prepare the following info before contacting them:\n"
            "- Your full name\n"
            "- Student ID\n"
            "- Clear description of the problem\n"
            "- Screenshots if possible\n"
            "- When the problem started\n\n"
            "This makes it much faster for them to help you."
        ),
        tags=["it support", "helpdesk", "wifi", "technical problem", "password reset", "software"],
        example_questions=[
            "Who do I contact if my login doesn't work?",
            "Wi-Fi isn't working, what do I do?",
        ],
        links=[
            {"label": "Metropolia IT Services", "url": "https://metropolia.fi"},
        ],
    ),
    Topic(
        id="wellbeing-and-support",
        title="Well-being & Student Support",
        short_description="Who to talk to if you feel stressed, lost or need support.",
        details=(
            "Starting your studies can be exciting but also stressful. It's normal to feel overwhelmed. "
            "Metropolia offers support through:\n\n"
            "- Student counsellors\n"
            "- Study psychologists\n"
            "- Health services\n"
            "- Tutors and student organisations\n\n"
            "If you feel lost about your studies, talk to your tutor teacher or student counsellor early. "
            "It's much easier to fix issues in the beginning than at the end of the semester."
        ),
        tags=["wellbeing", "support", "counsellor", "psychologist", "health", "stress", "mental health"],
        example_questions=[
            "Who do I talk to if I'm stressed?",
            "I feel behind in my studies, what do I do?",
        ],
        links=[
            {"label": "Student well-being services", "url": "https://metropolia.fi"},
        ],
    ),
    Topic(
        id="campus-basics",
        title="Campus Basics (Access, Printing, Food)",
        short_description="Everyday practical stuff on campus: access, printing, food, etc.",
        details=(
            "Daily life on campus includes things like access cards, printing, and food.\n\n"
            "- Access card / student card: needed for some doors, printing and student discounts.\n"
            "- Printing: usually done with your student card at designated printers.\n"
            "- Cafeteria: check daily menus online or via the app used on your campus.\n"
            "- Quiet study spaces: libraries and dedicated study areas are usually available.\n\n"
            "Explore your campus during the first weeks so you know where everything is."
        ),
        tags=["campus", "access card", "printing", "cafeteria", "food", "library"],
        example_questions=[
            "How do I use the printers?",
            "Where can I eat on campus?",
            "How do I get into the building?",
        ],
        links=[
            {"label": "Metropolia campuses", "url": "https://metropolia.fi"},
        ],
    ),
]


_WORD_RE = re.compile(r"\w+", re.UNICODE)

def tokenize(text: str):
    return {w.lower() for w in _WORD_RE.findall(text)}

def score_topic(query: str, topic: Topic) -> int:
    """
    Very simple 'AI-like' scoring:
    - Tokenize query
    - Tokenize topic tags + example questions + title
    - Return number of overlapping words
    """
    q_words = tokenize(query)
    corpus_text = " ".join(
        [topic.title]
        + topic.tags
        + topic.example_questions
        + [topic.short_description]
    )
    t_words = tokenize(corpus_text)
    overlap = q_words & t_words
    return len(overlap)


def find_best_topics(query: str, top_k: int = 3) -> List[Topic]:
    scored = [(score_topic(query, topic), topic) for topic in TOPICS]
    scored.sort(key=lambda x: x[0], reverse=True)
    filtered = [t for score, t in scored if score > 0]
    return filtered[:top_k] if filtered else []