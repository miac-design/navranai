"""
Phase 12: Semantic Memory (Content Deduplication).

Uses ChromaDB to store embeddings of past captions.
Checks new content against the last 30 days to prevent repetition.
"""
import logging
from datetime import datetime, timedelta
from typing import Optional, Tuple

logger = logging.getLogger("redm.memory")

# ChromaDB is optional — gracefully degrade if not installed
try:
    import chromadb
    from chromadb.config import Settings as ChromaSettings
    CHROMA_AVAILABLE = True
except ImportError:
    CHROMA_AVAILABLE = False
    logger.warning("ChromaDB not installed — deduplication disabled")


class ContentMemory:
    """Embedding-based content deduplication using ChromaDB."""

    SIMILARITY_THRESHOLD = 0.85  # Above this = too similar

    def __init__(self, persist_dir: str = "./chroma_db"):
        self._enabled = CHROMA_AVAILABLE
        if self._enabled:
            try:
                self.client = chromadb.PersistentClient(path=persist_dir)
                self.collection = self.client.get_or_create_collection(
                    name="redm_content",
                    metadata={"hnsw:space": "cosine"},
                )
                logger.info("ContentMemory initialized with %d items", self.collection.count())
            except Exception as e:
                logger.error("ChromaDB init failed: %s", e)
                self._enabled = False

    def check_duplicate(self, caption: str) -> Tuple[bool, Optional[str]]:
        """
        Check if a caption is too similar to recent content.
        Returns (is_duplicate, similar_caption_text).
        """
        if not self._enabled or not caption.strip():
            return False, None

        try:
            results = self.collection.query(
                query_texts=[caption],
                n_results=3,
            )

            if not results["distances"] or not results["distances"][0]:
                return False, None

            # ChromaDB returns cosine distance; lower = more similar
            # Convert to similarity: sim = 1 - distance
            for i, distance in enumerate(results["distances"][0]):
                similarity = 1 - distance
                if similarity >= self.SIMILARITY_THRESHOLD:
                    similar_text = results["documents"][0][i] if results["documents"] else "Unknown"
                    logger.warning(
                        "Duplicate detected (similarity: %.2f): %s...",
                        similarity, similar_text[:80],
                    )
                    return True, similar_text

            return False, None

        except Exception as e:
            logger.error("Dedup check failed: %s", e)
            return False, None

    def store(self, campaign_id: str, caption: str, content_type: str):
        """Store a caption embedding after it's approved."""
        if not self._enabled or not caption.strip():
            return

        try:
            doc_id = f"{campaign_id}_{content_type}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
            self.collection.add(
                documents=[caption],
                ids=[doc_id],
                metadatas=[{
                    "campaign_id": campaign_id,
                    "content_type": content_type,
                    "created_at": datetime.utcnow().isoformat(),
                }],
            )
            logger.info("Stored caption in memory: %s", doc_id)
        except Exception as e:
            logger.error("Failed to store in memory: %s", e)

    def get_count(self) -> int:
        """Get the number of stored captions."""
        if not self._enabled:
            return 0
        return self.collection.count()
