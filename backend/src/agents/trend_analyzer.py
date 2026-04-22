"""
Trend Analyzer — replicated from Fully_operational MVP 2.
Only change: gpt-4o → gpt-4o-mini (rate limit safety).
"""
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from src.tools.exa_search import ExaSearch
from src.tools.crawl4ai_scraper import Crawl4AIScraper
from src.state import AgentState
from pydantic import BaseModel, Field
from typing import List
from langsmith import traceable
import config


class TrendAnalysis(BaseModel):
    topic: str = Field(description="A concise headline for the trend.")
    context: str = Field(description="A detailed summary of the 'who, what, when, where, why' and why it matters now.")
    used_source_urls: List[str] = Field(description="A list of the specific article URLs from the provided text that you actually used to form this trend analysis.")


class TrendAnalyzer:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    @traceable(name="Trend Analyzer")
    def analyze_trends(self, state: AgentState):
        """
        Analyzes current human trafficking trends.
        """

        articles_content = []

        manual_url = state.get("manual_url")
        if manual_url:
            try:
                scraper = Crawl4AIScraper()
                content = scraper.read_url(manual_url)
                articles_content.append({
                    "title": "Manual Intercept Article",
                    "source": "Human Override",
                    "url": manual_url,
                    "content": content
                })
            except Exception as e:
                print(f"ERROR matching manual URL: {e}")
        else:
            # Primary Source: Google News RSS
            try:
                from src.tools.google_news import GoogleNewsSearch
                search_tool = GoogleNewsSearch()
                articles_content = search_tool.search_news(
                    query='"human trafficking"',
                    num_results=10,
                )
            except Exception as e:
                print(f"ERROR searching Google News: {e}")

        if not articles_content:
            print("ERROR: No articles retrieved.")
            return {"status": "error", "feedback": "News gathering failed."}

        # Combine standard content and prepare raw news array
        combined_text_list = []
        raw_news_list = []
        for i, article in enumerate(articles_content):
            title = article.get("title", "")
            source = article.get("source", "")
            url = article.get("url", "")
            content = article.get("content", "")
            combined_text_list.append(f"Source: {source} ({url})\nTitle: {title}\nContent: {content[:8000]}...")
            raw_news_list.append({"title": title, "source": source, "url": url, "content": content})

        combined_content = "\n\n".join(combined_text_list)

        parser = PydanticOutputParser(pydantic_object=TrendAnalysis)

        # Create a prompt for the structured output
        structured_prompt = ChatPromptTemplate.from_template(
            """
            You are a Trend Analyzer.
            Analyze the following news articles and identify the SINGLE most important current trend or story.
            
            CRITICAL RULES FOR ACCURACY:
            1. The trend MUST be explicitly and exclusively about HUMAN TRAFFICKING (e.g., labor trafficking, sex trafficking, debt bondage). 
            2. You MUST COMPLETELY IGNORE any articles that are about general human rights, drug trafficking, immigration, or other unrelated crimes. Do NOT force a connection or settle for a "general human rights" summary.
            3. Base your decision ONLY on the articles provided that actually meet the criteria above.
            4. If multiple relevant human trafficking stories exist, choose the one that is mentioned most frequently or carries the highest global legislative/law enforcement impact.
            5. MANUAL OVERRIDE RULE: If only a single article is provided, it means a human operator explicitly bypassed the search to inject it. You MUST process it as a valid trend regardless of the strict criteria above, and extract its core message.
            
            Articles:
            {articles}
            
            {format_instructions}
            """
        )

        chain = structured_prompt | self.llm | parser
        final_response: TrendAnalysis = chain.invoke({
            "articles": combined_content,
            "format_instructions": parser.get_format_instructions()
        })

        # Filter the raw_news_list to only include the sources the LLM specifically cited
        used_urls = final_response.used_source_urls
        filtered_news_list = [news for news in raw_news_list if news["url"] in used_urls]

        # Fallback in case the LLM messes up the URL formatting
        if not filtered_news_list:
            filtered_news_list = raw_news_list

        return {
            "trend_topic": final_response.topic,
            "trend_context": final_response.context,
            "raw_news": filtered_news_list,
            "all_retrieved_news": raw_news_list,
            "writer_prompt": None,
            "visual_style": None,
            "post_text": None,
            "image_path": None,
            "campaign_posts": None,
            "current_post_index": 0,
            "status": "planning"
        }
