import { notFound } from "next/navigation";
import type { Metadata } from "next";
import { articles, getArticle } from "@/lib/articles";
import Nav from "@/components/Nav";
import Cursor from "@/components/Cursor";
import ArticleReader from "@/components/ArticleReader";

export function generateStaticParams() {
  return articles.map((a) => ({ slug: a.slug }));
}

export function generateMetadata({
  params,
}: {
  params: { slug: string };
}): Metadata {
  const a = getArticle(params.slug);
  if (!a) return { title: "Not found — Navran" };
  return {
    title: `${a.headline} — Navran`,
    description: a.dek,
  };
}

export default function ArticlePage({ params }: { params: { slug: string } }) {
  const article = getArticle(params.slug);
  if (!article) notFound();

  const others = articles.filter((a) => a.slug !== article.slug).slice(0, 2);

  return (
    <main className="relative">
      <Cursor />
      <Nav variant="dawn" />
      <ArticleReader article={article} others={others} />
    </main>
  );
}
