# youtube-downloader
Downloads YouTube videos in the desired quality.
# Installation:
## Source code
```ps1
cd $folderToInstall
git clone https://github.com/neonzada/youtube-downloader.git
```
## Dependencies:
```ps1
cd $folderToInstall/youtube-downloader
pip install -r ./dependencies.txt
```
# Usage
The program has to be executed within the `youtube-downloader/source` where all of its modules are located. So to run the program you need to:
```ps1
cd $folderToInstall/youtube-downloader/source
python main.py
```

- ## To change videos and audios output path:

    in the [main.py](./source/main.py) do the following changes:
    ```python
    # FROM:
    OUTPUT_VIDEO = path.join(getcwd(), "..", "videos")
    OUTPUT_AUDIO = path.join(getcwd(), "..", "audios")

    # TO:
    OUTPUT_VIDEO = r"your_desired_path_for_videos" 
    OUTPUT_AUDIO = r"your_desired_path_for_audios"
    ```
    The settings menu on the GUI is currently on development, so this is the current way to change it