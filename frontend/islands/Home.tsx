import { FileUpload } from "../islands/FileUpload.tsx";
import { useSignal } from "@preact/signals";
import { EnvConfig } from "../models/envConfig.ts";
import { Prediction } from "../models/prediction.ts";

type Props = {
    config: EnvConfig
}

export function Home({ config }: Props) {
    const selectedFile = useSignal<File | null>(null);
    const classifiction = useSignal<string>("");
    const hasClassification = useSignal<boolean>(false);
    const hasSelectedFile = useSignal<boolean>(false);
    let lastSelectedFileName = "";

    async function getPredicitonForPbFile(pbFile: File): Promise<Prediction> {
        const formData = new FormData();
        formData.append("file", pbFile);
        const response = await fetch(`${config.apiUrl}/predict_movement`, {
            method: "POST",
            body: formData
        });
        const result = await response.json();
        const prediction: Prediction = {
            classification: result["classification"]
        };
        return prediction;
    }

    const onFileSelected = async (f: File) => {
        if (f === null) {
            hasSelectedFile.value = false;
            return;
        }
        if (f.name === lastSelectedFileName) {
            return;
        }
        lastSelectedFileName = f.name;
        console.log(lastSelectedFileName, f.name)
        hasSelectedFile.value = true;
        hasClassification.value = false;
        const prediction = await getPredicitonForPbFile(f);
        classifiction.value = prediction.classification;
        hasClassification.value = true;
    }

    selectedFile.subscribe(async f => {

    })

    return (
        <>
            <FileUpload supportedFileType=".pb" onFileSelected={onFileSelected} />

            {
                hasSelectedFile.value === false && (<>
                    <h2 class="text-xl font-bold my-4 text-center">Please select a  file</h2>
                </>)
            }

            {
                hasSelectedFile.value && hasClassification.value === false && (<>
                    <div class="absolute top-0 left-0 h-full w-full flex flex-row justify-center items-center backdrop-blur">
                        <h2 class="text-xl font-bold my-4 text-center">Classification in Progress...</h2>
                    </div>
                </>)
            }
            {
                hasClassification.value && (<>
                    <h2 class="text-2xl font-bold my-4 text-center">Classification Result is {classifiction}</h2>
                </>)
            }
        </>
    );
};
