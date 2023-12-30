import { FileUpload } from "../islands/FileUpload.tsx";
import { useSignal } from "@preact/signals";
import { EnvConfig } from "../models/envConfig.ts";

type Props = {
    config: EnvConfig
}

export function Home({ config }: Props) {
    const selectedPbFile = useSignal<File | null>(null);
    const predictionResult = useSignal<string>("");

    async function getPredicitonForPbFile(pbFile: File): Promise<string> {

        const formData = new FormData();
        formData.append("file", pbFile);
        const response = await fetch(`${config.apiUrl}/predict_movement`, {
            method: "POST",
            body: formData
        });
        const prediction = response.json();
        return JSON.stringify(prediction);
    }

    selectedPbFile.subscribe(async f => {
        if (f === null) {
            return;
        }
        predictionResult.value = await getPredicitonForPbFile(f);
    })

    return (
        <>
            <FileUpload supportedFileType=".pb" selectedFile={selectedPbFile} />
            <h2 class="text-xl font-bold my-4 text-center">Prediction is ...</h2>
            <h2 class="text-2xl font-bold my-4 text-center">{predictionResult}</h2>
        </>
    );
};
