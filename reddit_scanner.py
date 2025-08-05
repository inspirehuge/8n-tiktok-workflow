import os
import praw
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any
from dotenv import load_dotenv
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RedditScanner:
    def __init__(self):
        """Initialize Reddit scanner with PRAW."""
        load_dotenv()
        
        # Reddit API credentials
        self.client_id = os.getenv('REDDIT_CLIENT_ID')
        self.client_secret = os.getenv('REDDIT_CLIENT_SECRET')
        self.user_agent = os.getenv('REDDIT_USER_AGENT', 'ProductFinderBot/1.0')
        
        if not all([self.client_id, self.client_secret]):
            raise ValueError("Reddit API credentials must be set in .env file")
        
        # Initialize Reddit instance
        self.reddit = praw.Reddit(
            client_id=self.client_id,
            client_secret=self.client_secret,
            user_agent=self.user_agent
        )
        
        # Target subreddits for pain-related posts
        self.target_subreddits = [
            'ChronicPain',
            'BuyItForLife',
            'backpain',
            'migraine',
            'Fibromyalgia',
            'PlantarFasciitis',
            'kneepain',
            'shoulderpain',
            'neckpain',
            'sciatica',
            'arthritis',
            'insomnia',
            'sleep',
            'PainManagement',
            'ehlersdanlos',
            'disability'
        ]
        
        # Pain-related keywords for detection
        self.pain_keywords = [
            'pain', 'hurt', 'ache', 'sore', 'relief', 'chronic', 'suffering',
            'uncomfortable', 'stiff', 'tender', 'throbbing', 'burning',
            'sharp', 'dull', 'constant', 'severe', 'mild', 'moderate',
            'can\'t sleep', 'sleepless', 'insomnia', 'tired', 'exhausted',
            'inflammation', 'swollen', 'numb', 'tingling', 'weakness',
            'mobility', 'difficulty', 'struggle', 'help', 'solution',
            'treatment', 'therapy', 'medication', 'supplement', 'device',
            'product', 'recommend', 'suggestion', 'advice', 'what works'
        ]
        
        logger.info("RedditScanner initialized successfully")
    
    def _is_pain_related(self, text: str) -> bool:
        """Check if text contains pain-related keywords."""
        text_lower = text.lower()
        
        # Check for direct keyword matches
        for keyword in self.pain_keywords:
            if keyword in text_lower:
                return True
        
        # Check for pain-related patterns
        pain_patterns = [
            r'\b(my|have|got|experiencing)\s+\w*pain\w*',
            r'\b(relief|help|solution)\s+(for|with|from)',
            r'\b(what|any|best)\s+\w*\s+(works|helps|relieves)',
            r'\b(recommend|suggest|advice)\s+\w*\s+(for|to)',
            r'\b(can\'t|cannot|unable)\s+(sleep|walk|sit|stand|move)',
            r'\b(need|looking for|searching for)\s+\w*\s+(help|relief|solution)'
        ]
        
        for pattern in pain_patterns:
            if re.search(pattern, text_lower):
                return True
        
        return False
    
    def _extract_problem_category(self, title: str, content: str) -> str:
        """Extract problem category from post content."""
        combined_text = f"{title} {content}".lower()
        
        categories = {
            'Back Pain': ['back', 'spine', 'lumbar', 'sciatica', 'disc'],
            'Neck Pain': ['neck', 'cervical', 'whiplash'],
            'Knee Pain': ['knee', 'patella', 'meniscus'],
            'Foot Care': ['foot', 'feet', 'plantar', 'heel', 'arch', 'toe'],
            'Sleep Issues': ['sleep', 'insomnia', 'tired', 'exhausted', 'bed'],
            'Joint Pain': ['joint', 'arthritis', 'rheumatoid', 'osteoarthritis'],
            'Muscle Pain': ['muscle', 'strain', 'spasm', 'cramp'],
            'Headache/Migraine': ['headache', 'migraine', 'head', 'temple'],
            'Shoulder Pain': ['shoulder', 'rotator', 'cuff'],
            'General Pain': ['chronic', 'fibromyalgia', 'widespread', 'overall']
        }
        
        for category, keywords in categories.items():
            if any(keyword in combined_text for keyword in keywords):
                return category
        
        return 'General Pain'
    
    def scan_subreddit(self, subreddit_name: str, days_back: int = 7) -> List[Dict[str, Any]]:
        """Scan a specific subreddit for pain-related posts."""
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            posts = []
            
            # Calculate cutoff date
            cutoff_date = datetime.now() - timedelta(days=days_back)
            
            # Get recent posts (hot, new, top)
            for submission in subreddit.hot(limit=100):
                post_date = datetime.fromtimestamp(submission.created_utc)
                
                # Skip posts older than cutoff
                if post_date < cutoff_date:
                    continue
                
                # Check if post is pain-related
                full_text = f"{submission.title} {submission.selftext}"
                if self._is_pain_related(full_text):
                    category = self._extract_problem_category(submission.title, submission.selftext)
                    
                    post_data = {
                        'title': submission.title,
                        'content': submission.selftext[:500],  # Limit content length
                        'url': f"https://reddit.com{submission.permalink}",
                        'subreddit': subreddit_name,
                        'category': category,
                        'score': submission.score,
                        'num_comments': submission.num_comments,
                        'created_utc': submission.created_utc,
                        'created_date': post_date.strftime('%Y-%m-%d %H:%M:%S'),
                        'author': str(submission.author) if submission.author else 'deleted'
                    }
                    
                    posts.append(post_data)
                    logger.info(f"Found pain-related post: {submission.title[:50]}...")
            
            logger.info(f"Found {len(posts)} pain-related posts in r/{subreddit_name}")
            return posts
            
        except Exception as e:
            logger.error(f"Error scanning r/{subreddit_name}: {e}")
            return []
    
    def scan_all_subreddits(self, days_back: int = 7) -> List[Dict[str, Any]]:
        """Scan all target subreddits for pain-related posts."""
        all_posts = []
        
        logger.info(f"Starting scan of {len(self.target_subreddits)} subreddits...")
        
        for subreddit_name in self.target_subreddits:
            try:
                posts = self.scan_subreddit(subreddit_name, days_back)
                all_posts.extend(posts)
                
                # Add small delay to avoid rate limiting
                import time
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"Failed to scan r/{subreddit_name}: {e}")
                continue
        
        # Sort by score (popularity) descending
        all_posts.sort(key=lambda x: x['score'], reverse=True)
        
        logger.info(f"Total pain-related posts found: {len(all_posts)}")
        return all_posts
    
    def get_top_problems(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get top pain-related problems from Reddit."""
        posts = self.scan_all_subreddits()
        
        # Filter and limit results
        top_posts = posts[:limit]
        
        # Format for easier processing
        problems = []
        for post in top_posts:
            problem = {
                'reddit_title': post['title'],
                'reddit_content': post['content'],
                'reddit_url': post['url'],
                'category': post['category'],
                'subreddit': post['subreddit'],
                'score': post['score'],
                'date': post['created_date'],
                'search_query': self._generate_search_query(post['title'], post['content'])
            }
            problems.append(problem)
        
        return problems
    
    def _generate_search_query(self, title: str, content: str) -> str:
        """Generate TikTok search query from Reddit post."""
        # Combine title and content
        combined = f"{title} {content}".lower()
        
        # Extract key terms
        key_terms = []
        
        # Look for specific pain types
        pain_types = ['back pain', 'neck pain', 'knee pain', 'foot pain', 'headache', 'migraine']
        for pain_type in pain_types:
            if pain_type in combined:
                key_terms.append(pain_type.replace(' ', ''))
        
        # Look for product-related terms
        product_terms = ['relief', 'solution', 'product', 'device', 'tool', 'supplement']
        for term in product_terms:
            if term in combined:
                key_terms.append(term)
        
        # If no specific terms found, use general search
        if not key_terms:
            key_terms = ['pain relief', 'health product']
        
        return ' '.join(key_terms[:3])  # Limit to 3 terms

if __name__ == "__main__":
    # Test the Reddit scanner
    try:
        scanner = RedditScanner()
        problems = scanner.get_top_problems(limit=5)
        
        print(f"\nFound {len(problems)} problems:")
        for i, problem in enumerate(problems, 1):
            print(f"\n{i}. {problem['reddit_title']}")
            print(f"   Category: {problem['category']}")
            print(f"   Subreddit: r/{problem['subreddit']}")
            print(f"   Score: {problem['score']}")
            print(f"   Search Query: {problem['search_query']}")
            
    except Exception as e:
        logger.error(f"Test failed: {e}")