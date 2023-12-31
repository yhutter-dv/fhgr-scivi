import { GalleryElement } from "../components/GalleryElement.tsx";
import { Badge } from "../components/Badge.tsx";
import { sanitizedFeatureNamesToPathsMapping } from "../utils/features.ts";
import { SEP } from "https://deno.land/std@0.210.0/path/mod.ts";
export default async function Gallery() {

    const featureNamesToPathMapping = await sanitizedFeatureNamesToPathsMapping();
    const constructTitleFromPath = (path: string): string => {
        const pathParts = path.split(SEP)
        const lastPart = pathParts[pathParts.length - 1];
        const title = lastPart.replace("_", " ");
        return title;
    };

    return (
        <>
            <div class="px-4 py-8 mx-auto bg-slate-50">
                <div class="max-w-screen-md mx-auto flex flex-col items-center justify-center">
                    <h2 class="text-2xl font-bold my-4">Gallery</h2>
                    <h3 class="text-xl">
                        These Images have been generated with the help of the Script
                        <Badge text="create_gifs_and_overlays.py" />
                        Click on an image to open the corresponding GIF or Video file.
                    </h3>
                </div>
            </div>
            <div class="mx-1">
                {
                    featureNamesToPathMapping.map(f => (
                        <>
                            <div class="text-2xl font-bold my-4 capitalize text-center">
                                {f.featureName}
                            </div>

                            <div class="grid grid-cols-3 grid-flow-row gap-4 mt-4">
                                {
                                    f.previewImages.map((previewImage, index) =>
                                        <GalleryElement title={constructTitleFromPath(previewImage)} previewImagePath={previewImage} gifPath={f.gifs[index]} videoPath={f.videos[index]} />)
                                }
                            </div>
                        </>
                    ))
                }
            </div>
        </>
    );
}
