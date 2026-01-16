CREATE DATABASE BDSpotPer
ON PRIMARY
(
    NAME = 'BDSpotPer_Primary',
    FILENAME = 'C:\SQLData\BDSpotPer_Primary.mdf',
    SIZE = 50MB,
    FILEGROWTH = 10MB
),
FILEGROUP FG_GENERALDATA
(
    NAME = 'BDSpotPer_Data1',
    FILENAME = 'C:\SQLData\BDSpotPer_Data1.ndf',
    SIZE = 100MB,
    MAXSIZE = 500MB,
    FILEGROWTH = 50MB
),
(
    NAME = 'BDSpotPer_Data2',
    FILENAME = 'C:\SQLData\BDSpotPer_Data2.ndf',
    SIZE = 100MB,
    MAXSIZE = 500MB,
    FILEGROWTH = 50MB
),
FILEGROUP FG_PLAYLISTS
(
    NAME = 'BDSpotPer_Playlists',
    FILENAME = 'C:\SQLData\BDSpotPer_Playlists.ndf',
    SIZE = 100MB,
    MAXSIZE = 300MB,
    FILEGROWTH = 50MB
)
LOG ON
(
    NAME = 'BDSpotPer_Log',
    FILENAME = 'C:\SQLData\BDSpotPer_Log.ldf',
    SIZE = 50MB,
    FILEGROWTH = 25MB
);