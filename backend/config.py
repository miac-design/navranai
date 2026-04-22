"""
Global configuration for the RedM Command Center V3 backend.
"""
import os
import logging

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
LOG_FORMAT = "%(asctime)s | %(name)-25s | %(levelname)-7s | %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger("redm")

# ---------------------------------------------------------------------------
# API Management Toggles
# ---------------------------------------------------------------------------
API_CONFIG = {
    "EXA_ENABLED": True,
}

# ---------------------------------------------------------------------------
# News source domains for Exa search
# ---------------------------------------------------------------------------
NEWS_DOMAINS = [
    # Authorities
    "unodc.org",
    "polarisproject.org",
    "ctdatacollaborative.org",
    "hrw.org",
    "ijm.org",
    "ilo.org",
    "thorn.org",
    # Global News
    "reuters.com",
    "apnews.com",
    "theguardian.com",
    "bbc.com",
    "cnn.com",
    "aljazeera.com",
]

SOCIAL_DOMAINS = [
    "x.com",
]

# ---------------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------------
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///redm_v3.db")

# ---------------------------------------------------------------------------
# Content defaults
# ---------------------------------------------------------------------------
CONTENT_TYPES = ["reactive", "stat", "explainer", "action", "hope"]

PLATFORM_SPECS = {
    "ig_square":  (1080, 1080),
    "ig_stories": (1080, 1920),
    "x_card":     (1600, 900),
    "li_post":    (1200, 627),
    "fb_post":    (1200, 630),
}

SUPPORTED_LANGUAGES = ["en", "es", "fr", "pt"]
