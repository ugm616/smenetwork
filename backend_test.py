
import requests
import sys
import uuid
import time
from datetime import datetime

class SMENetworkAPITester:
    def __init__(self, base_url):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.created_video_ids = []
        self.created_category_ids = []

    def run_test(self, name, method, endpoint, expected_status, data=None, params=None):
        """Run a single API test"""
        url = f"{self.base_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}
        
        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, params=params)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=headers)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    return success, response.json()
                except:
                    return success, {}
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                try:
                    print(f"Response: {response.json()}")
                except:
                    print(f"Response: {response.text}")
                return False, {}

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, {}

    def test_root_endpoint(self):
        """Test the root endpoint"""
        success, response = self.run_test(
            "Root Endpoint",
            "GET",
            "",
            200
        )
        return success

    def test_create_category(self, name, description=""):
        """Test creating a category"""
        success, response = self.run_test(
            f"Create Category: {name}",
            "POST",
            "api/categories",
            200,
            data={"name": name, "description": description}
        )
        if success and 'id' in response:
            self.created_category_ids.append(response['id'])
            return True, response
        return False, {}

    def test_get_categories(self):
        """Test getting all categories"""
        success, response = self.run_test(
            "Get All Categories",
            "GET",
            "api/categories",
            200
        )
        return success, response

    def test_create_video(self, video_data):
        """Test creating a video"""
        success, response = self.run_test(
            f"Create Video: {video_data['title']}",
            "POST",
            "api/videos",
            200,
            data=video_data
        )
        if success and 'id' in response:
            self.created_video_ids.append(response['id'])
            return True, response
        return False, {}

    def test_get_videos(self, category=None, is_premium=None, is_live=None):
        """Test getting videos with optional filters"""
        params = {}
        if category:
            params['category'] = category
        if is_premium is not None:
            params['is_premium'] = is_premium
        if is_live is not None:
            params['is_live'] = is_live
            
        filter_desc = ", ".join([f"{k}={v}" for k, v in params.items()]) if params else "no filters"
        success, response = self.run_test(
            f"Get Videos with {filter_desc}",
            "GET",
            "api/videos",
            200,
            params=params
        )
        return success, response

    def test_get_video_by_id(self, video_id):
        """Test getting a video by ID"""
        success, response = self.run_test(
            f"Get Video by ID: {video_id}",
            "GET",
            f"api/videos/{video_id}",
            200
        )
        return success, response

    def test_search_videos(self, query):
        """Test searching for videos"""
        success, response = self.run_test(
            f"Search Videos for: {query}",
            "GET",
            "api/search",
            200,
            params={"q": query}
        )
        return success, response

    def test_featured_content(self):
        """Test getting featured content"""
        success, response = self.run_test(
            "Get Featured Content",
            "GET",
            "api/featured",
            200
        )
        return success, response

    def test_increment_view_count(self, video_id):
        """Test incrementing a video's view count"""
        success, response = self.run_test(
            f"Increment View Count for Video: {video_id}",
            "PUT",
            f"api/videos/{video_id}/view",
            200
        )
        return success, response

    def test_video_url_parsing(self, urls):
        """Test video URL parsing for different types"""
        results = []
        for url_type, url in urls.items():
            video_data = {
                "title": f"Test {url_type} Video",
                "description": f"Testing {url_type} URL parsing",
                "url": url,
                "thumbnail": "https://via.placeholder.com/300x200",
                "category": "Test",
                "tags": ["test", url_type]
            }
            success, response = self.test_create_video(video_data)
            if success:
                # Verify the video_type was correctly identified
                expected_type = url_type.lower()
                actual_type = response.get('video_type', '')
                type_correct = expected_type == actual_type
                
                if type_correct:
                    print(f"✅ URL correctly identified as {actual_type}")
                else:
                    print(f"❌ URL incorrectly identified as {actual_type}, expected {expected_type}")
                    success = False
                
                results.append((url_type, success))
            else:
                results.append((url_type, False))
        
        return results

def main():
    # Get the backend URL from environment
    backend_url = "https://7beeae22-45fe-4d0d-a80e-46bc3b071f6f.preview.emergentagent.com"
    
    # Setup tester
    tester = SMENetworkAPITester(backend_url)
    
    print("=" * 50)
    print("SME Network API Testing")
    print("=" * 50)
    
    # Test root endpoint
    tester.test_root_endpoint()
    
    # Test categories
    print("\n--- Testing Categories ---")
    # Check if Business category exists
    success, categories = tester.test_get_categories()
    business_exists = False
    if success:
        for category in categories:
            if category.get('name') == 'Business':
                business_exists = True
                break
    
    # Create test category if Business doesn't exist
    if not business_exists:
        tester.test_create_category("Business", "Business and entrepreneurship content")
    
    # Create a unique test category
    test_category_name = f"Test Category {uuid.uuid4().hex[:8]}"
    tester.test_create_category(test_category_name, "Test category for API testing")
    
    # Test videos
    print("\n--- Testing Videos ---")
    # Create test videos with different URL types
    test_urls = {
        "YouTube": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "Rumble": "https://rumble.com/v2j3hyu-5-tips-for-small-business-success.html",
        "Direct": "https://example.com/video.mp4"
    }
    
    url_parsing_results = tester.test_video_url_parsing(test_urls)
    
    # Create a test video in the Business category
    business_video = {
        "title": "Business Strategy Test",
        "description": "A test video about business strategy",
        "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "thumbnail": "https://via.placeholder.com/300x200",
        "category": "Business",
        "tags": ["business", "strategy", "test"]
    }
    success, video_response = tester.test_create_video(business_video)
    
    # Test getting videos
    if success:
        video_id = video_response['id']
        
        # Test getting video by ID
        tester.test_get_video_by_id(video_id)
        
        # Test getting videos by category
        tester.test_get_videos(category="Business")
        
        # Test search functionality
        tester.test_search_videos("Business")
        tester.test_search_videos("strategy")
        
        # Test featured content
        tester.test_featured_content()
        
        # Test view count increment
        tester.test_increment_view_count(video_id)
        
        # Verify view count was incremented
        success, updated_video = tester.test_get_video_by_id(video_id)
        if success:
            initial_views = video_response.get('view_count', 0)
            updated_views = updated_video.get('view_count', 0)
            if updated_views > initial_views:
                print(f"✅ View count successfully incremented from {initial_views} to {updated_views}")
            else:
                print(f"❌ View count not incremented: {initial_views} -> {updated_views}")
    
    # Print results
    print("\n" + "=" * 50)
    print(f"Tests passed: {tester.tests_passed}/{tester.tests_run} ({tester.tests_passed/tester.tests_run*100:.1f}%)")
    print("=" * 50)
    
    # URL parsing results
    print("\nURL Parsing Results:")
    for url_type, success in url_parsing_results:
        status = "✅ Passed" if success else "❌ Failed"
        print(f"{url_type}: {status}")
    
    return 0 if tester.tests_passed == tester.tests_run else 1

if __name__ == "__main__":
    sys.exit(main())
