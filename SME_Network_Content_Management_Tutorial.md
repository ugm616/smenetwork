# SME Network - Content Management Tutorial

## Table of Contents
1. [Getting Started](#getting-started)
2. [Adding Content](#adding-content)
3. [Managing Categories](#managing-categories)
4. [Removing Content](#removing-content)
5. [Video Metadata Management](#video-metadata-management)
6. [Best Practices](#best-practices)

---

## Getting Started

### Accessing the Admin Panel
1. Open your SME Network website in a browser
2. Look for the **red "+" button** in the bottom-right corner of the screen
3. Click the button to open the **"Add New Video"** panel

### Understanding Video Formats
Your platform supports three video formats:
- **YouTube**: Videos hosted on YouTube.com
- **Rumble**: Videos hosted on Rumble.com  
- **External/Direct**: Direct video file URLs (MP4, WebM, etc.)

---

## Adding Content

### 1. Adding YouTube Videos

**Step-by-Step Process:**

1. **Get the YouTube URL:**
   - Go to YouTube and find your video
   - Copy the URL (formats supported):
     - `https://www.youtube.com/watch?v=VIDEO_ID`
     - `https://youtu.be/VIDEO_ID`

2. **Fill out the form:**
   - **Title**: Enter your video title (will auto-populate from YouTube if API works)
   - **Description**: Add detailed description
   - **Video URL**: Paste the YouTube URL
   - **Thumbnail URL**: Leave blank (auto-fetched) or add custom thumbnail
   - **Category**: Select from dropdown
   - **Tags**: Add comma-separated tags (e.g., "business, strategy, startup")
   - **Premium Content**: Check if this requires subscription
   - **Live Stream**: Check if this is a live stream

3. **Example YouTube Entry:**
   ```
   Title: "Digital Marketing Masterclass 2025"
   Description: "Learn advanced digital marketing strategies including SEO, PPC, and social media marketing."
   URL: https://www.youtube.com/watch?v=abc123xyz
   Thumbnail: (leave blank for auto-fetch)
   Category: Business
   Tags: marketing, digital, SEO, strategy
   Premium Content: ✓ (checked)
   Live Stream: ☐ (unchecked)
   ```

### 2. Adding Rumble Videos

**Step-by-Step Process:**

1. **Get the Rumble URL:**
   - Go to Rumble and find your video
   - Copy the URL (formats supported):
     - `https://rumble.com/VIDEO_ID-title.html`
     - `https://rumble.com/embed/VIDEO_ID/`

2. **Fill out the form:**
   - **Title**: Enter descriptive title
   - **Description**: Add comprehensive description
   - **Video URL**: Paste the Rumble URL
   - **Thumbnail URL**: Add custom thumbnail (Rumble thumbnails don't auto-fetch)
   - **Category**: Select appropriate category
   - **Tags**: Add relevant tags
   - **Premium/Live**: Set as needed

3. **Example Rumble Entry:**
   ```
   Title: "Entrepreneurship Success Stories"
   Description: "Inspiring stories from successful entrepreneurs who built their businesses from scratch."
   URL: https://rumble.com/v2j3hyu-business-success-stories.html
   Thumbnail: https://images.unsplash.com/photo-1560472354-b33ff0c44a43?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80
   Category: Business
   Tags: entrepreneurship, success, stories, inspiration
   Premium Content: ☐ (unchecked)
   Live Stream: ☐ (unchecked)
   ```

### 3. Adding External/Direct Video Sources

**Step-by-Step Process:**

1. **Get the Direct Video URL:**
   - Ensure your video is hosted on a accessible server
   - Copy the direct file URL (must end in .mp4, .webm, .ogg, etc.)
   - Example: `https://example.com/videos/training-video.mp4`

2. **Fill out the form:**
   - **Title**: Enter descriptive title
   - **Description**: Add detailed description
   - **Video URL**: Paste the direct video URL
   - **Thumbnail URL**: Add custom thumbnail (required for direct videos)
   - **Category**: Select category
   - **Tags**: Add relevant tags
   - **Premium/Live**: Set as needed

3. **Example Direct Video Entry:**
   ```
   Title: "Company Training Module 1"
   Description: "Internal training video covering company policies and procedures."
   URL: https://cdn.company.com/training/module1.mp4
   Thumbnail: https://cdn.company.com/thumbnails/module1-thumb.jpg
   Category: Education
   Tags: training, internal, policies, procedures
   Premium Content: ✓ (checked)
   Live Stream: ☐ (unchecked)
   ```

---

## Managing Categories

### Adding New Categories

**Method 1: Through the Admin Interface (when adding videos)**
1. If you need a new category while adding a video, contact your administrator
2. Categories must be created via API calls

**Method 2: Using API (for administrators)**
```bash
curl -X POST "https://your-domain.com/api/categories" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Finance",
    "description": "Financial education and investment content"
  }'
```

### Default Categories Available:
- **Business**: Business and entrepreneurship content
- **Education**: Educational and tutorial videos
- **Technology**: Technology and innovation content
- **Live Streams**: Live streaming content with donations

### Category Best Practices:
- Keep category names short and clear
- Use broad categories that can accommodate multiple videos
- Consider your audience when creating categories
- Don't create too many categories (5-10 is optimal)

---

## Removing Content

### Method 1: Database Direct (Administrator Only)
Since there's no delete button in the UI currently, content removal requires database access:

```bash
# Remove a specific video by ID
curl -X DELETE "https://your-domain.com/api/videos/VIDEO_ID"
```

### Method 2: Contact Administrator
For non-technical users:
1. Note down the video title and ID
2. Contact your system administrator
3. Provide the specific video details for removal

### Finding Video IDs:
1. Open browser developer tools (F12)
2. Go to Network tab
3. Click on a video
4. Look for API calls to see the video ID
5. OR check the database directly

---

## Video Metadata Management

### 1. Title Guidelines
- **Keep it descriptive and engaging**
- **Recommended length**: 50-60 characters
- **Include key search terms**
- **Examples:**
  - Good: "Digital Marketing Strategies for Small Businesses 2025"
  - Poor: "Marketing Video"

### 2. Description Best Practices
- **Length**: 150-300 characters for optimal display
- **Include key information**: What viewers will learn
- **Use engaging language**
- **Include relevant keywords naturally**
- **Example:**
  ```
  "Master advanced digital marketing strategies including SEO, PPC, social media marketing, and content creation. Perfect for entrepreneurs and small business owners looking to grow their online presence in 2025."
  ```

### 3. Tags Strategy
- **Use 3-8 relevant tags per video**
- **Separate with commas**
- **Include broad and specific terms**
- **Think about what users might search for**
- **Examples:**
  - Business video: `business, strategy, entrepreneurship, startup, SME`
  - Tech video: `technology, AI, programming, innovation, tutorial`
  - Education: `education, learning, tutorial, training, course`

### 4. Thumbnail Guidelines
- **Recommended size**: 1280x720 pixels (16:9 aspect ratio)
- **File formats**: JPG, PNG, WebP
- **Use high-quality, engaging images**
- **Include text overlay if needed**
- **Ensure it represents the video content**
- **Good thumbnail sources**:
  - Unsplash: `https://images.unsplash.com/`
  - Pexels: `https://images.pexels.com/`
  - Custom created thumbnails

### 5. Premium Content vs Free Content
**Mark as Premium when:**
- Content requires subscription to access
- High-value, exclusive content
- Advanced tutorials or courses
- Paid content

**Keep as Free when:**
- Introduction or teaser content
- General educational material
- Marketing content
- Community-building content

### 6. Live Stream Settings
**Mark as Live Stream when:**
- Content is broadcast in real-time
- Interactive Q&A sessions
- Live events or conferences
- Streams that accept donations

---

## Best Practices

### Content Organization
1. **Plan your content strategy**
   - Define your target audience
   - Create content pillars (Business, Education, etc.)
   - Plan regular content updates

2. **Maintain consistent quality**
   - Use high-quality thumbnails
   - Write compelling descriptions
   - Use consistent tagging strategy

3. **SEO Optimization**
   - Include keywords in titles naturally
   - Use relevant tags
   - Write descriptive metadata

### Video URL Best Practices

**YouTube URLs:**
- Always use the full YouTube URL
- Both `youtube.com/watch?v=` and `youtu.be/` formats work
- Ensure videos are public or unlisted (not private)

**Rumble URLs:**
- Use the full Rumble page URL
- Both regular page URLs and embed URLs work
- Ensure videos are publicly accessible

**Direct Video URLs:**
- Must be publicly accessible
- Use HTTPS when possible
- Ensure proper CORS headers if hosting on different domain
- Supported formats: MP4, WebM, OGG

### Content Curation Tips

1. **Quality over quantity**
   - Focus on valuable, engaging content
   - Regularly review and update old content

2. **Audience engagement**
   - Monitor which videos get the most views
   - Create more content in popular categories
   - Respond to viewer feedback

3. **Content mixing**
   - Balance free and premium content
   - Mix different video lengths
   - Include both educational and entertainment value

---

## Troubleshooting Common Issues

### Video Won't Play
1. **Check URL format**: Ensure URL is correct and publicly accessible
2. **Check video privacy**: YouTube videos must be public or unlisted
3. **Check CORS**: For direct videos, ensure proper CORS headers

### Thumbnail Not Loading
1. **Check thumbnail URL**: Ensure it's a direct image link
2. **Use HTTPS**: Mixed content issues can block HTTP images
3. **Check image size**: Very large images may not load properly

### Search Not Finding Videos
1. **Check tags**: Ensure relevant tags are added
2. **Check title/description**: Include searchable keywords
3. **Allow indexing time**: New content may take a moment to be searchable

---

## Support and Maintenance

For additional help:
1. Check the browser console for error messages
2. Verify all URLs are accessible
3. Contact your system administrator for database-level issues
4. Keep your content organized with consistent metadata

Remember: Good content management is key to a successful video platform. Take time to properly categorize, tag, and describe your videos for the best user experience!