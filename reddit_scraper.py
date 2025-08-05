import praw
import re
from typing import List, Dict
import os
from datetime import datetime, timedelta


def get_problems() -> List[Dict]:
    """
    Scrapes Reddit for user pain/problem posts from specified subreddits.
    
    Returns:
        List of dictionaries containing problem, context, and keywords
    """
    
    # Initialize Reddit instance
    reddit = praw.Reddit(
        client_id=os.getenv('REDDIT_CLIENT_ID', 'your_client_id'),
        client_secret=os.getenv('REDDIT_CLIENT_SECRET', 'your_client_secret'),
        user_agent=os.getenv('REDDIT_USER_AGENT', 'ProductDiscovery/1.0')
    )
    
    # Target subreddits for pain/problem discovery
    subreddits = [
        'BuyItForLife', 'Frugal', 'ChronicPain', 'backpain', 'plantarfasciitis',
        'Productivity', 'Arthritis', 'ShoulderPain', 'Sciatica'
    ]
    
    # Keywords that indicate pain/problems/help requests
    pain_keywords = [
        'pain', 'hurt', 'ache', 'sore', 'chronic', 'help', 'recommend', 
        'suggestion', 'advice', 'problem', 'issue', 'struggle', 'difficulty',
        'fatigue', 'tired', 'exhausted', 'relief', 'solution', 'fix'
    ]
    
    problems = []
    
    for subreddit_name in subreddits:
        try:
            subreddit = reddit.subreddit(subreddit_name)
            
            # Search recent posts (last week)
            for submission in subreddit.hot(limit=50):
                # Check if post is recent (within last 7 days)
                post_time = datetime.fromtimestamp(submission.created_utc)
                if datetime.now() - post_time > timedelta(days=7):
                    continue
                
                # Combine title and selftext for analysis
                full_text = f"{submission.title} {submission.selftext}".lower()
                
                # Check if post contains pain/problem keywords
                if any(keyword in full_text for keyword in pain_keywords):
                    # Extract problem and context
                    problem = extract_problem(submission.title, submission.selftext)
                    if problem:
                        keywords = extract_keywords(full_text)
                        
                        problems.append({
                            "problem": problem,
                            "context": submission.selftext[:200] + "..." if len(submission.selftext) > 200 else submission.selftext,
                            "keywords": keywords,
                            "subreddit": subreddit_name,
                            "post_id": submission.id
                        })
                        
                        # Limit to prevent overwhelming the system
                        if len(problems) >= 20:
                            break
            
            if len(problems) >= 20:
                break
                
        except Exception as e:
            print(f"Error accessing subreddit {subreddit_name}: {e}")
            continue
    
    return problems


def extract_problem(title: str, selftext: str) -> str:
    """
    Extract the main problem from title and post content.
    
    Args:
        title: Post title
        selftext: Post content
        
    Returns:
        Extracted problem statement
    """
    # Combine title and first sentence of selftext
    problem_text = title
    
    if selftext:
        # Get first sentence of selftext
        sentences = re.split(r'[.!?]+', selftext)
        if sentences and len(sentences[0].strip()) > 10:
            problem_text += f" - {sentences[0].strip()}"
    
    # Clean and limit length
    problem_text = re.sub(r'\s+', ' ', problem_text).strip()
    return problem_text[:150] + "..." if len(problem_text) > 150 else problem_text


def extract_keywords(text: str) -> List[str]:
    """
    Extract relevant keywords from the problem text.
    
    Args:
        text: Text to extract keywords from
        
    Returns:
        List of extracted keywords
    """
    # Common pain/problem related terms
    keyword_patterns = [
        r'\b(back|neck|shoulder|knee|foot|feet|ankle|hip|wrist|elbow)\s*(?:pain|ache|hurt|sore)\b',
        r'\b(?:chronic|severe|constant|daily)\s*(?:pain|ache|fatigue)\b',
        r'\b(?:standing|sitting|walking|working|sleeping)\s*(?:all day|long hours|too long)\b',
        r'\b(?:arthritis|sciatica|fibromyalgia|plantar fasciitis|carpal tunnel)\b',
        r'\b(?:office|desk|retail|warehouse|construction|nursing)\s*(?:work|job|worker)\b',
        r'\b(?:insoles|cushion|support|brace|pillow|mattress|chair|shoes)\b',
        r'\b(?:relief|solution|help|recommendation|advice)\b'
    ]
    
    keywords = []
    
    for pattern in keyword_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        keywords.extend(matches)
    
    # Also extract common nouns that might be relevant
    common_terms = [
        'pain', 'back', 'neck', 'shoulder', 'knee', 'foot', 'feet', 'standing', 
        'sitting', 'work', 'office', 'retail', 'support', 'relief', 'help',
        'chronic', 'arthritis', 'sciatica', 'insoles', 'cushion', 'pillow'
    ]
    
    for term in common_terms:
        if term in text:
            keywords.append(term)
    
    # Remove duplicates and return unique keywords
    return list(set([kw.lower().strip() for kw in keywords if len(kw.strip()) > 2]))


if __name__ == "__main__":
    # Test the scraper
    problems = get_problems()
    print(f"Found {len(problems)} problems:")
    for i, problem in enumerate(problems[:3]):  # Show first 3
        print(f"\n{i+1}. Problem: {problem['problem']}")
        print(f"   Keywords: {problem['keywords']}")
        print(f"   Context: {problem['context'][:100]}...")