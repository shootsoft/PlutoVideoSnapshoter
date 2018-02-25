Pluto Video Snapshoter
====

# Features

- Automatically take snapshots for each slice of subtitles for a video with a given time range.
- Stitch snapshots into one image

# Usage

- Open the video
- Open srt file (optional, if the srt file doesn't have the same name of the video)
- Select output path (optional, if the output is different from video file's folder)
- Select time range (optional, default time range is 0:0:0 ~ video's duration time)
- Run task
- Concat snapshots

![Snapshot UI](doc/images/snapshot_ui.png)

![Snapshot UI](doc/images/snapshot_ui_stitching.png)

![Snapshot UI](doc/images/snapshot_ui_stitching_preview.png)


# Development

## Mac

Recommendation Python 3.4+

```
brew install qt5
brew link qt5 --force
sudo pip install -r requirements.txt
```

[Qt Designer](https://www.qt.io/download) is required for window UI design.

Running

```
python src/app.py
```

Building (not fully working yet)

```
python build.py
```


