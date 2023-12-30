import { GalleryElement, GalleryElementProps } from "../components/GalleryElement.tsx";
import { Badge } from "../components/Badge.tsx";
import { sanitizedFeatureNamesToPathsMapping } from "../utils/features.ts";

export default async function Gallery() {

    const featureNamesToPathMapping = await sanitizedFeatureNamesToPathsMapping();
    const galleryProps: GalleryElementProps[] = featureNamesToPathMapping.map(f => {
        return { title: f.featureName, gifs: f.gifs, previewImages: f.previewImages, videos: f.videos };
    });


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
            {galleryProps.map(prop => <GalleryElement title={prop.title} gifs={prop.gifs} previewImages={prop.previewImages} videos={prop.videos} />)}
        </>
    );
}
