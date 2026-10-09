-- Creates a cleaned marketing engagement view for Power BI analysis.
-- The view standardizes content types, separates combined views and clicks,
-- formats engagement dates, and removes newsletter content that is not
-- relevant to the marketing engagement analysis.

CREATE VIEW dbo.fact_engagement
AS

-- Query to clean and normalize the engagement_data table

SELECT 
    EngagementID,  -- Selects the unique identifier for each engagement record
    ContentID,  -- Selects the unique identifier for each piece of content
	CampaignID,  -- Selects the unique identifier for each marketing campaign
    ProductID,  -- Selects the unique identifier for each product
    UPPER(REPLACE(ContentType, 'Socialmedia', 'Social Media')) AS ContentType,  -- Replaces "Socialmedia" with "Social Media" and then converts all ContentType values to uppercase
    LEFT(ViewsClicksCombined, CHARINDEX('-', ViewsClicksCombined) - 1) AS Views,  -- Extracts the Views part from the ViewsClicksCombined column by taking the substring before the '-' character
    RIGHT(ViewsClicksCombined, LEN(ViewsClicksCombined) - CHARINDEX('-', ViewsClicksCombined)) AS Clicks,  -- Extracts the Clicks part from the ViewsClicksCombined column by taking the substring after the '-' character
    Likes,  -- Selects the number of likes the content received
    -- Converts the EngagementDate to the dd.mm.yyyy format
    FORMAT(CONVERT(DATE, EngagementDate), 'dd.MM.yyyy') AS EngagementDate  -- Converts and formats the date as dd.MM.yyyy
FROM 
    dbo.engagement_data  -- Specifies the source table from which to select the data
WHERE 
    ContentType != 'Newsletter';  -- Filters out rows where ContentType is 'Newsletter' as these are not relevant for our analysis