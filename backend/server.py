from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
import uuid
import re
import requests
from datetime import datetime

# Environment variables
MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
DB_NAME = os.environ.get('DB_NAME', 'sme_network')
YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY')

# Initialize FastAPI
app = FastAPI(title="SME Network API", description="Video on Demand Service API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB connection
client = MongoClient(MONGO_URL)
db = client[DB_NAME]
videos_collection = db.videos
categories_collection = db.categories

# Pydantic models
class VideoBase(BaseModel):
    title: str
    description: str
    url: str
    thumbnail: str
    category: str
    tags: List[str] = []
    duration: Optional[str] = None
    is_premium: bool = False
    is_live: bool = False

class Video(VideoBase):
    id: str
    video_type: str  # 'youtube', 'rumble', 'direct'
    video_id: Optional[str] = None
    created_at: datetime
    view_count: int = 0

class Category(BaseModel):
    id: str
    name: str
    description: str
    created_at: datetime

class SearchResponse(BaseModel):
    videos: List[Video]
    total: int
    page: int
    per_page: int

# Utility functions
def extract_video_info(url: str) -> Dict[str, Any]:
    """Extract video type and ID from URL"""
    youtube_pattern = r'(?:youtube\.com/watch\?v=|youtu\.be/)([^&\n?#]+)'
    rumble_pattern = r'rumble\.com/(?:embed/)?([^/?]+)'
    
    youtube_match = re.search(youtube_pattern, url)
    rumble_match = re.search(rumble_pattern, url)
    
    if youtube_match:
        return {
            'type': 'youtube',
            'video_id': youtube_match.group(1),
            'embed_url': f'https://www.youtube.com/embed/{youtube_match.group(1)}'
        }
    elif rumble_match:
        return {
            'type': 'rumble',
            'video_id': rumble_match.group(1),
            'embed_url': f'https://rumble.com/embed/{rumble_match.group(1)}/'
        }
    else:
        return {
            'type': 'direct',
            'video_id': None,
            'embed_url': url
        }

def get_youtube_metadata(video_id: str) -> Dict[str, Any]:
    """Fetch YouTube video metadata"""
    if not YOUTUBE_API_KEY:
        return {}
    
    try:
        url = f"https://www.googleapis.com/youtube/v3/videos"
        params = {
            'id': video_id,
            'part': 'snippet,contentDetails,statistics',
            'key': YOUTUBE_API_KEY
        }
        response = requests.get(url, params=params)
        data = response.json()
        
        if data.get('items'):
            item = data['items'][0]
            snippet = item['snippet']
            content_details = item['contentDetails']
            statistics = item.get('statistics', {})
            
            return {
                'title': snippet['title'],
                'description': snippet['description'],
                'thumbnail': snippet['thumbnails']['high']['url'],
                'duration': content_details['duration'],
                'view_count': int(statistics.get('viewCount', 0))
            }
    except Exception as e:
        print(f"Error fetching YouTube metadata: {e}")
    
    return {}

# API Routes
@app.get("/")
async def root():
    return {"message": "SME Network API", "status": "running"}

@app.post("/api/videos", response_model=Video)
async def create_video(video: VideoBase):
    """Create a new video"""
    try:
        # Extract video information
        video_info = extract_video_info(video.url)
        
        # Get metadata for YouTube videos
        metadata = {}
        if video_info['type'] == 'youtube' and video_info['video_id']:
            metadata = get_youtube_metadata(video_info['video_id'])
        
        # Create video document
        video_doc = {
            'id': str(uuid.uuid4()),
            'title': metadata.get('title', video.title),
            'description': metadata.get('description', video.description),
            'url': video.url,
            'thumbnail': metadata.get('thumbnail', video.thumbnail),
            'category': video.category,
            'tags': video.tags,
            'duration': metadata.get('duration', video.duration),
            'is_premium': video.is_premium,
            'is_live': video.is_live,
            'video_type': video_info['type'],
            'video_id': video_info['video_id'],
            'embed_url': video_info['embed_url'],
            'created_at': datetime.utcnow(),
            'view_count': metadata.get('view_count', 0)
        }
        
        # Insert into database
        result = videos_collection.insert_one(video_doc)
        if result.inserted_id:
            return Video(**video_doc)
        else:
            raise HTTPException(status_code=500, detail="Failed to create video")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/videos", response_model=List[Video])
async def get_videos(
    category: Optional[str] = None,
    is_premium: Optional[bool] = None,
    is_live: Optional[bool] = None,
    limit: int = Query(20, le=100),
    skip: int = Query(0, ge=0)
):
    """Get videos with optional filtering"""
    try:
        # Build query
        query = {}
        if category:
            query['category'] = category
        if is_premium is not None:
            query['is_premium'] = is_premium
        if is_live is not None:
            query['is_live'] = is_live
        
        # Execute query
        cursor = videos_collection.find(query).skip(skip).limit(limit).sort('created_at', -1)
        videos = []
        
        for doc in cursor:
            del doc['_id']  # Remove MongoDB ObjectId
            videos.append(Video(**doc))
        
        return videos
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/videos/{video_id}", response_model=Video)
async def get_video(video_id: str):
    """Get a specific video by ID"""
    try:
        video_doc = videos_collection.find_one({'id': video_id})
        if not video_doc:
            raise HTTPException(status_code=404, detail="Video not found")
        
        del video_doc['_id']
        return Video(**video_doc)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/search", response_model=SearchResponse)
async def search_videos(
    q: str = Query(..., min_length=1),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, le=100)
):
    """Search videos by title, description, tags, or category"""
    try:
        # Build search query
        search_query = {
            '$or': [
                {'title': {'$regex': q, '$options': 'i'}},
                {'description': {'$regex': q, '$options': 'i'}},
                {'category': {'$regex': q, '$options': 'i'}},
                {'tags': {'$regex': q, '$options': 'i'}}
            ]
        }
        
        # Calculate pagination
        skip = (page - 1) * per_page
        
        # Execute search
        cursor = videos_collection.find(search_query).skip(skip).limit(per_page).sort('created_at', -1)
        total = videos_collection.count_documents(search_query)
        
        videos = []
        for doc in cursor:
            del doc['_id']
            videos.append(Video(**doc))
        
        return SearchResponse(
            videos=videos,
            total=total,
            page=page,
            per_page=per_page
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/categories", response_model=List[Category])
async def get_categories():
    """Get all categories"""
    try:
        cursor = categories_collection.find().sort('name', 1)
        categories = []
        
        for doc in cursor:
            del doc['_id']
            categories.append(Category(**doc))
        
        return categories
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/categories", response_model=Category)
async def create_category(name: str, description: str = ""):
    """Create a new category"""
    try:
        category_doc = {
            'id': str(uuid.uuid4()),
            'name': name,
            'description': description,
            'created_at': datetime.utcnow()
        }
        
        result = categories_collection.insert_one(category_doc)
        if result.inserted_id:
            return Category(**category_doc)
        else:
            raise HTTPException(status_code=500, detail="Failed to create category")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/featured")
async def get_featured_content():
    """Get featured content for homepage"""
    try:
        # Get latest videos by category
        categories = list(categories_collection.find())
        featured_content = []
        
        for category in categories:
            videos = list(videos_collection.find(
                {'category': category['name']}
            ).limit(10).sort('created_at', -1))
            
            # Remove MongoDB ObjectId
            for video in videos:
                del video['_id']
            
            if videos:
                featured_content.append({
                    'category': category['name'],
                    'videos': videos
                })
        
        # Get hero video (latest non-premium video)
        hero_video = videos_collection.find_one(
            {'is_premium': False},
            sort=[('created_at', -1)]
        )
        
        if hero_video:
            del hero_video['_id']
        
        return {
            'hero_video': hero_video,
            'categories': featured_content
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/videos/{video_id}/view")
async def increment_view_count(video_id: str):
    """Increment view count for a video"""
    try:
        result = videos_collection.update_one(
            {'id': video_id},
            {'$inc': {'view_count': 1}}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Video not found")
        
        return {"message": "View count incremented"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)