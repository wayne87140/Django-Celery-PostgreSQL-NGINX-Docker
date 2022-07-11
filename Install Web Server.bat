@ECHO OFF
FOR /D %%G in ("./WebServer_*") DO (SET folder_dir=%%G)
@ECHO on
docker-compose -f ./%folder_dir%/docker-compose.yml up -d --build
PAUSE