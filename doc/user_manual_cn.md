视频截图字幕拼接精灵使用说明
==============
本软件运行需要系统安装相应的视频解码类库，推荐 K-Lite Codec Pack http://www.codecguide.com/download_kl.htm

软件特点：

- 多平台 （macOS/Windows/Linux）
- 视频手动截图
- 视频依据字幕自动截图
- 自动检测字幕区域
- 允许单张批量图片手动调整字幕区域
- 截图拼接一气呵成

视频截图字幕拼接精灵是一款能够在多个平台下使用的视频截图软件，本软件同时集成了依据字幕截图，图片字幕区域自动识别功能。能够将多张带有字幕的截图拼接成一张完整图片。效果如图:
![预览](images/snapshot_ui_stitching_preview.png)

## 启动应用

1. Windows下启动。
![Launch](images/usage/screenshot_exe.png)
1. macOS下启动。
![Launch](images/usage/screenshot_app.png)

## 使用说明

1. 打开视频。
![Open a video](images/usage/screenshot_open.png)
1. (可选) 选择截图存放路径。
![Output folder](images/usage/screenshot_output.png)
1. (可选, 针对`Auto Snapshots`，这个是必选) 打开字幕文件 (*.srt). 如果字幕文件与视频文件是相同的文件名，这个字幕文件会被自动加载。注意：本软件现阶段并不支持渲染字幕到视频或者截屏上。
![Open srt file](images/usage/screenshot_srt.png)
1. 播放视频或者手动截图（当视频被打开之后会立刻开始自动播放，此时，播放按钮会变成暂停，单机视频区域也可以播放或者暂停视频)。
![Play](images/usage/screenshot_play.png)
![Single snapshot](images/usage/screenshot_single.png)
1. 选择 `Start` 和 `End`, 之后就可以通过点击`Auto Anapshot`针对有字幕的每一帧自动进行截屏。
![Task](images/usage/screenshot_task.png)
1. 跳转到`Image Stitching`。
![Jump](images/usage/screenshot_jump.png)
1. 选择视频字幕上下区域。
![Up and Down limit](images/usage/screenshot_updown.png)
1. 预览拼接效果。
![Jump](images/usage/screenshot_preview.png)
1. 保存拼接的图片。
![Save](images/usage/screenshot_save.png)

## 高级

1. 字幕区域自动识别。
![Save](images/auto_detection/subtitle_auto_detection.png)
1. 预览/保存选择性拼接。
![Save](images/usage/screenshot_preview_selected.png)

