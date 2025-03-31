import time
from flask import Flask, request, jsonify, stream_with_context, Response
from flask_cors import CORS
from flask_socketio import SocketIO, emit

from agents import workflow_graph
from database import cursor, connection
from sql import GET_SEQUENCE_DATA
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
CORS(app, origins="*")

socketio = SocketIO(app, cors_allowed_origins="*", transports=["websocket"])


@socketio.on('connect')
def connected():
    print('Client connected')
    emit('connected', {'message': 'Connected to server'})


@app.route("/")
async def home():
    return "This is home"


@app.route("/api/login", methods=["GET", "POST"])
async def login():
    return "This is login"


@app.route("/api/register", methods=["GET", "POST"])
async def register():
    # cursor.execute(CREATE_USERS_TABLE)
    connection.commit()
    return "users table created"


# @app.route("/api/new-chat", methods=["POST", "GET"])
@socketio.on("human_response")
def newchat(data):
    user_messages = data.get("userInput")
    name = data.get("name")
    title = data.get("title")
    company = data.get("company")


    config = {"configurable": {"thread_id": "1"}}

    system_prompt = "You are a helpful AI chatbot that assist to gather and ask about information about recruiting message outreach details sequence"\
                     f"The user name is {name} work at {company}, as {title} with 20 years of experience" \
                    "When enough data is collect, you begin to create a message sequence, not INSTRUCTION STEPS using provided tools name generate_sequence fo the workspace" \
                    "The user should be able to request edit by you or they can manually edit that" \
                    "You should know how many steps, title, and description on your own and don't ask user about that" \
                    "You only need to gather information enough from the user" \
                    "Remember to response very shortly, not too much" \
                    "When you begin generate message steps, response GENERATE SEQUENCE..." \
                    "When you begin update message steps, response UPDATING SEQUENCE..." \
                    "You must NEVER generate sequence in the chat, it happens in the back system, and after finish sequence generation, ask user follow up questions" \
                    "FINAL THING, you generate message steps, not INSTRUCTION STEPS" \
                    "Example, Hi {candidate_name}, my name is ...."

    try:
        response = workflow_graph.stream({"messages": [{"role": "human", "content":
            user_messages}, {"role": "system", "content": system_prompt}]},
                                         config=config, stream_mode="values")



        ai_response = None
        sequence = {}

        for result in response:
            ai_response = result["messages"][-1].content
            if "GENERATE SEQUENCE..." in result["messages"][-2].content:
                emit("calling_tool", {"calling_tool": "Generating"})
                if "tool_calls" in result["messages"][-2].additional_kwargs:
                    sequence = result["messages"][-2].additional_kwargs.get("tool_calls")[0].get("function").get(
                        "arguments")
                    sequence = json.loads(sequence)

                    print(sequence.get("description"))
            if "UPDATING SEQUENCE..." in result["messages"][-2].content:
                emit("calling_tool", {"calling_tool": "Updating"})
                if "tool_calls" in result["messages"][-2].additional_kwargs:
                    sequence = result["messages"][-2].additional_kwargs.get("tool_calls")[0].get("function").get(
                        "arguments")
                    sequence = json.loads(sequence)

# Replace newlines with spaces or empty string
        emit("ai_response", {"messages": ai_response, "workspace": sequence.get("description")}, broadcast=True)

    except Exception as e:
        print(e)
        print("\n")
        return jsonify({"messages": "Failed to load"})


class SequenceData:
    title: str
    description: list
    num_steps: int


# @socketio.on("generate_sequence")
# def handle_hr_sequence(data: SequenceData):
#     print(data)
#     response = generate_sequence(data.num_steps, data.description, data.title)
#     print("Received HR sequence")
#     print(response)
#     emit("generate_sequence", response)  # Ensure the event matches the frontend listener4
@app.route("/api/sequences", methods=["GET"])
async def sequences():
    """
    Generate sequences based on user information, updates and retreive information
    """
    try:
        sequence_id = 1
        cursor.execute(GET_SEQUENCE_DATA, (sequence_id,))
        data = cursor.fetchone()  # fetch one row to avoid index errors

        if data:
            return jsonify({"data": data}), 200  # Explicitly set a success status code
        else:
            return jsonify({"error": "No sequence found"}), 404

    except Exception as e:
        print("Error fetching sequences:", e)
        return jsonify({"error": "Failed to retrieve sequence"}), 500


# AI or manual edit
@app.route("/api/preferences", methods=["GET", "POST", "PUT"])
async def preferences():
    # number of steps
    # [Step 1, step 2, ,.. step n]
    # if request.method == "GET":
    #     cursor.execute(GET_SEQUENCE_DATA, ("7"))
    #     data = cursor.fetchone()
    #     print(data)
    pass

# if __name__ == "__main__":
#     socketio.run(app, debug=True, port=5000)
