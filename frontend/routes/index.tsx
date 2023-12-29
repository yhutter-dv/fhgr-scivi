import { Home } from "../islands/Home.tsx";

export default function Index() {
  return (
    <>
      <div class="px-4 py-8 mx-auto bg-slate-50">
        <div class="max-w-screen-md mx-auto flex flex-col items-center justify-center">
          <h2 class="text-2xl font-bold my-4">What is it?</h2>
          <h3 class="text-xl">A Tennis Move Recognizer powered by <a class="underline underline-offset-2 decoration-2 hover:text-sky-500 ease-in duration-150" href="https://en.wikipedia.org/wiki/Dynamic_time_warping" target="_blank">DTW</a></h3>
        </div>
      </div>
      <Home />
    </>
  );
}
