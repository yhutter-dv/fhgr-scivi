const FEATURES_DIRECTORY_PATH = "./static/features/";

type FeatureNameToPathsMapping = {
  featureName: string;
  gifs: string[];
  previewImages: string[];
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
  return (await getFeatureNames()).map((f) =>
    joinPath(FEATURES_DIRECTORY_PATH, f)
  );
}

async function getGifPathsForFeatureName(
  featureNamePath: string,
): Promise<{ featureNamePath: string; gifPaths: string[] }> {
  const gifNames = [];
  const gifsPath = `${featureNamePath}/gifs`;
  for await (const dirEntry of Deno.readDir(gifsPath)) {
    gifNames.push(dirEntry.name);
  }
  const gifPaths = gifNames.map((f) => joinPath(gifsPath, f));
  return {
    featureNamePath,
    gifPaths,
  };
}

function sanitizeFeatureName(featureName: string): string {
  return featureName.replaceAll("_", " ");
}

function joinPath(a: string, b: string): string {
  if (a.endsWith("/") == true) {
    return `${a}${b}`;
  }
  return `${a}/${b}`;
}

export async function sanitizedFeatureNamesToPathsMapping(): Promise<
  FeatureNameToPathsMapping[]
> {
  const featureNamePaths = await getFeatureNamePaths();
  const sanitizedFeatureNames = await getSanitizedFeatureNames();
  const featureNamesToGifPathsMapping: FeatureNameToPathsMapping[] = [];
  let index = 0;
  for await (const featureNamePath of featureNamePaths) {
    const result = await getGifPathsForFeatureName(featureNamePath);
    featureNamesToGifPathsMapping.push({
      featureName: sanitizedFeatureNames[index],
      gifs: result.gifPaths,
      previewImages: [],
    });
    index += 1;
  }

  return featureNamesToGifPathsMapping;
}
