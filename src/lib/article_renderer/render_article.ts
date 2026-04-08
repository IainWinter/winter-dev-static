/*
    The goal of this file is to go from markdown format to a list of blocks.
    This should not be react nodes yet because this stuff should be able to be stored in a db.
    That means it should also be more of a mapping of source, so don't render code or equations yet.
*/

import { pysplit } from "../utils";
import type { ArticleBlock } from "./article_blocks";

type ArticleFunction = (args: string) => ArticleBlock;
type ArticleFunctionMap = Record<string, ArticleFunction>;

function splitArgs(args: string, count: number): string[] {
    return pysplit(args, ",", count).map((s: string) => s.trim());
}

const ARTICLE_FUNCTIONS: ArticleFunctionMap = {
    "sub-title2": (args: string) => ({
        type: "sub-title2",
        text: args
    }),

    "image": (args: string) => ({
        type: "image",
        src: args,
        half: false
    }),

    "image-half": (args: string) => ({
        type: "image",
        src: args,
        half: true
    }),

    "svg": (args: string) => ({
        type: "svg",
        src: args,
        half: false
    }),

    "svg-half": (args: string) => ({
        type: "svg",
        src: args,
        half: true
    }),

    "iframe": (args: string) => ({
        type: "iframe",
        src: args
    }),

    "iframe-youtube-video": (args: string) => ({
        type: "youtube",
        src: args
    }),

    "equation": (args: string) => ({
        type: "equation",
        latex: args,
        inline: false
    }),

    "equation-inline": (args: string) => ({
        type: "equation",
        latex: args,
        inline: true
    }),

    "br": () => ({
        type: "br"
    }),

    "title": (args: string) => {
        const id = args.split(" ", 1)[0];
        return {
            type: "title",
            id,
            text: args
        };
    },

    "sub-title": (args: string) => {
        const id = args.split(" ", 1)[0];
        return {
            type: "sub-title",
            id,
            text: args
        };
    },

    "link": (args: string) => {
        const [text, href] = splitArgs(args, 2);
        return {
            type: "link",
            text,
            href
        };
    },

    "code": (args: string) => {
        const [filename, language, code] = splitArgs(args, 3);

        return {
            type: "code",
            code,
            language,
            filename: filename.endsWith("_") ? undefined : filename
        };
    },

    "text-open": () => ({
        type: "text-open",
    }),

    "text-close": () => ({
        type: "text-close",
    }),

    "text": (args: string) => ({
        type: "text",
        text: args
    })
};

type ArticleToken = {
    type: string;
    beginIndex: number;
    endIndex: number;
};

function tokenize(text: string, startIndex: number, functions: ArticleFunctionMap): ArticleToken[] {
    const tokens: ArticleToken[] = [];

    let i = startIndex;
    let lastTextStart = i;
    let isTextOpen = false;

    const finishTextBlock = (end: number) => {
        if (lastTextStart < end) {
            isTextOpen = false;

            tokens.push({
                type: "text",
                beginIndex: lastTextStart,
                endIndex: end
            });

            tokens.push({
                type: "text-close",
                beginIndex: end,
                endIndex: end
            });
        }
    };

    while (i < text.length) {
        if (text[i] === "\n" || text[i] === '\r') {
            let j = i;
            while (j < text.length && text[j] === "\n" || text[j] === "\r") {
                j++;
            }

            if (j - i >= 2) {
                finishTextBlock(i);

                i = j;
                lastTextStart = j;
            }

            continue;
        }

        else if (text[i] === "[") {
            const startName = i + 1;
            const endName = text.indexOf("]", startName);

            if (endName !== -1 && text[endName + 1] === "(") {
                const funcName = text.slice(startName, endName);

                if (funcName in functions) {
                    let argStart = endName + 2;
                    let argEnd = argStart;
                    let parenCount = 1;

                    while (argEnd < text.length && parenCount > 0) {
                        if (text[argEnd] === "(") {
                            parenCount++;
                        }

                        else if (text[argEnd] === ")") {
                            parenCount--;
                        }
                        
                        argEnd++;
                    }

                    if (parenCount === 0) {
                        if (isTextOpen && i != lastTextStart) {
                            tokens.push({
                                type: "text",
                                beginIndex: lastTextStart,
                                endIndex: i
                            });
                        }

                        tokens.push({
                            type: funcName,
                            beginIndex: i,
                            endIndex: argEnd
                        });

                        i = argEnd;
                        lastTextStart = i;
                        
                        continue;
                    }
                }
            }
        }

        else if (!isTextOpen && text[i] !== ' ') {
            isTextOpen = true;
            tokens.push({
                type: "text-open",
                beginIndex: i,
                endIndex: i
            });
        }

        i++;
    }

    finishTextBlock(text.length);

    return tokens;
}

export function renderArticle(text: string): ArticleBlock[] {
    const headerDelimiterIndex = text.indexOf("---");
    const startIndex = headerDelimiterIndex === -1 ? 0 : headerDelimiterIndex + 3;
    const tokens = tokenize(text, startIndex, ARTICLE_FUNCTIONS);
    const out: ArticleBlock[] = [];

    for (const token of tokens) {
        const raw = text.slice(token.beginIndex, token.endIndex);

        let result: ArticleBlock | ArticleBlock[];

        if (token.type === "text") {
            result = {
                type: "text",
                text: raw
            };
        } else {
            const fn = ARTICLE_FUNCTIONS[token.type];

            const openParen = raw.indexOf("(");
            const closeParen = raw.lastIndexOf(")");

            const args =
                openParen !== -1 && closeParen !== -1 && closeParen > openParen
                    ? raw.slice(openParen + 1, closeParen)
                    : "";

            result = fn(args);
        }

        out.push(result);
    }

    return out;
}