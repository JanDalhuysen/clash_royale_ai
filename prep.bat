@echo off
echo Preparing YOLO dataset folders...

REM Delete existing folders
rmdir /s /q train
rmdir /s /q test
rmdir /s /q valid

REM Create main folders
mkdir train
mkdir test
mkdir valid

REM Create images and labels subfolders
mkdir train\images
mkdir train\labels
mkdir test\images
mkdir test\labels
mkdir valid\images
mkdir valid\labels

REM Copy images to all sets
xcopy images_to_label\* train\images\ /E /I /Y
xcopy images_to_label\* test\images\ /E /I /Y
xcopy images_to_label\* valid\images\ /E /I /Y

REM Copy labels to all sets
xcopy labels\* train\labels\ /E /I /Y
xcopy labels\* test\labels\ /E /I /Y
xcopy labels\* valid\labels\ /E /I /Y

echo Done!
pause
