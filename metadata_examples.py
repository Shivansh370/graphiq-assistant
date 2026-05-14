examples = [
    {
        "question": "Which are the Top 5 SQL Columns used in most different reports?",
        "query":
"""MATCH (:SSRSReport)-[:HAS_COLUMN]->(c:SQLColumn)
RETURN c.SQLColumnName, COUNT(*) AS ReportsCount
ORDER BY ReportsCount DESC
LIMIT 5
""",
    },
    {
        "question": "What is the definition of 'Active Flag'?",
        "query":
"""MATCH (t:Term)-[:HAS_DEFINITION]->(d:Definition),
      (t)-[:HAS_CATEGORY]->(tc:TermCategory),
      (tc)-[:HAS_FUNCTIONAL_AREA]->(tfa:TermFunctionalArea),
      (tfa)-[:HAS_BUSINESS_SEGMENT]->(tb:BusinessSegment)
WHERE t.termName = 'Active Flag' AND d.termDefinition IS NOT NULL
RETURN t.termName AS Term,
       d.termDefinition AS Description,
       tc.termCategory AS Category,
       tfa.termFunctinoalArea AS FunctionalArea,
       tb.termBusinessSegment AS BusinessSegment;

""",
    },
    {
        "question": "Which Reports are related to the term 'Client Id'?",
        "query":
"""MATCH (r:SSRSReport)-[:HAS_COLUMN]->(c:SQLColumn)-[:MATCH_TERM]->(t:Term)
WHERE t.termName = 'Client Id'
RETURN r.reportName
""",
    },
    {
        "question": "Which are all the definition for the term 'Active Flag'?",
        "query":
"""MATCH (t:Term)-[:HAS_DEFINITION]->(d:Definition),
      (t)-[:HAS_CATEGORY]->(tc:TermCategory),
      (tc)-[:HAS_FUNCTIONAL_AREA]->(tfa:TermFunctionalArea),
      (tfa)-[:HAS_BUSINESS_SEGMENT]->(tb:BusinessSegment)
WHERE t.termName = 'Active Flag' AND d.termDefinition IS NOT NULL
RETURN t.termName AS Term,
       d.termDefinition AS Description,
       tc.termCategory AS Category,
       tfa.termFunctinoalArea AS FunctionalArea,
       tb.termBusinessSegment AS BusinessSegment;

""",
    },
    {
        "question": "Which is the Category with most terms associated and how many?",
        "query":
"""MATCH (c:TermCategory)-[:HAS_TERM]->(t:Term)
RETURN c.termCategory AS Category, count(t) AS TermsCount
ORDER BY TermsCount DESC
LIMIT 1
""",
    },
    {
        "question": "Which is the Table with the most Columns?",
        "query":
"""MATCH (t:SQLTable)-[:HAS_COLUMN]-(c: SQLColumn)
WITH t.id AS id, t.name AS name, t.type AS type, count(c) AS TotalColumns
RETURN id, name, type, TotalColumns
ORDER BY TotalColumns DESC
""",
    },
    {
        "question": "Which is the report with most terms associated?",
        "query":
"""MATCH (r:SSRSReport)-[:HAS_COLUMN]->(c:SQLColumn)-[:MATCH_TERM]->(t:Term)
RETURN r.reportName, COUNT(t) AS TermsCount
ORDER BY TermsCount DESC
LIMIT 1
""",
    },
    {
        "question": "Show me opportunities to consolidate reports in the functional area RDM",
        "query":
"""MATCH (r:SSRSReport)-[:HAS_COLUMN]->(col:SQLColumn)-[:MATCH_TERM]->(:Term)-[:HAS_CATEGORY]->(:TermCategory)-[:HAS_FUNCTIONAL_AREA]->(fa:TermFunctionalArea)
WHERE fa.termFunctionalArea = 'RDM'
WITH r, collect(DISTINCT(col.SQLColumnName)) as ReportColumns
WITH r, ReportColumns
MATCH (r)-[c:HAS_COLUMN]->(col:SQLColumn)
WITH COUNT(DISTINCT(col)) AS numOfColumns, ReportColumns, r
WITH ReportColumns ,collect({{reportName: r.reportName, reportLocation: r.reportLocation, numberOfColumns: numOfColumns, overlapRatio: (size(ReportColumns) * 1.00) / numOfColumns}}) AS report_cluster
WHERE size(report_cluster) > 1 AND size(ReportColumns) > 1
WITH report_cluster, ReportColumns
UNWIND report_cluster as report
WITH avg(report.overlapRatio) as averageOverlapRatio, COLLECT(report) as report_cluster, ReportColumns
RETURN {{averageOverlapRatio: averageOverlapRatio, reports: report_cluster}} as GroupOfReportsToConsolidate, {{sharedColumns: ReportColumns, amountOfSharedColumns: size(ReportColumns)}} as SharedColumnsBetweenReports
ORDER BY GroupOfReportsToConsolidate.averageOverlapRatio DESC
LIMIT 5;
""",
    },
    {
        "question": "What are similar terms to Inspection?",
        "query":
"""MATCH (term1: Term)-[:MATCH_SQL_COLUMN]->(col:SQLColumn)<-[:MATCH_SQL_COLUMN]-(term2: Term)
WHERE term1.termName = 'Inspection' AND term1 <> term2
WITH term1, term2, COLLECT(col) AS sharedColumns
WHERE size(sharedColumns) > 1
UNWIND sharedColumns as col
MATCH (col)<-[:HAS_COLUMN]-(report: SSRSReport)
WITH term1, term2, COLLECT({{column: col.SQLColumnName, report: report.reportName, reportLocation: report.reportLocation}}) as columnReports
MATCH (term1)-[:HAS_CATEGORY]-(tc:TermCategory)-[:HAS_FUNCTIONAL_AREA]-(fa:TermFunctionalArea)-[:HAS_BUSINESS_SEGMENT]-(bs:BusinessSegment)
MATCH (term2)-[:HAS_CATEGORY]-(tc:TermCategory)-[:HAS_FUNCTIONAL_AREA]-(fa:TermFunctionalArea)-[:HAS_BUSINESS_SEGMENT]-(bs:BusinessSegment)
MATCH (term1)-[:HAS_DEFINITION]-(d1:Definition)
MATCH (term2)-[:HAS_DEFINITION]-(d2:Definition)
RETURN term1.termName as Term1, d1.termDefinition as Term1Definition, tc.termCategory as Term1Category, fa.termFunctionalArea as term1FunctionalArea, bs.termBusinessSegment as Term1BusinessSegment,
term2.termName as Term2, d2.termDefinition as Term2Definition, tc.termCategory as Term2Category, fa.termFunctionalArea as term2FunctionalArea, bs.termBusinessSegment as Term2BusinessSegment, size(columnReports) as OverlapColumnsCount, OverlapcolumnReports
ORDER BY OverlapCount DESC
""",
    },
    {
        "question": "Show me some reports that include the term Private Label. What other terms are being repeated among these reports?",
        "query":
"""MATCH (r:SSRSReport)-[:HAS_COLUMN]->(col:SQLColumn)-[:MATCH_TERM]->(t:Term)-[:HAS_CATEGORY]->(tc: TermCategory)
WHERE tc.termCategory = 'Claim' AND t.termName = 'Private Label'
MATCH (r)-[:HAS_COLUMN]->(col2:SQLColumn)-[:MATCH_TERM]->(otherTerm:Term)
WHERE otherTerm <> t
RETURN r.reportName AS report, r.reportLocation as reportLocation, COLLECT(DISTINCT otherTerm.termName) AS commonTerms
LIMIT 10
""",
    },
    {
        "question": "Show me opportunities to consolidate reports in the functional area Customer Care",
        "query":
"""MATCH (r:SSRSReport)-[:HAS_COLUMN]->(col:SQLColumn)-[:MATCH_TERM]->(:Term)-[:HAS_CATEGORY]->(:TermCategory)-[:HAS_FUNCTIONAL_AREA]->(fa:TermFunctionalArea)
WHERE fa.termFunctionalArea = 'Customer Care'
WITH r, collect(DISTINCT(col.SQLColumnName)) as ReportColumns
WITH r, ReportColumns
MATCH (r)-[c:HAS_COLUMN]->(col:SQLColumn)
WITH COUNT(DISTINCT(col)) AS numOfColumns, ReportColumns, r
WITH ReportColumns ,collect({{reportName: r.reportName, reportLocation: r.reportLocation, numberOfColumns: numOfColumns, overlapRatio: (size(ReportColumns) * 1.00) / numOfColumns}}) AS report_cluster
WHERE size(report_cluster) > 1 AND size(ReportColumns) > 1
WITH report_cluster, ReportColumns
UNWIND report_cluster as report
WITH avg(report.overlapRatio) as averageOverlapRatio, COLLECT(report) as report_cluster, ReportColumns
RETURN {{averageOverlapRatio: averageOverlapRatio, reports: report_cluster}} as GroupOfReportsToConsolidate, {{sharedColumns: ReportColumns, amountOfSharedColumns: size(ReportColumns)}} as SharedColumnsBetweenReports
ORDER BY GroupOfReportsToConsolidate.averageOverlapRatio DESC
LIMIT 5;
""",
    },
    {
        "question": "What are some reports that contain the term Ivr Bypass?",
        "query":
"""MATCH (report:SSRSReport)-[:HAS_COLUMN]->(column:SQLColumn)-[:MATCH_TERM]->(term:Term)-[:HAS_CATEGORY]->(category:TermCategory)-[:HAS_FUNCTIONAL_AREA]->(fa:TermFunctionalArea)-[:HAS_BUSINESS_SEGMENT]->(bs:BusinessSegment)
WHERE term.termName = 'Ivr Bypass'
RETURN term.termName as TermName, category.termCategory as TermCategory, fa.termFunctionalArea as TermFunctionalArea, bs.termBusinessSegment as TermBusinessSegment, report.reportName as ReportName, report.reportLocation as ReportLocatio
""",
    },
    {
        "question": "What is the definition for the term Active Flag?",
        "query":
"""MATCH (t:Term)-[:HAS_DEFINITION]->(d:Definition), (t)-[:HAS_CATEGORY]-(tc:TermCategory)-[:HAS_FUNCTIONAL_AREA]-(tfa:TermFunctionalArea)-[:HAS_BUSINESS_SEGMENT]-(tb:BusinessSegment)
WHERE t.termName = 'Active Flag' AND d.termDefinition IS NOT NULL
RETURN t.termName, d.termDefinition, tc.termCategory, tfa.termFunctionalArea, tb.termBusinessSegment;
""",
    },
    {
        "question": "What is the definition for the term Active Flag under Loss Draft?",
        "query":
"""MATCH (t:Term)-[:HAS_DEFINITION]->(d:Definition), (t)-[:HAS_CATEGORY]-(tc:TermCategory)-[:HAS_FUNCTIONAL_AREA]-(tfa:TermFunctionalArea)-[:HAS_BUSINESS_SEGMENT]-(tb:BusinessSegment)
WHERE t.termName = 'Active Flag' AND d.termDefinition IS NOT NULL AND tc.termCategory = 'Loss Draft'
RETURN t.termName, d.termDefinition, tc.termCategory, tfa.termFunctionalArea, tb.businessSegment
""",
    },
    {
        "question": "What is the definition for the term Active Flag under Global Home",
        "query":
"""MATCH (t:Term)-[:HAS_DEFINITION]->(d:Definition), (t)-[:HAS_CATEGORY]-(tc:TermCategory)-[:HAS_FUNCTIONAL_AREA]-(tfa:TermFunctionalArea)-[:HAS_BUSINESS_SEGMENT]-(tb:BusinessSegment)
WHERE t.termName = 'Active Flag' AND d.termDefinition IS NOT NULL AND tb.termBusinessSegment = 'Global Home'
RETURN t.termName, d.termDefinition, tc.termCategory, tfa.termFunctionalArea, tb.termBusinessSegment
""",
    },
    {
        "question": "What is the definition for the term Active Flag under Enterprise",
        "query":
"""MATCH (t:Term)-[:HAS_DEFINITION]->(d:Definition), (t)-[:HAS_CATEGORY]-(tc:TermCategory)-[:HAS_FUNCTIONAL_AREA]-(tfa:TermFunctionalArea)-[:HAS_BUSINESS_SEGMENT]-(tb:BusinessSegment)
WHERE t.termName = 'Active Flag' AND d.termDefinition IS NOT NULL AND tb.termBusinessSegment = 'Enterprise'
RETURN t.termName, d.termDefinition, tc.termCategory, tfa.termFunctionalArea, tb.termBusinessSegment
""",
    },
    {
        "question": "How many reports are related to the term Reason Code?",
        "query":
"""MATCH (t:Term)-[:MATCH_SQL_COLUMN]->(col:SQLColumn)-[:HAS_REPORT]->(r:SSRSReport)
WHERE t.termName = 'Reason Code'
WITH COLLECT([r.reportName, col.SQLColumnName]) as reports
RETURN reports, size(reports) as TotalNumberOfReports
""",
    },
    {
        "question": "What are some reports that contain the term Insco Name?s",
        "query":
"""MATCH (report:SSRSReport)-[:HAS_COLUMN]->(column:SQLColumn)-[:MATCH_TERM]->(term:Term)-[:HAS_CATEGORY]->(category:TermCategory)-[:HAS_FUNCTIONAL_AREA]->(fa:TermFunctionalArea)-[:HAS_BUSINESS_SEGMENT]->(bs:BusinessSegment)
WHERE term.termName = 'Insco Name'
RETURN term.termName as TermName, category.termCategory as TermCategory, fa.termFunctionalArea as TermFunctionalArea, bs.termBusinessSegment as TermBusinessSegment, report.reportName as ReportName, report.reportLocation as ReportLocation
""",
    },
    {
        "question": "What are some reports that contain the term Borrower?",
        "query":
"""MATCH (report:SSRSReport)-[:HAS_COLUMN]->(column:SQLColumn)-[:MATCH_TERM]->(term:Term)-[:HAS_CATEGORY]->(category:TermCategory)-[:HAS_FUNCTIONAL_AREA]->(fa:TermFunctionalArea)-[:HAS_BUSINESS_SEGMENT]->(bs:BusinessSegment)
WHERE term.termName = 'Borrower'
RETURN term.termName as TermName, category.termCategory as TermCategory, fa.termFunctionalArea as TermFunctionalArea, bs.termBusinessSegment as TermBusinessSegment, report.reportName as ReportName, report.reportLocation as ReportLocation
""",
    },
    {
        "question": "What are some terms mentioned in the report HYLA_Performance_Report and what are their meanings?",
        "query":
"""MATCH (r:SSRSReport {reportName: 'HYLA_Performance_Report'})-[:HAS_COLUMN]->(c:SQLColumn)-[:MATCH_TERM]->(t:Term)-[:HAS_DEFINITION]->(d:Definition)
RETURN r.reportName as reportName, t.termName AS Term, d.termDefinition AS Definition;
""",
    },
    {
        "question": "In which tables I can find the term Service Level?",
        "query":
"""MATCH (t:Term {termName: 'Service Level'})-[:MATCH_SQL_COLUMN]->(c:SQLColumn)-[:HAS_TABLE]->(table:SQLTable)-[:HAS_DATABASE]->(database:SQLDatabase)-[:HAS_SERVER]->(server:SQLServer)
RETURN t.termName as term, table.objectName AS TableName, table.objectType as Type, database.databaseName as DatabaseName, server.serverName as ServerName
""",
    },
    {
        "question": "Suggest me reports that might be related to SMS Claim Texting Report",
        "query":
"""MATCH (r1:SSRSReport)-[:HAS_COLUMN]->(col:SQLColumn)-[:MATCH_TERM]->(t:Term)<-[:MATCH_TERM]-(col2:SQLColumn)<-[:HAS_COLUMN]-(r2:SSRSReport)
WHERE r1.reportName = 'SMS Claims Texting Report' AND r1 <> r2
WITH r1, r2, COLLECT(DISTINCT(t)) AS sharedTerms
WHERE size(sharedTerms) > 4
UNWIND sharedTerms as term
MATCH (term)-[:HAS_CATEGORY]-(tc:TermCategory)-[:HAS_FUNCTIONAL_AREA]-(fa:TermFunctionalArea)-[:HAS_BUSINESS_SEGMENT]-(bs:BusinessSegment)
WITH r1, r2, COLLECT({{term: term.termName, termCategory: tc.termCategory, termFunctionalArea: fa.termFunctionalArea, termBusinessSegment: bs.termBusinessSegment}}) as sharedTerms
RETURN r1.reportName as report1Name, r1.reportLocation as report1Location, r2.reportName as report2Name, r2.reportLocation as report2Location, size(sharedTerms) as amountOverlapTermsBetweenReports, sharedTerms
ORDER BY amountOverlapTermsBetweenReports DESC
LIMIT 5;
""",
    },
    {
        "question": "In which Tables does the term Peril appears?",
        "query":
"""MATCH (t:Term {termName: 'Peril'})-[:MATCH_SQL_COLUMN]->(c:SQLColumn)-[:HAS_TABLE]->(table:SQLTable)-[:HAS_DATABASE]->(database:SQLDatabase)-[:HAS_SERVER]->(server:SQLServer)
RETURN t.termName as Term, table.objectName AS TableName, table.objectType as Type, database.databaseName as DatabaseName, server.serverName as ServerName
""",
    },
    {
        "question": "How many claims have the 'Claim Event Status PK' as 'Sent To Open'?",
        "query":
"""MATCH (c: Claim)
WHERE c.claimEventStatusSK = 'Sent To Open'
RETURN count(c) AS SentToOpenClaims
""",
    },
    {
        "question": "What are some reports that contain the term UPB?",
        "query":
"""MATCH (report:SSRSReport)-[:HAS_COLUMN]->(column:SQLColumn)-[:MATCH_TERM]->(term:Term)-[:HAS_CATEGORY]->(category:TermCategory)-[:HAS_FUNCTIONAL_AREA]->(fa:TermFunctionalArea)-[:HAS_BUSINESS_SEGMENT]->(bs:BusinessSegment)
WHERE term.termName = 'UPB'
RETURN term.termName as TermName, category.termCategory as TermCategory, fa.termFunctionalArea as TermFunctionalArea, bs.termBusinessSegment as TermBusinessSegment, report.reportName as ReportName, report.reportLocation as ReportLocation
""",
    },
    {
        "question": "What are some reports that contain the term Is LPI?",
        "query":
"""MATCH (report:SSRSReport)-[:HAS_COLUMN]->(column:SQLColumn)-[:MATCH_TERM]->(term:Term)-[:HAS_CATEGORY]->(category:TermCategory)-[:HAS_FUNCTIONAL_AREA]->(fa:TermFunctionalArea)-[:HAS_BUSINESS_SEGMENT]->(bs:BusinessSegment)
WHERE term.termName = 'Is LPI'
RETURN term.termName as TermName, category.termCategory as TermCategory, fa.termFunctionalArea as TermFunctionalArea, bs.termBusinessSegment as TermBusinessSegment, report.reportName as ReportName, report.reportLocation as ReportLocation
""",
    },
    {
        "question": "Show reports that I should consider merging. explain why",
        "query":
"""MATCH (r:SSRSReport)-[:HAS_COLUMN]->(col:SQLColumn)-[:MATCH_TERM]->(:Term)-[:HAS_CATEGORY]->(:TermCategory)-[:HAS_FUNCTIONAL_AREA]->(fa:TermFunctionalArea)
WHERE fa.termFunctionalArea = 'Loss Draft'
WITH r, collect(DISTINCT(col.SQLColumnName)) as ReportColumns
WITH r, ReportColumns
MATCH (r)-[c:HAS_COLUMN]->(col:SQLColumn)
WITH COUNT(DISTINCT(col)) AS numOfColumns, ReportColumns, r
WITH ReportColumns ,collect({{reportName: r.reportName, reportLocation: r.reportLocation, numberOfColumns: numOfColumns, overlapRatio: (size(ReportColumns) * 1.00) / numOfColumns}}) AS report_cluster
WHERE size(report_cluster) > 1 AND size(ReportColumns) > 1
WITH report_cluster, ReportColumns
UNWIND report_cluster as report
WITH avg(report.overlapRatio) as averageOverlapRatio, COLLECT(report) as report_cluster, ReportColumns
RETURN {{averageOverlapRatio: averageOverlapRatio, reports: report_cluster}} as GroupOfReportsToConsolidate, {{sharedColumns: ReportColumns, amountOfSharedColumns: size(ReportColumns)}} as SharedColumnsBetweenReports
ORDER BY GroupOfReportsToConsolidate.averageOverlapRatio DESC
LIMIT 5;
""",
    },
    {
        "question": "Suggest reports that could be consolidated in the functional area Loss Draft",
        "query":
"""MATCH (r:SSRSReport)-[:HAS_COLUMN]->(col:SQLColumn)-[:MATCH_TERM]->(:Term)-[:HAS_CATEGORY]->(:TermCategory)-[:HAS_FUNCTIONAL_AREA]->(fa:TermFunctionalArea)
WHERE fa.termFunctionalArea = 'Loss Draft'
WITH r, collect(DISTINCT(col.SQLColumnName)) as ReportColumns
WITH r, ReportColumns
MATCH (r)-[c:HAS_COLUMN]->(col:SQLColumn)
WITH COUNT(DISTINCT(col)) AS numOfColumns, ReportColumns, r
WITH ReportColumns ,collect({{reportName: r.reportName, reportLocation: r.reportLocation, numberOfColumns: numOfColumns, overlapRatio: (size(ReportColumns) * 1.00) / numOfColumns}}) AS report_cluster
WHERE size(report_cluster) > 1 AND size(ReportColumns) > 1
WITH report_cluster, ReportColumns
UNWIND report_cluster as report
WITH avg(report.overlapRatio) as averageOverlapRatio, COLLECT(report) as report_cluster, ReportColumns
RETURN {{averageOverlapRatio: averageOverlapRatio, reports: report_cluster}} as GroupOfReportsToConsolidate, {{sharedColumns: ReportColumns, amountOfSharedColumns: size(ReportColumns)}} as SharedColumnsBetweenReports
ORDER BY GroupOfReportsToConsolidate.averageOverlapRatio DESC
LIMIT 5;
""",
    },
    {
        "question": "Shuggest reports that could be consolidated in the functional area Loss Draft",
        "query":
"""MATCH (r:SSRSReport)-[:HAS_COLUMN]->(col:SQLColumn)-[:MATCH_TERM]->(:Term)-[:HAS_CATEGORY]->(:TermCategory)-[:HAS_FUNCTIONAL_AREA]->(fa:TermFunctionalArea)
WHERE fa.termFunctionalArea = 'Loss Draft'
WITH r, collect(DISTINCT(col.SQLColumnName)) as ReportColumns
WITH r, ReportColumns
MATCH (r)-[c:HAS_COLUMN]->(col:SQLColumn)
WITH COUNT(DISTINCT(col)) AS numOfColumns, ReportColumns, r
WITH ReportColumns ,collect({{reportName: r.reportName, reportLocation: r.reportLocation, numberOfColumns: numOfColumns, overlapRatio: (size(ReportColumns) * 1.00) / numOfColumns}}) AS report_cluster
WHERE size(report_cluster) > 1 AND size(ReportColumns) > 1
WITH report_cluster, ReportColumns
UNWIND report_cluster as report
WITH avg(report.overlapRatio) as averageOverlapRatio, COLLECT(report) as report_cluster, ReportColumns
RETURN {{averageOverlapRatio: averageOverlapRatio, reports: report_cluster}} as GroupOfReportsToConsolidate, {{sharedColumns: ReportColumns, amountOfSharedColumns: size(ReportColumns)}} as SharedColumnsBetweenReports
ORDER BY GroupOfReportsToConsolidate.averageOverlapRatio DESC
LIMIT 5;
""",
    },
    {
        "question": "Show me which reports I could consolidate in the funcitonal area Loss Draft",
        "query":
"""MATCH (r:SSRSReport)-[:HAS_COLUMN]->(col:SQLColumn)-[:MATCH_TERM]->(:Term)-[:HAS_CATEGORY]->(:TermCategory)-[:HAS_FUNCTIONAL_AREA]->(fa:TermFunctionalArea)
WHERE fa.termFunctionalArea = 'Loss Draft'
WITH r, collect(DISTINCT(col.SQLColumnName)) as ReportColumns
WITH r, ReportColumns
MATCH (r)-[c:HAS_COLUMN]->(col:SQLColumn)
WITH COUNT(DISTINCT(col)) AS numOfColumns, ReportColumns, r
WITH ReportColumns ,collect({{reportName: r.reportName, reportLocation: r.reportLocation, numberOfColumns: numOfColumns, overlapRatio: (size(ReportColumns) * 1.00) / numOfColumns}}) AS report_cluster
WHERE size(report_cluster) > 1 AND size(ReportColumns) > 1
WITH report_cluster, ReportColumns
UNWIND report_cluster as report
WITH avg(report.overlapRatio) as averageOverlapRatio, COLLECT(report) as report_cluster, ReportColumns
RETURN {{averageOverlapRatio: averageOverlapRatio, reports: report_cluster}} as GroupOfReportsToConsolidate, {{sharedColumns: ReportColumns, amountOfSharedColumns: size(ReportColumns)}} as SharedColumnsBetweenReports
ORDER BY GroupOfReportsToConsolidate.averageOverlapRatio DESC
LIMIT 5;
""",
    },
    {
        "question": "Show me opportunities to consolidate reports in the functional area Loss Draft",
        "query":
"""MATCH (r:SSRSReport)-[:HAS_COLUMN]->(col:SQLColumn)-[:MATCH_TERM]->(:Term)-[:HAS_CATEGORY]->(:TermCategory)-[:HAS_FUNCTIONAL_AREA]->(fa:TermFunctionalArea)
WHERE fa.termFunctionalArea = 'Loss Draft'
WITH r, collect(DISTINCT(col.SQLColumnName)) as ReportColumns
WITH r, ReportColumns
MATCH (r)-[c:HAS_COLUMN]->(col:SQLColumn)
WITH COUNT(DISTINCT(col)) AS numOfColumns, ReportColumns, r
WITH ReportColumns ,collect({{reportName: r.reportName, reportLocation: r.reportLocation, numberOfColumns: numOfColumns, overlapRatio: (size(ReportColumns) * 1.00) / numOfColumns}}) AS report_cluster
WHERE size(report_cluster) > 1 AND size(ReportColumns) > 1
WITH report_cluster, ReportColumns
UNWIND report_cluster as report
WITH avg(report.overlapRatio) as averageOverlapRatio, COLLECT(report) as report_cluster, ReportColumns
RETURN {{averageOverlapRatio: averageOverlapRatio, reports: report_cluster}} as GroupOfReportsToConsolidate, {{sharedColumns: ReportColumns, amountOfSharedColumns: size(ReportColumns)}} as SharedColumnsBetweenReports
ORDER BY GroupOfReportsToConsolidate.averageOverlapRatio DESC
LIMIT 5;
""",
    },
    {
        "question": "Show me opportunities to consolidate reports in the functional area Quality",
        "query":
"""MATCH (r:SSRSReport)-[:HAS_COLUMN]->(col:SQLColumn)-[:MATCH_TERM]->(:Term)-[:HAS_CATEGORY]->(:TermCategory)-[:HAS_FUNCTIONAL_AREA]->(fa:TermFunctionalArea)
WHERE fa.termFunctionalArea = 'Quality'
WITH r, collect(DISTINCT(col.SQLColumnName)) as ReportColumns
WITH r, ReportColumns
MATCH (r)-[c:HAS_COLUMN]->(col:SQLColumn)
WITH COUNT(DISTINCT(col)) AS numOfColumns, ReportColumns, r
WITH ReportColumns ,collect({{reportName: r.reportName, reportLocation: r.reportLocation, numberOfColumns: numOfColumns, overlapRatio: (size(ReportColumns) * 1.00) / numOfColumns}}) AS report_cluster
WHERE size(report_cluster) > 1 AND size(ReportColumns) > 1
WITH report_cluster, ReportColumns
UNWIND report_cluster as report
WITH avg(report.overlapRatio) as averageOverlapRatio, COLLECT(report) as report_cluster, ReportColumns
RETURN {{averageOverlapRatio: averageOverlapRatio, reports: report_cluster}} as GroupOfReportsToConsolidate, {{sharedColumns: ReportColumns, amountOfSharedColumns: size(ReportColumns)}} as SharedColumnsBetweenReports
ORDER BY GroupOfReportsToConsolidate.averageOverlapRatio DESC
LIMIT 5;
""",
    },
    {
        "question": "Show me opportunities to consolidate reports in the functional area Insurance Tracking",
        "query":
"""MATCH (r:SSRSReport)-[:HAS_COLUMN]->(col:SQLColumn)-[:MATCH_TERM]->(:Term)-[:HAS_CATEGORY]->(:TermCategory)-[:HAS_FUNCTIONAL_AREA]->(fa:TermFunctionalArea)
WHERE fa.termFunctionalArea = 'Insurance Tracking'
WITH r, collect(DISTINCT(col.SQLColumnName)) as ReportColumns
WITH r, ReportColumns
MATCH (r)-[c:HAS_COLUMN]->(col:SQLColumn)
WITH COUNT(DISTINCT(col)) AS numOfColumns, ReportColumns, r
WITH ReportColumns ,collect({{reportName: r.reportName, reportLocation: r.reportLocation, numberOfColumns: numOfColumns, overlapRatio: (size(ReportColumns) * 1.00) / numOfColumns}}) AS report_cluster
WHERE size(report_cluster) > 1 AND size(ReportColumns) > 1
WITH report_cluster, ReportColumns
UNWIND report_cluster as report
WITH avg(report.overlapRatio) as averageOverlapRatio, COLLECT(report) as report_cluster, ReportColumns
RETURN {{averageOverlapRatio: averageOverlapRatio, reports: report_cluster}} as GroupOfReportsToConsolidate, {{sharedColumns: ReportColumns, amountOfSharedColumns: size(ReportColumns)}} as SharedColumnsBetweenReports
ORDER BY GroupOfReportsToConsolidate.averageOverlapRatio DESC
LIMIT 5;
""",
    },
    {
        "question": "Show me groups of more than 2 reports that I should consider consolidating and that share more than 3 columns among each other, belonging to the functional area Insurance Tracking",
        "query":
"""MATCH (r:SSRSReport)-[:HAS_COLUMN]->(col:SQLColumn)-[:MATCH_TERM]->(:Term)-[:HAS_CATEGORY]->(:TermCategory)-[:HAS_FUNCTIONAL_AREA]->(fa:TermFunctionalArea)
WHERE fa.termFunctionalArea = 'Insurance Tracking'
WITH r, collect(DISTINCT(col.SQLColumnName)) as ReportColumns
WITH r, ReportColumns
MATCH (r)-[c:HAS_COLUMN]->(col:SQLColumn)
WITH COUNT(DISTINCT(col)) AS numOfColumns, ReportColumns, r
WITH ReportColumns ,collect({{reportName: r.reportName, reportLocation: r.reportLocation, numberOfColumns: numOfColumns, overlapRatio: (size(ReportColumns) * 1.00) / numOfColumns}}) AS report_cluster
WHERE size(report_cluster) > 2 AND size(ReportColumns) > 3
WITH report_cluster, ReportColumns
UNWIND report_cluster as report
WITH avg(report.overlapRatio) as averageOverlapRatio, COLLECT(report) as report_cluster, ReportColumns
RETURN {{averageOverlapRatio: averageOverlapRatio, reports: report_cluster}} as GroupOfReportsToConsolidate, {{sharedColumns: ReportColumns, amountOfSharedColumns: size(ReportColumns)}} as SharedColumnsBetweenReports
ORDER BY GroupOfReportsToConsolidate.averageOverlapRatio DESC
LIMIT 5;
""",
    },
    {
        "question": "Show opportunities to consolidate reports that share 6 or more columns in the functional area Quality",
        "query":
"""MATCH (r:SSRSReport)-[:HAS_COLUMN]->(col:SQLColumn)-[:MATCH_TERM]->(:Term)-[:HAS_CATEGORY]->(:TermCategory)-[:HAS_FUNCTIONAL_AREA]->(fa:TermFunctionalArea)
WHERE fa.termFunctionalArea = 'Quality'
WITH r, collect(DISTINCT(col.SQLColumnName)) as ReportColumns
WITH r, ReportColumns
MATCH (r)-[c:HAS_COLUMN]->(col:SQLColumn)
WITH COUNT(DISTINCT(col)) AS numOfColumns, ReportColumns, r
WITH ReportColumns ,collect({{reportName: r.reportName, reportLocation: r.reportLocation, numberOfColumns: numOfColumns, overlapRatio: (size(ReportColumns) * 1.00) / numOfColumns}}) AS report_cluster
WHERE size(report_cluster) > 1 AND size(ReportColumns) > 5
WITH report_cluster, ReportColumns
UNWIND report_cluster as report
WITH avg(report.overlapRatio) as averageOverlapRatio, COLLECT(report) as report_cluster, ReportColumns
RETURN {{averageOverlapRatio: averageOverlapRatio, reports: report_cluster}} as GroupOfReportsToConsolidate, {{sharedColumns: ReportColumns, amountOfSharedColumns: size(ReportColumns)}} as SharedColumnsBetweenReports
ORDER BY GroupOfReportsToConsolidate.averageOverlapRatio DESC
LIMIT 5;
""",
    },
    {
        "question": "Show opportunities to consolidate more than 4 reports and share at least 3 columns in the functional area Loss Draft",
        "query":
"""MATCH (r:SSRSReport)-[:HAS_COLUMN]->(col:SQLColumn)-[:MATCH_TERM]->(:Term)-[:HAS_CATEGORY]->(:TermCategory)-[:HAS_FUNCTIONAL_AREA]->(fa:TermFunctionalArea)
WHERE fa.termFunctionalArea = 'Loss Draft'
WITH r, collect(DISTINCT(col.SQLColumnName)) as ReportColumns
WITH r, ReportColumns
MATCH (r)-[c:HAS_COLUMN]->(col:SQLColumn)
WITH COUNT(DISTINCT(col)) AS numOfColumns, ReportColumns, r
WITH ReportColumns ,collect({{reportName: r.reportName, reportLocation: r.reportLocation, numberOfColumns: numOfColumns, overlapRatio: (size(ReportColumns) * 1.00) / numOfColumns}}) AS report_cluster
WHERE size(report_cluster) > 4 AND size(ReportColumns) > 3
WITH report_cluster, ReportColumns
UNWIND report_cluster as report
WITH avg(report.overlapRatio) as averageOverlapRatio, COLLECT(report) as report_cluster, ReportColumns
RETURN {{averageOverlapRatio: averageOverlapRatio, reports: report_cluster}} as GroupOfReportsToConsolidate, {{sharedColumns: ReportColumns, amountOfSharedColumns: size(ReportColumns)}} as SharedColumnsBetweenReports
ORDER BY GroupOfReportsToConsolidate.averageOverlapRatio DESC
LIMIT 5;
""",
    },
    {
        "question": "What is the definition for the term Fema Event, to which category belongs and which reports are related to this term ?",
        "query":
"""MATCH (term:Term {termName: 'Fema Event'})-[:HAS_DEFINITION]->(definition:Definition), (term)-[:HAS_CATEGORY]->(category:TermCategory), (term)-[:MATCH_SQL_COLUMN]->(column:SQLColumn)-[:HAS_REPORT]->(report:SSRSReport)
WITH term , category, definition, COLLECT({{reportName: report.reportName, reportLocation: report.reportLocation}}) as reports
RETURN {{termName: term.termName, definition: definition.termDefinition, category: category.termCategory, reports:reports}}
""",
    },
    {
        "question": "What is the meaning of Incurred Amount? Show me some reports that contain this term. What other terms are mentioned among these reports?",
        "query":
"""MATCH (t:Term)-[:HAS_DEFINITION]->(d:Definition), (t)-[:HAS_CATEGORY]-(tc:TermCategory)-[:HAS_FUNCTIONAL_AREA]-(tfa:TermFunctionalArea)-[:HAS_BUSINESS_SEGMENT]-(tb:BusinessSegment)
WHERE t.termName = 'Incurred Amount' AND d.termDefinition IS NOT NULL
WITH t, d, tc, tfa, tb
MATCH (report:SSRSReport)-[:HAS_COLUMN]->(column:SQLColumn)-[:MATCH_TERM]->(t)
WITH t, d, tc, tfa, tb, report
MATCH (report)-[:HAS_COLUMN]->(col:SQLColumn)-[:MATCH_TERM]->(otherTerm:Term)
WHERE otherTerm <> t
RETURN t.termName, d.termDefinition, tc.termCategory, tfa.termFunctionalArea, tb.termBusinessSegment, report.reportName as ReportName, report.reportLocation as ReportLocation, COLLECT(DISTINCT otherTerm.termName) AS commonTerms
LIMIT 10;
""",
    },
    {
        "question": "What is the meaning of Incurred Amount? Show me some reports that contain this term. What other terms are mentioned among these reports?",
        "query":
"""MATCH (t:Term)-[:HAS_DEFINITION]->(d:Definition), (t)-[:HAS_CATEGORY]-(tc:TermCategory)-[:HAS_FUNCTIONAL_AREA]-(tfa:TermFunctionalArea)-[:HAS_BUSINESS_SEGMENT]-(tb:BusinessSegment)
WHERE t.termName = 'Incurred Amount' AND d.termDefinition IS NOT NULL
WITH t, d, tc, tfa, tb
MATCH (report:SSRSReport)-[:HAS_COLUMN]->(column:SQLColumn)-[:MATCH_TERM]->(t)
WITH t, d, tc, tfa, tb, report
MATCH (report)-[:HAS_COLUMN]->(col:SQLColumn)-[:MATCH_TERM]->(otherTerm:Term)
WHERE otherTerm <> t
RETURN t.termName, d.termDefinition, tc.termCategory, tfa.termFunctionalArea, tb.termBusinessSegment, report.reportName as ReportName, report.reportLocation as ReportLocation, COLLECT(DISTINCT otherTerm.termName) AS commonTerms
LIMIT 10;
""",
    },
    {
        "question": "What is the definition for Client name",
        "query":
"""MATCH (t:Term)-[:HAS_DEFINITION]->(d:Definition), (t)-[:HAS_CATEGORY]-(tc:TermCategory)-[:HAS_FUNCTIONAL_AREA]-(tfa:TermFunctionalArea)-[:HAS_BUSINESS_SEGMENT]-(tb:BusinessSegment)
WHERE t.termName = 'Client Name' AND d.termDefinition IS NOT NULL
RETURN t.termName, d.termDefinition, tc.termCategory, tfa.termFunctionalArea, tb.termBusinessSegment;
""",
    },
]