import { useEffect, useRef, useState } from "react";
import { io } from "socket.io-client";
import "./Chat.css";
import "../Workspace/Workspace.css";

const socket = io("ws://localhost:5000", {
  transports: ["websocket"],
});

const testSocket = new WebSocket(
  "wss://localhost:5000/socket.io/?EIO=4&transport=websocket"
);

export default function ChatBot() {
  const [messages, setMessages] = useState([
    {
      sender: "ai",
      text: "Hello there! How can I assist you with HR outreach?",
    },
  ]);
  const [userInput, setUserInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [workspaces, setWorkspaces] = useState<any>(null);
  const [description, setDescription] = useState<any>([]);
  const chatBoxRef = useRef<HTMLDivElement>(null);

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!userInput.trim()) return;

    const newMessage = { sender: "human", text: userInput };
    setMessages((prev) => [...prev, newMessage]);

    setIsLoading(true);
    socket.emit("human_response", userInput);
    setUserInput("");
  };

  useEffect(() => {
    if (chatBoxRef.current) {
      chatBoxRef.current.scrollTop = chatBoxRef.current.scrollHeight;
    }
    socket.on("connect", () => {
      console.log("Connected to server:", socket.connected);
    });

    socket.on("ai_response", (data) => {
      setMessages((prev) => [...prev, { sender: "ai", text: data?.messages }]);
      setWorkspaces(data?.workspace);
      console.log(data?.workspace);
      setDescription(data?.workspace);
      setIsLoading(false);
    });

    return () => {
      socket.off("ai_response");
      socket.off("connect");
    };
  }, [messages, description]);

  return (
    <>
      <div className="chat-container">
        <h4 className="chat-header">Chat with Helix</h4>

        <div className="message-container" ref={chatBoxRef}>
          {messages.map((msg, index) => (
            <div key={index} className={msg.sender}>
              <p className={`${msg.sender}-name`}>
                {msg.sender === "human" ? "You" : "Helix"}
              </p>
              <p className={`${msg.sender}-message`}>{msg.text}</p>
              <p className={`time time-${msg.sender}`}>Thursday</p>
            </div>
          ))}

          {isLoading && (
            <div className="typing-indicator">
              <div className="dot"></div>
              <div className="dot"></div>
              <div className="dot"></div>
            </div>
          )}
        </div>

        <form className="chat-input" onSubmit={handleSendMessage}>
          <input
            type="text"
            className="flex-grow p-2 border rounded-lg text-sm"
            onChange={(e) => setUserInput(e.target.value)}
            value={userInput}
            placeholder="Chat with Helix"
          />
          <button
            type="submit"
            className="p-2 bg-purple-500 text-white rounded-lg"
          >
            Send
          </button>
        </form>
      </div>
      <div className="workspace-container">
        <h4 className="workspace-header">Workspace</h4>
        <div>
          {workspaces && workspaces.length > 0 ? (
            workspaces.map((step: string, index: number) => (
              <div className="step-container">
                <div className="card" key={index}>
                  <strong>Step {index + 1}: </strong>
                  {step}
                </div>
              </div>
            ))
          ) : (
            <p>No workspaces available</p>
          )}
        </div>
      </div>
    </>
  );
}
