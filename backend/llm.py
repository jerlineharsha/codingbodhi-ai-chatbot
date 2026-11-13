import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai


load_dotenv(Path(__file__).resolve().parent / ".env")

WELCOME_MESSAGE = (
    "👋 Hello! Welcome to CodingBodhi!\n\n"
    "How can we help you today?\n\n"
    "1️⃣ Courses\n"
    "2️⃣ Internships\n"
    "3️⃣ Services\n"
    "4️⃣ Contact Us"
)

MAIN_MENU = (
    "🏠 Main Menu\n\n"
    "1️⃣ Courses\n"
    "2️⃣ Internships\n"
    "3️⃣ Services\n"
    "4️⃣ Contact Us"
)

COURSE_MENU = (
    "📚 Courses\n\n"
    "Please select an option:\n\n"
    "1️⃣ Course Details\n"
    "2️⃣ Course Fees\n"
    "3️⃣ Course Enquiry\n"
    "0️⃣ Main Menu"
)

INTERNSHIP_MENU = (
    "💼 Internships\n\n"
    "Please select an option:\n\n"
    "1️⃣ Internship Details\n"
    "2️⃣ Eligibility\n"
    "3️⃣ Apply for Internship\n"
    "0️⃣ Main Menu"
)

SERVICES_MESSAGE = (
    "🛠️ Services\n\n"
    "CodingBodhi offers live online Full Stack Engineering + AI and "
    "Data Engineering + AI training, with hands-on projects, mentor "
    "support, career guidance, and placement assistance.\n\n"
    "0️⃣ Main Menu"
)

CONTACT_MESSAGE = (
    "📞 Contact Us\n\n"
    "Call or WhatsApp: +91 96267 12101\n"
    "Email: info@codingbodhi.com\n"
    "Address: D No 8/2, Omalur Main Road, Angammal Colony, "
    "Salem, Tamil Nadu, India, 636009\n\n"
    "0️⃣ Main Menu"
)

COURSE_DETAILS = (
    "📚 Course Details\n\n"
    "1️⃣ Full Stack Engineering + AI\n"
    "Beginner-friendly training in HTML, CSS, JavaScript, Git, React, "
    "Node.js, Express.js, MongoDB, and AWS. The beginner path covers "
    "30 days of foundations, 3 months of frontend, and 3 months of backend. "
    "Working professionals who know the fundamentals and have 1+ year of "
    "programming experience can take a 4-month program.\n\n"
    "2️⃣ Data Engineering + AI\n"
    "Beginner-friendly training in Python, SQL, Snowflake, dbt, Power BI, "
    "Fivetran, and Airflow. The beginner path covers 30 days of foundations, "
    "3 months of analytics engineering, and 3 months of modern ETL and cloud "
    "data engineering. Working professionals who know the fundamentals and "
    "have 1+ year of SQL or Python experience can take a 4-month program.\n\n"
    "Both programs include live online classes, hands-on projects, mentor "
    "support, career guidance, and placement assistance. Classes are "
    "beginner-friendly and open to learners from any educational background.\n\n"
    "0️⃣ Main Menu"
)

COURSE_FEES = (
    "💰 Course Fees\n\n"
    "Course fees aren't listed on the CodingBodhi website. For current "
    "fees and batch details, call or WhatsApp +91 96267 12101, or email "
    "info@codingbodhi.com.\n\n"
    "0️⃣ Main Menu"
)

COURSE_ENQUIRY = (
    "📝 Course Enquiry\n\n"
    "Tell us your name and whether you're interested in Full Stack "
    "Engineering + AI or Data Engineering + AI. For admissions help, call "
    "or WhatsApp +91 96267 12101, or email info@codingbodhi.com.\n\n"
    "0️⃣ Main Menu"
)

INTERNSHIP_DETAILS = (
    "💼 Internship Details\n\n"
    "The CodingBodhi website doesn't list internship openings or details. "
    "For current opportunities, call or WhatsApp +91 96267 12101, or email "
    "info@codingbodhi.com.\n\n"
    "0️⃣ Main Menu"
)

INTERNSHIP_ELIGIBILITY = (
    "🎓 Eligibility\n\n"
    "Internship eligibility requirements aren't published on the "
    "CodingBodhi website. Please contact the team for current information: "
    "+91 96267 12101 or info@codingbodhi.com.\n\n"
    "0️⃣ Main Menu"
)

INTERNSHIP_APPLY = (
    "📝 Apply for Internship\n\n"
    "An internship application process isn't listed on the CodingBodhi "
    "website. For current opportunities and application instructions, "
    "contact +91 96267 12101 or info@codingbodhi.com.\n\n"
    "0️⃣ Main Menu"
)

_MAIN_MENU_OPTIONS = {
    "1": COURSE_MENU,
    "2": INTERNSHIP_MENU,
    "3": SERVICES_MESSAGE,
    "4": CONTACT_MESSAGE,
}

_MENU_OPTIONS = {
    COURSE_MENU: {
        "1": COURSE_DETAILS,
        "2": COURSE_FEES,
        "3": COURSE_ENQUIRY,
    },
    INTERNSHIP_MENU: {
        "1": INTERNSHIP_DETAILS,
        "2": INTERNSHIP_ELIGIBILITY,
        "3": INTERNSHIP_APPLY,
    },
    SERVICES_MESSAGE: {},
    CONTACT_MESSAGE: {},
    COURSE_DETAILS: {},
    COURSE_FEES: {},
    COURSE_ENQUIRY: {},
    INTERNSHIP_DETAILS: {},
    INTERNSHIP_ELIGIBILITY: {},
    INTERNSHIP_APPLY: {},
}


class ChatGenerationError(RuntimeError):
    pass


def menu_response(
    user_message: str,
    history: list[dict[str, str]] | None = None,
) -> str | None:
    choice = user_message.strip()
    if not choice.isdecimal():
        return None

    last_bot_message = next(
        (turn["message"] for turn in reversed(history or []) if turn["sender"] == "bot"),
        None,
    )
    is_main_menu = last_bot_message in {None, WELCOME_MESSAGE, MAIN_MENU}

    if choice == "0":
        return MAIN_MENU if is_main_menu or last_bot_message in _MENU_OPTIONS else None

    if is_main_menu:
        return _MAIN_MENU_OPTIONS.get(choice, MAIN_MENU)

    options = _MENU_OPTIONS.get(last_bot_message)
    if options is None:
        return None
    return options.get(choice, last_bot_message)


def _local_response(user_message: str) -> str | None:
    message = user_message.casefold()

    if message.strip(" !.,?") in {"hi", "hello", "hey", "hii"}:
        return WELCOME_MESSAGE

    if "roadmap" in message:
        if "python" in message:
            return (
                "A beginner Python roadmap: learn syntax and core data types, "
                "practice functions and collections, then build small projects "
                "and explore a specialization."
            )
        if "web" in message:
            return (
                "A web development roadmap: learn HTML and CSS, practice "
                "JavaScript, build responsive projects, then explore APIs, "
                "databases, and deployment."
            )
        if "ai" in message or "machine learning" in message:
            return (
                "An AI roadmap: start with Python, learn data handling and "
                "basic statistics, study machine-learning fundamentals, then "
                "build and evaluate small projects."
            )
        return "Which roadmap would you like: Python, Artificial Intelligence, or Web Development?"

    if any(word in message for word in ("fee", "fees", "price", "cost", "tuition")):
        return (
            "Course fees aren't listed on the CodingBodhi website. For current "
            "fees and batch details, call or WhatsApp +91 96267 12101, or "
            "email info@codingbodhi.com."
        )

    if "internship" in message:
        return (
            "The CodingBodhi website doesn't list internship openings, "
            "eligibility, or application details. For current opportunities, "
            "call or WhatsApp +91 96267 12101, or email info@codingbodhi.com."
        )

    if "course" in message:
        return (
            "CodingBodhi offers two beginner-friendly programs: Full Stack "
            "Engineering + AI (HTML, CSS, JavaScript, Git, React, Node.js, "
            "Express.js, MongoDB, AWS) and Data Engineering + AI (Python, "
            "SQL, Snowflake, dbt, Power BI, Fivetran, Airflow). Both include "
            "live online classes, hands-on projects, mentor support, career "
            "guidance, and placement assistance. Contact +91 96267 12101 or "
            "info@codingbodhi.com for fees and current batches."
        )

    if any(word in message for word in ("contact", "phone", "email", "address", "whatsapp")):
        return (
            "Call or WhatsApp CodingBodhi at +91 96267 12101, or email "
            "info@codingbodhi.com. Office: D No 8/2, Omalur Main Road, "
            "Angammal Colony, Salem, Tamil Nadu, India, 636009."
        )

    if any(word in message for word in ("service", "program", "training", "classes")):
        return (
            "CodingBodhi offers live online Full Stack Engineering + AI and "
            "Data Engineering + AI training, with hands-on projects, mentor "
            "support, career guidance, and placement assistance."
        )

    if any(word in message for word in ("career", "placement", "interview", "resume")):
        return (
            "CodingBodhi's placement assistance includes technical skill "
            "assessment, resume and LinkedIn profile support, project feedback, "
            "mock technical and HR interviews, and soft-skills training. "
            "Suitable hiring opportunities may be shared with eligible learners "
            "when available; placement isn't guaranteed."
        )

    return None


def _create_interaction(
    client: genai.Client,
    model: str,
    contents: list[dict],
    instruction: str,
):
    return client.interactions.create(
        model=model,
        input=contents,
        system_instruction=instruction,
        timeout=20,
    )


def generate_response(
    user_message: str,
    history: list[dict[str, str]] | None = None,
) -> str:
    menu_reply = menu_response(user_message, history)
    if menu_reply is not None:
        return menu_reply

    local_response = _local_response(user_message)
    if local_response is not None:
        return local_response

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ChatGenerationError(
            "The chatbot is not configured. Set GEMINI_API_KEY in backend/.env."
        )

    contents = []
    for turn in history or []:
        contents.append(
            {
                "type": "model_output" if turn["sender"] == "bot" else "user_input",
                "content": [{"type": "text", "text": turn["message"]}],
            }
        )
    contents.append(
        {
            "type": "user_input",
            "content": [{"type": "text", "text": user_message}],
        }
    )

    system_instruction = """
You are CodingBodhi AI, the friendly assistant for the CodingBodhi website.
Help visitors with courses, internships, learning roadmaps, careers, placements,
and general programming questions. Be concise, warm, and practical. Do not invent
CodingBodhi-specific details. Use these published website facts:
- Programs: Full Stack Engineering + AI, and Data Engineering + AI.
- Full Stack covers HTML, CSS, JavaScript, Git, React, Node.js, Express.js,
  MongoDB, and AWS. Beginner path: 30-day foundation, 3 months frontend,
  3 months backend. Working professionals who know the fundamentals and have
  1+ year of programming experience can take a 4-month program.
- Data Engineering covers Python, SQL, Snowflake, dbt, Power BI, Fivetran,
  and Airflow. Beginner path: 30-day foundation, 3 months analytics engineering,
  3 months modern ETL and cloud data engineering. Working professionals who
  know the fundamentals and have 1+ year of SQL or Python experience can take
  a 4-month program.
- Both programs are beginner-friendly, live online, and include hands-on
  projects, mentor support, career guidance, and placement assistance.
- Fees and internship openings, eligibility, and application details are not
  listed on the website. Do not guess or promise a placement.
- Contact: call or WhatsApp +91 96267 12101; info@codingbodhi.com.
- Address: D No 8/2, Omalur Main Road, Angammal Colony, Salem, Tamil Nadu,
  India, 636009.
For unknown or changing details, say they aren't listed and recommend contacting
CodingBodhi.
"""

    try:
        client = genai.Client(api_key=api_key)
        model = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
        try:
            response = _create_interaction(
                client, model, contents, system_instruction
            )
        except Exception as error:
            if getattr(error, "status_code", None) not in {429, 500, 502, 503, 504}:
                raise

            fallback_model = os.getenv("GEMINI_FALLBACK_MODEL", "gemini-3.6-flash")
            if fallback_model == model:
                raise

            response = _create_interaction(
                client, fallback_model, contents, system_instruction
            )
    except Exception as error:
        raise ChatGenerationError(
            "The AI service is busy or unavailable. Please try again shortly."
        ) from error

    answer = (response.output_text or "").strip()
    if not answer:
        raise ChatGenerationError("The AI service returned an empty response.")
    return answer
