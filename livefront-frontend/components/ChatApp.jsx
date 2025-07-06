import { useState, useEffect, useRef } from 'react';
import { FiX, FiSend } from 'react-icons/fi';
import axios from 'axios';

const API = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

function ProductCard({ product }) {
  return (
    <div className="max-w-xs bg-white shadow rounded-lg overflow-hidden">
      {product.imageUrl && (
        <img
          src={product.imageUrl}
          alt={product.name}
          className="h-32 w-full object-cover"
        />
      )}
      <div className="p-3">
        <h4 className="font-semibold text-lg">{product.name}</h4>
        {product.description && (
          <p className="text-sm text-gray-600 mt-1">{product.description}</p>
        )}
        <div className="mt-2 flex items-center justify-between">
          <span className="font-bold">${product.price.toFixed(2)}</span>
          <button className="bg-blue-500 text-white px-2 py-1 rounded hover:bg-blue-600 text-xs">
            View
          </button>
        </div>
      </div>
    </div>
  );
}

export default function ChatApp({ onClose }) {
  const [users, setUsers] = useState([]);
  const [userId, setUserId] = useState(null);
  const [convId, setConvId] = useState(null);
  const [msgs, setMsgs] = useState([]);
  const [input, setInput] = useState('');
  const bottomRef = useRef();

  // Scroll to bottom on new message
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [msgs]);

  // Load user profiles
  useEffect(() => {
    axios
      .get(`${API}/users`)
      .then(res => setUsers(res.data))
      .catch(console.error);
  }, []);

  // On profile select: clear and welcome
  useEffect(() => {
    if (!userId) return;
    setMsgs([]);
    setConvId(null);

    axios
      .get(`${API}/welcome/${userId}`)
      .then(res => {
        setMsgs(res.data.messages.map(t => ({ sender: 'bot', text: t })));
      })
      .catch(() => {
        setMsgs([
          { sender: 'bot', text: "Hi there! I'm Capper—ready to help." },
        ]);
      });
  }, [userId]);

  const send = async () => {
    if (!input.trim() || !userId) return;

    const loadingIndex = msgs.length + 1;
    setMsgs(m => [...m, { sender: 'user', text: input.trim() }, { sender: 'bot', loading: true }]);
    const text = input.trim();
    setInput('');

    try {
      const { data } = await axios.post(`${API}/chat`, {
        user_id: userId,
        conversation_id: convId,
        message: text,
      });
      setConvId(data.conversation_id);
      setMsgs(m =>
        m.map((msg, idx) => {
          if (idx !== loadingIndex) return msg;
          if (data.recommendations && data.recommendations.length) {
            return {
              sender: 'bot',
              text: data.reply,
              recommendations: data.recommendations,
            };
          }
          return { sender: 'bot', text: data.reply };
        })
      );
    } catch (err) {
      setMsgs(m =>
        m.map((msg, idx) =>
          idx === loadingIndex
            ? { sender: 'bot', text: 'Sorry, something went wrong.' }
            : msg
        )
      );
    }
  };

  const onKeyDown = e => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      send();
    }
  };

  return (
    <div className="fixed inset-0 flex items-center justify-center p-4 z-50" style={{ backgroundColor: '#a49e15' }}>
      <div className="bg-white w-full max-w-xl h-[80vh] rounded-3xl flex flex-col overflow-hidden">
        {/* Header */}
        <div className="flex flex-col items-center p-4 border-b relative bg-white">
          <img
            src="/logo.png"
            alt="Carton Caps Logo"
            className="h-12 mb-2"
            style={{ objectFit: 'contain' }}
          />
          <h2 className="text-lg font-semibold text-center w-full">
            Capper - Carton Caps Personal Assistant
          </h2>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-3 bg-gray-50">
          {!userId && (
            <p className="text-center text-gray-500">
              Select a profile below to get started
            </p>
          )}

          {msgs.map((m, i) => (
            <div
              key={i}
              className={`flex ${m.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
              {m.loading ? (
                <div className="flex space-x-1">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" />
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-200" />
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-400" />
                </div>
              ) : m.recommendations ? (
                <div className="space-y-2">
                  <div
                    className="max-w-[75%] px-4 py-2 rounded-2xl break-words bg-white text-gray-900 border">
                    {m.text}
                  </div>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    {m.recommendations.map(prod => (
                      <ProductCard key={prod.id} product={prod} />
                    ))}
                  </div>
                </div>
              ) : (
                <div
                  className={`max-w-[75%] px-4 py-2 rounded-2xl break-words ${m.sender === 'user'
                    ? 'bg-blue-600 text-white rounded-br-none'
                    : 'bg-white text-gray-900 rounded-bl-none border'
                    }`}>
                  {m.text}
                </div>
              )}
            </div>
          ))}

          <div ref={bottomRef} />
        </div>

        {/* Input */}
        <div className="p-4 border-t flex items-start space-x-2">
          <select
            className="border rounded-lg p-2 flex-shrink-0"
            value={userId || ''}
            onChange={e => setUserId(Number(e.target.value))}>
            <option value="" disabled>
              Select profie
            </option>
            {users.map(u => (
              <option key={u.id} value={u.id}>
                {u.name}
              </option>
            ))}
          </select>

          <textarea
            className="flex-1 border rounded-2xl p-2 focus:outline-none focus:ring resize-none"
            rows={1}
            disabled={!userId}
            placeholder={userId ? 'Send a message…' : 'Select profile first'}
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={onKeyDown}
          />

          <button
            onClick={send}
            disabled={!input.trim() || !userId}
            className="text-blue-600 disabled:text-gray-400">
            <FiSend size={24} />
          </button>
        </div>
      </div>
    </div>
  );
}