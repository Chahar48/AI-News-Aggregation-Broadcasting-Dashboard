// frontend/src/components/BroadcastModal.tsx

import { useState } from "react";
import { X, Mail, Linkedin, MessageCircle, FileText, Send } from "lucide-react";
import { broadcastAction } from "@/lib/api";

interface BroadcastModalProps {
  favoriteId: number;
  news: any; // news_item from backend
  onClose: () => void;
}

export default function BroadcastModal({ favoriteId, news, onClose }: BroadcastModalProps) {
  const [platform, setPlatform] = useState<string>("");
  const [message, setMessage] = useState<string>("");
  const [loading, setLoading] = useState(false);
  const [done, setDone] = useState(false);

  // Platforms for UI selection
  const platforms = [
    { key: "email", label: "Email", icon: <Mail size={18} /> },
    { key: "whatsapp", label: "WhatsApp", icon: <MessageCircle size={18} /> },
    { key: "linkedin", label: "LinkedIn", icon: <Linkedin size={18} /> },
    { key: "blog", label: "Blog (Markdown)", icon: <FileText size={18} /> },
    { key: "newsletter", label: "Newsletter", icon: <Send size={18} /> },
  ];

  const handleBroadcast = async () => {
    if (!platform) {
      alert("Please choose a platform.");
      return;
    }

    setLoading(true);

    try {
      await broadcastAction(favoriteId, platform, message || null);
      setDone(true);
    } catch (err) {
      alert("Failed to broadcast. Check backend logs.");
    }

    setLoading(false);
  };

  return (
    <div className="fixed inset-0 bg-black/40 flex justify-center items-center z-50">
      <div className="bg-white rounded-xl shadow-xl p-6 w-[90%] max-w-lg relative">

        {/* Close button */}
        <button
          onClick={onClose}
          className="absolute right-4 top-4 text-gray-500 hover:text-gray-700"
        >
          <X size={22} />
        </button>

        <h2 className="text-xl font-semibold">Broadcast News</h2>
        <p className="text-gray-700 text-sm mt-2 mb-4">{news.title}</p>

        {/* Select Platform */}
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Choose a platform
          </label>

          <div className="grid grid-cols-2 gap-3">
            {platforms.map((p) => (
              <button
                key={p.key}
                onClick={() => setPlatform(p.key)}
                className={`border p-3 rounded-lg flex items-center justify-center gap-2 transition ${
                  platform === p.key
                    ? "bg-primary text-white"
                    : "hover:bg-gray-100"
                }`}
              >
                {p.icon}
                {p.label}
              </button>
            ))}
          </div>
        </div>

        {/* Message box */}
        <div className="mb-4">
          <label className="block text-sm font-medium mb-1">Custom message (optional)</label>
          <textarea
            className="w-full border rounded-lg p-2 text-sm focus:ring-primary focus:ring"
            rows={4}
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Add a personalized caption or comment..."
          />
        </div>

        <button
          onClick={handleBroadcast}
          disabled={loading}
          className="w-full bg-primary text-white py-2 rounded-lg hover:bg-blue-700 transition flex items-center justify-center gap-2"
        >
          {loading ? "Sending..." : <><Send size={18} /> Send Broadcast</>}
        </button>

        {done && (
          <p className="text-green-600 text-sm text-center mt-3">
            Broadcast sent successfully!
          </p>
        )}
      </div>
    </div>
  );
}
