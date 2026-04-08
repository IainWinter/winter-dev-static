import { joinPath, listDirectory, loadFile, loadMetadata } from "./file_loader";

const ARTICLES_DIR = "articles";

export type ArticleMetadata = {
    slug: string;
    thumbnail?: string;
    title: string;
    date: string;
};

export type ArticleSlug = {
    slug: string;
};

function getArticleMetadata(path: string): ArticleMetadata {
    const slug = path.substring(0, path.length - 3);
    const content = loadFile(joinPath(ARTICLES_DIR, path));

    return loadMetadata(content, (raw) => ({
        slug: `articles/${slug}`,
        title: raw.title,
        thumbnail: raw.thumbnail ?? null,
        date: raw.date ?? "",
    }));
}

export function getArticles(): ArticleMetadata[] {
    return listDirectory(ARTICLES_DIR)
        .map((f) => getArticleMetadata(f))
        .sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime());
}

export function getArticleSlugs(): ArticleSlug[] {
    return listDirectory(ARTICLES_DIR)
        .map((f) => ({ slug: f.substring(0, f.length - 3) }));
}

export function getArticleBySlug(articleSlug: string): string {
    return loadFile(joinPath(ARTICLES_DIR, `${articleSlug}.md`));
}