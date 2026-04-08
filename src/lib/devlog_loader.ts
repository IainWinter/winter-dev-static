import { joinPath, listDirectory, loadFile, loadMetadata } from "./file_loader";

const REGOLITH_DIR = "regolith";

export type Devlog = {
    title: string;
    date: string;
    content: string;
};

function getDevlog(path: string): Devlog {
    const content = loadFile(joinPath(REGOLITH_DIR, path));

    return loadMetadata(content, (raw) => ({
        title: raw.title,
        date: raw.date ?? "",
        content: content
    }));
}

export function getDevlogs(): Devlog[] {
    return listDirectory(REGOLITH_DIR)
        .map((f) => getDevlog(f))
        .sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime());
}