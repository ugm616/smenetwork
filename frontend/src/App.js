import React, { useState, useEffect } from 'react';
import './App.css';

const API_BASE_URL = process.env.REACT_APP_BACKEND_URL;

// Video Player Component
const VideoPlayer = ({ video, onClose }) => {
  const [isPlaying, setIsPlaying] = useState(false);

  useEffect(() => {
    // Increment view count when video starts playing
    if (isPlaying && video) {
      fetch(`${API_BASE_URL}/api/videos/${video.id}/view`, {
        method: 'PUT'
      }).catch(console.error);
    }
  }, [isPlaying, video]);

  const renderPlayer = () => {
    if (!video) return null;

    switch (video.video_type) {
      case 'youtube':
        return (
          <iframe
            src={`${video.embed_url}?autoplay=1&rel=0`}
            frameBorder="0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowFullScreen
            className="w-full h-full"
            onLoad={() => setIsPlaying(true)}
          />
        );
      case 'rumble':
        return (
          <iframe
            src={`${video.embed_url}?autoplay=1`}
            frameBorder="0"
            allowFullScreen
            className="w-full h-full"
            onLoad={() => setIsPlaying(true)}
          />
        );
      case 'direct':
        return (
          <video
            src={video.url}
            controls
            autoPlay
            className="w-full h-full"
            onPlay={() => setIsPlaying(true)}
          >
            Your browser does not support the video tag.
          </video>
        );
      default:
        return <div className="text-white">Unsupported video format</div>;
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-90 z-50 flex items-center justify-center">
      <div className="relative w-full max-w-6xl mx-4">
        <button
          onClick={onClose}
          className="absolute -top-12 right-0 text-white text-2xl hover:text-gray-300 z-10"
        >
          ✕
        </button>
        <div className="bg-black rounded-lg overflow-hidden aspect-video">
          {renderPlayer()}
        </div>
        {video && (
          <div className="mt-4 text-white">
            <h2 className="text-2xl font-bold mb-2">{video.title}</h2>
            <p className="text-gray-300 mb-2">{video.description}</p>
            <div className="flex items-center gap-4 text-sm text-gray-400">
              <span>Category: {video.category}</span>
              <span>Views: {video.view_count || 0}</span>
              {video.is_premium && <span className="bg-yellow-600 px-2 py-1 rounded text-xs">PREMIUM</span>}
              {video.is_live && <span className="bg-red-600 px-2 py-1 rounded text-xs">LIVE</span>}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

// Video Card Component
const VideoCard = ({ video, onClick }) => {
  return (
    <div
      className="relative min-w-[300px] h-[200px] bg-gray-800 rounded-lg overflow-hidden cursor-pointer transform hover:scale-105 transition-transform duration-200"
      onClick={() => onClick(video)}
    >
      <img
        src={video.thumbnail}
        alt={video.title}
        className="w-full h-full object-cover"
        onError={(e) => {
          e.target.src = 'https://via.placeholder.com/300x200/333333/ffffff?text=Video';
        }}
      />
      <div className="absolute inset-0 bg-gradient-to-t from-black via-transparent to-transparent" />
      <div className="absolute bottom-0 left-0 right-0 p-4">
        <h3 className="text-white font-semibold text-sm mb-1 line-clamp-2">{video.title}</h3>
        <div className="flex items-center gap-2 text-xs text-gray-300">
          <span>{video.category}</span>
          {video.is_premium && <span className="bg-yellow-600 px-1 py-0.5 rounded">PREMIUM</span>}
          {video.is_live && <span className="bg-red-600 px-1 py-0.5 rounded">LIVE</span>}
        </div>
      </div>
      <div className="absolute top-2 right-2 bg-black bg-opacity-70 text-white text-xs px-2 py-1 rounded">
        {video.duration || 'N/A'}
      </div>
    </div>
  );
};

// Category Row Component
const CategoryRow = ({ category, videos, onVideoClick }) => {
  return (
    <div className="mb-8">
      <h2 className="text-white text-2xl font-bold mb-4">{category}</h2>
      <div className="flex gap-4 overflow-x-auto pb-4 scrollbar-hide">
        {videos.map(video => (
          <VideoCard
            key={video.id}
            video={video}
            onClick={onVideoClick}
          />
        ))}
      </div>
    </div>
  );
};

// Hero Section Component
const HeroSection = ({ video, onPlayClick }) => {
  if (!video) return null;

  return (
    <div
      className="relative h-[60vh] bg-cover bg-center flex items-center"
      style={{
        backgroundImage: `linear-gradient(to right, rgba(0,0,0,0.8), rgba(0,0,0,0.4)), url(${video.thumbnail})`
      }}
    >
      <div className="container mx-auto px-6">
        <div className="max-w-lg">
          <h1 className="text-white text-5xl font-bold mb-4">{video.title}</h1>
          <p className="text-gray-200 text-lg mb-6 line-clamp-3">{video.description}</p>
          <div className="flex gap-4">
            <button
              onClick={() => onPlayClick(video)}
              className="bg-white text-black px-8 py-3 rounded font-semibold hover:bg-gray-200 transition-colors flex items-center gap-2"
            >
              ▶ Play
            </button>
            <button className="bg-gray-600 bg-opacity-70 text-white px-8 py-3 rounded font-semibold hover:bg-opacity-90 transition-colors">
              ℹ More Info
            </button>
          </div>
          <div className="flex items-center gap-4 mt-4 text-sm text-gray-300">
            <span>Category: {video.category}</span>
            <span>Views: {video.view_count || 0}</span>
            {video.is_premium && <span className="bg-yellow-600 px-2 py-1 rounded text-xs">PREMIUM</span>}
            {video.is_live && <span className="bg-red-600 px-2 py-1 rounded text-xs">LIVE</span>}
          </div>
        </div>
      </div>
    </div>
  );
};

// Search Component
const SearchBar = ({ onSearch, searchTerm, setSearchTerm }) => {
  const handleSubmit = (e) => {
    e.preventDefault();
    if (searchTerm.trim()) {
      onSearch(searchTerm.trim());
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex-1 max-w-lg">
      <div className="relative">
        <input
          type="text"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          placeholder="Search videos, categories, tags..."
          className="w-full bg-gray-800 text-white px-4 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-600"
        />
        <button
          type="submit"
          className="absolute right-2 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-white"
        >
          🔍
        </button>
      </div>
    </form>
  );
};

// Navigation Component
const Navigation = ({ onSearch, searchTerm, setSearchTerm, onHomeClick }) => {
  return (
    <nav className="bg-black bg-opacity-90 backdrop-blur-sm fixed top-0 left-0 right-0 z-40 px-6 py-4">
      <div className="container mx-auto flex items-center justify-between">
        <h1
          className="text-red-600 text-2xl font-bold cursor-pointer"
          onClick={onHomeClick}
        >
          SME Network
        </h1>
        <SearchBar
          onSearch={onSearch}
          searchTerm={searchTerm}
          setSearchTerm={setSearchTerm}
        />
        <div className="flex items-center gap-4">
          <button className="text-white hover:text-gray-300">Browse</button>
          <button className="text-white hover:text-gray-300">My List</button>
          <button className="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700 transition-colors">
            Sign In
          </button>
        </div>
      </div>
    </nav>
  );
};

// Admin Panel Component (for adding videos)
const AdminPanel = ({ onAddVideo, categories }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    url: '',
    thumbnail: '',
    category: '',
    tags: '',
    is_premium: false,
    is_live: false
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    const videoData = {
      ...formData,
      tags: formData.tags.split(',').map(tag => tag.trim()).filter(tag => tag)
    };
    onAddVideo(videoData);
    setFormData({
      title: '',
      description: '',
      url: '',
      thumbnail: '',
      category: '',
      tags: '',
      is_premium: false,
      is_live: false
    });
    setIsOpen(false);
  };

  if (!isOpen) {
    return (
      <button
        onClick={() => setIsOpen(true)}
        className="fixed bottom-6 right-6 bg-red-600 text-white p-4 rounded-full hover:bg-red-700 transition-colors z-30"
      >
        + Add Video
      </button>
    );
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-90 z-50 flex items-center justify-center">
      <div className="bg-gray-900 p-6 rounded-lg w-full max-w-2xl max-h-[90vh] overflow-y-auto">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-white text-2xl font-bold">Add New Video</h2>
          <button
            onClick={() => setIsOpen(false)}
            className="text-white text-2xl hover:text-gray-300"
          >
            ✕
          </button>
        </div>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-white mb-2">Title</label>
            <input
              type="text"
              value={formData.title}
              onChange={(e) => setFormData({...formData, title: e.target.value})}
              className="w-full bg-gray-800 text-white p-3 rounded"
              required
            />
          </div>
          <div>
            <label className="block text-white mb-2">Description</label>
            <textarea
              value={formData.description}
              onChange={(e) => setFormData({...formData, description: e.target.value})}
              className="w-full bg-gray-800 text-white p-3 rounded h-24"
              required
            />
          </div>
          <div>
            <label className="block text-white mb-2">Video URL (YouTube, Rumble, or Direct)</label>
            <input
              type="url"
              value={formData.url}
              onChange={(e) => setFormData({...formData, url: e.target.value})}
              className="w-full bg-gray-800 text-white p-3 rounded"
              placeholder="https://youtube.com/watch?v=... or https://rumble.com/..."
              required
            />
          </div>
          <div>
            <label className="block text-white mb-2">Thumbnail URL</label>
            <input
              type="url"
              value={formData.thumbnail}
              onChange={(e) => setFormData({...formData, thumbnail: e.target.value})}
              className="w-full bg-gray-800 text-white p-3 rounded"
              placeholder="https://example.com/thumbnail.jpg"
            />
          </div>
          <div>
            <label className="block text-white mb-2">Category</label>
            <select
              value={formData.category}
              onChange={(e) => setFormData({...formData, category: e.target.value})}
              className="w-full bg-gray-800 text-white p-3 rounded"
              required
            >
              <option value="">Select Category</option>
              {categories.map(cat => (
                <option key={cat.id} value={cat.name}>{cat.name}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-white mb-2">Tags (comma-separated)</label>
            <input
              type="text"
              value={formData.tags}
              onChange={(e) => setFormData({...formData, tags: e.target.value})}
              className="w-full bg-gray-800 text-white p-3 rounded"
              placeholder="education, tutorial, business"
            />
          </div>
          <div className="flex gap-4">
            <label className="flex items-center text-white">
              <input
                type="checkbox"
                checked={formData.is_premium}
                onChange={(e) => setFormData({...formData, is_premium: e.target.checked})}
                className="mr-2"
              />
              Premium Content
            </label>
            <label className="flex items-center text-white">
              <input
                type="checkbox"
                checked={formData.is_live}
                onChange={(e) => setFormData({...formData, is_live: e.target.checked})}
                className="mr-2"
              />
              Live Stream
            </label>
          </div>
          <div className="flex gap-4 pt-4">
            <button
              type="submit"
              className="bg-red-600 text-white px-6 py-3 rounded hover:bg-red-700 transition-colors"
            >
              Add Video
            </button>
            <button
              type="button"
              onClick={() => setIsOpen(false)}
              className="bg-gray-600 text-white px-6 py-3 rounded hover:bg-gray-700 transition-colors"
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

// Main App Component
function App() {
  const [currentVideo, setCurrentVideo] = useState(null);
  const [featuredContent, setFeaturedContent] = useState({ hero_video: null, categories: [] });
  const [searchResults, setSearchResults] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchInitialData();
  }, []);

  const fetchInitialData = async () => {
    try {
      setLoading(true);
      
      // Fetch featured content and categories
      const [featuredResponse, categoriesResponse] = await Promise.all([
        fetch(`${API_BASE_URL}/api/featured`),
        fetch(`${API_BASE_URL}/api/categories`)
      ]);

      const featured = await featuredResponse.json();
      const categoriesData = await categoriesResponse.json();

      setFeaturedContent(featured);
      setCategories(categoriesData);

      // Create default categories if none exist
      if (categoriesData.length === 0) {
        await createDefaultCategories();
      }
    } catch (error) {
      console.error('Error fetching initial data:', error);
    } finally {
      setLoading(false);
    }
  };

  const createDefaultCategories = async () => {
    const defaultCategories = [
      { name: 'Business', description: 'Business and entrepreneurship content' },
      { name: 'Education', description: 'Educational and tutorial videos' },
      { name: 'News', description: 'News and current events' },
      { name: 'Entertainment', description: 'Entertainment content' },
      { name: 'Technology', description: 'Technology and innovation' },
      { name: 'Live Streams', description: 'Live streaming content' }
    ];

    for (const category of defaultCategories) {
      try {
        await fetch(`${API_BASE_URL}/api/categories`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(category)
        });
      } catch (error) {
        console.error('Error creating category:', error);
      }
    }

    // Refresh categories
    const response = await fetch(`${API_BASE_URL}/api/categories`);
    const categoriesData = await response.json();
    setCategories(categoriesData);
  };

  const handleSearch = async (query) => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/search?q=${encodeURIComponent(query)}`);
      const data = await response.json();
      setSearchResults(data);
    } catch (error) {
      console.error('Error searching:', error);
    }
  };

  const handleVideoClick = (video) => {
    setCurrentVideo(video);
  };

  const handleCloseVideo = () => {
    setCurrentVideo(null);
  };

  const handleHomeClick = () => {
    setSearchResults(null);
    setSearchTerm('');
    fetchInitialData();
  };

  const handleAddVideo = async (videoData) => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/videos`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(videoData)
      });

      if (response.ok) {
        fetchInitialData(); // Refresh content
      } else {
        console.error('Error adding video:', await response.text());
      }
    } catch (error) {
      console.error('Error adding video:', error);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center">
        <div className="text-white text-2xl">Loading SME Network...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-black">
      <Navigation
        onSearch={handleSearch}
        searchTerm={searchTerm}
        setSearchTerm={setSearchTerm}
        onHomeClick={handleHomeClick}
      />

      <div className="pt-16">
        {searchResults ? (
          // Search Results View
          <div className="container mx-auto px-6 py-8">
            <h1 className="text-white text-3xl font-bold mb-6">
              Search Results for "{searchTerm}" ({searchResults.total} results)
            </h1>
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4">
              {searchResults.videos.map(video => (
                <VideoCard
                  key={video.id}
                  video={video}
                  onClick={handleVideoClick}
                />
              ))}
            </div>
            {searchResults.videos.length === 0 && (
              <div className="text-gray-400 text-center py-12">
                No videos found matching your search.
              </div>
            )}
          </div>
        ) : (
          // Home View
          <>
            <HeroSection
              video={featuredContent.hero_video}
              onPlayClick={handleVideoClick}
            />
            <div className="container mx-auto px-6 py-8">
              {featuredContent.categories.map(categoryData => (
                <CategoryRow
                  key={categoryData.category}
                  category={categoryData.category}
                  videos={categoryData.videos}
                  onVideoClick={handleVideoClick}
                />
              ))}
              {featuredContent.categories.length === 0 && (
                <div className="text-gray-400 text-center py-12">
                  No videos available. Add some videos to get started!
                </div>
              )}
            </div>
          </>
        )}
      </div>

      {currentVideo && (
        <VideoPlayer
          video={currentVideo}
          onClose={handleCloseVideo}
        />
      )}

      <AdminPanel
        onAddVideo={handleAddVideo}
        categories={categories}
      />
    </div>
  );
}

export default App;