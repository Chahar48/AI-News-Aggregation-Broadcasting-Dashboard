// frontend/src/components/NewsCard.tsx

import { useState } from "react";
import clsx from "clsx"; // ✅ FIXED (default import)
import { Megaphone } from "lucide-react"; // ✅ SAFE icon

interface NewsCardProps {
  newsItem: any;
  onFavorite?: () => void;
  onBroadcast?: () => void;
}

export default function NewsCard({
  newsItem,
  onFavorite,
  onBroadcast,
}: NewsCardProps) {
  const [isExpanded, setIsExpanded] = useState(false);

  const {
    title,
    summary,
    published_at,
    source_id,
    url,
  } = newsItem;

  return (
    <div className="bg-card shadow-card p-5 rounded-xl border border-gray-200 hover:shadow-lg transition">
      
      {/* Title */}
      <h3
        className="text-lg font-semibold text-gray-800 mb-2 hover:underline cursor-pointer"
        onClick={() => url && window.open(url, "_blank")}
      >
        {title}
      </h3>

      {/* Summary */}
      <p className="text-sm text-gray-700">
        {summary
          ? isExpanded
            ? summary
            : summary.slice(0, 150) + "..."
          : "No summary available"}
      </p>

      {summary?.length > 150 && (
        <button
          className="text-blue-600 text-xs mt-1 hover:underline"
          onClick={() => setIsExpanded(!isExpanded)}
        >
          {isExpanded ? "Show less" : "Read more"}
        </button>
      )}

      {/* Footer */}
      <div className="mt-4 flex justify-between items-center text-sm text-gray-600">
        <span>
          {published_at
            ? new Date(published_at).toLocaleDateString()
            : "Unknown date"}
        </span>
        <span className="text-gray-500">Source ID: {source_id}</span>
      </div>

      {/* Actions */}
      <div className="mt-4 flex gap-3">
        
        {/* Favorite */}
        <button
          onClick={onFavorite}
          className={clsx(
            "px-3 py-1 rounded-md text-white text-sm transition",
            "bg-primary hover:bg-blue-700"
          )}
        >
          ⭐ Favorite
        </button>

        {/* Broadcast */}
        <button
          onClick={onBroadcast}
          className={clsx(
            "px-3 py-1 rounded-md text-white text-sm flex items-center gap-1 transition",
            "bg-secondary hover:bg-slate-700"
          )}
        >
          <Megaphone size={16} />
          Broadcast
        </button>
      </div>
    </div>
  );
}

// // frontend/src/components/NewsCard.tsx

// import { useState } from "react";
// import { clsx } from "clsx";
// import { Broadcast } from "lucide-react";

// interface NewsCardProps {
//   newsItem: any;
//   onFavorite?: () => void;
//   onBroadcast?: () => void;
// }

// export default function NewsCard({ newsItem, onFavorite, onBroadcast }: NewsCardProps) {
//   const [isExpanded, setIsExpanded] = useState(false);

//   const {
//     title,
//     summary,
//     published_at,
//     source_id,
//     url
//   } = newsItem;

//   return (
//     <div className="bg-card shadow-card p-5 rounded-xl border border-gray-200 hover:shadow-lg transition cursor-pointer">
      
//       {/* Title */}
//       <h3
//         className="text-lg font-semibold text-gray-800 mb-2 hover:underline"
//         onClick={() => url && window.open(url, "_blank")}
//       >
//         {title}
//       </h3>

//       {/* Summary */}
//       <p className="text-sm text-gray-700">
//         {isExpanded ? summary : summary?.slice(0, 150) + "..."}
//       </p>

//       {summary?.length > 150 && (
//         <button
//           className="text-blue-600 text-xs mt-1 hover:underline"
//           onClick={() => setIsExpanded(!isExpanded)}
//         >
//           {isExpanded ? "Show less" : "Read more"}
//         </button>
//       )}

//       {/* Footer */}
//       <div className="mt-4 flex justify-between items-center text-sm text-gray-600">
//         <span>
//           {published_at ? new Date(published_at).toLocaleDateString() : "Unknown date"}
//         </span>
//         <span className="text-gray-500">Source: {source_id}</span>
//       </div>

//       {/* Actions */}
//       <div className="mt-4 flex gap-3">
        
//         {/* Favorite Button */}
//         <button
//           onClick={onFavorite}
//           className={clsx(
//             "px-3 py-1 rounded-md text-white text-sm transition",
//             "bg-primary hover:bg-blue-700"
//           )}
//         >
//           ⭐ Favorite
//         </button>

//         {/* Broadcast Button */}
//         <button
//           onClick={onBroadcast}
//           className={clsx(
//             "px-3 py-1 rounded-md text-white text-sm flex items-center gap-1 transition",
//             "bg-secondary hover:bg-slate-700"
//           )}
//         >
//           <Broadcast size={16} />
//           Broadcast
//         </button>

//       </div>
//     </div>
//   );
// }
