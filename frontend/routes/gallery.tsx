import { GalleryElement, GalleryElementProps } from "../components/GalleryElement.tsx";
import { Badge } from "../components/Badge.tsx";

export default async function Gallery() {
    const FEATURES_DIRECTORY_PATH = "./static/features/";

    async function getFeatureNames(): Promise<string[]> {
        const featureNames = [];
        for await (const dirEntry of Deno.readDir(FEATURES_DIRECTORY_PATH)) {
            featureNames.push(dirEntry.name);
        }
        return featureNames;
    }

    async function getGifPathsForFeatureName(featureNamePath: string): Promise<{ featureNamePath: string, gifPaths: string[] }> {
        const gifNames = [];
        const gifsPath = `${featureNamePath}/gifs`;
        for await (const dirEntry of Deno.readDir(gifsPath)) {
            gifNames.push(dirEntry.name);
        }
        const gifPaths = gifNames.map(f => joinPath(gifsPath, f))
        return {
            featureNamePath,
            gifPaths
        };
    }

    function sanitizeFeatureName(featureName: string): string {
        return featureName.replaceAll("_", " ");
    }

    function joinPath(a: string, b: string): string {
        if (a.endsWith("/") == true) {
            return `${a}${b}`;
        }
        return `${a}/${b}`
    }

    const featureNames = await getFeatureNames();
    const sanitizedFeatureNames = featureNames.map(f => sanitizeFeatureName(f));
    const featureNamePaths = featureNames.map(f => joinPath(FEATURES_DIRECTORY_PATH, f))

    const galleryProps: GalleryElementProps[] = [];
    let index = 0;
    for await (const featureNamePath of featureNamePaths) {
        const result = await getGifPathsForFeatureName(featureNamePath);
        galleryProps.push({
            title: sanitizedFeatureNames[index],
            gifs: result.gifPaths
        });
        index += 1;
    }

    const galleryElements = galleryProps.map(prop => <GalleryElement title={prop.title} gifs={prop.gifs} />);

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
            {galleryElements}
        </>
    );
}
