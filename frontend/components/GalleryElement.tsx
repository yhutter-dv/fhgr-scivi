export type GalleryElementProps = {
    title: string;
    gifs: string[];
};

export function GalleryElement({ title, gifs }: GalleryElementProps) {
    const gifPathsRelativeToStaticDir = gifs.map(f => f.replace("./static/", ""));
    const gifElements = gifPathsRelativeToStaticDir.map(f => (
        <div class="rounded border">
            <img src={f} />
        </div>
    ));

    return (
        <div class="mx-1">
            <div class="text-2xl font-bold my-4 capitalize text-center">
                {title}
            </div>

            <div class="grid grid-cols-3 grid-flow-row gap-4 mt-4">
                {gifElements}
            </div>
        </div>
    );
}
