import React, { useState } from "react";
import './Chat.css';

function Chat() {
    const [message, setMessage] = useState("");
    const [response, setResponse] = useState("");

    const sendMessage = async () => {
        try {
            const res = await fetch("http://127.0.0.1:5000/query", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ input: message })
            });

            const data = await res.json();
            setResponse(data.response);
        } catch (error) {
            console.error("Error:", error);
        }
    };


    // HTML structure of the chat page
    // UI developments occur here, but all backend interactions are handled by the functions defined above.
    // Update visuals below as needed, but keep backend calls in their respective functions to maintain separation of concerns. 
    // Styles are in Admin.css.
    return (
        <div className="chat-box">
            <h2>AI Chat</h2>

            <input
                type="text"
                placeholder="Ask something..."
                value={message}
                onChange={(e) => setMessage(e.target.value)}
            />

            <button onClick={sendMessage}>Send</button>

            <div className="response">
                <strong>Response:</strong>
                <p>{response}</p>
            </div>
        </div>
    );
}

export default Chat;