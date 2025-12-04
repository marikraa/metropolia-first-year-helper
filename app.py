from flask import Flask, render_template, request, redirect, url_for, session
from topics_data import TOPICS, find_best_topics
from ai_answer import generate_answer

app = Flask(__name__)
app.secret_key = "dev-secret-key"   # Only needed so session works

def get_theme():
    """
    Get theme from URL or session.
    """
    if "theme" in request.args:
        session["theme"] = request.args["theme"]
    return session.get("theme", "light")


def get_topic_by_id(topic_id: str):
    for t in TOPICS:
        if t.id == topic_id:
            return t
    return None

@app.route("/", methods=["GET", "POST"])
def index():
    query = None
    suggestions = []
    ai_answer = None

    theme = get_theme()

    if request.method == "POST":
        query = request.form.get("question", "").strip()
        if query:
            suggestions = find_best_topics(query)
            if suggestions:
                ai_answer = generate_answer(query, suggestions)
        else:
            return redirect(url_for("index", theme=theme))

    return render_template(
        "index.html",
        topics=TOPICS,
        query=query,
        suggestions=suggestions,
        ai_answer=ai_answer,
        theme=theme
    )

@app.route("/topic/<topic_id>")
def topic_detail(topic_id):
    theme = get_theme()

    topic = get_topic_by_id(topic_id)
    if topic is None:
        return render_template("topic.html", topic=None, theme=theme), 404

    return render_template("topic.html", topic=topic, theme=theme)

if __name__ == "__main__":
    app.run(debug=True)