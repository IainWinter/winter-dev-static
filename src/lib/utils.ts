export function partition<T>(array: T[], predicate: (item: T) => boolean) {
    const init: T[][] = [[], []];

    return array.reduce(([pass, fail], item) => {
        (predicate(item) ? pass : fail).push(item);
        return [pass, fail];
    }, init);
}

export function pysplit(str: string, sep: string, n: number) {
    const result = [];
    let start = 0;

    for (let i = 1; i < n; i++) {
        const idx = str.indexOf(sep, start);
        if (idx === -1) break; // no more separators
        result.push(str.slice(start, idx));
        start = idx + sep.length;
    }

    result.push(str.slice(start)); // rest of the string as last element
    return result;
}

export function themeValue<T>(theme: string, light: T, dark: T) {
    return theme === 'light' ? light : dark;
}