// frontend/src/pages/index.tsx

import { useState } from "react";
import useSWR from "swr";
import { fetchNews, markFavorite, refreshNews } from "@/lib/api";
import NewsCard from "@/components/NewsCard";

export default function HomePage() {
  const [page] = useState(1);

  const { data, error, isLoading, mutate } = useSWR(
    ["news", page],
    () => fetchNews(page, 20)
  );

  const handleRefresh = async () => {
    await refreshNews();
    mutate();
  };

  if (error) {
    return <div className="p-6 text-red-600">Failed to load news.</div>;
  }

  if (isLoading) {
    return <div className="p-6">Loading news...</div>;
  }

  const newsItems = data?.items ?? [];

  return (
    <div className="min-h-screen bg-gray-100">
      
      {/* Header */}
      <header className="bg-secondary text-white p-4 shadow">
        <div className="container mx-auto flex justify-between items-center">
          <h1 className="text-2xl font-semibold">AI News Dashboard</h1>
          <button
            onClick={handleRefresh}
            className="bg-primary px-4 py-2 rounded-md text-white hover:bg-blue-700 transition"
          >
            Refresh News
          </button>
        </div>
      </header>

      {/* Feed */}
      <main className="container mx-auto p-6">
        <h2 className="text-xl font-semibold mb-4">Latest AI News</h2>

        {newsItems.length === 0 && (
          <div className="text-gray-600">No news available.</div>
        )}

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {newsItems.map((item: any) => (
            <NewsCard
              key={item.id}
              newsItem={item}
              onFavorite={async () => {
                await markFavorite(item.id);
                alert("Added to favorites");
              }}
            />
          ))}
        </div>
      </main>
    </div>
  );
}