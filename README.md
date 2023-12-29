# Tennis Move Recognizer
The purpose of this project is to provide a model that can distinguish between different Tennis moves, henceforth the name `temovre` (Tennis Move Recognizer). The project was done in collaboration with the company Subsequent during the module Scientific Visuliazation @ FHGR.

## Explanation about Python Scripts
|Script|Purpose|
|---|------|
|create_gifs_and_video_overlays.py|Generates GIF Files from Matplotlib as well as Video Overlays where the individual keypoints are visible. In order for this to work please make sure that you have `ffmpeg` installed on your system.|

## Jupyter Notebook
In order to explore the data in more depth we have created a Jupyter Notebook in order to run it do the following commands:

### UNIX System (Linux and MacOS)
```bash
cd jupyter_notebooks
python -m venv ./venv
source venv/bin/activate.sh
pip install -r requirements.txt
python -m ipykernel install --user --name=venv
jupyter notebook ./
```

### Windows
```bash
cd jupyter_notebooks
python -m venv ./venv
.\venv\Scripts\Activate.bat
pip install -r requirements.txt
python -m ipykernel install --user --name=venv
jupyter notebook ./
```

Next a Browser Tab should open. Then you can select the Jupyter Notebook of your choice.

> Important: Please do not forget to select the installed `venv` as the kernel in order to utilize the installed virtual environment in the Jupyter Notebook.

## Frontend
The Frontend is build with the awesome [Deno Fresh Framework](https://fresh.deno.dev/). Therefore in order for things to work please make sure you have [Deno] (https://docs.deno.com/runtime/manual/getting_started/installation) installed.

After that to start up the frontend simply run:

```bash
cd frontend
deno task start
```

## Used Ressources
|Ressource|Description|
|---|------|
|[Dynamic Time Warping Tutorial Series](https://www.youtube.com/watch?v=ERKDHZyZDwA)|An awesome YouTube Tutorial Series which explains Dynamic Time Warping in more Detail.|