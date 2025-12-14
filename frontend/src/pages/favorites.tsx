// frontend/src/pages/favorites.tsx

import { useState } from "react";
import useSWR from "swr";

import {
  fetchFavorites,
  removeFavorite,
  markFavorite,
} from "@/lib/api";

import NewsCard from "@/components/NewsCard";
import BroadcastModal from "@/components/BroadcastModal";

export default function FavoritesPage() {
  const { data, error, isLoading, mutate } = useSWR(
    "/favorites",
    () => fetchFavorites()
  );

  const [selectedFavorite, setSelectedFavorite] = useState<any>(null);
  const [showModal, setShowModal] = useState(false);

  if (error) return <div className="p-6 text-red-600">Failed to load favorites.</div>;
  if (isLoading) return <div className="p-6">Loading favorites...</div>;

  const favorites = data || [];

  return (
    <div className="min-h-screen bg-gray-100">
      
      {/* Header */}
      <header className="bg-secondary text-white p-4 shadow">
        <div className="container mx-auto">
          <h1 className="text-2xl font-semibold">My Favorites</h1>
        </div>
      </header>

      <main className="container mx-auto p-6">

        {favorites.length === 0 && (
          <p className="text-gray-600">You have no favorite items yet.</p>
        )}

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {favorites.map((fav: any) => (
            <NewsCard
              key={fav.id}
              newsItem={fav.news_item}
              onFavorite={async () => {
                await removeFavorite(fav.id);
                mutate();
              }}
              onBroadcast={() => {
                setSelectedFavorite(fav);
                setShowModal(true);
              }}
            />
          ))}
        </div>
      </main>

      {/* Broadcast Modal */}
      {showModal && selectedFavorite && (
        <BroadcastModal
          favoriteId={selectedFavorite.id}
          news={selectedFavorite.news_item}
          onClose={() => {
            setSelectedFavorite(null);
            setShowModal(false);
          }}
        />
      )}
    </div>
  );
}
