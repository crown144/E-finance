USE [master]
GO
/****** Object:  Database [MRP]    Script Date: 2023/10/12 16:18:14 ******/
CREATE DATABASE [MRP]
 CONTAINMENT = NONE
 ON  PRIMARY 
( NAME = N'MRP', FILENAME = N'C:\Program Files\Microsoft SQL Server\MSSQL16.MSSQLSERVER\MSSQL\DATA\MRP.mdf' , SIZE = 8192KB , MAXSIZE = UNLIMITED, FILEGROWTH = 65536KB )
 LOG ON 
( NAME = N'MRP_log', FILENAME = N'C:\Program Files\Microsoft SQL Server\MSSQL16.MSSQLSERVER\MSSQL\DATA\MRP_log.ldf' , SIZE = 8192KB , MAXSIZE = 2048GB , FILEGROWTH = 65536KB )
 WITH CATALOG_COLLATION = DATABASE_DEFAULT, LEDGER = OFF
GO
ALTER DATABASE [MRP] SET COMPATIBILITY_LEVEL = 160
GO
IF (1 = FULLTEXTSERVICEPROPERTY('IsFullTextInstalled'))
begin
EXEC [MRP].[dbo].[sp_fulltext_database] @action = 'enable'
end
GO
ALTER DATABASE [MRP] SET ANSI_NULL_DEFAULT OFF 
GO
ALTER DATABASE [MRP] SET ANSI_NULLS OFF 
GO
ALTER DATABASE [MRP] SET ANSI_PADDING OFF 
GO
ALTER DATABASE [MRP] SET ANSI_WARNINGS OFF 
GO
ALTER DATABASE [MRP] SET ARITHABORT OFF 
GO
ALTER DATABASE [MRP] SET AUTO_CLOSE OFF 
GO
ALTER DATABASE [MRP] SET AUTO_SHRINK OFF 
GO
ALTER DATABASE [MRP] SET AUTO_UPDATE_STATISTICS ON 
GO
ALTER DATABASE [MRP] SET CURSOR_CLOSE_ON_COMMIT OFF 
GO
ALTER DATABASE [MRP] SET CURSOR_DEFAULT  GLOBAL 
GO
ALTER DATABASE [MRP] SET CONCAT_NULL_YIELDS_NULL OFF 
GO
ALTER DATABASE [MRP] SET NUMERIC_ROUNDABORT OFF 
GO
ALTER DATABASE [MRP] SET QUOTED_IDENTIFIER OFF 
GO
ALTER DATABASE [MRP] SET RECURSIVE_TRIGGERS OFF 
GO
ALTER DATABASE [MRP] SET  DISABLE_BROKER 
GO
ALTER DATABASE [MRP] SET AUTO_UPDATE_STATISTICS_ASYNC OFF 
GO
ALTER DATABASE [MRP] SET DATE_CORRELATION_OPTIMIZATION OFF 
GO
ALTER DATABASE [MRP] SET TRUSTWORTHY OFF 
GO
ALTER DATABASE [MRP] SET ALLOW_SNAPSHOT_ISOLATION OFF 
GO
ALTER DATABASE [MRP] SET PARAMETERIZATION SIMPLE 
GO
ALTER DATABASE [MRP] SET READ_COMMITTED_SNAPSHOT OFF 
GO
ALTER DATABASE [MRP] SET HONOR_BROKER_PRIORITY OFF 
GO
ALTER DATABASE [MRP] SET RECOVERY FULL 
GO
ALTER DATABASE [MRP] SET  MULTI_USER 
GO
ALTER DATABASE [MRP] SET PAGE_VERIFY CHECKSUM  
GO
ALTER DATABASE [MRP] SET DB_CHAINING OFF 
GO
ALTER DATABASE [MRP] SET FILESTREAM( NON_TRANSACTED_ACCESS = OFF ) 
GO
ALTER DATABASE [MRP] SET TARGET_RECOVERY_TIME = 60 SECONDS 
GO
ALTER DATABASE [MRP] SET DELAYED_DURABILITY = DISABLED 
GO
ALTER DATABASE [MRP] SET ACCELERATED_DATABASE_RECOVERY = OFF  
GO
EXEC sys.sp_db_vardecimal_storage_format N'MRP', N'ON'
GO
ALTER DATABASE [MRP] SET QUERY_STORE = ON
GO
ALTER DATABASE [MRP] SET QUERY_STORE (OPERATION_MODE = READ_WRITE, CLEANUP_POLICY = (STALE_QUERY_THRESHOLD_DAYS = 30), DATA_FLUSH_INTERVAL_SECONDS = 900, INTERVAL_LENGTH_MINUTES = 60, MAX_STORAGE_SIZE_MB = 1000, QUERY_CAPTURE_MODE = AUTO, SIZE_BASED_CLEANUP_MODE = AUTO, MAX_PLANS_PER_QUERY = 200, WAIT_STATS_CAPTURE_MODE = ON)
GO
USE [MRP]
GO
/****** Object:  Table [dbo].[MRP]    Script Date: 2023/10/12 16:18:15 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[MRP](
	[父物料名称] [nchar](10) NULL,
	[子物料名称] [nchar](10) NULL,
	[调配方式] [nchar](10) NULL,
	[构成数] [int] NULL,
	[损耗率] [float] NULL,
	[工序库存] [int] NULL,
	[资产库存] [int] NULL,
	[作业提前期] [int] NULL,
	[配料提前期] [int] NULL,
	[供应商提前期] [int] NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[资产负债表]    Script Date: 2023/10/12 16:18:15 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[资产负债表](
	[序号] [nchar](20) NOT NULL,
	[资产类说明] [nchar](30) NOT NULL,
	[资产类方向] [nchar](10) NULL,
	[资产类汇总序号] [nchar](10) NULL,
	[变量名] [nchar](10) NULL
) ON [PRIMARY]
GO
USE [master]
GO
ALTER DATABASE [MRP] SET  READ_WRITE 
GO
