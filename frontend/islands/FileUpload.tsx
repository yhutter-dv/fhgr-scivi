import { Badge } from "../components/Badge.tsx";
import { Signal } from "@preact/signals";

type Props = {
    supportedFileType: string;
    selectedFile: Signal<File | null>;
};


export function FileUpload({ supportedFileType, selectedFile }: Props) {

    function onFileChanged(event: Event) {
        const target = event.target as HTMLInputElement;
        if (target.files && target.files.length > 0) {
            selectedFile.value = target.files[0];
        }
    }

    return (
        <div class="flex flex-column justify-center">
            <div class="mx-4 my-8 px-4 py-8 border-2 border-dotted w-full text-center hover:bg-slate-100 ease-in duration-150">
                <p class="text-xl font-bold mb-4">Click Button below and select your <Badge text={`${supportedFileType} file`} /></p>
                <input onChange={onFileChanged} id="file-upload" type="file" class="file:bg-neutral-100 file:px-3 file:py-1 file:rounded hover:file:cursor-pointer" accept={supportedFileType} />
            </div>
        </div>
    );
}