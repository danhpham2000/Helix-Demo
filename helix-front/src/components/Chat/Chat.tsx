import { useEffect, useRef, useState } from "react";
import "./Chat.css";

export default function ChatBot() {
  const [messages, setMessages] = useState([
    {
      sender: "ai",
      text: "Hello there! How can I assist you with HR outreach?",
    },
  ]);
  const [userInput, setUserInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [useSequence, setUseSequence] = useState(false);

  const chatBoxRef: any = useRef(null);

  const handleSendMessage = async (e: any) => {
    setUserInput("");
    e.preventDefault();
    if (userInput.trim() === "") return;

    const newMessages = [...messages, { sender: "human", text: userInput }];
    setMessages(newMessages);

    setIsLoading(true);
    const response = await fetchAIResponse(newMessages);
    console.log(response.use_sequence);
    setMessages([...newMessages, { sender: "ai", text: response.messages }]);
    setUseSequence(response.use_sequence);
    setIsLoading(false);
  };

  const fetchAIResponse = async (chatHistory: any) => {
    try {
      const response = await fetch("http://127.0.0.1:5000/api/new-chat", {
        method: "POST",
        body: JSON.stringify({ user_messages: userInput }),
        headers: { "Content-Type": "application/json" },
      });

      const result = await response.json();

      return result;
    } catch (err) {
      return err;
    }
  };

  useEffect(() => {
    if (chatBoxRef.current) {
      chatBoxRef.current.scrollTop = chatBoxRef.current.scrollHeight;
    }
  }, [messages, isLoading]);
  return (
    <div className="chat-container">
      <h4 className="chat-header">Chat with Helix</h4>
      {/* <div className="message-container">
        <div className="human">
          <p className="human-name">Human Name</p>
          <p className="human-message">Reach out to the founders in SF.</p>
          <p className="time time-human">Thursday</p>
        </div>
        <div className="ai">
          <p className="ai-name">Helix AI</p>
          <p className="ai-message">Generating content...</p>
          <p className="time time-ai">Thursday</p>
        </div>
      </div> */}

      <div className="message-container" ref={chatBoxRef}>
        {messages.map((msg, index) => (
          <div key={index} className={`${msg.sender}`}>
            <p className={`${msg.sender}-name`}>
              {msg.sender === "human" ? "Human" : "Helix"}
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
        {/* Message Input Field */}
        <input
          type="text"
          className="flex-grow p-2 border rounded-lg text-sm"
          onChange={(e) => setUserInput(e.target.value)}
          value={userInput}
          placeholder="Chat with Helix"
        />

        {/* Send Message Button */}
        <button
          type="submit"
          className="p-2 bg-purple-500 text-white rounded-lg button"
        >
          Send
        </button>
      </form>
    </div>
  );
}
