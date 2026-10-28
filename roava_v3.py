import streamlit as st
import re
SYNONYMS = {
    "chill": ["relax", "quiet", "calm"],
    "beach": ["ocean", "sea"],
    "sunset": ["view", "sunset view", "cliff"],
    "luxury": ["premium", "exclusive"],
    "design": ["modern", "boutique", "private"],
} 

st.set_page_config(layout="wide", page_title="Roava")

MOCK_FEED = [
    {
        "id": "a101",
        "title": "Uluwatu Temple",
        "location": "Uluwatu",
        "type": "sight",
        "tags": ["cliff", "sunset", "ocean view", "cultural", "iconic"],
        "image_url": "https://images.unsplash.com/photo-1704253411612-e4deb715dcd8?q=80&w=2670&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        "summary": "exploring mysterious ancient temple at uluwatu with a can't-miss-out sunset view",
        "category": "attraction",
        "best_time": "evening",
        "duration": 2,
        "priority": 3
    },
    
    {
        "id": "a102",
        "title": "Padang Padang Beach",
        "location": "Uluwatu",
        "type": "sight",
        "tags": ["beach", "surf", "cove", "aesthetic", "relax"],
        "image_url": "https://images.unsplash.com/photo-1650621886779-19747038a1f7?q=80&w=2670&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        "summary": "stepping on the sand of uluwatu's well-known beach along with beautiful ocean view",
        "category": "attraction",
        "best_time": "morning",
        "duration": 2,
        "priority": 2
    },
    
    {
        "id": "a103",
        "title": "Karang Boma Cliff",
        "location": "Uluwatu",
        "type": "sight",
        "tags": ["cliff", "viewpoint", "sunset", "photo spot", "dramatic"],
        "image_url": "https://images.unsplash.com/photo-1747873202807-3fced6233f35?q=80&w=2670&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        "summary": "stolling or just lay down on the beach to witness uluwatu's majestic cliff at the ocean edge",
        "category": "attraction",
        "best_time": "evening",
        "duration": 1,
        "priority": 2
    },
    
    {
        "id": "a105",
        "title": "Uluwatu Surf Session",
        "location": "Uluwatu",
        "type": "activity",
        "category": "attraction",
        "tags": ["surf", "ocean", "experience", "activity", "adventure"],
        "image_url": "https://images.unsplash.com/photo-1621951289270-b942dc5f4320?q=80&w=2268&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        "summary": "Catch waves at Uluwatu’s famous surf spots with dramatic cliffside views",
        "best_time": "morning",
        "duration": 2,
        "priority": 2
    },
    
    {
        "id":"a106",
        "title": "Snorkeling at Blue Point",
        "category": "attraction",
        "type": "activity",
        "location": "Uluwatu",
        "summary": "explore clear waters and coral life along the cliffs",
        "tags": ["snorkel", "ocean", "relax"],
        "image_url": "https://media.istockphoto.com/id/2133683684/photo/pov-senior-woman-observing-tropical-fish-underwater-at-coral-reef.jpg?s=1024x1024&w=is&k=20&c=bzmd_5VZMtJca9wRQ4m2U5O6W1_BHFdQ_9zNPmc5phI=",
        "best_time": "morning",
        "duration": 2.5,
        "priority": 8
    },
    
    {
        "id": "a107",
        "title": "Cliffside Spa Treatment",
        "category": "attraction",
        "type": "activity",
        "location": "Uluwatu",
        "summary": "relaxing massage session overlooking the ocean cliffs",
        "tags": ["spa", "relax", "luxury", "wellness"],
        "best_time": "afternoon",
        "duration": 2,
        "priority": 7,
        "image_url": "https://media.istockphoto.com/id/527675071/photo/outdoor-relaxation.jpg?s=1024x1024&w=is&k=20&c=XMKXBvdR9g56QFEKp-M6YYCRH4AhFGeo7w4UndkojbI="
    },
    
    {
        "id": "a108",
        "title": "Suka Espresso",
        "location": "Uluwatu",
        "type": "chill",
        "category": "attraction",
        "tags": ["cafe", "brunch", "coffee", "aesthetic", "relax"],
        "image_url": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?q=80&w=2748&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        "summary": "Take a sip of ice coffee in a locally famous cafe with chill vibe and nice view",
        "best_time": "morning",
        "duration": 1.5,
        "priority": 1
    },
    
    {
        "id": "101",
        "title": "Alila Villas Uluwatu",
        "category": "hotel",
        "location": "Uluwatu",
        "price_level": "high",

        "image_url": "https://lh3.googleusercontent.com/p/AF1QipOXo-aQn7bryJcqSQuZ226zFPwgTTGobHJlik3l=s1360-w1360-h1020",
        "summary": "Iconic cliffside villas with modern design and panoramic ocean views",

        "tags": ["sleek", "cliff", "design", "ocean", "private"],

        "role": "primary",
        "entry_point": True,
        "priority": 1,

        "status": "available"
    },
    
    {
        "id": "102",
        "title": "Anantara Uluwatu Bali Resort",
        "category": "hotel",
        "location": "Uluwatu",
        "price_level": "high",

        "image_url": "https://lh3.googleusercontent.com/p/AF1QipOWiZ-Gb1n4TFh_g0UJSqViox2Gt5X30ESdFIg9=s1360-w1360-h1020",
        "summary": "Oceanfront resort with spacious suites and sunset views in Uluwatu",

        "tags": ["design", "ocean", "resort", "sunset", "comfortable"],

        "role": "primary",
        "entry_point": True,
        "priority": 2,

        "status": "available"
    },
    
    {
        "id": "103",
        "title": "Karma Kandara",
        "category": "hotel",
        "location": "Uluwatu",
        "price_level": "high",

        "image_url": "https://lh3.googleusercontent.com/gps-cs-s/AHVAweqLFtnhJ_MEDlg2SxHQcyCYfDaGAVoOMBwJfnImYxS8LeF6v5zutc0j45bClmotKZ5hbC2qG9iXVZCjxRpR7eBsONyQYRMgteG0v3-EAM30g_Qk9vs33r79wkN_muOIQrKT8Vv0Iw=s1360-w1360-h1020",
        "summary": "Luxury cliffside villas with private beach club and vibrant atmosphere",

        "tags": ["modern", "cliff", "beach", "villa", "social", "pool"],

        "role": "primary",
        "entry_point": True,
        "priority": 3,

        "status": "available"
    },
    
    {
        "id": "104",
        "title": "The Edge Bali",
        "category": "hotel",
        "location": "Uluwatu",
        "price_level": "high",

        "image_url": "https://lh3.googleusercontent.com/p/AF1QipOxrI7mC1oWx0UDABMyG--wAchfRSwqRRAPRroV=s1360-w1360-h1020",
        "summary": "Ultra-luxury cliffside villas with private pools and dramatic views",

        "tags": ["hidden", "cliff", "private", "villa", "exclusive", "spotless"],

        "role": "backup",
        "entry_point": False,
        "priority": 4,

        "status": "available"
    },
     
    {
        "id": "105",
        "title": "Bvlgari Resort Bali",
        "category": "hotel",
        "location": "Uluwatu",
        "price_level": "high",

        "image_url": "https://lh3.googleusercontent.com/p/AF1QipOTW5vru-8uZdd6knGM730tJJxdF9dpoRei5DK3=s1360-w1360-h1020",
        "summary": "High-end luxury resort blending Italian elegance with Balinese design",

        "tags": ["luxury", "design", "exclusive", "cliff", "brand"],

        "role": "backup",
        "entry_point": False,
        "priority": 5,

        "status": "available"
    },
    
    {
        "id": "201",
        "title": "Radisson Blu Bali Uluwatu",
        "category": "hotel",
        "location": "Uluwatu",
        "price_level": "mid",
        "image_url": "https://lh3.googleusercontent.com/p/AF1QipPHDXVOkcgGRdFxOfWuKk-md3qsQ0S0DMghUrT5=s1360-w1360-h1020",
        "summary": "Modern ocean-view resort with clean design and great value",
        "tags": ["ocean", "modern", "resort", "value", "comfortable"],
        "role": "primary",
        "entry_point": True,
        "priority": 1,
        "status": "available"
    },
    
    {
    "id": "202",
    "title": "Renaissance Bali Uluwatu Resort & Spa",
    "category": "hotel",
    "location": "Uluwatu",
    "price_level": "mid",
    "image_url": "https://lh3.googleusercontent.com/gps-cs-s/AHVAweqKuusxgiPCDNK98Mc33QhBs7_ywRBjaCKTzTD53PuDrmrRMWUwHobYw96Fa_q-3MA0WU9DW9DLssOqKX2hqDQLclEuwRzNQLGy0hCqQ0YPk8n4a3-uoR_EzcVT4_p9YCisZ893=s1360-w1360-h1020",
    "summary": "Cliffside resort with pools, sunset vibe, and stylish atmosphere",
    "tags": ["cliff", "sunset", "resort", "luxury", "view"],
    "role": "primary",
    "entry_point": True,
    "priority": 2,
    "status": "available"
    },

{
    "id": "203",
    "title": "La Joya Biu Biu Resort",
    "category": "hotel",
    "location": "Uluwatu",
    "price_level": "mid",
    "image_url": "https://lh3.googleusercontent.com/gps-cs-s/AHVAweptTzdgramYidKp3f-kUu5_bbmW2YICrNqL0HoEv5dT1g345nLOeIU0I1ZTASu90LaEgglvLTQIQD8ZQqV6PKsNAJptOScI5QttzyaiRIN--qj0Eu_4HGnOty20dQxvPxWFis4K=s1360-w1360-h1020",
    "summary": "Unique cliff villas with dramatic sunset views",
    "tags": ["cliff", "sunset", "rustic", "unique", "view"],
    "role": "primary",
    "entry_point": True,
    "priority": 3,
    "status": "available"
},

{
    "id": "301",
    "title": "The Room Padang-Padang",
    "category": "hotel",
    "location": "Uluwatu",
    "price_level": "low",
    "image_url": "https://lh3.googleusercontent.com/p/AF1QipMyOgrlEkB-pDWnU8qDk-YuZcCEJOhbC9TXPotr=s1360-w1360-h1020",
    "summary": "Clean and modern budget stay near Padang Padang beach with a balanced and comfortable vibe",
    "tags": ["clean", "modern", "budget", "central", "pool"],
    "role": "primary",
    "entry_point": True,
    "priority": 1,
    "status": "available"
},
{
    "id": "302",
    "title": "Gravity Boutique Hotel",
    "category": "hotel",
    "location": "Uluwatu",
    "price_level": "low",
    "image_url": "https://images.trvl-media.com/lodging/60000000/59950000/59949300/59949203/91e92e9f.jpg?impolicy=resizecrop&rw=1200&ra=fit",
    "summary": "Chill boutique hotel with relaxed atmosphere, greenery, and a quiet pool setting",
    "tags": ["chill", "quiet", "pool", "relax", "private"],
    "role": "primary",
    "entry_point": True,
    "priority": 2,
    "status": "available"
},

{
    "id": "303",
    "title": "Sal Secret Spot",
    "category": "hotel",
    "location": "Uluwatu",
    "price_level": "low",
    "image_url": "https://lh3.googleusercontent.com/gps-cs-s/AHVAwerLNRDosn0YjQjXxmBOL5MhZAS5tP5yiusGiYIwij960D1qGDkXOdhzKGZF_d9XJiIXILPPKliruYZEFSl2W4_Kg93HZyf4tEKY2u0JA9l_wqN27SKPF-vsl--wenWXaXPl50g=s1360-w1360-h1020",
    "summary": "Hidden cliffside stay with strong sunset views and boutique character",
    "tags": ["hidden", "boutique", "sunset", "cliff", "viewpoint"],
    "role": "primary",
    "entry_point": True,
    "priority": 3,
    "status": "available"
},

{
  "title": "Mason Uluwatu",
  "location": "Uluwatu",
  "price_level": "high",
  "cuisine": "Western / Steakhouse",
  "fit_moment": "main_day",
  "category": "restaurant",
  "image_url": "https://lh3.googleusercontent.com/p/AF1QipOWv3XoQSNXeadTRZA2dethxE7METniocKn5-e5=s1360-w1360-h1020",
  "summary": "modern wood-fire grill serving high-quality steaks in a refined and low-key setting",
  "tags": [
    "steak",
    "grill",
    "premium",
    "date night",
    "refined",
    "low noise"
  ],
  "style_words": [
    "warm lighting",
    "wood fire",
    "serious food",
    "controlled atmosphere"
  ]
},

{
  "title": "Warung Bejana",
  "location": "Uluwatu",
  "price_level": "low",
  "cuisine": "Indonesian",
  "fit_moment": "arrival",
  "category": "restaurant",
  "image_url": "https://lh3.googleusercontent.com/gps-cs-s/AHVAwequlZ2EPhn0SU0NPCjI-m2QtsUpdlvdsKY7Ci1eapt4XrwKSIiQ6IYfnliymL3cUnanfM0ESDHrUuj8IKMxs98qlouxHPloUZJGOg72QOmL5rBwRFbZQKezkyz-TMFfF-1ETGwIIY8hR4-a=s1360-w1360-h1020",
  "summary": "authentic indonesian spot offering simple local flavors in a relaxed, no-frills environment",
  "tags": [
    "local",
    "authentic",
    "casual",
    "low noise",
    "non-touristy"
  ],
  "style_words": [
    "simple",
    "grounded",
    "everyday Bali",
    "no-frills"
  ]
},

{
  "title": "Bartolo Uluwatu",
  "location": "Uluwatu",
  "price_level": "mid",
  "cuisine": "Western / Italian",
  "fit_moment": "arrival, chill_day",
  "category": "restaurant",
  "image_url": "https://lh3.googleusercontent.com/gps-cs-s/AHVAweqc4V5eOcEnYJHCRVxM_2ARLP8yu4O2t89FMFSCWn7hpTSl_e0Ak8KWtPs1iTceJL2dThe_va5ZZKtJsJLUo8IevSf_eDkmtnu_NbrI-0gnx95sZeIesridMNHkqVj3tbBH6Ufl=s1360-w1360-h1020",
  "summary": "cozy western spot perfect for a relaxed dinner with a calm and easy vibe",
  "tags": [
    "chill",
    "casual",
    "western",
    "cozy",
    "low stimulation"
  ],
  "style_words": [
    "soft lighting",
    "relaxed dinner",
    "easy conversation",
    "quiet vibe"
  ]
},

{
  "title": "Tsune",
  "location": "Uluwatu",
  "price_level": "high",
  "cuisine": "Japanese / Omakase",
  "fit_moment": "main_day",
  "category": "restaurant",
  "image_url": "https://lh3.googleusercontent.com/gps-cs-s/AHVAweqJRUYZomj2EhLQ9tFmV2VF5cNzN1QIDV9g4Bgho9TyaZwyaFv_fziFLmhlfy5ETXKXRsZoYHLlkLMZOmVJFWzLO62eRXbXC0LctDQ9cKZGGJKuLkl4wGjuZB9c-rjJ-QQ7jv-1DECiGVKL=s1360-w1360-h1020",
  "summary": "intimate omakase experience focused on precision, quality, and a quiet dining atmosphere",
  "tags": [
    "fine dining",
    "japanese",
    "omakase",
    "quiet",
    "minimal",
    "focused experience"
  ],
  "style_words": [
    "precision",
    "minimalism",
    "chef interaction",
    "slow dining"
  ]
},

{
  "title": "Akasa Restaurant Bali",
  "location": "Uluwatu",
  "price_level": "high",
  "cuisine": "Modern European / Fine Dining",
  "fit_moment": "final_night",
  "category": "restaurant",
  "image_url": "https://lh3.googleusercontent.com/p/AF1QipP2-lFlj5JRSjhgDSkK0z8CoQcyIvlAX0frDtLq=s1360-w1360-h1020",
  "summary": "cliffside dining with ocean views, ideal for a calm and memorable sunset dinner",
  "tags": [
    "fine dining",
    "view",
    "sunset",
    "romantic",
    "spacious",
    "calm"
  ],
  "style_words": [
    "open space",
    "ocean view",
    "slow evening",
    "elevated mood"
  ]
}
]


def get_attractions(feed_items, location):
    return [
        x for x in feed_items
        if x.get("location", "").lower() == location
        and x.get("category") == "attraction"
        and x.get("type", "attraction") in ["attraction", "activity"]
    ]


def get_hotels(feed, location):
    return [
        x for x in feed
        if x.get("category") == "hotel"
        and x.get("location") == location
    ]

HOTEL_CLUSTERS = {
    "uluwatu_high_budget": [
        "Alila Villas Uluwatu",
        "Anantara Uluwatu Bali Resort",
        "Karma Kandara",
        "The Edge Bali",
        "Bulgari Resort Bali"
    ],
     "uluwatu_mid_budget": [
        "Radisson Blu Bali Uluwatu",
        "Renaissance Bali Uluwatu Resort & Spa",
        "La Joya Biu Biu Resort"
    ],
     "uluwatu_low_budget": [
         "The Room Padang-Padang",
         "Gravity Boutique Hotel",
         "Sal Secret Spot"
     ]
}
       
def init_state():
    if "feed_items" not in st.session_state:
        st.session_state.feed_items = MOCK_FEED

    if "itinerary" not in st.session_state:
        st.session_state.itinerary = {"days": []}

    if "trip_preferences" not in st.session_state:
       st.session_state.trip_preferences = {
    "destination": "Uluwatu",
    "days": 3,
    "budget": "high",
    "style": "beach, ocean, sunset"
}
       
      

def score_item(item, style_text, budget):
    style_words = [w for w in re.split(r"[,\s]+", style_text.lower()) if w]
    tags_lower = [t.lower() for t in item["tags"]]
    summary = item["summary"].lower()
    score = 0

    expanded_words = []
    for word in style_words:
        expanded_words.append(word)
        if word in SYNONYMS:
            expanded_words.extend(SYNONYMS[word])

    expanded_words = list(dict.fromkeys(expanded_words))

    for word in expanded_words:
        if word in tags_lower:
            score += 5
        elif word in summary:
            score += 1

    # budget logic: 先轻一点，不要压过style
    if budget == "low":
        if "luxury" in tags_lower or "exclusive" in tags_lower:
            score -= 2

    elif budget == "high":
        if "luxury" in tags_lower or "private" in tags_lower or "exclusive" in tags_lower:
            score += 1

    return score

def pick_hotel(feed_items, budget, style_text, destination):
    hotels = [
        h for h in feed_items
        if h["category"] == "hotel"
        and h["location"] == destination
        and h["price_level"] == budget
    ]

    # primary
    primary = [h for h in hotels if h["role"] == "primary"]

    primary_sorted = sorted(
    primary,
    key=lambda x: (-score_item(x, style_text, budget), x["priority"])
)
    
    

    for h in primary_sorted:
        if h["status"] == "available":
            return h

    # fallback
    backup = [h for h in hotels if h["role"] == "backup"]

    backup_sorted = sorted(
    backup,
    key=lambda x: (-score_item(x, style_text, budget), x["priority"])
)
     
    

    for h in backup_sorted:
        if h["status"] == "available":
            return h

    return None

def pick_attractions(attractions, user_input):
    results = []

    for item in attractions:
        score = 0
        for tag in item.get("tags", []):
            if tag in user_input.lower():
                score += 1

        if score > 0:
            results.append((score, item))

    results.sort(reverse=True, key=lambda x: x[0])

    return [x[1] for x in results[:3]]  # 选前3个

def pick_daily_items(feed_items, budget, style_text, total_days):
    non_hotels = [x for x in feed_items if x["category"] != "hotel"]

    ranked = sorted(
        non_hotels,
        key=lambda x: score_item(x, style_text, budget),
        reverse=True
    )

    if not ranked:
        return [[] for _ in range(total_days)]

    days = [[] for _ in range(total_days)]
    idx = 0

    for item in ranked:
        days[idx % total_days].append(item)
        idx += 1

    return days

def distribute_attractions_simple(attractions, total_days, style_text=""):
    style_words = style_text.lower().split()
    used_ids = set()
    daily_items = []

    for day_index in range(total_days):
        day_plan = []

        # Morning slot
        morning_item = pick_best_item(attractions, "morning", used_ids, style_words)
        if morning_item:
            day_plan.append(morning_item)
            used_ids.add(morning_item["id"])

        # Afternoon slot
        afternoon_item = pick_best_item(attractions, "afternoon", used_ids, style_words)
        if afternoon_item:
            day_plan.append(afternoon_item)
            used_ids.add(afternoon_item["id"])

        daily_items.append(day_plan)

    return daily_items

def get_restaurants(feed_items, location):
    results = []
    for item in feed_items:
        category = (item.get("category") or "").lower()
        item_location = (item.get("location") or item.get("area") or "").lower()

        if category == "restaurant" and location in item_location:
            results.append({
                "title": item.get("title") or item.get("name") or "Untitled Restaurant",
                "category": "restaurant",
                "location": item.get("location") or item.get("area") or location.title(),
                "summary": item.get("summary", ""),
                "image_url": item.get("image_url", ""),
                "tags": item.get("tags", []),
                "price_level": item.get("price_level", ""),
                "cuisine": item.get("cuisine", "")
            })
    return results

def distribute_restaurants_simple(restaurants, total_days):
    daily_restaurants = []

    for i in range(total_days):
        if i < len(restaurants):
            daily_restaurants.append(restaurants[i])
        else:
            daily_restaurants.append(None)

    return daily_restaurants

def get_time_bonus(item, slot):
    best_time = item.get("best_time", "").lower()
    slot = slot.lower()

    if slot == "flexible":
        return 0

    if best_time == slot:
        return 3

    if best_time in ["morning", "afternoon"] and slot in ["morning", "afternoon"]:
        return 1

    return 0

def score_place(item, slot, style_words=None):
    score = item.get("priority", 0)

    tags = [t.lower() for t in item.get("tags", [])]
    title = item.get("title", "").lower()
    item_type = item.get("type", "").lower()

    if style_words:
        for word in style_words:
            w = word.lower()
            if w in tags or w in title:
                score += 2

    score += get_time_bonus(item, slot)

    # Optional: mild slot preference
    if slot == "afternoon" and item_type == "activity":
        score += 1

    return score


def pick_best_item(candidates, slot, used_ids, style_words=None):
    valid = [x for x in candidates if x["id"] not in used_ids]

    if not valid:
        return None

    ranked = sorted(
        valid,
        key=lambda x: score_place(x, slot, style_words),
        reverse=True
    )

    return ranked[0]

def distribute_attractions_smart(attractions, total_days, style_text=""):
    style_words = style_text.lower().split()
    used_ids = set()
    daily_items = []

    for day_index in range(total_days):
        day_plan = []

        # 每天先尽量拿1个最合适的
        morning_item = pick_best_item(attractions, "morning", used_ids, style_words)
        if morning_item:
            day_plan.append(morning_item)
            used_ids.add(morning_item["id"])

        afternoon_item = pick_best_item(attractions, "afternoon", used_ids, style_words)
        if afternoon_item:
            day_plan.append(afternoon_item)
            used_ids.add(afternoon_item["id"])

        # 补位到2个
        while len(day_plan) < 2:
            fallback_item = pick_best_item(attractions, "flexible", used_ids, style_words)
            if not fallback_item:
                break
            day_plan.append(fallback_item)
            used_ids.add(fallback_item["id"])

        daily_items.append(day_plan)

    return daily_items

def build_ai_style_itinerary(feed_items, destination, total_days, budget, style_text):
    location = destination.lower()

    attractions = get_attractions(feed_items, location)
    restaurants = get_restaurants(feed_items, location)

    hotel = pick_hotel(feed_items, budget, style_text, destination)
    daily_items = distribute_attractions_smart(attractions, total_days, style_text)
    daily_restaurants = distribute_restaurants_simple(restaurants, total_days)

    days = []

    for i in range(total_days):
        day_items = []
        today_restaurant = daily_restaurants[i] if i < len(daily_restaurants) else None

        # Day 1: hotel check-in
        if hotel and i == 0:
            day_items.append({
                "time": "Check-in",
                "title": hotel.get("title", "Hotel"),
                "category": hotel.get("category", "hotel"),
                "location": hotel.get("location", destination),
                "notes": f"Recommended stay based on your {budget} budget and {style_text} preferences.",
                "image_url": hotel.get("image_url", ""),
                "tags": hotel.get("tags", [])
            })

        slots = ["morning", "afternoon"]
        today_items = daily_items[i] if i < len(daily_items) else []

        for j, item in enumerate(today_items[:2]):
            day_items.append({
                "time": slots[j] if j < len(slots) else "Flexible",
                "title": item.get("title", "Untitled"),
                "category": item.get("category", "attraction"),
                "location": item.get("location", destination),
                "notes": item.get("summary", ""),
                "image_url": item.get("image_url", ""),
                "tags": item.get("tags", [])
            })

        if today_restaurant:
            day_items.append({
                "time": "Evening",
                "title": today_restaurant.get("title", "Dinner"),
                "category": today_restaurant.get("category", "restaurant"),
                "location": today_restaurant.get("location", destination),
                "notes": today_restaurant.get("summary", ""),
                "image_url": today_restaurant.get("image_url", ""),
                "tags": today_restaurant.get("tags", [])
            })

        days.append({
            "day": i + 1,
            "items": day_items
        })

    return {
        "days": days,
        "hotel": hotel
    }

def apply_agent_edit(itinerary, instruction):
    text = instruction.lower()

    if "relaxed" in text or "slower" in text or "less" in text:
        for day in itinerary["days"]:
            day["items"] = day["items"][:2]

    elif "food" in text or "restaurant" in text:
        if itinerary["days"]:
            itinerary["days"][0]["items"].append({
                "time": "Evening",
                "title": "Extra foodie stop",
                "category": "restaurant",
                "location": "Tokyo",
                "notes": "Added based on your request for more food spots."
            })

    elif "nightlife" in text:
        if itinerary["days"]:
            itinerary["days"][-1]["items"].append({
                "time": "Late night",
                "title": "Late-night bar stop",
                "category": "nightlife",
                "location": "Tokyo",
                "notes": "Added based on your nightlife preference."
            })

    return itinerary

init_state()

left, right = st.columns([2.2, 1.2])

with left:
    st.title("Roava")
    st.caption("Tell Roava what kind of trip you want. It builds the plan for you.")

    destination = st.text_input(
        "Destination",
        value=st.session_state.trip_preferences["destination"]
    )
    st.session_state.trip_preferences["destination"] = destination

    c1, c2, c3 = st.columns(3)
    with c1:
        days = st.slider("Days", 1, 7, st.session_state.trip_preferences["days"])
        st.session_state.trip_preferences["days"] = days
    with c2:
        budget = st.selectbox(
            "Budget",
            ["low", "mid", "high"],
            index=["low", "mid", "high"].index(st.session_state.trip_preferences["budget"])
        )
        st.session_state.trip_preferences["budget"] = budget
    with c3:
        style = st.text_input(
            "Style",
            value=st.session_state.trip_preferences["style"],
            placeholder="foodie, nightlife, design"
        )
        st.session_state.trip_preferences["style"] = style

    if st.button("Generate Full Plan", use_container_width=True):
        st.session_state.itinerary = build_ai_style_itinerary(
            st.session_state.feed_items,
            destination,
            days,
            budget,
            style
        )

    st.markdown("### Explore")
    st.caption("These are inspiration cards. Main flow should be: tell Roava what you want → Roava builds the trip.")

    cards = st.session_state.feed_items
    for i in range(0, len(cards), 2):
        col1, col2 = st.columns(2)

        with col1:
            item = cards[i]
            st.image(item["image_url"], use_container_width=True)
            st.subheader(item["title"])
            st.write(f"**{item['category'].title()}** · {item['location']}")
            st.write(item["summary"])
            st.caption(" · ".join(item["tags"]))

        if i + 1 < len(cards):
            with col2:
                item = cards[i + 1]
                st.image(item["image_url"], use_container_width=True)
                st.subheader(item["title"])
                st.write(f"**{item['category'].title()}** · {item['location']}")
                st.write(item["summary"])
                st.caption(" · ".join(item["tags"]))

with right:
    st.subheader("Current Itinerary")

    if st.session_state.itinerary["days"]:
        for day in st.session_state.itinerary["days"]:
            st.markdown(f"### Day {day['day']}")
            if not day["items"]:
                st.write("No items yet.")
            for stop in day["items"]:
                st.write(f"**{stop['time']} · {stop['title']}**")
                st.caption(stop["notes"])
    else:
        st.info("Generate a plan to see the itinerary.")

    st.markdown("---")

    st.subheader("Refine the Plan")

    prompt = st.text_input(
        "Tell Roava what to change",
        placeholder="Add more beach views / make it more relaxed / more sunset dining"
    )

    if st.button("Update Plan", use_container_width=True):
        st.session_state.itinerary = apply_agent_edit(
            st.session_state.itinerary,
            prompt
        )
               