export type GalleryElementProps = {
    title: string;
    gifs: string[];
    previewImages: string[];
    videos: string[];
};

export function GalleryElement({ title, gifs, previewImages, videos }: GalleryElementProps) {
    const pathRelativeToStaticDir = (path: string) => path.replace("./static/", "");
    const elements = previewImages.map((previewImage, index) => {
        return {
            previewImage: pathRelativeToStaticDir(previewImage),
            gif: pathRelativeToStaticDir(gifs[index]),
            video: pathRelativeToStaticDir(videos[index])
        }
    });

    return (
        <div class="mx-1">
            <div class="text-2xl font-bold my-4 capitalize text-center">
                {title}
            </div>

            <div class="grid grid-cols-3 grid-flow-row gap-4 mt-4">
                {elements.map(e => (
                    <div class="rounded border flex flex-col p-2">
                        <div class="flex flex-row justify-end">
                            <a class="underline underline-offset-1 pr-2" href={e.gif} target="_blank">See Gif</a>
                            <a class="underline underline-offset-1" href={e.video} target="_blank">See Video</a>
                        </div>
                        <img src={e.previewImage} />
                    </div>
                ))}
            </div>
        </div>
    );
}
