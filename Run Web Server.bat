@ECHO OFF
FOR /D %%G in ("./WebServer_*") DO (SET folder_dir=%%G)
@ECHO on
docker-compose -f ./%folder_dir%/docker-compose.yml -f ./%folder_dir%/docker-compose.prod.yml up -d
PAUSE