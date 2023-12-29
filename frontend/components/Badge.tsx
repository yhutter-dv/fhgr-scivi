type Props = {
    text: string;
};

export function Badge({ text }: Props) {

    return (
        <span class="text-sm font-bold inline-block bg-green-200 rounded px-2 mx-2">
            {text}
        </span>
    );
}