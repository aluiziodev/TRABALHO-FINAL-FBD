CREATE DATABASE BDSpotPer
ON PRIMARY
(
    NAME = 'BDSpotPer_Primary',
    FILENAME = '/var/opt/mssql/data/BDSpotPer_Primary.mdf',
    SIZE = 50MB,
    FILEGROWTH = 10MB
),
FILEGROUP FG_GENERALDATA
(
    NAME = 'BDSpotPer_Data1',
    FILENAME = '/var/opt/mssql/data/BDSpotPer_Data1.ndf',
    SIZE = 100MB,
    MAXSIZE = 500MB,
    FILEGROWTH = 50MB
),
(
    NAME = 'BDSpotPer_Data2',
    FILENAME = '/var/opt/mssql/data/BDSpotPer_Data2.ndf',
    SIZE = 100MB,
    MAXSIZE = 500MB,
    FILEGROWTH = 50MB
),
FILEGROUP FG_PLAYLISTS
(
    NAME = 'BDSpotPer_Playlists',
    FILENAME = '/var/opt/mssql/data/BDSpotPer_Playlists.ndf',
    SIZE = 100MB,
    MAXSIZE = 300MB,
    FILEGROWTH = 50MB
)
LOG ON
(
    NAME = 'BDSpotPer_Log',
    FILENAME = '/var/opt/mssql/data/BDSpotPer_Log.ldf',
    SIZE = 50MB,
    FILEGROWTH = 25MB
);