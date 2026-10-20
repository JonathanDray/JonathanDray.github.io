@echo off
cd /d C:\dev\vela
set VELA_SCREENSHOT_RES=1600x900
set VELA_SCREENSHOT_SAMPLES=8
set OUT=%TEMP%\vela-shots
set VELA_HDRI=assets\hdri\kloofendal_partly_cloudy_2k.hdr
set VELA_SCREENSHOT=%OUT%\island.png
build\examples\island\island.exe
set VELA_SCREENSHOT=%OUT%\voxel.png
build\examples\voxel\voxel.exe
set VELA_HDRI=
set VELA_SCREENSHOT=%OUT%\snow.png
build\examples\snow\snow.exe
set VELA_SCREENSHOT=%OUT%\grass.png
build\examples\grass\grass.exe
