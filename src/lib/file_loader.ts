/*
    Load files and list files in content directory
*/

import fs from "fs";
import path from "path";

const CONTENT_DIR = path.join(process.cwd(), "src/content");

export function joinPath(root: string, sub: string): string {
    return path.join(root, sub);
}

function resolvePath(contentPath: string): string {
    return joinPath(CONTENT_DIR, contentPath);
}

export function listDirectory(directoryPath: string): string[] {
    const path = resolvePath(directoryPath);
    const files = fs.readdirSync(path);
    return files;
}

export function loadFile(filePath: string): string {
    const path = resolvePath(filePath);
    return fs.readFileSync(path, "utf-8");
}

function parseMetadataBlock(content: string): Record<string, string> {
    const delimiterIndex = content.indexOf("---");
    if (delimiterIndex === -1) {
        throw new Error("No metadata block found");
    }

    const metaBlock = content.substring(0, delimiterIndex);
    const lines = metaBlock.split("\n");

    const result: Record<string, string> = {};

    for (const line of lines) {
        const colonIndex = line.indexOf(":");
        if (colonIndex === -1) {
            continue;
        }

        const key = line.substring(0, colonIndex).trim();
        const value = line.substring(colonIndex + 1).trim();

        if (key.length === 0) {
            continue;
        }

        result[key] = value;
    }

    return result;
}

export function loadMetadata<T>(content: string, transform: (raw: Record<string, string>) => T): T {
    const raw = parseMetadataBlock(content);
    return transform(raw);
}