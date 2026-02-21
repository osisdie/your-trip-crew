"""Seed the database with 17 sample travel packages (with i18n translations)."""

import asyncio

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlmodel import SQLModel

from app.config import settings
from app.models.package import PackageDay, PackageTag, TravelPackage

# Shared tag translation lookup — add new languages as needed
TAG_TRANSLATIONS: dict[str, dict[str, dict[str, str]]] = {
    # Japan locations
    "tokyo": {"zh": {"tag": "東京"}},
    "kyoto": {"zh": {"tag": "京都"}},
    "osaka": {"zh": {"tag": "大阪"}},
    "hokkaido": {"zh": {"tag": "北海道"}},
    "okinawa": {"zh": {"tag": "沖繩"}},
    "fuji": {"zh": {"tag": "富士山"}},
    "hakone": {"zh": {"tag": "箱根"}},
    "niseko": {"zh": {"tag": "二世谷"}},
    "tohoku": {"zh": {"tag": "東北"}},
    # Taiwan locations
    "taipei": {"zh": {"tag": "台北"}},
    "tainan": {"zh": {"tag": "台南"}},
    "taichung": {"zh": {"tag": "台中"}},
    "hualien": {"zh": {"tag": "花蓮"}},
    "taroko": {"zh": {"tag": "太魯閣"}},
    "kenting": {"zh": {"tag": "墾丁"}},
    "beitou": {"zh": {"tag": "北投"}},
    "jiufen": {"zh": {"tag": "九份"}},
    "sun-moon-lake": {"zh": {"tag": "日月潭"}},
    "alishan": {"zh": {"tag": "阿里山"}},
    # Categories / activities
    "urban": {"zh": {"tag": "都市"}},
    "culture": {"zh": {"tag": "文化"}},
    "food": {"zh": {"tag": "美食"}},
    "nightlife": {"zh": {"tag": "夜生活"}},
    "temples": {"zh": {"tag": "寺廟"}},
    "skiing": {"zh": {"tag": "滑雪"}},
    "winter": {"zh": {"tag": "冬季"}},
    "onsen": {"zh": {"tag": "溫泉"}},
    "family": {"zh": {"tag": "親子"}},
    "kids": {"zh": {"tag": "兒童"}},
    "theme-parks": {"zh": {"tag": "主題樂園"}},
    "theme-park": {"zh": {"tag": "主題樂園"}},
    "nature": {"zh": {"tag": "自然"}},
    "hiking": {"zh": {"tag": "健行"}},
    "beach": {"zh": {"tag": "海灘"}},
    "snorkeling": {"zh": {"tag": "浮潛"}},
    "relaxation": {"zh": {"tag": "放鬆"}},
    "islands": {"zh": {"tag": "離島"}},
    "adventure": {"zh": {"tag": "冒險"}},
    "cycling": {"zh": {"tag": "自行車"}},
    "ramen": {"zh": {"tag": "拉麵"}},
    "sushi": {"zh": {"tag": "壽司"}},
    "cooking": {"zh": {"tag": "烹飪"}},
    "night-market": {"zh": {"tag": "夜市"}},
    "railway": {"zh": {"tag": "鐵路"}},
    "round-island": {"zh": {"tag": "環島"}},
    "mountains": {"zh": {"tag": "山岳"}},
    "history": {"zh": {"tag": "歷史"}},
    "tropical": {"zh": {"tag": "熱帶"}},
    "tea": {"zh": {"tag": "茶"}},
    "hot-springs": {"zh": {"tag": "溫泉"}},
    "taiwan": {"zh": {"tag": "台灣"}},
}

PACKAGES = [
    # ─── Japan ──────────────────────────────────────
    {
        "title": "Tokyo Explorer: 5-Day Urban Adventure",
        "slug": "tokyo-explorer-5day",
        "destination": "Japan",
        "category": "Urban",
        "summary": "Discover Tokyo's iconic neighborhoods from Shibuya to Asakusa with guided tours, street food, and nightlife.",
        "description": "This 5-day Tokyo package takes you through the heart of Japan's capital. Start with the famous Tsukiji Outer Market, explore Harajuku's fashion scene, visit ancient Senso-ji temple, experience Akihabara's electric town, and end with panoramic views from Tokyo Skytree. Includes JR Pass and metro card.",
        "duration_days": 5,
        "price_usd": 1200,
        "cover_image_url": "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=600&h=400&fit=crop",
        "highlights": [
            "Tsukiji Market food tour",
            "Harajuku & Shibuya crossing",
            "Senso-ji Temple",
            "Tokyo Skytree sunset",
            "Robot Restaurant experience",
        ],
        "translations": {
            "zh": {
                "title": "東京探索：5日都市冒險",
                "summary": "從澀谷到淺草，導覽東京最經典的街區，品嚐街頭美食，體驗繽紛夜生活。",
                "description": "這個5天東京套餐帶您深入日本首都的心臟地帶。從知名的築地場外市場開始，探索原宿的時尚文化，參拜古老的淺草寺，體驗秋葉原的電器街，最後在東京晴空塔享受全景美景。包含JR Pass和地鐵卡。",
                "highlights": [
                    "築地市場美食之旅",
                    "原宿和澀谷十字路口",
                    "淺草寺",
                    "東京晴空塔夕陽",
                    "機器人餐廳體驗",
                ],
            }
        },
        "tags": ["tokyo", "urban", "food", "culture", "nightlife"],
        "days": [
            {
                "day_number": 1,
                "title": "Arrival & Shinjuku",
                "description": "Arrive at Narita/Haneda, check into hotel. Evening walk through Shinjuku's neon streets and Golden Gai.",
                "activities": [
                    {"time": "14:00", "name": "Airport transfer"},
                    {"time": "18:00", "name": "Shinjuku exploration"},
                    {"time": "20:00", "name": "Golden Gai bar hopping"},
                ],
                "translations": {
                    "zh": {
                        "title": "抵達 & 新宿",
                        "description": "抵達成田/羽田機場，入住酒店。傍晚漫步新宿霓虹街道和黃金街。",
                    }
                },
            },
            {
                "day_number": 2,
                "title": "Tsukiji & Ginza",
                "description": "Morning at Tsukiji Outer Market for sushi breakfast, afternoon in upscale Ginza, evening at teamLab Borderless.",
                "activities": [
                    {"time": "07:00", "name": "Tsukiji Market tour"},
                    {"time": "13:00", "name": "Ginza shopping"},
                    {"time": "17:00", "name": "teamLab Borderless"},
                ],
                "translations": {
                    "zh": {
                        "title": "築地 & 銀座",
                        "description": "早晨在築地場外市場享用壽司早餐，下午逛高檔銀座，晚間參觀 teamLab Borderless。",
                    }
                },
            },
            {
                "day_number": 3,
                "title": "Asakusa & Akihabara",
                "description": "Visit Senso-ji temple, explore Nakamise-dori, afternoon in Akihabara's anime & electronics district.",
                "activities": [
                    {"time": "09:00", "name": "Senso-ji Temple"},
                    {"time": "12:00", "name": "Lunch at Asakusa"},
                    {"time": "14:00", "name": "Akihabara tour"},
                ],
                "translations": {
                    "zh": {
                        "title": "淺草 & 秋葉原",
                        "description": "參拜淺草寺，逛仲見世通，下午前往秋葉原動漫電器街。",
                    }
                },
            },
            {
                "day_number": 4,
                "title": "Harajuku & Shibuya",
                "description": "Meiji Shrine, Takeshita Street, Shibuya Crossing, and Shibuya Sky observation deck.",
                "activities": [
                    {"time": "09:00", "name": "Meiji Shrine"},
                    {"time": "11:00", "name": "Harajuku & Takeshita St"},
                    {"time": "15:00", "name": "Shibuya Sky"},
                ],
                "translations": {
                    "zh": {
                        "title": "原宿 & 澀谷",
                        "description": "明治神宮、竹下通、澀谷十字路口和 Shibuya Sky 觀景台。",
                    }
                },
            },
            {
                "day_number": 5,
                "title": "Skytree & Departure",
                "description": "Morning at Tokyo Skytree, souvenir shopping, airport transfer.",
                "activities": [
                    {"time": "09:00", "name": "Tokyo Skytree"},
                    {"time": "12:00", "name": "Last shopping"},
                    {"time": "15:00", "name": "Airport transfer"},
                ],
                "translations": {
                    "zh": {
                        "title": "晴空塔 & 離開",
                        "description": "上午參觀東京晴空塔，購買紀念品，前往機場。",
                    }
                },
            },
        ],
    },
    {
        "title": "Kyoto & Osaka Cultural Journey",
        "slug": "kyoto-osaka-cultural-7day",
        "destination": "Japan",
        "category": "Culture",
        "summary": "7 days exploring ancient temples, tea ceremonies, geisha districts, and Osaka's legendary street food.",
        "description": "Immerse yourself in Japan's cultural heartland. Walk through thousands of vermilion torii gates at Fushimi Inari, participate in a traditional tea ceremony, explore the bamboo groves of Arashiyama, and devour Osaka's finest takoyaki and okonomiyaki. This package includes a private geisha district walking tour.",
        "duration_days": 7,
        "price_usd": 2100,
        "cover_image_url": "https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?w=600&h=400&fit=crop",
        "highlights": [
            "Fushimi Inari Shrine",
            "Tea ceremony experience",
            "Arashiyama Bamboo Grove",
            "Gion geisha district",
            "Osaka street food tour",
        ],
        "translations": {
            "zh": {
                "title": "京都 & 大阪文化之旅",
                "summary": "7天探索古老寺廟、茶道體驗、藝妓街區和大阪傳奇街頭美食。",
                "description": "沉浸在日本的文化心臟地帶。穿越伏見稻荷數千座朱紅色鳥居，參加傳統茶道，探索嵐山竹林，品嚐大阪最正宗的章魚燒和大阪燒。此套餐包含私人藝妓街區導覽。",
                "highlights": [
                    "伏見稻荷大社",
                    "茶道體驗",
                    "嵐山竹林",
                    "祇園藝妓街區",
                    "大阪街頭美食之旅",
                ],
            }
        },
        "tags": ["kyoto", "osaka", "culture", "temples", "food"],
        "days": [
            {
                "day_number": 1,
                "title": "Arrival in Kyoto",
                "description": "Arrive via Shinkansen, check in at traditional ryokan, evening stroll through Gion.",
                "activities": [],
                "translations": {
                    "zh": {
                        "title": "抵達京都",
                        "description": "搭乘新幹線抵達，入住傳統旅館，傍晚漫步祇園。",
                    }
                },
            },
            {
                "day_number": 2,
                "title": "Eastern Kyoto Temples",
                "description": "Kiyomizu-dera, Philosopher's Path, Ginkaku-ji.",
                "activities": [],
                "translations": {"zh": {"title": "東京都寺廟", "description": "清水寺、哲學之道、銀閣寺。"}},
            },
            {
                "day_number": 3,
                "title": "Fushimi Inari & Tea",
                "description": "Morning hike through torii gates, afternoon tea ceremony.",
                "activities": [],
                "translations": {
                    "zh": {
                        "title": "伏見稻荷 & 茶道",
                        "description": "上午穿越鳥居健行，下午體驗茶道。",
                    }
                },
            },
            {
                "day_number": 4,
                "title": "Arashiyama",
                "description": "Bamboo grove, Togetsukyo Bridge, monkey park.",
                "activities": [],
                "translations": {"zh": {"title": "嵐山", "description": "竹林、渡月橋、猴子公園。"}},
            },
            {
                "day_number": 5,
                "title": "Day Trip to Nara",
                "description": "Todai-ji, friendly deer park, Kasuga Grand Shrine.",
                "activities": [],
                "translations": {"zh": {"title": "奈良一日遊", "description": "東大寺、可愛的鹿公園、春日大社。"}},
            },
            {
                "day_number": 6,
                "title": "Osaka Food Adventure",
                "description": "Dotonbori, Kuromon Market, street food crawl.",
                "activities": [],
                "translations": {
                    "zh": {
                        "title": "大阪美食探險",
                        "description": "道頓堀、黑門市場、街頭美食巡禮。",
                    }
                },
            },
            {
                "day_number": 7,
                "title": "Osaka Castle & Departure",
                "description": "Morning at Osaka Castle, departure.",
                "activities": [],
                "translations": {"zh": {"title": "大阪城 & 離開", "description": "上午參觀大阪城，啟程離開。"}},
            },
        ],
    },
    {
        "title": "Hokkaido Winter Ski Paradise",
        "slug": "hokkaido-ski-6day",
        "destination": "Japan",
        "category": "Skiing",
        "summary": "6 days of world-class powder skiing in Niseko and Furano with hot spring relaxation.",
        "description": "Experience Japan's legendary powder snow. Ski Niseko's four interconnected resorts, try night skiing under the stars, relax in natural onsen, and savor fresh Hokkaido seafood. Suitable for all skill levels with English-speaking instructors available.",
        "duration_days": 6,
        "price_usd": 2800,
        "cover_image_url": "https://images.unsplash.com/photo-1551524559-8af4e6624178?w=600&h=400&fit=crop",
        "highlights": [
            "Niseko powder skiing",
            "Night skiing experience",
            "Onsen hot springs",
            "Hokkaido seafood",
            "Furano day trip",
        ],
        "translations": {
            "zh": {
                "title": "北海道冬季滑雪天堂",
                "summary": "6天世界級粉雪滑雪，盡享二世谷和富良野，搭配溫泉放鬆。",
                "description": "體驗日本傳奇粉雪。在二世谷四大互通滑雪場馳騁，星空下夜間滑雪，天然溫泉放鬆身心，品嚐新鮮北海道海鮮。適合各種程度，提供英語教練。",
                "highlights": [
                    "二世谷粉雪滑雪",
                    "夜間滑雪體驗",
                    "溫泉泡湯",
                    "北海道海鮮",
                    "富良野一日遊",
                ],
            }
        },
        "tags": ["hokkaido", "skiing", "winter", "onsen", "niseko"],
        "days": [
            {
                "day_number": 1,
                "title": "Arrival at New Chitose",
                "description": "Fly into Sapporo, transfer to Niseko, settle into ski lodge.",
                "activities": [],
                "translations": {
                    "zh": {
                        "title": "抵達新千歲機場",
                        "description": "飛抵札幌，轉乘前往二世谷，入住滑雪小屋。",
                    }
                },
            },
            {
                "day_number": 2,
                "title": "Niseko Grand Hirafu",
                "description": "Full day skiing at Grand Hirafu, evening onsen.",
                "activities": [],
                "translations": {
                    "zh": {
                        "title": "二世谷比羅夫",
                        "description": "全天在比羅夫滑雪場滑雪，晚間泡溫泉。",
                    }
                },
            },
            {
                "day_number": 3,
                "title": "Niseko Village & Annupuri",
                "description": "Explore different Niseko resorts, night skiing.",
                "activities": [],
                "translations": {
                    "zh": {
                        "title": "二世谷村 & 安努普利",
                        "description": "探索不同的二世谷滑雪場，體驗夜間滑雪。",
                    }
                },
            },
            {
                "day_number": 4,
                "title": "Furano Day Trip",
                "description": "Ski Furano's excellent terrain, visit cheese factory.",
                "activities": [],
                "translations": {
                    "zh": {
                        "title": "富良野一日遊",
                        "description": "在富良野優質雪道滑雪，參觀起司工廠。",
                    }
                },
            },
            {
                "day_number": 5,
                "title": "Free Ski Day",
                "description": "Choose your favorite resort, afternoon spa.",
                "activities": [],
                "translations": {"zh": {"title": "自由滑雪日", "description": "選擇喜愛的滑雪場，下午享受 SPA。"}},
            },
            {
                "day_number": 6,
                "title": "Departure",
                "description": "Morning dip in onsen, transfer to airport.",
                "activities": [],
                "translations": {"zh": {"title": "離開", "description": "早晨最後泡一次溫泉，前往機場。"}},
            },
        ],
    },
    {
        "title": "Japan Family Fun: Kid-Friendly 6 Days",
        "slug": "japan-family-6day",
        "destination": "Japan",
        "category": "Family",
        "summary": "A family-friendly Tokyo & Osaka trip with theme parks, interactive museums, and kid-approved food.",
        "description": "Designed for families with children ages 3-12. Visit Tokyo DisneySea, explore the Ghibli Museum, race go-karts in Tokyo, enjoy Osaka's Universal Studios, and discover kid-friendly ramen shops. All hotels have family rooms, and itinerary pacing is kid-friendly.",
        "duration_days": 6,
        "price_usd": 3200,
        "cover_image_url": "https://images.unsplash.com/photo-1524413840807-0c3cb6fa808d?w=600&h=400&fit=crop",
        "highlights": [
            "Tokyo DisneySea",
            "Ghibli Museum",
            "Universal Studios Japan",
            "Kid-friendly food tours",
            "Pokemon Center visit",
        ],
        "translations": {
            "zh": {
                "title": "日本親子遊：6天歡樂之旅",
                "summary": "適合全家的東京大阪之旅，主題樂園、互動博物館和孩子最愛的美食。",
                "description": "專為3-12歲兒童家庭設計。參觀東京迪士尼海洋、探索吉卜力美術館、東京卡丁車體驗、大阪環球影城，以及發現兒童友善拉麵店。所有飯店皆有家庭房，行程節奏適合兒童。",
                "highlights": [
                    "東京迪士尼海洋",
                    "吉卜力美術館",
                    "日本環球影城",
                    "兒童美食之旅",
                    "寶可夢中心",
                ],
            }
        },
        "tags": ["family", "kids", "theme-parks", "tokyo", "osaka"],
        "days": [
            {
                "day_number": 1,
                "title": "Tokyo Arrival",
                "description": "Arrive and settle in, explore Odaiba.",
                "activities": [],
                "translations": {"zh": {"title": "抵達東京", "description": "抵達並入住，探索台場。"}},
            },
            {
                "day_number": 2,
                "title": "Tokyo DisneySea",
                "description": "Full day at DisneySea.",
                "activities": [],
                "translations": {"zh": {"title": "東京迪士尼海洋", "description": "全天暢遊迪士尼海洋。"}},
            },
            {
                "day_number": 3,
                "title": "Ghibli & Shibuya",
                "description": "Ghibli Museum, Pokemon Center, Shibuya.",
                "activities": [],
                "translations": {
                    "zh": {
                        "title": "吉卜力 & 澀谷",
                        "description": "吉卜力美術館、寶可夢中心、澀谷。",
                    }
                },
            },
            {
                "day_number": 4,
                "title": "Shinkansen to Osaka",
                "description": "Bullet train experience, arrive Osaka, Dotonbori.",
                "activities": [],
                "translations": {
                    "zh": {
                        "title": "新幹線前往大阪",
                        "description": "體驗子彈列車，抵達大阪，逛道頓堀。",
                    }
                },
            },
            {
                "day_number": 5,
                "title": "Universal Studios",
                "description": "Full day at USJ, Super Nintendo World.",
                "activities": [],
                "translations": {
                    "zh": {
                        "title": "環球影城",
                        "description": "全天暢遊日本環球影城，超級任天堂世界。",
                    }
                },
            },
            {
                "day_number": 6,
                "title": "Departure",
                "description": "Morning shopping, departure.",
                "activities": [],
                "translations": {"zh": {"title": "離開", "description": "上午購物，啟程離開。"}},
            },
        ],
    },
    {
        "title": "Mt. Fuji & Hakone Nature Retreat",
        "slug": "fuji-hakone-nature-4day",
        "destination": "Japan",
        "category": "Nature",
        "summary": "4-day nature escape with Mt. Fuji views, Hakone hot springs, and Lake Ashi cruises.",
        "description": "Escape Tokyo for stunning natural scenery. Take the romance car to Hakone, cruise Lake Ashi with views of Mt. Fuji, ride the Hakone Ropeway, and soak in world-class onsen. Visit the Fuji Five Lakes region for photography and hiking.",
        "duration_days": 4,
        "price_usd": 950,
        "highlights": [
            "Mt. Fuji views",
            "Lake Ashi cruise",
            "Hakone Ropeway",
            "Traditional ryokan stay",
            "Onsen experience",
        ],
        "translations": {
            "zh": {
                "title": "富士山 & 箱根自然之旅",
                "summary": "4天自然逃離之旅，飽覽富士山美景、箱根溫泉和蘆之湖遊船。",
                "description": "逃離東京，享受壯麗自然風光。搭乘浪漫號前往箱根，乘船遊蘆之湖欣賞富士山，搭乘箱根空中纜車，浸泡世界級溫泉。造訪富士五湖地區攝影和健行。",
                "highlights": [
                    "富士山美景",
                    "蘆之湖遊船",
                    "箱根空中纜車",
                    "傳統旅館住宿",
                    "溫泉體驗",
                ],
            }
        },
        "tags": ["nature", "fuji", "hakone", "onsen", "hiking"],
        "days": [
            {
                "day_number": 1,
                "title": "Tokyo to Hakone",
                "description": "Romance Car to Hakone, check into ryokan.",
                "activities": [],
                "translations": {"zh": {"title": "東京到箱根", "description": "搭乘浪漫號前往箱根，入住旅館。"}},
            },
            {
                "day_number": 2,
                "title": "Hakone Loop",
                "description": "Ropeway, Owakudani, Lake Ashi pirate ship cruise.",
                "activities": [],
                "translations": {
                    "zh": {
                        "title": "箱根環線",
                        "description": "空中纜車、大涌谷、蘆之湖海賊船遊船。",
                    }
                },
            },
            {
                "day_number": 3,
                "title": "Fuji Five Lakes",
                "description": "Drive to Kawaguchiko, Chureito Pagoda, lakeside walk.",
                "activities": [],
                "translations": {
                    "zh": {
                        "title": "富士五湖",
                        "description": "驅車前往河口湖，新倉山淺間公園忠靈塔，湖畔散步。",
                    }
                },
            },
            {
                "day_number": 4,
                "title": "Return to Tokyo",
                "description": "Morning onsen, return.",
                "activities": [],
                "translations": {"zh": {"title": "返回東京", "description": "早晨泡溫泉，返回東京。"}},
            },
        ],
    },
    {
        "title": "Okinawa Beach & Island Hopping",
        "slug": "okinawa-beach-5day",
        "destination": "Japan",
        "category": "Relaxation",
        "summary": "5 days of tropical beaches, snorkeling, and Ryukyu culture in Okinawa's islands.",
        "description": "Discover Japan's tropical paradise. Snorkel in crystal-clear waters, explore Shuri Castle, island-hop to Kerama Islands, enjoy Okinawan cuisine, and relax on white sand beaches.",
        "duration_days": 5,
        "price_usd": 1600,
        "highlights": [
            "Kerama Islands snorkeling",
            "Shuri Castle",
            "Okinawan food",
            "Beach relaxation",
            "Glass-bottom boat",
        ],
        "translations": {
            "zh": {
                "title": "沖繩海灘跳島之旅",
                "summary": "5天熱帶海灘、浮潛和琉球文化之旅，暢遊沖繩群島。",
                "description": "探索日本的熱帶天堂。在清澈海水中浮潛，參觀首里城，跳島遊慶良間群島，品嚐沖繩料理，在白沙海灘上放鬆。",
                "highlights": ["慶良間群島浮潛", "首里城", "沖繩美食", "海灘放鬆", "玻璃底船"],
            }
        },
        "tags": ["okinawa", "beach", "snorkeling", "relaxation", "islands"],
        "days": [
            {
                "day_number": 1,
                "title": "Naha Arrival",
                "description": "Arrive in Naha, Kokusai Street, Okinawan dinner.",
                "activities": [],
                "translations": {"zh": {"title": "抵達那霸", "description": "抵達那霸，逛國際通，享用沖繩晚餐。"}},
            },
            {
                "day_number": 2,
                "title": "Shuri Castle & South",
                "description": "Shuri Castle, Peace Memorial Park.",
                "activities": [],
                "translations": {"zh": {"title": "首里城 & 南部", "description": "首里城、和平紀念公園。"}},
            },
            {
                "day_number": 3,
                "title": "Kerama Islands",
                "description": "Day trip to Zamami, snorkeling, beach.",
                "activities": [],
                "translations": {"zh": {"title": "慶良間群島", "description": "座間味島一日遊，浮潛，海灘。"}},
            },
            {
                "day_number": 4,
                "title": "Northern Okinawa",
                "description": "Churaumi Aquarium, Emerald Beach.",
                "activities": [],
                "translations": {"zh": {"title": "沖繩北部", "description": "美麗海水族館、翡翠海灘。"}},
            },
            {
                "day_number": 5,
                "title": "Departure",
                "description": "Morning beach time, departure.",
                "activities": [],
                "translations": {"zh": {"title": "離開", "description": "上午海灘時光，啟程離開。"}},
            },
        ],
    },
    {
        "title": "Japanese Food Odyssey: Tokyo to Osaka",
        "slug": "japan-food-odyssey-7day",
        "destination": "Japan",
        "category": "Food & Drink",
        "summary": "7-day culinary journey from Tokyo's Michelin stars to Osaka's street food heaven.",
        "description": "A food lover's dream through Japan. Sushi at Tsukiji, ramen in Tokyo's best shops, Wagyu in Kobe, street food in Osaka's Dotonbori, sake tasting in Fushimi, and a cooking class making authentic Japanese dishes.",
        "duration_days": 7,
        "price_usd": 2500,
        "highlights": [
            "Tsukiji sushi breakfast",
            "Ramen tour",
            "Kobe beef experience",
            "Osaka street food",
            "Sake tasting & cooking class",
        ],
        "translations": {
            "zh": {
                "title": "日本美食之旅：東京到大阪",
                "summary": "7天美食之旅，從東京米其林星級餐廳到大阪街頭美食天堂。",
                "description": "美食愛好者的夢想之旅。築地壽司、東京最佳拉麵店、神戶和牛、大阪道頓堀街頭美食、伏見清酒品嚐，以及正宗日本料理烹飪課程。",
                "highlights": [
                    "築地壽司早餐",
                    "拉麵巡禮",
                    "神戶牛肉體驗",
                    "大阪街頭美食",
                    "清酒品嚐 & 料理教室",
                ],
            }
        },
        "tags": ["food", "ramen", "sushi", "osaka", "cooking"],
        "days": [
            {
                "day_number": 1,
                "title": "Tokyo Sushi & Ramen",
                "description": "Tsukiji sushi, evening ramen crawl.",
                "activities": [],
                "translations": {"zh": {"title": "東京壽司 & 拉麵", "description": "築地壽司，晚間拉麵巡禮。"}},
            },
            {
                "day_number": 2,
                "title": "Depachika & Izakaya",
                "description": "Department store food halls, izakaya night.",
                "activities": [],
                "translations": {
                    "zh": {
                        "title": "百貨地下街 & 居酒屋",
                        "description": "百貨公司美食街，居酒屋之夜。",
                    }
                },
            },
            {
                "day_number": 3,
                "title": "Cooking Class",
                "description": "Japanese cooking workshop, Yanaka street food.",
                "activities": [],
                "translations": {"zh": {"title": "料理教室", "description": "日本料理烹飪課程，谷中街頭美食。"}},
            },
            {
                "day_number": 4,
                "title": "Shinkansen to Kyoto",
                "description": "Ekiben on bullet train, Nishiki Market.",
                "activities": [],
                "translations": {
                    "zh": {
                        "title": "新幹線前往京都",
                        "description": "新幹線上享用鐵路便當，錦市場。",
                    }
                },
            },
            {
                "day_number": 5,
                "title": "Kyoto & Sake",
                "description": "Tofu cuisine, Fushimi sake district.",
                "activities": [],
                "translations": {"zh": {"title": "京都 & 清酒", "description": "豆腐料理，伏見清酒釀造區。"}},
            },
            {
                "day_number": 6,
                "title": "Kobe Beef Day",
                "description": "Kobe beef teppanyaki, Chinatown.",
                "activities": [],
                "translations": {"zh": {"title": "神戶牛肉日", "description": "神戶牛鐵板燒，南京町中華街。"}},
            },
            {
                "day_number": 7,
                "title": "Osaka Grand Finale",
                "description": "Kuromon Market, Dotonbori feast, departure.",
                "activities": [],
                "translations": {"zh": {"title": "大阪壓軸", "description": "黑門市場、道頓堀盛宴，啟程離開。"}},
            },
        ],
    },
    {
        "title": "Tohoku Adventure: Hidden Japan",
        "slug": "tohoku-adventure-5day",
        "destination": "Japan",
        "category": "Adventure",
        "summary": "5 days exploring Japan's wild northeast: ancient forests, volcanic hot springs, and samurai history.",
        "description": "Venture off the beaten path into Tohoku. Hike through Shirakami Sanchi's ancient beech forests, visit the mystical Zao fox village, soak in Ginzan Onsen's atmospheric hot springs, and explore Kakunodate's samurai district.",
        "duration_days": 5,
        "price_usd": 1400,
        "highlights": [
            "Shirakami Sanchi forest",
            "Zao Fox Village",
            "Ginzan Onsen",
            "Kakunodate samurai town",
            "Matsushima Bay cruise",
        ],
        "translations": {
            "zh": {
                "title": "東北冒險：秘境日本",
                "summary": "5天探索日本東北秘境：古老森林、火山溫泉和武士歷史。",
                "description": "深入日本東北秘境。穿越白神山地古老的山毛櫸森林，造訪神秘的藏王狐狸村，浸泡銀山溫泉的氛圍感溫泉，探索角館武家屋敷。",
                "highlights": [
                    "白神山地森林",
                    "藏王狐狸村",
                    "銀山溫泉",
                    "角館武士城鎮",
                    "松島灣遊船",
                ],
            }
        },
        "tags": ["tohoku", "adventure", "nature", "onsen", "hiking"],
        "days": [
            {
                "day_number": 1,
                "title": "Sendai & Matsushima",
                "description": "Shinkansen to Sendai, Matsushima Bay.",
                "activities": [],
                "translations": {"zh": {"title": "仙台 & 松島", "description": "搭乘新幹線前往仙台，松島灣。"}},
            },
            {
                "day_number": 2,
                "title": "Zao & Fox Village",
                "description": "Zao onsen area, fox village.",
                "activities": [],
                "translations": {"zh": {"title": "藏王 & 狐狸村", "description": "藏王溫泉區，狐狸村。"}},
            },
            {
                "day_number": 3,
                "title": "Ginzan Onsen",
                "description": "Travel to Ginzan Onsen, evening stroll.",
                "activities": [],
                "translations": {"zh": {"title": "銀山溫泉", "description": "前往銀山溫泉，傍晚散步。"}},
            },
            {
                "day_number": 4,
                "title": "Kakunodate",
                "description": "Samurai district, cherry bark crafts.",
                "activities": [],
                "translations": {"zh": {"title": "角館", "description": "武家屋敷街區，櫻皮工藝。"}},
            },
            {
                "day_number": 5,
                "title": "Return",
                "description": "Morning hike, return to Tokyo.",
                "activities": [],
                "translations": {"zh": {"title": "返回", "description": "上午健行，返回東京。"}},
            },
        ],
    },
    # ─── Taiwan ─────────────────────────────────────
    {
        "title": "Taipei City Break: 4 Days",
        "slug": "taipei-city-break-4day",
        "destination": "Taiwan",
        "category": "Urban",
        "summary": "4 days in Taipei with night markets, temples, Taipei 101, and amazing street food.",
        "description": "Experience Taipei's incredible energy. Visit the iconic Taipei 101, explore Longshan Temple, wander through Jiufen's atmospheric alleyways, indulge at Shilin Night Market, and hike Elephant Mountain for city views. Includes MRT pass.",
        "duration_days": 4,
        "price_usd": 650,
        "cover_image_url": "https://images.unsplash.com/photo-1470004914212-05527e49370b?w=600&h=400&fit=crop",
        "highlights": [
            "Taipei 101 observation deck",
            "Shilin Night Market",
            "Jiufen Old Street",
            "Longshan Temple",
            "Elephant Mountain hike",
        ],
        "translations": {
            "zh": {
                "title": "台北城市輕旅行：4天",
                "summary": "4天台北之旅，夜市、寺廟、台北101和令人驚艷的街頭美食。",
                "description": "體驗台北不可思議的活力。參觀地標台北101，探索龍山寺，漫步九份氛圍感小巷，大啖士林夜市美食，登象山欣賞城市全景。包含捷運卡。",
                "highlights": ["台北101觀景台", "士林夜市", "九份老街", "龍山寺", "象山步道"],
            }
        },
        "tags": ["taipei", "urban", "night-market", "food", "temples"],
        "days": [
            {
                "day_number": 1,
                "title": "Taipei Arrival",
                "description": "Arrive at Taoyuan Airport, MRT to hotel, evening at Shilin Night Market.",
                "activities": [],
                "translations": {
                    "zh": {
                        "title": "抵達台北",
                        "description": "抵達桃園機場，搭捷運到飯店，晚間逛士林夜市。",
                    }
                },
            },
            {
                "day_number": 2,
                "title": "Central Taipei",
                "description": "Taipei 101, Xinyi district, Longshan Temple, Bopiliao Historic Block.",
                "activities": [],
                "translations": {
                    "zh": {
                        "title": "台北市中心",
                        "description": "台北101、信義區、龍山寺、剝皮寮歷史街區。",
                    }
                },
            },
            {
                "day_number": 3,
                "title": "Jiufen Day Trip",
                "description": "Train to Jiufen, explore old street, Shifen waterfalls.",
                "activities": [],
                "translations": {"zh": {"title": "九份一日遊", "description": "搭火車到九份，逛老街，十分瀑布。"}},
            },
            {
                "day_number": 4,
                "title": "Elephant Mountain & Departure",
                "description": "Sunrise hike at Elephant Mountain, departure.",
                "activities": [],
                "translations": {"zh": {"title": "象山 & 離開", "description": "象山日出健行，啟程離開。"}},
            },
        ],
    },
    {
        "title": "Taiwan Round-Island Railway",
        "slug": "taiwan-round-island-8day",
        "destination": "Taiwan",
        "category": "Adventure",
        "summary": "8-day rail journey around Taiwan: Taipei, Hualien, Taitung, Kenting, Tainan, Sun Moon Lake.",
        "description": "Circle the entire island by train. Start in Taipei, take the scenic railway to Hualien for Taroko Gorge, continue to Taitung's hot air balloon festival area, south to tropical Kenting, historic Tainan, and magical Sun Moon Lake before returning to Taipei.",
        "duration_days": 8,
        "price_usd": 1800,
        "highlights": [
            "Taroko Gorge",
            "Kenting beaches",
            "Sun Moon Lake",
            "Tainan temples",
            "East coast scenery",
        ],
        "translations": {
            "zh": {
                "title": "台灣環島鐵路之旅",
                "summary": "8天鐵路環島：台北、花蓮、台東、墾丁、台南、日月潭。",
                "description": "搭火車環遊全島。從台北出發，搭乘景觀鐵路到花蓮遊太魯閣，繼續前往台東熱氣球地區，南下熱帶墾丁、歷史古都台南，以及夢幻日月潭，最後返回台北。",
                "highlights": ["太魯閣峽谷", "墾丁海灘", "日月潭", "台南寺廟", "東海岸風光"],
            }
        },
        "tags": ["taiwan", "railway", "adventure", "nature", "round-island"],
        "days": [
            {
                "day_number": 1,
                "title": "Taipei Start",
                "description": "Taipei exploration, prepare for journey.",
                "activities": [],
                "translations": {"zh": {"title": "台北出發", "description": "台北市區探索，準備旅程。"}},
            },
            {
                "day_number": 2,
                "title": "Hualien & Taroko",
                "description": "Train to Hualien, Taroko Gorge.",
                "activities": [],
                "translations": {"zh": {"title": "花蓮 & 太魯閣", "description": "搭火車到花蓮，太魯閣峽谷。"}},
            },
            {
                "day_number": 3,
                "title": "East Coast",
                "description": "Scenic east coast, Shitiping.",
                "activities": [],
                "translations": {"zh": {"title": "東海岸", "description": "壯麗東海岸風光，石梯坪。"}},
            },
            {
                "day_number": 4,
                "title": "Taitung",
                "description": "Hot springs, aboriginal culture.",
                "activities": [],
                "translations": {"zh": {"title": "台東", "description": "溫泉、原住民文化。"}},
            },
            {
                "day_number": 5,
                "title": "Kenting",
                "description": "Tropical beaches, national park.",
                "activities": [],
                "translations": {"zh": {"title": "墾丁", "description": "熱帶海灘、國家公園。"}},
            },
            {
                "day_number": 6,
                "title": "Tainan",
                "description": "Ancient capital, temples, street food.",
                "activities": [],
                "translations": {"zh": {"title": "台南", "description": "古都、寺廟、街頭美食。"}},
            },
            {
                "day_number": 7,
                "title": "Sun Moon Lake",
                "description": "HSR to Taichung, Sun Moon Lake.",
                "activities": [],
                "translations": {"zh": {"title": "日月潭", "description": "搭高鐵到台中，日月潭。"}},
            },
            {
                "day_number": 8,
                "title": "Return to Taipei",
                "description": "HSR back, departure.",
                "activities": [],
                "translations": {"zh": {"title": "返回台北", "description": "搭高鐵返回台北，啟程離開。"}},
            },
        ],
    },
    {
        "title": "Taiwan Night Market Food Trail",
        "slug": "taiwan-night-market-food-5day",
        "destination": "Taiwan",
        "category": "Food & Drink",
        "summary": "5 days eating through Taiwan's best night markets from Taipei to Tainan.",
        "description": "Taiwan is a food paradise. This trail takes you through Shilin, Raohe, Feng Chia, and Tainan's Garden Night Market. Learn to make bubble tea, taste stinky tofu, try beef noodle soup competitions, and discover hidden local gems.",
        "duration_days": 5,
        "price_usd": 800,
        "highlights": [
            "Shilin Night Market",
            "Raohe Street Market",
            "Feng Chia Night Market",
            "Bubble tea workshop",
            "Tainan food capital",
        ],
        "translations": {
            "zh": {
                "title": "台灣夜市美食之旅",
                "summary": "5天吃遍台灣最棒的夜市，從台北到台南。",
                "description": "台灣是美食天堂。這條美食路線帶您走遍士林、饒河、逢甲和台南花園夜市。學做珍珠奶茶、嚐臭豆腐、品嚐牛肉麵大賽冠軍，發掘在地隱藏美食。",
                "highlights": [
                    "士林夜市",
                    "饒河街夜市",
                    "逢甲夜市",
                    "珍珠奶茶 DIY",
                    "台南美食之都",
                ],
            }
        },
        "tags": ["food", "night-market", "taipei", "taichung", "tainan"],
        "days": [
            {
                "day_number": 1,
                "title": "Taipei: Shilin & Raohe",
                "description": "Two of Taipei's greatest night markets.",
                "activities": [],
                "translations": {"zh": {"title": "台北：士林 & 饒河", "description": "台北最棒的兩大夜市。"}},
            },
            {
                "day_number": 2,
                "title": "Taipei: Beef Noodle & Boba",
                "description": "Best beef noodle soup spots, bubble tea making.",
                "activities": [],
                "translations": {
                    "zh": {
                        "title": "台北：牛肉麵 & 珍奶",
                        "description": "最佳牛肉麵名店，珍珠奶茶 DIY。",
                    }
                },
            },
            {
                "day_number": 3,
                "title": "Taichung: Feng Chia",
                "description": "HSR to Taichung, massive Feng Chia market.",
                "activities": [],
                "translations": {"zh": {"title": "台中：逢甲", "description": "搭高鐵到台中，逛超大的逢甲夜市。"}},
            },
            {
                "day_number": 4,
                "title": "Tainan: Food Capital",
                "description": "Tainan's legendary food scene.",
                "activities": [],
                "translations": {"zh": {"title": "台南：美食之都", "description": "台南傳奇美食場景。"}},
            },
            {
                "day_number": 5,
                "title": "Kaohsiung & Departure",
                "description": "Liuhe Night Market, departure from Kaohsiung.",
                "activities": [],
                "translations": {"zh": {"title": "高雄 & 離開", "description": "六合夜市，從高雄啟程。"}},
            },
        ],
    },
    {
        "title": "Taroko Gorge & Hualien Nature",
        "slug": "taroko-gorge-hualien-3day",
        "destination": "Taiwan",
        "category": "Nature",
        "summary": "3-day nature adventure through Taiwan's most dramatic landscape: Taroko National Park.",
        "description": "Marvel at marble canyons, hike through mist-covered trails, cross suspension bridges, and cycle along the Pacific coast. Taroko Gorge is Taiwan's natural crown jewel.",
        "duration_days": 3,
        "price_usd": 500,
        "highlights": [
            "Taroko Gorge trails",
            "Qingshui Cliffs",
            "Shakadang Trail",
            "Hualien night market",
            "Pacific coast cycling",
        ],
        "translations": {
            "zh": {
                "title": "太魯閣峽谷 & 花蓮自然之旅",
                "summary": "3天自然探險，走訪台灣最壯觀的地景：太魯閣國家公園。",
                "description": "驚嘆大理石峽谷，穿越雲霧繚繞的步道，走過吊橋，沿太平洋海岸騎自行車。太魯閣峽谷是台灣的自然瑰寶。",
                "highlights": [
                    "太魯閣步道",
                    "清水斷崖",
                    "砂卡噹步道",
                    "花蓮夜市",
                    "太平洋海岸自行車",
                ],
            }
        },
        "tags": ["nature", "taroko", "hualien", "hiking", "cycling"],
        "days": [
            {
                "day_number": 1,
                "title": "Hualien Arrival",
                "description": "Train from Taipei, Hualien city, night market.",
                "activities": [],
                "translations": {"zh": {"title": "抵達花蓮", "description": "從台北搭火車，花蓮市區，夜市。"}},
            },
            {
                "day_number": 2,
                "title": "Taroko Gorge Full Day",
                "description": "Shakadang Trail, Swallow Grotto, Eternal Spring Shrine.",
                "activities": [],
                "translations": {"zh": {"title": "太魯閣全日遊", "description": "砂卡噹步道、燕子口、長春祠。"}},
            },
            {
                "day_number": 3,
                "title": "Coast & Return",
                "description": "Qingshui Cliffs, cycling, return.",
                "activities": [],
                "translations": {"zh": {"title": "海岸 & 返回", "description": "清水斷崖、騎自行車、返回。"}},
            },
        ],
    },
    {
        "title": "Taiwan Family Adventure: 5 Days",
        "slug": "taiwan-family-5day",
        "destination": "Taiwan",
        "category": "Family",
        "summary": "Kid-friendly Taiwan trip: Taipei Zoo, Maokong gondola, Leofoo Village, and night markets.",
        "description": "Perfect for families. Visit Taipei Zoo and ride the Maokong Gondola, enjoy Leofoo Village theme park, make DIY pineapple cakes, explore interactive museums, and let kids try all the fun night market games.",
        "duration_days": 5,
        "price_usd": 1100,
        "highlights": [
            "Taipei Zoo & Maokong",
            "Leofoo Village Theme Park",
            "Pineapple cake DIY",
            "Interactive science museum",
            "Night market games",
        ],
        "translations": {
            "zh": {
                "title": "台灣親子遊：5天",
                "summary": "適合兒童的台灣之旅：台北動物園、貓空纜車、六福村和夜市。",
                "description": "完美的家庭旅行。參觀台北動物園搭貓空纜車，暢玩六福村主題樂園，DIY 鳳梨酥，探索互動科學博物館，讓孩子們盡情享受夜市遊戲。",
                "highlights": [
                    "台北動物園 & 貓空",
                    "六福村主題樂園",
                    "鳳梨酥 DIY",
                    "互動科學博物館",
                    "夜市遊戲",
                ],
            }
        },
        "tags": ["family", "kids", "taipei", "theme-park", "night-market"],
        "days": [
            {
                "day_number": 1,
                "title": "Taipei Arrival",
                "description": "Settle in, Ximending area exploration.",
                "activities": [],
                "translations": {"zh": {"title": "抵達台北", "description": "入住飯店，探索西門町。"}},
            },
            {
                "day_number": 2,
                "title": "Zoo & Maokong",
                "description": "Taipei Zoo, Maokong Gondola, tea houses.",
                "activities": [],
                "translations": {
                    "zh": {
                        "title": "動物園 & 貓空",
                        "description": "台北動物園、貓空纜車、茶藝館。",
                    }
                },
            },
            {
                "day_number": 3,
                "title": "Leofoo Village",
                "description": "Full day at the theme park.",
                "activities": [],
                "translations": {"zh": {"title": "六福村", "description": "全天暢玩主題樂園。"}},
            },
            {
                "day_number": 4,
                "title": "Culture & Cooking",
                "description": "Science museum, pineapple cake workshop.",
                "activities": [],
                "translations": {"zh": {"title": "文化 & 手作", "description": "科學博物館、鳳梨酥手作體驗。"}},
            },
            {
                "day_number": 5,
                "title": "Last Day & Departure",
                "description": "Shilin Night Market, departure.",
                "activities": [],
                "translations": {"zh": {"title": "最後一天 & 離開", "description": "士林夜市，啟程離開。"}},
            },
        ],
    },
    {
        "title": "Sun Moon Lake & Alishan Highlands",
        "slug": "sun-moon-lake-alishan-4day",
        "destination": "Taiwan",
        "category": "Nature",
        "summary": "4 days in Taiwan's mountain heartland: Sun Moon Lake serenity and Alishan sunrise.",
        "description": "Experience Taiwan's alpine beauty. Cycle around Sun Moon Lake, visit Wenwu Temple, take the historic Alishan Forest Railway, witness the famous sunrise from Zhushan, and walk among thousand-year-old cypress trees.",
        "duration_days": 4,
        "price_usd": 700,
        "highlights": [
            "Sun Moon Lake cycling",
            "Alishan Forest Railway",
            "Zhushan sunrise",
            "Ancient cypress trees",
            "Aboriginal culture",
        ],
        "translations": {
            "zh": {
                "title": "日月潭 & 阿里山高山之旅",
                "summary": "4天台灣山林心臟：日月潭寧靜與阿里山日出。",
                "description": "體驗台灣的高山之美。環日月潭騎自行車，參拜文武廟，搭乘歷史悠久的阿里山森林鐵路，在祝山觀賞知名日出，漫步千年檜木林。",
                "highlights": [
                    "日月潭環湖自行車",
                    "阿里山森林鐵路",
                    "祝山日出",
                    "千年檜木",
                    "原住民文化",
                ],
            }
        },
        "tags": ["nature", "sun-moon-lake", "alishan", "mountains", "cycling"],
        "days": [
            {
                "day_number": 1,
                "title": "To Sun Moon Lake",
                "description": "HSR to Taichung, bus to Sun Moon Lake.",
                "activities": [],
                "translations": {"zh": {"title": "前往日月潭", "description": "搭高鐵到台中，轉乘巴士到日月潭。"}},
            },
            {
                "day_number": 2,
                "title": "Lake Day",
                "description": "Cycling, boat tour, Wenwu Temple.",
                "activities": [],
                "translations": {"zh": {"title": "日月潭日", "description": "騎自行車、搭船遊湖、文武廟。"}},
            },
            {
                "day_number": 3,
                "title": "Alishan",
                "description": "Transfer to Alishan, forest railway, sunset.",
                "activities": [],
                "translations": {"zh": {"title": "阿里山", "description": "轉往阿里山，森林鐵路，觀賞夕陽。"}},
            },
            {
                "day_number": 4,
                "title": "Sunrise & Return",
                "description": "3am wake-up for sunrise, return.",
                "activities": [],
                "translations": {"zh": {"title": "日出 & 返回", "description": "凌晨3點起床看日出，返回。"}},
            },
        ],
    },
    {
        "title": "Kenting Tropical Beach Escape",
        "slug": "kenting-beach-escape-3day",
        "destination": "Taiwan",
        "category": "Relaxation",
        "summary": "3 days of sun, sand, and snorkeling in Taiwan's tropical south.",
        "description": "Taiwan's southern tip offers a tropical escape. White sand beaches at Baisha Bay, snorkeling at Houwan, surfing at Nanwan, and exploring Kenting National Park's coral formations and lighthouse.",
        "duration_days": 3,
        "price_usd": 450,
        "highlights": [
            "Baisha Bay beach",
            "Snorkeling at Houwan",
            "Kenting National Park",
            "Eluanbi Lighthouse",
            "Night market seafood",
        ],
        "translations": {
            "zh": {
                "title": "墾丁熱帶海灘之旅",
                "summary": "3天陽光、沙灘和浮潛，盡在台灣熱帶南端。",
                "description": "台灣南端的熱帶逃離之旅。白沙灣白沙海灘、後灣浮潛、南灣衝浪，以及探索墾丁國家公園的珊瑚礁地形和燈塔。",
                "highlights": ["白沙灣海灘", "後灣浮潛", "墾丁國家公園", "鵝鑾鼻燈塔", "夜市海鮮"],
            }
        },
        "tags": ["beach", "kenting", "tropical", "snorkeling", "relaxation"],
        "days": [
            {
                "day_number": 1,
                "title": "Arrive Kenting",
                "description": "HSR to Zuoying, shuttle to Kenting, beach.",
                "activities": [],
                "translations": {"zh": {"title": "抵達墾丁", "description": "搭高鐵到左營，接駁車到墾丁，海灘。"}},
            },
            {
                "day_number": 2,
                "title": "Water Activities",
                "description": "Snorkeling, surfing, national park.",
                "activities": [],
                "translations": {"zh": {"title": "水上活動", "description": "浮潛、衝浪、國家公園。"}},
            },
            {
                "day_number": 3,
                "title": "Lighthouse & Departure",
                "description": "Eluanbi Lighthouse, departure.",
                "activities": [],
                "translations": {"zh": {"title": "燈塔 & 離開", "description": "鵝鑾鼻燈塔，啟程離開。"}},
            },
        ],
    },
    {
        "title": "Tainan Heritage & Culture Walk",
        "slug": "tainan-heritage-3day",
        "destination": "Taiwan",
        "category": "Culture",
        "summary": "3 days exploring Taiwan's ancient capital: temples, history, and the best food on the island.",
        "description": "Tainan is Taiwan's oldest city and cultural heart. Explore Anping Fort and its tree house, countless ornate temples, traditional craft workshops, and what locals consider the best food in all of Taiwan.",
        "duration_days": 3,
        "price_usd": 400,
        "highlights": [
            "Anping Old Fort",
            "Confucius Temple",
            "Shennong Street",
            "Tainan street food",
            "Anping Tree House",
        ],
        "translations": {
            "zh": {
                "title": "台南古蹟文化漫步",
                "summary": "3天探索台灣古都：寺廟、歷史，以及全島最好吃的美食。",
                "description": "台南是台灣最古老的城市和文化中心。探索安平古堡和樹屋、無數精美寺廟、傳統工藝工坊，以及在地人公認的全台灣最好吃的美食。",
                "highlights": ["安平古堡", "孔廟", "神農街", "台南街頭美食", "安平樹屋"],
            }
        },
        "tags": ["culture", "tainan", "history", "temples", "food"],
        "days": [
            {
                "day_number": 1,
                "title": "Tainan Arrival",
                "description": "HSR from Taipei, Confucius Temple area.",
                "activities": [],
                "translations": {"zh": {"title": "抵達台南", "description": "從台北搭高鐵，孔廟周邊。"}},
            },
            {
                "day_number": 2,
                "title": "Anping District",
                "description": "Old fort, tree house, oyster omelets.",
                "activities": [],
                "translations": {"zh": {"title": "安平區", "description": "古堡、樹屋、蚵仔煎。"}},
            },
            {
                "day_number": 3,
                "title": "Shennong St & Departure",
                "description": "Colorful street, last food tour, departure.",
                "activities": [],
                "translations": {
                    "zh": {
                        "title": "神農街 & 離開",
                        "description": "彩色街道、最後美食巡禮，啟程離開。",
                    }
                },
            },
        ],
    },
    {
        "title": "Taiwan Tea & Hot Springs Journey",
        "slug": "taiwan-tea-hotsprings-4day",
        "destination": "Taiwan",
        "category": "Relaxation",
        "summary": "4 days of tea culture and natural hot springs from Beitou to Jiufen.",
        "description": "Explore Taiwan's rich tea heritage and volcanic hot springs. Visit Beitou's thermal valley, learn oolong tea preparation in Maokong, explore Jiufen's tea houses, and relax in Wulai's riverside hot springs.",
        "duration_days": 4,
        "price_usd": 600,
        "highlights": [
            "Beitou hot springs",
            "Maokong tea farms",
            "Jiufen tea houses",
            "Wulai aboriginal village",
            "Tea ceremony workshop",
        ],
        "translations": {
            "zh": {
                "title": "台灣茶道 & 溫泉之旅",
                "summary": "4天品茶與天然溫泉之旅，從北投到九份。",
                "description": "探索台灣豐富的茶文化和火山溫泉。造訪北投地熱谷，在貓空學習烏龍茶沖泡，探索九份茶藝館，在烏來溪畔溫泉中放鬆。",
                "highlights": ["北投溫泉", "貓空茶園", "九份茶藝館", "烏來原住民村落", "茶道體驗"],
            }
        },
        "tags": ["tea", "hot-springs", "relaxation", "beitou", "jiufen"],
        "days": [
            {
                "day_number": 1,
                "title": "Beitou Hot Springs",
                "description": "Thermal Valley, hot spring hotels.",
                "activities": [],
                "translations": {"zh": {"title": "北投溫泉", "description": "地熱谷、溫泉旅館。"}},
            },
            {
                "day_number": 2,
                "title": "Maokong Tea Country",
                "description": "Gondola ride, tea plantation tours.",
                "activities": [],
                "translations": {"zh": {"title": "貓空茶鄉", "description": "搭纜車、茶園導覽。"}},
            },
            {
                "day_number": 3,
                "title": "Jiufen & Shifen",
                "description": "Mountain tea houses, sky lanterns.",
                "activities": [],
                "translations": {"zh": {"title": "九份 & 十分", "description": "山城茶藝館、天燈。"}},
            },
            {
                "day_number": 4,
                "title": "Wulai & Departure",
                "description": "Aboriginal village, riverside springs.",
                "activities": [],
                "translations": {"zh": {"title": "烏來 & 離開", "description": "原住民村落、溪畔溫泉。"}},
            },
        ],
    },
]


async def seed():
    engine = create_async_engine(settings.database_url)
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with session_factory() as db:
        for pkg_data in PACKAGES:
            days_data = pkg_data.pop("days", [])
            tags_data = pkg_data.pop("tags", [])

            package = TravelPackage(**pkg_data)
            db.add(package)
            await db.flush()

            for day_data in days_data:
                day = PackageDay(package_id=package.id, **day_data)
                db.add(day)

            for tag_name in tags_data:
                tag_trans = TAG_TRANSLATIONS.get(tag_name)
                tag = PackageTag(
                    package_id=package.id,
                    tag=tag_name,
                    translations=tag_trans,
                )
                db.add(tag)

        await db.commit()
        print(f"Seeded {len(PACKAGES)} travel packages successfully!")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(seed())
