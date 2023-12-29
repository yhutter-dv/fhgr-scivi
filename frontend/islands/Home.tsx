import { FileUpload } from "../islands/FileUpload.tsx";
import { Badge } from "../components/Badge.tsx";

import { useSignal } from "@preact/signals";

export function Home() {
    const selectedPbFile = useSignal<File | null>(null);
    const predictionResult = useSignal<string>("");

    async function getPredicitonForPbFile(pbFile: File): Promise<string> {

        const formData = new FormData();
        formData.append("file", pbFile);
        const response = await fetch('http://localhost:6969/predict_movement', {
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
}
