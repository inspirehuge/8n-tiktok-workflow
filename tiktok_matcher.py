from typing import List, Dict
import random
from datetime import datetime


def find_matching_products(keywords: List[str], problem: str) -> List[Dict]:
    """
    Simulate TikTok product search based on keywords and problem description.
    
    Args:
        keywords: List of keywords extracted from the problem
        problem: Original problem description
        
    Returns:
        List of matching product dictionaries
    """
    
    # Simulate product database with realistic TikTok-style products
    product_database = {
        'foot': [
            {
                "title": "Smart Arch Support Insoles",
                "category": "Foot Care",
                "videoUrl": "https://www.tiktok.com/@footcare_guru/video/7234567890",
                "description": "Revolutionary insoles with memory foam for all-day comfort. Perfect for retail workers!",
                "views": "1.2M",
                "source": "TikTok"
            },
            {
                "title": "Compression Foot Sleeves",
                "category": "Health & Wellness",
                "videoUrl": "https://www.tiktok.com/@wellness_tips/video/7234567891",
                "description": "Reduce swelling and pain with these amazing compression sleeves",
                "views": "850K",
                "source": "TikTok"
            },
            {
                "title": "Plantar Fasciitis Night Splint",
                "category": "Medical Devices",
                "videoUrl": "https://www.tiktok.com/@health_solutions/video/7234567892",
                "description": "Wake up pain-free with this overnight stretching device",
                "views": "2.1M",
                "source": "TikTok"
            }
        ],
        'back': [
            {
                "title": "Lumbar Support Cushion",
                "category": "Office Ergonomics",
                "videoUrl": "https://www.tiktok.com/@office_hacks/video/7234567893",
                "description": "Transform any chair into an ergonomic powerhouse",
                "views": "3.2M",
                "source": "TikTok"
            },
            {
                "title": "Posture Corrector Brace",
                "category": "Health Accessories",
                "videoUrl": "https://www.tiktok.com/@posture_perfect/video/7234567894",
                "description": "Invisible under clothes, fixes your posture instantly",
                "views": "1.8M",
                "source": "TikTok"
            },
            {
                "title": "Memory Foam Seat Cushion",
                "category": "Comfort Products",
                "videoUrl": "https://www.tiktok.com/@comfort_zone/video/7234567895",
                "description": "Relieves tailbone and lower back pressure while sitting",
                "views": "950K",
                "source": "TikTok"
            }
        ],
        'neck': [
            {
                "title": "Cervical Support Pillow",
                "category": "Sleep Products",
                "videoUrl": "https://www.tiktok.com/@sleep_better/video/7234567896",
                "description": "Orthopedic pillow that aligns your spine perfectly",
                "views": "1.5M",
                "source": "TikTok"
            },
            {
                "title": "Neck Stretching Device",
                "category": "Physical Therapy",
                "videoUrl": "https://www.tiktok.com/@stretch_therapy/video/7234567897",
                "description": "10 minutes a day eliminates neck tension",
                "views": "2.3M",
                "source": "TikTok"
            }
        ],
        'shoulder': [
            {
                "title": "Shoulder Ice Pack Wrap",
                "category": "Pain Relief",
                "videoUrl": "https://www.tiktok.com/@pain_relief_pro/video/7234567898",
                "description": "Hands-free ice therapy that stays in place",
                "views": "1.1M",
                "source": "TikTok"
            },
            {
                "title": "Resistance Band Set",
                "category": "Exercise Equipment",
                "videoUrl": "https://www.tiktok.com/@home_physio/video/7234567899",
                "description": "Strengthen shoulders and prevent future injuries",
                "views": "800K",
                "source": "TikTok"
            }
        ],
        'knee': [
            {
                "title": "Compression Knee Sleeve",
                "category": "Sports Medicine",
                "videoUrl": "https://www.tiktok.com/@active_recovery/video/7234567900",
                "description": "Professional-grade support for daily activities",
                "views": "1.7M",
                "source": "TikTok"
            },
            {
                "title": "Knee Pillow for Side Sleepers",
                "category": "Sleep Aids",
                "videoUrl": "https://www.tiktok.com/@sleep_solutions/video/7234567901",
                "description": "Aligns your hips and reduces knee pressure all night",
                "views": "1.3M",
                "source": "TikTok"
            }
        ],
        'office': [
            {
                "title": "Standing Desk Converter",
                "category": "Office Furniture",
                "videoUrl": "https://www.tiktok.com/@workspace_upgrade/video/7234567902",
                "description": "Transform any desk into a sit-stand workstation",
                "views": "2.8M",
                "source": "TikTok"
            },
            {
                "title": "Ergonomic Mouse Pad with Wrist Rest",
                "category": "Computer Accessories",
                "videoUrl": "https://www.tiktok.com/@ergo_office/video/7234567903",
                "description": "Prevents carpal tunnel and wrist strain",
                "views": "650K",
                "source": "TikTok"
            }
        ],
        'sleep': [
            {
                "title": "Weighted Blanket",
                "category": "Sleep Products",
                "videoUrl": "https://www.tiktok.com/@better_sleep/video/7234567904",
                "description": "Reduces anxiety and improves sleep quality naturally",
                "views": "4.2M",
                "source": "TikTok"
            },
            {
                "title": "White Noise Machine",
                "category": "Sleep Aids",
                "videoUrl": "https://www.tiktok.com/@sleep_sounds/video/7234567905",
                "description": "Block out distractions for deeper sleep",
                "views": "1.9M",
                "source": "TikTok"
            }
        ],
        'general': [
            {
                "title": "Heating Pad with Auto-Shutoff",
                "category": "Pain Relief",
                "videoUrl": "https://www.tiktok.com/@pain_away/video/7234567906",
                "description": "Soothing heat therapy for any body part",
                "views": "1.4M",
                "source": "TikTok"
            },
            {
                "title": "Massage Gun",
                "category": "Recovery Tools",
                "videoUrl": "https://www.tiktok.com/@recovery_guru/video/7234567907",
                "description": "Professional percussion therapy at home",
                "views": "3.5M",
                "source": "TikTok"
            },
            {
                "title": "Epsom Salt Bath Soak",
                "category": "Bath Products",
                "videoUrl": "https://www.tiktok.com/@bath_therapy/video/7234567908",
                "description": "Magnesium-rich formula reduces muscle tension",
                "views": "920K",
                "source": "TikTok"
            }
        ]
    }
    
    matching_products = []
    
    # Find products based on keywords
    for keyword in keywords:
        keyword_lower = keyword.lower()
        
        # Check for direct matches in product categories
        if keyword_lower in product_database:
            products = product_database[keyword_lower]
            # Add 1-2 random products from this category
            selected_products = random.sample(products, min(2, len(products)))
            matching_products.extend(selected_products)
        
        # Check for partial matches
        for category, products in product_database.items():
            if keyword_lower in category or any(keyword_lower in p['title'].lower() or 
                                             keyword_lower in p['description'].lower() 
                                             for p in products):
                if category not in [p.get('matched_category') for p in matching_products]:
                    selected_product = random.choice(products)
                    selected_product['matched_category'] = category
                    matching_products.append(selected_product)
    
    # If no specific matches, add some general products
    if not matching_products:
        matching_products.extend(random.sample(product_database['general'], 2))
    
    # Add problem context and current date to each product
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    for product in matching_products:
        product['problem'] = problem
        product['date'] = current_date
        product['matched_keywords'] = keywords
        
        # Remove temporary fields
        if 'matched_category' in product:
            del product['matched_category']
    
    # Remove duplicates based on title
    seen_titles = set()
    unique_products = []
    for product in matching_products:
        if product['title'] not in seen_titles:
            seen_titles.add(product['title'])
            unique_products.append(product)
    
    # Limit to max 3 products per problem to avoid spam
    return unique_products[:3]


def simulate_tiktok_search(query: str) -> List[Dict]:
    """
    Simulate a direct TikTok search query.
    
    Args:
        query: Search query string
        
    Returns:
        List of simulated TikTok product results
    """
    # This could be extended to use actual TikTok API in the future
    keywords = query.lower().split()
    return find_matching_products(keywords, query)


if __name__ == "__main__":
    # Test the matcher
    test_keywords = ["foot", "pain", "standing", "retail"]
    test_problem = "foot pain from standing all day at retail job"
    
    products = find_matching_products(test_keywords, test_problem)
    print(f"Found {len(products)} matching products:")
    
    for i, product in enumerate(products):
        print(f"\n{i+1}. {product['title']}")
        print(f"   Category: {product['category']}")
        print(f"   Views: {product['views']}")
        print(f"   Description: {product['description']}")
        print(f"   Video: {product['videoUrl']}")