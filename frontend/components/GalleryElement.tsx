import { relative } from "https://deno.land/std@0.210.0/path/mod.ts";
import { Badge } from "./Badge.tsx";

type Props = {
    title: string;
    gifPath: string;
    previewImagePath: string;
    videoPath: string;
};

export function GalleryElement({ title, gifPath, previewImagePath, videoPath }: Props) {
    const pathRelativeToStaticDir = (path: string) => relative("static", path);

    return (
        <div class="rounded border flex flex-col p-2">
            <div class="flex flex-row justify-end">
                <a class="underline underline-offset-1 pr-2" href={pathRelativeToStaticDir(gifPath)} target="_blank">See Gif</a>
                <a class="underline underline-offset-1" href={pathRelativeToStaticDir(videoPath)} target="_blank">See Video</a>
            </div>
            <h2 class="text-lg text-center my-4 capitalize"><Badge text={title} /></h2>
            <img src={pathRelativeToStaticDir(previewImagePath)} />
        </div>
    );
}
