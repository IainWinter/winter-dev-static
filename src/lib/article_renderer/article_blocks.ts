export type ArticleTextBlockOpen = {
    type: 'text-open';
};

export type ArticleTextBlock = {
    type: 'text';
    text: string;
};

export type ArticleTextBlockClose = {
    type: 'text-close';
};

export type ArticleTitleBlock = {
    type: 'title';
    id: string;
    text: string;
};

export type ArticleSubTitleBlock = {
    type: 'sub-title';
    id: string;
    text: string;
};

export type ArticleSubTitle2Block = {
    type: 'sub-title2';
    text: string;
};

export type ArticleLinkBlock = {
    type: 'link';
    text: string;
    href: string;
};

export type ArticleImageBlock = {
    type: 'image';
    src: string;
    half: boolean;
};

export type ArticleSVGBlock = {
    type: 'svg';
    src: string;
    half: boolean;
};

export type ArticleIframeBlock = {
    type: 'iframe';
    src: string;
};

export type ArticleYouTubeBlock = {
    type: 'youtube';
    src: string;
};

export type ArticleCodeBlock = {
    type: 'code';
    code: string;
    language: string;
    filename?: string;
};

export type ArticleEquationBlock = {
    type: 'equation';
    latex: string;
    inline: boolean;
};

export type ArticleBreakBlock = {
    type: 'br';
};

export type ArticleBlock =
    | ArticleTextBlockOpen
    | ArticleTextBlock
    | ArticleTextBlockClose
    | ArticleTitleBlock
    | ArticleSubTitleBlock
    | ArticleSubTitle2Block
    | ArticleLinkBlock
    | ArticleImageBlock
    | ArticleSVGBlock
    | ArticleIframeBlock
    | ArticleYouTubeBlock
    | ArticleCodeBlock
    | ArticleEquationBlock
    | ArticleBreakBlock;