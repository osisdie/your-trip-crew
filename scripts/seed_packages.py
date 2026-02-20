"""Seed the database with 18 sample travel packages."""

import asyncio
import uuid

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlmodel import SQLModel

from app.config import settings
from app.models.package import PackageDay, PackageTag, TravelPackage

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
        "highlights": ["Tsukiji Market food tour", "Harajuku & Shibuya crossing", "Senso-ji Temple", "Tokyo Skytree sunset", "Robot Restaurant experience"],
        "tags": ["tokyo", "urban", "food", "culture", "nightlife"],
        "days": [
            {"day_number": 1, "title": "Arrival & Shinjuku", "description": "Arrive at Narita/Haneda, check into hotel. Evening walk through Shinjuku's neon streets and Golden Gai.", "activities": [{"time": "14:00", "name": "Airport transfer"}, {"time": "18:00", "name": "Shinjuku exploration"}, {"time": "20:00", "name": "Golden Gai bar hopping"}]},
            {"day_number": 2, "title": "Tsukiji & Ginza", "description": "Morning at Tsukiji Outer Market for sushi breakfast, afternoon in upscale Ginza, evening at teamLab Borderless.", "activities": [{"time": "07:00", "name": "Tsukiji Market tour"}, {"time": "13:00", "name": "Ginza shopping"}, {"time": "17:00", "name": "teamLab Borderless"}]},
            {"day_number": 3, "title": "Asakusa & Akihabara", "description": "Visit Senso-ji temple, explore Nakamise-dori, afternoon in Akihabara's anime & electronics district.", "activities": [{"time": "09:00", "name": "Senso-ji Temple"}, {"time": "12:00", "name": "Lunch at Asakusa"}, {"time": "14:00", "name": "Akihabara tour"}]},
            {"day_number": 4, "title": "Harajuku & Shibuya", "description": "Meiji Shrine, Takeshita Street, Shibuya Crossing, and Shibuya Sky observation deck.", "activities": [{"time": "09:00", "name": "Meiji Shrine"}, {"time": "11:00", "name": "Harajuku & Takeshita St"}, {"time": "15:00", "name": "Shibuya Sky"}]},
            {"day_number": 5, "title": "Skytree & Departure", "description": "Morning at Tokyo Skytree, souvenir shopping, airport transfer.", "activities": [{"time": "09:00", "name": "Tokyo Skytree"}, {"time": "12:00", "name": "Last shopping"}, {"time": "15:00", "name": "Airport transfer"}]},
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
        "highlights": ["Fushimi Inari Shrine", "Tea ceremony experience", "Arashiyama Bamboo Grove", "Gion geisha district", "Osaka street food tour"],
        "tags": ["kyoto", "osaka", "culture", "temples", "food"],
        "days": [
            {"day_number": 1, "title": "Arrival in Kyoto", "description": "Arrive via Shinkansen, check in at traditional ryokan, evening stroll through Gion.", "activities": []},
            {"day_number": 2, "title": "Eastern Kyoto Temples", "description": "Kiyomizu-dera, Philosopher's Path, Ginkaku-ji.", "activities": []},
            {"day_number": 3, "title": "Fushimi Inari & Tea", "description": "Morning hike through torii gates, afternoon tea ceremony.", "activities": []},
            {"day_number": 4, "title": "Arashiyama", "description": "Bamboo grove, Togetsukyo Bridge, monkey park.", "activities": []},
            {"day_number": 5, "title": "Day Trip to Nara", "description": "Todai-ji, friendly deer park, Kasuga Grand Shrine.", "activities": []},
            {"day_number": 6, "title": "Osaka Food Adventure", "description": "Dotonbori, Kuromon Market, street food crawl.", "activities": []},
            {"day_number": 7, "title": "Osaka Castle & Departure", "description": "Morning at Osaka Castle, departure.", "activities": []},
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
        "highlights": ["Niseko powder skiing", "Night skiing experience", "Onsen hot springs", "Hokkaido seafood", "Furano day trip"],
        "tags": ["hokkaido", "skiing", "winter", "onsen", "niseko"],
        "days": [
            {"day_number": 1, "title": "Arrival at New Chitose", "description": "Fly into Sapporo, transfer to Niseko, settle into ski lodge.", "activities": []},
            {"day_number": 2, "title": "Niseko Grand Hirafu", "description": "Full day skiing at Grand Hirafu, evening onsen.", "activities": []},
            {"day_number": 3, "title": "Niseko Village & Annupuri", "description": "Explore different Niseko resorts, night skiing.", "activities": []},
            {"day_number": 4, "title": "Furano Day Trip", "description": "Ski Furano's excellent terrain, visit cheese factory.", "activities": []},
            {"day_number": 5, "title": "Free Ski Day", "description": "Choose your favorite resort, afternoon spa.", "activities": []},
            {"day_number": 6, "title": "Departure", "description": "Morning dip in onsen, transfer to airport.", "activities": []},
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
        "highlights": ["Tokyo DisneySea", "Ghibli Museum", "Universal Studios Japan", "Kid-friendly food tours", "Pokemon Center visit"],
        "tags": ["family", "kids", "theme-parks", "tokyo", "osaka"],
        "days": [
            {"day_number": 1, "title": "Tokyo Arrival", "description": "Arrive and settle in, explore Odaiba.", "activities": []},
            {"day_number": 2, "title": "Tokyo DisneySea", "description": "Full day at DisneySea.", "activities": []},
            {"day_number": 3, "title": "Ghibli & Shibuya", "description": "Ghibli Museum, Pokemon Center, Shibuya.", "activities": []},
            {"day_number": 4, "title": "Shinkansen to Osaka", "description": "Bullet train experience, arrive Osaka, Dotonbori.", "activities": []},
            {"day_number": 5, "title": "Universal Studios", "description": "Full day at USJ, Super Nintendo World.", "activities": []},
            {"day_number": 6, "title": "Departure", "description": "Morning shopping, departure.", "activities": []},
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
        "highlights": ["Mt. Fuji views", "Lake Ashi cruise", "Hakone Ropeway", "Traditional ryokan stay", "Onsen experience"],
        "tags": ["nature", "fuji", "hakone", "onsen", "hiking"],
        "days": [
            {"day_number": 1, "title": "Tokyo to Hakone", "description": "Romance Car to Hakone, check into ryokan.", "activities": []},
            {"day_number": 2, "title": "Hakone Loop", "description": "Ropeway, Owakudani, Lake Ashi pirate ship cruise.", "activities": []},
            {"day_number": 3, "title": "Fuji Five Lakes", "description": "Drive to Kawaguchiko, Chureito Pagoda, lakeside walk.", "activities": []},
            {"day_number": 4, "title": "Return to Tokyo", "description": "Morning onsen, return.", "activities": []},
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
        "highlights": ["Kerama Islands snorkeling", "Shuri Castle", "Okinawan food", "Beach relaxation", "Glass-bottom boat"],
        "tags": ["okinawa", "beach", "snorkeling", "relaxation", "islands"],
        "days": [
            {"day_number": 1, "title": "Naha Arrival", "description": "Arrive in Naha, Kokusai Street, Okinawan dinner.", "activities": []},
            {"day_number": 2, "title": "Shuri Castle & South", "description": "Shuri Castle, Peace Memorial Park.", "activities": []},
            {"day_number": 3, "title": "Kerama Islands", "description": "Day trip to Zamami, snorkeling, beach.", "activities": []},
            {"day_number": 4, "title": "Northern Okinawa", "description": "Churaumi Aquarium, Emerald Beach.", "activities": []},
            {"day_number": 5, "title": "Departure", "description": "Morning beach time, departure.", "activities": []},
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
        "highlights": ["Tsukiji sushi breakfast", "Ramen tour", "Kobe beef experience", "Osaka street food", "Sake tasting & cooking class"],
        "tags": ["food", "ramen", "sushi", "osaka", "cooking"],
        "days": [
            {"day_number": 1, "title": "Tokyo Sushi & Ramen", "description": "Tsukiji sushi, evening ramen crawl.", "activities": []},
            {"day_number": 2, "title": "Depachika & Izakaya", "description": "Department store food halls, izakaya night.", "activities": []},
            {"day_number": 3, "title": "Cooking Class", "description": "Japanese cooking workshop, Yanaka street food.", "activities": []},
            {"day_number": 4, "title": "Shinkansen to Kyoto", "description": "Ekiben on bullet train, Nishiki Market.", "activities": []},
            {"day_number": 5, "title": "Kyoto & Sake", "description": "Tofu cuisine, Fushimi sake district.", "activities": []},
            {"day_number": 6, "title": "Kobe Beef Day", "description": "Kobe beef teppanyaki, Chinatown.", "activities": []},
            {"day_number": 7, "title": "Osaka Grand Finale", "description": "Kuromon Market, Dotonbori feast, departure.", "activities": []},
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
        "highlights": ["Shirakami Sanchi forest", "Zao Fox Village", "Ginzan Onsen", "Kakunodate samurai town", "Matsushima Bay cruise"],
        "tags": ["tohoku", "adventure", "nature", "onsen", "hiking"],
        "days": [
            {"day_number": 1, "title": "Sendai & Matsushima", "description": "Shinkansen to Sendai, Matsushima Bay.", "activities": []},
            {"day_number": 2, "title": "Zao & Fox Village", "description": "Zao onsen area, fox village.", "activities": []},
            {"day_number": 3, "title": "Ginzan Onsen", "description": "Travel to Ginzan Onsen, evening stroll.", "activities": []},
            {"day_number": 4, "title": "Kakunodate", "description": "Samurai district, cherry bark crafts.", "activities": []},
            {"day_number": 5, "title": "Return", "description": "Morning hike, return to Tokyo.", "activities": []},
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
        "highlights": ["Taipei 101 observation deck", "Shilin Night Market", "Jiufen Old Street", "Longshan Temple", "Elephant Mountain hike"],
        "tags": ["taipei", "urban", "night-market", "food", "temples"],
        "days": [
            {"day_number": 1, "title": "Taipei Arrival", "description": "Arrive at Taoyuan Airport, MRT to hotel, evening at Shilin Night Market.", "activities": []},
            {"day_number": 2, "title": "Central Taipei", "description": "Taipei 101, Xinyi district, Longshan Temple, Bopiliao Historic Block.", "activities": []},
            {"day_number": 3, "title": "Jiufen Day Trip", "description": "Train to Jiufen, explore old street, Shifen waterfalls.", "activities": []},
            {"day_number": 4, "title": "Elephant Mountain & Departure", "description": "Sunrise hike at Elephant Mountain, departure.", "activities": []},
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
        "highlights": ["Taroko Gorge", "Kenting beaches", "Sun Moon Lake", "Tainan temples", "East coast scenery"],
        "tags": ["taiwan", "railway", "adventure", "nature", "round-island"],
        "days": [
            {"day_number": 1, "title": "Taipei Start", "description": "Taipei exploration, prepare for journey.", "activities": []},
            {"day_number": 2, "title": "Hualien & Taroko", "description": "Train to Hualien, Taroko Gorge.", "activities": []},
            {"day_number": 3, "title": "East Coast", "description": "Scenic east coast, Shitiping.", "activities": []},
            {"day_number": 4, "title": "Taitung", "description": "Hot springs, aboriginal culture.", "activities": []},
            {"day_number": 5, "title": "Kenting", "description": "Tropical beaches, national park.", "activities": []},
            {"day_number": 6, "title": "Tainan", "description": "Ancient capital, temples, street food.", "activities": []},
            {"day_number": 7, "title": "Sun Moon Lake", "description": "HSR to Taichung, Sun Moon Lake.", "activities": []},
            {"day_number": 8, "title": "Return to Taipei", "description": "HSR back, departure.", "activities": []},
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
        "highlights": ["Shilin Night Market", "Raohe Street Market", "Feng Chia Night Market", "Bubble tea workshop", "Tainan food capital"],
        "tags": ["food", "night-market", "taipei", "taichung", "tainan"],
        "days": [
            {"day_number": 1, "title": "Taipei: Shilin & Raohe", "description": "Two of Taipei's greatest night markets.", "activities": []},
            {"day_number": 2, "title": "Taipei: Beef Noodle & Boba", "description": "Best beef noodle soup spots, bubble tea making.", "activities": []},
            {"day_number": 3, "title": "Taichung: Feng Chia", "description": "HSR to Taichung, massive Feng Chia market.", "activities": []},
            {"day_number": 4, "title": "Tainan: Food Capital", "description": "Tainan's legendary food scene.", "activities": []},
            {"day_number": 5, "title": "Kaohsiung & Departure", "description": "Liuhe Night Market, departure from Kaohsiung.", "activities": []},
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
        "highlights": ["Taroko Gorge trails", "Qingshui Cliffs", "Shakadang Trail", "Hualien night market", "Pacific coast cycling"],
        "tags": ["nature", "taroko", "hualien", "hiking", "cycling"],
        "days": [
            {"day_number": 1, "title": "Hualien Arrival", "description": "Train from Taipei, Hualien city, night market.", "activities": []},
            {"day_number": 2, "title": "Taroko Gorge Full Day", "description": "Shakadang Trail, Swallow Grotto, Eternal Spring Shrine.", "activities": []},
            {"day_number": 3, "title": "Coast & Return", "description": "Qingshui Cliffs, cycling, return.", "activities": []},
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
        "highlights": ["Taipei Zoo & Maokong", "Leofoo Village Theme Park", "Pineapple cake DIY", "Interactive science museum", "Night market games"],
        "tags": ["family", "kids", "taipei", "theme-park", "night-market"],
        "days": [
            {"day_number": 1, "title": "Taipei Arrival", "description": "Settle in, Ximending area exploration.", "activities": []},
            {"day_number": 2, "title": "Zoo & Maokong", "description": "Taipei Zoo, Maokong Gondola, tea houses.", "activities": []},
            {"day_number": 3, "title": "Leofoo Village", "description": "Full day at the theme park.", "activities": []},
            {"day_number": 4, "title": "Culture & Cooking", "description": "Science museum, pineapple cake workshop.", "activities": []},
            {"day_number": 5, "title": "Last Day & Departure", "description": "Shilin Night Market, departure.", "activities": []},
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
        "highlights": ["Sun Moon Lake cycling", "Alishan Forest Railway", "Zhushan sunrise", "Ancient cypress trees", "Aboriginal culture"],
        "tags": ["nature", "sun-moon-lake", "alishan", "mountains", "cycling"],
        "days": [
            {"day_number": 1, "title": "To Sun Moon Lake", "description": "HSR to Taichung, bus to Sun Moon Lake.", "activities": []},
            {"day_number": 2, "title": "Lake Day", "description": "Cycling, boat tour, Wenwu Temple.", "activities": []},
            {"day_number": 3, "title": "Alishan", "description": "Transfer to Alishan, forest railway, sunset.", "activities": []},
            {"day_number": 4, "title": "Sunrise & Return", "description": "3am wake-up for sunrise, return.", "activities": []},
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
        "highlights": ["Baisha Bay beach", "Snorkeling at Houwan", "Kenting National Park", "Eluanbi Lighthouse", "Night market seafood"],
        "tags": ["beach", "kenting", "tropical", "snorkeling", "relaxation"],
        "days": [
            {"day_number": 1, "title": "Arrive Kenting", "description": "HSR to Zuoying, shuttle to Kenting, beach.", "activities": []},
            {"day_number": 2, "title": "Water Activities", "description": "Snorkeling, surfing, national park.", "activities": []},
            {"day_number": 3, "title": "Lighthouse & Departure", "description": "Eluanbi Lighthouse, departure.", "activities": []},
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
        "highlights": ["Anping Old Fort", "Confucius Temple", "Shennong Street", "Tainan street food", "Anping Tree House"],
        "tags": ["culture", "tainan", "history", "temples", "food"],
        "days": [
            {"day_number": 1, "title": "Tainan Arrival", "description": "HSR from Taipei, Confucius Temple area.", "activities": []},
            {"day_number": 2, "title": "Anping District", "description": "Old fort, tree house, oyster omelets.", "activities": []},
            {"day_number": 3, "title": "Shennong St & Departure", "description": "Colorful street, last food tour, departure.", "activities": []},
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
        "highlights": ["Beitou hot springs", "Maokong tea farms", "Jiufen tea houses", "Wulai aboriginal village", "Tea ceremony workshop"],
        "tags": ["tea", "hot-springs", "relaxation", "beitou", "jiufen"],
        "days": [
            {"day_number": 1, "title": "Beitou Hot Springs", "description": "Thermal Valley, hot spring hotels.", "activities": []},
            {"day_number": 2, "title": "Maokong Tea Country", "description": "Gondola ride, tea plantation tours.", "activities": []},
            {"day_number": 3, "title": "Jiufen & Shifen", "description": "Mountain tea houses, sky lanterns.", "activities": []},
            {"day_number": 4, "title": "Wulai & Departure", "description": "Aboriginal village, riverside springs.", "activities": []},
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
                tag = PackageTag(package_id=package.id, tag=tag_name)
                db.add(tag)

        await db.commit()
        print(f"Seeded {len(PACKAGES)} travel packages successfully!")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(seed())
