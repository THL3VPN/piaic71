from flask import Flask, request, render_template_string
import sqlite3
from collections import Counter
import google.generativeai as genai
import os
from dotenv import load_dotenv

DB_PATH = "lsi_incidents.db"

app = Flask(__name__)

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

HTML_FORM = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>LSI Submission Form</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    body {
      background: linear-gradient(135deg, #e0eafc 0%, #cfdef3 100%);
      font-family: 'Segoe UI', Arial, sans-serif;
      margin: 0;
      padding: 0;
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .form-container {
      background: #fff;
      border-radius: 18px;
      box-shadow: 0 8px 32px rgba(44, 62, 80, 0.15);
      padding: 2.5rem 2.2rem;
      max-width: 440px;
      width: 100%;
      display: flex;
      flex-direction: column;
      gap: 1.2rem;
      border: 1.5px solid #e5e7eb;
    }
    h2 {
      text-align: center;
      color: #2d3e50;
      margin-bottom: 0.5rem;
      font-weight: 600;
      letter-spacing: 1px;
    }
    form {
      display: flex;
      flex-direction: column;
      gap: 1.1rem;
    }
    .form-group {
      display: flex;
      flex-direction: column;
      gap: 0.5rem;
    }
    label {
      color: #34495e;
      font-weight: 500;
      font-size: 1rem;
      margin-bottom: 0.1rem;
    }
    input, textarea, select {
      width: 100%;
      padding: 0.8rem 1rem;
      border: 1.5px solid #dbeafe;
      border-radius: 8px;
      font-size: 1rem;
      background: #f8fafc;
      transition: border-color 0.2s, box-shadow 0.2s;
      outline: none;
      box-sizing: border-box;
    }
    input:focus, textarea:focus, select:focus {
      border-color: #2563eb;
      background: #fff;
      box-shadow: 0 0 0 2px #60a5fa33;
    }
    textarea {
      resize: vertical;
      min-height: 80px;
      max-height: 200px;
    }
    button {
      width: 100%;
      padding: 1rem;
      background: linear-gradient(90deg, #60a5fa 0%, #2563eb 100%);
      color: #fff;
      border: none;
      border-radius: 8px;
      font-size: 1.1rem;
      font-weight: 600;
      cursor: pointer;
      box-shadow: 0 2px 8px rgba(44, 62, 80, 0.08);
      transition: background 0.2s, box-shadow 0.2s;
      margin-top: 0.5rem;
    }
    button:hover {
      background: linear-gradient(90deg, #2563eb 0%, #60a5fa 100%);
      box-shadow: 0 4px 16px rgba(44, 62, 80, 0.15);
    }
    .dashboard-btn {
      display: block;
      text-align: center;
      margin-top: 1rem;
      background: #2563eb;
      color: #fff;
      border: none;
      padding: 0.8rem 1.2rem;
      border-radius: 8px;
      font-size: 1rem;
      cursor: pointer;
      text-decoration: none;
      font-weight: 600;
    }
    .dashboard-btn:hover {
      background: #60a5fa;
      color: #fff;
    }
  </style>
</head>
<body>
  <div class="form-container">
    <h2>LSI Submission Form</h2>
    <form method="POST" action="/">
      <div class="form-group">
        <label for="name">Name</label>
        <input type="text" id="name" name="name" required placeholder="Enter your name">
      </div>
      <div class="form-group">
        <label for="department">Department</label>
        <select id="department" name="department" required>
          <option value="" disabled selected>Select your department</option>
          <option value="sales">Sales</option>
          <option value="marketing">Marketing</option>
          <option value="engineering">Engineering</option>
          <option value="audit">Audit</option>
          <option value="information-technology">Information Technology</option>
        </select>
      </div>
      <div class="form-group">
        <label for="lsi_summary">LSI Summary</label>
        <input type="text" id="lsi_summary" name="lsi_summary" required placeholder="Short summary">
      </div>
      <div class="form-group">
        <label for="lsi_details">LSI Details</label>
        <textarea id="lsi_details" name="lsi_details" required placeholder="Detailed description"></textarea>
      </div>
      <button type="submit">Submit</button>
    </form>
    <a href="/dashboard" class="dashboard-btn">Go to Dashboard</a>
    <a href="/lsi-search" class="dashboard-btn" style="margin-top:0.5rem;background:#10b981;">LSI AI Search</a>
    {% if message %}
      <p style="color: green; text-align: center;">{{ message }}</p>
    {% endif %}
  </div>
  <script>
    document.addEventListener('DOMContentLoaded', function() {
      const summaryInput = document.getElementById('lsi_summary');
      const detailsInput = document.getElementById('lsi_details');

      const suggestions = {
        "network": "Describe the network issue, its impact, and any troubleshooting steps taken.",
        "login": "Explain the login problem, affected users, and resolution steps.",
        "server": "Provide details about the server incident, downtime, and recovery actions.",
        "audit": "Summarize the audit findings and any corrective actions.",
        "sales": "Detail the sales incident, customer impact, and follow-up.",
        "marketing": "Describe the marketing issue and steps to resolve it."
      };

      summaryInput.addEventListener('input', function() {
        let value = summaryInput.value.toLowerCase();
        let found = "";
        Object.keys(suggestions).forEach(key => {
          if (value.includes(key)) {
            found = suggestions[key];
          }
        });
        if (found) {
          detailsInput.placeholder = found;
        } else {
          detailsInput.placeholder = "Detailed description";
        }
      });
    });
  </script>
</body>
</html>
"""

LSI_SEARCH_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>LSI AI Search</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    body {
      background: linear-gradient(135deg, #e0eafc 0%, #cfdef3 100%);
      font-family: 'Segoe UI', Arial, sans-serif;
      margin: 0;
      padding: 0;
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .chat-container {
      background: #fff;
      border-radius: 18px;
      box-shadow: 0 8px 32px rgba(44, 62, 80, 0.15);
      padding: 2.5rem 2.2rem;
      max-width: 540px;
      width: 100%;
      display: flex;
      flex-direction: column;
      gap: 1.2rem;
      border: 1.5px solid #e5e7eb;
      min-height: 60vh;
    }
    .chat-title {
      text-align: center;
      color: #2563eb;
      font-size: 2rem;
      font-weight: 600;
      margin-bottom: 1rem;
    }
    .chat-history {
      flex: 1;
      overflow-y: auto;
      margin-bottom: 1rem;
      padding: 1rem;
      background: #f8fafc;
      border-radius: 12px;
      box-shadow: 0 2px 8px #dbeafe;
      max-height: 300px;
    }
    .chat-message {
      margin-bottom: 1.2rem;
      display: flex;
      flex-direction: column;
    }
    .user-msg {
      align-self: flex-end;
      background: #2563eb;
      color: #fff;
      padding: 0.7rem 1rem;
      border-radius: 12px 12px 0 12px;
      max-width: 80%;
      margin-bottom: 0.3rem;
      font-weight: 500;
    }
    .gemini-msg {
      align-self: flex-start;
      background: #f3f4f6;
      color: #2563eb;
      padding: 0.7rem 1rem;
      border-radius: 12px 12px 12px 0;
      max-width: 80%;
      margin-bottom: 0.3rem;
      font-weight: 500;
      border: 1px solid #dbeafe;
    }
    .chat-form {
      display: flex;
      gap: 0.5rem;
      margin-top: 1rem;
    }
    .chat-input {
      flex: 1;
      padding: 0.8rem 1rem;
      border-radius: 8px;
      border: 1.5px solid #dbeafe;
      font-size: 1rem;
      background: #f8fafc;
      outline: none;
    }
    .chat-btn {
      padding: 0.8rem 1.2rem;
      border-radius: 8px;
      background: #2563eb;
      color: #fff;
      border: none;
      font-size: 1rem;
      font-weight: 600;
      cursor: pointer;
      box-shadow: 0 2px 8px #dbeafe;
      transition: background 0.2s;
    }
    .chat-btn:hover {
      background: #60a5fa;
      color: #fff;
    }
    .action-btns {
      display: flex;
      gap: 1rem;
      justify-content: center;
      margin-top: 1.5rem;
    }
    .back-btn, .clear-btn {
      display: inline-block;
      background: #10b981;
      color: #fff;
      padding: 0.7em 1.5em;
      border-radius: 8px;
      text-decoration: none;
      font-weight: 600;
      box-shadow: 0 2px 8px #dbeafe;
      text-align: center;
      border: none;
      cursor: pointer;
      font-size: 1rem;
      transition: background 0.2s;
    }
    .back-btn:hover, .clear-btn:hover {
      background: #2563eb;
      color: #fff;
    }
  </style>
</head>
<body>
  <div class="chat-container">
    <div class="chat-title">LSI AI Search</div>
    <div class="chat-history" id="chat-history">
      {% for msg in history %}
        <div class="chat-message">
          {% if msg.role == 'user' %}
            <div class="user-msg">{{ msg.content }}</div>
          {% else %}
            <div class="gemini-msg">{{ msg.content }}</div>
          {% endif %}
        </div>
      {% endfor %}
    </div>
    <form method="POST" class="chat-form">
      <input type="text" name="user_query" class="chat-input" placeholder="Type your question..." required autofocus>
      <button type="submit" class="chat-btn">Send</button>
    </form>
    <div class="action-btns">
      <a href="/" class="back-btn">Back to Form</a>
      <form method="POST" action="/clear-chat" style="display:inline;">
        <button type="submit" class="clear-btn">Clear Chat</button>
      </form>
    </div>
  </div>
  <script>
    // Auto-scroll to bottom of chat history
    window.onload = function() {
      var chatHistory = document.getElementById('chat-history');
      chatHistory.scrollTop = chatHistory.scrollHeight;
    };
  </script>
</body>
</html>
"""

from flask import session, redirect, url_for

app.secret_key = "your_secret_key"  # Needed for session

@app.route("/lsi-search", methods=["GET", "POST"])
def lsi_search():
    # Start a new session chat history if not present
    if "history" not in session:
        session["history"] = []
    history = session["history"]

    system_prompt = (
        "You are an LSI AI assistant. "
        "When answering user questions, carefully check the LSI Summary and LSI Details fields from the incident records. "
        "Base your answer only on the information found in those fields. "
        "The answer should be very precise."
    )

    if request.method == "POST":
        user_query = request.form.get("user_query")
        history.append({"role": "user", "content": user_query})

        # Get all incidents from DB
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT name, department, lsi_summary, lsi_details FROM incidents")
        rows = cursor.fetchall()
        conn.close()
        # Prepare context for Gemini
        context = "\n".join([f"Name: {r[0]}, Dept: {r[1]}, Summary: {r[2]}, Details: {r[3]}" for r in rows])
        prompt = (
            f"{system_prompt}\n"
            f"User question: {user_query}\n\n"
            f"Here are the incidents:\n{context}\n\n"
            f"Based on the incidents, provide the most relevant answer to the user's question."
        )
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        answer = response.text
        history.append({"role": "gemini", "content": answer})
        session["history"] = history
        return redirect(url_for("lsi_search"))

    return render_template_string(LSI_SEARCH_PAGE, history=history)

@app.route("/clear-chat", methods=["POST"])
def clear_chat():
    session.pop("history", None)
    return redirect(url_for("lsi_search"))

@app.route("/", methods=["GET", "POST"])
def serve_form():
    message = ""
    if request.method == "POST":
        name = request.form.get("name")
        department = request.form.get("department")
        lsi_summary = request.form.get("lsi_summary")
        lsi_details = request.form.get("lsi_details")
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO incidents (name, department, lsi_summary, lsi_details) VALUES (?, ?, ?, ?)",
            (name, department, lsi_summary, lsi_details)
        )
        conn.commit()
        conn.close()
        message = "Incident submitted successfully!"
    return render_template_string(HTML_FORM, message=message)

@app.route("/view")
def view_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, department, lsi_summary, lsi_details, approved FROM incidents")
    rows = cursor.fetchall()
    conn.close()
    html = """
    <h2>All LSI Incident Records</h2>
    <table border="1" cellpadding="8" style="border-collapse:collapse;">
      <tr>
        <th>ID</th>
        <th>Name</th>
        <th>Department</th>
        <th>LSI Summary</th>
        <th>LSI Details</th>
        <th>Approved</th>
      </tr>
    """
    for row in rows:
        html += "<tr>" + "".join(f"<td>{str(cell)}</td>" for cell in row) + "</tr>"
    html += "</table><br><a href='/'>Back to Form</a>"
    return html

@app.route("/dashboard")
def dashboard():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, department, lsi_summary, lsi_details, approved FROM incidents")
    rows = cursor.fetchall()
    conn.close()

    departments = [row[2] for row in rows]
    dept_counts = Counter(departments)

    # Dashboard styling matches the submission form
    dept_table = """
    <style>
      .dashboard-container {
        background: #fff;
        border-radius: 18px;
        box-shadow: 0 8px 32px rgba(44, 62, 80, 0.15);
        padding: 2.5rem 2.2rem;
        max-width: 700px;
        margin: 2rem auto;
        width: 100%;
        display: flex;
        flex-direction: column;
        gap: 1.2rem;
        border: 1.5px solid #e5e7eb;
      }
      .dashboard-title {
        text-align: center;
        color: #2d3e50;
        margin-bottom: 0.5rem;
        font-weight: 600;
        letter-spacing: 1px;
        font-size: 2rem;
      }
      .dashboard-table {
        width: 100%;
        border-collapse: collapse;
        background: #f8fafc;
        border-radius: 12px;
        box-shadow: 0 2px 8px #dbeafe;
        overflow: hidden;
      }
      .dashboard-table th {
        background: #2563eb;
        color: #fff;
        padding: 1rem;
        font-size: 1.1rem;
        font-weight: 600;
      }
      .dashboard-table td {
        background: #fff;
        color: #34495e;
        padding: 0.9rem;
        font-size: 1rem;
        text-align: center;
      }
      .dashboard-table tr:not(:first-child):hover td {
        background: #e0eafc;
      }
      .dashboard-link {
        color: #2563eb;
        font-weight: bold;
        text-decoration: none;
        border-bottom: 1.5px solid #2563eb;
        transition: color 0.2s;
      }
      .dashboard-link:hover {
        color: #60a5fa;
        border-bottom: 1.5px solid #60a5fa;
      }
      .back-btn {
        display: inline-block;
        background: linear-gradient(90deg, #60a5fa 0%, #2563eb 100%);
        color: #fff;
        padding: 0.7em 1.5em;
        border-radius: 8px;
        text-decoration: none;
        font-weight: 600;
        box-shadow: 0 2px 8px #dbeafe;
        margin-top: 1.5rem;
        text-align: center;
      }
      .back-btn:hover {
        background: linear-gradient(90deg, #2563eb 0%, #60a5fa 100%);
        color: #fff;
      }
    </style>
    <div class="dashboard-container">
      <div class="dashboard-title">LSI Dashboard</div>
      <table class="dashboard-table">
        <tr>
          <th>Department</th>
          <th>LSI Count</th>
        </tr>
    """
    for dept, count in dept_counts.items():
        dept_table += f"""
        <tr>
          <td>{dept.title()}</td>
          <td>
            <a href="/dashboard/{dept}" class="dashboard-link">{count}</a>
          </td>
        </tr>
        """
    dept_table += """
      </table>
      <div style='text-align:center;'>
        <a href='/' class='back-btn'>Back to Form</a>
      </div>
    </div>
    """

    return dept_table

@app.route("/dashboard/<department>")
def department_lsi(department):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, lsi_summary, lsi_details, approved FROM incidents WHERE department=?", (department,))
    rows = cursor.fetchall()
    conn.close()

    html = """
    <style>
      .dashboard-container {
        background: #fff;
        border-radius: 18px;
        box-shadow: 0 8px 32px rgba(44, 62, 80, 0.15);
        padding: 2.5rem 2.2rem;
        max-width: 700px;
        margin: 2rem auto;
        width: 100%;
        display: flex;
        flex-direction: column;
        gap: 1.2rem;
        border: 1.5px solid #e5e7eb;
      }
      .dashboard-title {
        text-align: center;
        color: #2d3e50;
        margin-bottom: 0.5rem;
        font-weight: 600;
        letter-spacing: 1px;
        font-size: 2rem;
      }
      .dashboard-table {
        width: 100%;
        border-collapse: collapse;
        background: #f8fafc;
        border-radius: 12px;
        box-shadow: 0 2px 8px #dbeafe;
        overflow: hidden;
      }
      .dashboard-table th {
        background: #2563eb;
        color: #fff;
        padding: 1rem;
        font-size: 1.1rem;
        font-weight: 600;
      }
      .dashboard-table td {
        background: #fff;
        color: #34495e;
        padding: 0.9rem;
        font-size: 1rem;
        text-align: center;
      }
      .dashboard-table tr:not(:first-child):hover td {
        background: #e0eafc;
      }
      .back-btn {
        display: inline-block;
        background: linear-gradient(90deg, #60a5fa 0%, #2563eb 100%);
        color: #fff;
        padding: 0.7em 1.5em;
        border-radius: 8px;
        text-decoration: none;
        font-weight: 600;
        box-shadow: 0 2px 8px #dbeafe;
        margin-top: 1.5rem;
        text-align: center;
      }
      .back-btn:hover {
        background: linear-gradient(90deg, #2563eb 0%, #60a5fa 100%);
        color: #fff;
      }
    </style>
    """
    html += f"""
    <div class="dashboard-container">
      <div class="dashboard-title">LSIs for {department.title()}</div>
      <table class="dashboard-table">
        <tr>
          <th>ID</th>
          <th>Name</th>
          <th>Summary</th>
          <th>Details</th>
          <th>Approved</th>
        </tr>
    """
    for row in rows:
        html += "<tr>"
        html += "".join(f"<td>{str(cell)}</td>" for cell in row)
        html += "</tr>"
    html += """
      </table>
      <div style='text-align:center;'>
        <a href='/dashboard' class='back-btn'>Back to Dashboard</a>
      </div>
    </div>
    """
    return html

@app.route("/search", methods=["POST"])
def search():
    user_query = request.form.get("user_query")
    # Get all incidents from DB
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name, department, lsi_summary, lsi_details FROM incidents")
    rows = cursor.fetchall()
    conn.close()
    # Prepare context for Gemini
    context = "\n".join([f"Name: {r[0]}, Dept: {r[1]}, Summary: {r[2]}, Details: {r[3]}" for r in rows])
    prompt = f"User question: {user_query}\n\nHere are the incidents:\n{context}\n\nBased on the incidents, provide the most relevant answer to the user's question."
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    answer = response.text
    html = f"""
    <div class="form-container">
      <h2>Gemini Search Result</h2>
      <div style="background:#f8fafc;padding:1.2rem;border-radius:8px;margin-bottom:1rem;">{answer}</div>
      <a href="/" class="dashboard-btn">Back</a>
    </div>
    """
    return html

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9090, debug=True)