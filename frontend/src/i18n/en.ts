import type { zh } from "./zh";

// Ensures en has exactly the same keys as zh, with string values
export const en: { [K in keyof typeof zh]: string } = {
  // Navbar
  "nav.brand": "AI Trip Planner",
  "nav.packages": "Packages",
  "nav.chat": "AI Chat",
  "nav.trips": "My Trips",
  "nav.signIn": "Sign In",
  "nav.logout": "Logout",

  // HomePage — Hero
  "home.hero.title": "Plan Your Dream Trip",
  "home.hero.titleAccent": "with AI",
  "home.hero.subtitle":
    "Tell our AI assistant where you want to go, and get a complete itinerary with hotels, activities, transport, and cost breakdowns — all in seconds.",
  "home.hero.startPlanning": "Start Planning",
  "home.hero.signInToStart": "Sign In to Start",
  "home.hero.browsePackages": "Browse Packages",

  // HomePage — How it works
  "home.how.title": "How It Works",
  "home.how.step1.title": "Tell Us Your Dream",
  "home.how.step1.desc":
    "Describe your ideal trip in natural language — destination, dates, budget, travel style.",
  "home.how.step2.title": "AI Plans Everything",
  "home.how.step2.desc":
    "Our multi-agent system researches flights, hotels, activities, and local tips simultaneously.",
  "home.how.step3.title": "Get Your Itinerary",
  "home.how.step3.desc":
    "Receive a detailed day-by-day plan with cost breakdowns, maps, and booking links.",

  // HomePage — Featured
  "home.featured.title": "Featured Packages",
  "home.featured.viewAll": "View all →",

  // PackagesPage
  "packages.title": "Travel Packages",
  "packages.subtitle":
    "Browse curated travel packages for Japan and Taiwan",
  "packages.searchPlaceholder": "Search with AI...",
  "packages.searchBtn": "Search",
  "packages.noResults": "No packages found matching your criteria.",
  "packages.allDestinations": "All Destinations",
  "packages.allCategories": "All Categories",

  // PackageDetailPage
  "pkgDetail.back": "← Back to packages",
  "pkgDetail.notFound": "Package not found",
  "pkgDetail.perPerson": "/ person",
  "pkgDetail.days": "days",
  "pkgDetail.highlights": "Highlights",
  "pkgDetail.dayByDay": "Day-by-Day Itinerary",
  "pkgDetail.day": "Day",

  // ChatPage
  "chat.newChat": "+ New Chat",
  "chat.defaultTitle": "AI Trip Planner",
  "chat.emptyTitle": "Start Planning Your Trip",
  "chat.emptyDesc":
    "Tell me where you want to go, when, your budget, and any preferences. I'll create a complete itinerary for you!",
  "chat.placeholder": "Describe your dream trip...",
  "chat.send": "Send",
  "chat.hint": "Press Enter to send, Shift+Enter for new line",
  "chat.planning": "Planning your trip...",
  "chat.startMsg": "Send a message to start planning!",
  "chat.prompt1": "Plan a 5-day Tokyo trip for 2",
  "chat.prompt2": "Family ski trip to Hokkaido",
  "chat.prompt3": "Taiwan food tour, 4 days",
  "chat.prompt4": "帶小孩去日本滑雪5天",

  // LoginPage
  "login.title": "Welcome to AI Trip Planner",
  "login.subtitle": "Sign in to start planning your perfect trip",
  "login.google": "Continue with Google",
  "login.line": "Continue with LINE",
  "login.terms":
    "By signing in, you agree to our Terms of Service and Privacy Policy.",
  "login.freeTier": "Free tier: 5 AI queries/day",

  // AuthCallbackPage
  "auth.signingIn": "Signing you in...",

  // ProfilePage
  "profile.title": "Profile",
  "profile.tier": "tier",
  "profile.todayUsage": "Today's Usage",
  "profile.queriesUsed": "queries used",
  "profile.remaining": "remaining",
  "profile.dailyLimit": "daily limit",
  "profile.upgrade": "Upgrade to Premium for 50 queries/day",
  "profile.myItineraries": "My Itineraries",
  "profile.noItineraries": "No itineraries yet.",
  "profile.startPlanning": "Start planning!",

  // ItineraryPage
  "itinerary.back": "← My Trips",
  "itinerary.notFound": "Itinerary not found",
  "itinerary.travelers": "traveler(s)",
  "itinerary.total": "Total",
  "itinerary.dayByDay": "Day-by-Day Plan",
  "itinerary.costBreakdown": "Cost Breakdown",

  // CostBreakdown categories
  "cost.flights": "Flights",
  "cost.hotels": "Hotels",
  "cost.activities": "Activities",
  "cost.transport": "Local Transport",
  "cost.meals": "Meals",
  "cost.esim": "eSIM / Data",
  "cost.misc": "Miscellaneous",

  // UsageBadge
  "usage.queriesLeft": "queries left",

  // Footer
  "footer.powered": "AI Trip Planner — Powered by CrewAI + MCP",
  "footer.about": "About",
  "footer.privacy": "Privacy",
  "footer.terms": "Terms",

  // Common
  "common.days": "days",
} as const;
