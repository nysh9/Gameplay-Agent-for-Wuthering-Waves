import { useMemo, useRef, useState } from "react";
import ReactMarkdown from "react-markdown";
import abbyAvatar from "./assets/abby.webp";
import "./App.css";

type Message = { role: "user" | "assistant"; content: string };

const API_URL = `${import.meta.env.VITE_API_URL ?? "http://localhost:8000"}/chat`;

const PARTICLE_COUNT = 30;

const SUGGESTIONS = [
  "How do I build Jinhsi?",
  "Who should I pull next?",
  "What should I farm at UL 40?",
];

function App() {
  const particles = useMemo(
    () =>
      Array.from({ length: PARTICLE_COUNT }, () => ({
        left: Math.random() * 100,
        size: 3 + Math.random() * 5,
        duration: 8 + Math.random() * 12,
        delay: Math.random() * 12,
      })),
    []
  );

  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  function pickSuggestion(text: string) {
    setInput(text);
    inputRef.current?.focus();
  }

  async function sendMessage(e: React.FormEvent) {
    e.preventDefault();
    const text = input.trim();
    if (!text || loading) return;

    const nextHistory: Message[] = [...messages, { role: "user", content: text }];
    setMessages(nextHistory);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ messages: nextHistory }),
      });
      const data = await res.json();
      setMessages((m) => [...m, { role: "assistant", content: data.response }]);
    } catch (err) {
      setMessages((m) => [
        ...m,
        { role: "assistant", content: `Error: ${(err as Error).message}` },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="app">
      <div className="particles" aria-hidden="true">
        {particles.map((p, i) => (
          <span
            key={i}
            className="particle"
            style={{
              left: `${p.left}%`,
              width: `${p.size}px`,
              height: `${p.size}px`,
              animationDuration: `${p.duration}s`,
              animationDelay: `${p.delay}s`,
            }}
          />
        ))}
      </div>

      <main className="chat">
        {messages.length === 0 && (
          <div className="welcome">
            <img src={abbyAvatar} alt="" className="welcome-avatar" />
            <h2 className="welcome-title">Wuthering Waves Agent</h2>
            <p className="welcome-subtitle">Your personal Resonator advisor</p>
            <div className="suggestions">
              {SUGGESTIONS.map((s) => (
                <button
                  key={s}
                  type="button"
                  className="chip"
                  onClick={() => pickSuggestion(s)}
                >
                  {s}
                </button>
              ))}
            </div>
          </div>
        )}
        {messages.map((m, i) => (
          <div key={i} className={`msg ${m.role}`}>
            {m.role === "assistant" && (
              <img src={abbyAvatar} alt="" className="avatar" />
            )}
            <div className="bubble">
              {m.role === "assistant" ? (
                <ReactMarkdown>{m.content}</ReactMarkdown>
              ) : (
                m.content
              )}
            </div>
          </div>
        ))}
        {loading && (
          <div className="msg assistant">
            <img src={abbyAvatar} alt="" className="avatar" />
            <div className="bubble">Thinking…</div>
          </div>
        )}
      </main>

      <form className="composer" onSubmit={sendMessage}>
        <input
          ref={inputRef}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask anything…"
          disabled={loading}
        />
        <button type="submit" disabled={loading || !input.trim()}>
          Send
        </button>
      </form>
    </div>
  );
}

export default App;
