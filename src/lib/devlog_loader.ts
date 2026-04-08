import { joinPath, listDirectory, loadFile, loadMetadata } from "./file_loader";

const REGOLITH_DIR = "regolith";

export type Devlog = {
    title: string;
    date: string;
    published: boolean;
    content: string;
};

function getDevlog(path: string): Devlog {
    const content = loadFile(joinPath(REGOLITH_DIR, path));

    return loadMetadata(content, (raw) => ({
        title: raw.title,
        date: raw.date ?? "",
        published: (raw.published ?? "true") === "true",
        content: content
    }));
}

export function getDevlogs(): Devlog[] {
    return listDirectory(REGOLITH_DIR)
        .map(f => getDevlog(f))
        .filter(d => d.published)
        .sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime());
}