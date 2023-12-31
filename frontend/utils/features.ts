import { join } from "https://deno.land/std@0.210.0/path/mod.ts";

const FEATURES_DIRECTORY_PATH = "./static/features/";

type FeatureNameToPathsMapping = {
  featureName: string;
  gifs: string[];
  previewImages: string[];
  videos: string[];
};

async function getFeatureNames(): Promise<string[]> {
  const featureNames = [];
  for await (const dirEntry of Deno.readDir(FEATURES_DIRECTORY_PATH)) {
    featureNames.push(dirEntry.name);
  }
  return featureNames;
}

async function getSanitizedFeatureNames(): Promise<string[]> {
  return (await getFeatureNames()).map((f) => sanitizeFeatureName(f));
}

async function getFeatureNamePaths(): Promise<string[]> {
  return (await getFeatureNames()).map((f) => join(FEATURES_DIRECTORY_PATH, f));
}

async function getFilesUnderPath(path: string) {
  const fileNames = [];
  for await (const dirEntry of Deno.readDir(path)) {
    fileNames.push(dirEntry.name);
  }
  const filePaths = fileNames.map((f) => join(path, f));
  return filePaths;
}

function sanitizeFeatureName(featureName: string): string {
  return featureName.replaceAll("_", " ");
}

export async function sanitizedFeatureNamesToPathsMapping(): Promise<
  FeatureNameToPathsMapping[]
> {
  const featureNamePaths = await getFeatureNamePaths();
  const sanitizedFeatureNames = await getSanitizedFeatureNames();
  const featureNamesToGifPathsMapping: FeatureNameToPathsMapping[] = [];
  let index = 0;
  for await (const featureNamePath of featureNamePaths) {
    const gifPaths = await getFilesUnderPath(`${featureNamePath}/gifs`);
    const previewImagePaths = await getFilesUnderPath(
      `${featureNamePath}/preview_images`,
    );
    const videoPaths = await getFilesUnderPath(
      `${featureNamePath}/video_overlays`,
    );
    featureNamesToGifPathsMapping.push({
      featureName: sanitizedFeatureNames[index],
      gifs: gifPaths,
      previewImages: previewImagePaths,
      videos: videoPaths,
    });
    index += 1;
  }

  return featureNamesToGifPathsMapping;
}
