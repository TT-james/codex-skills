param(
    [Parameter(Mandatory=$true)]
    [ValidateSet('inspect','update','expand')]
    [string]$Mode,

    [Parameter(Mandatory=$true)]
    [string]$ReportPath,

    [string]$OutPath,
    [string]$SqlDir,

    [string]$StartDate = '2026-04-01 00:00:00',
    [string]$EndDate = '2026-04-30 23:59:59',
    [string]$StartYear = '2026-01-01 00:00:00',
    [string]$EndYear = '2026-04-30 23:59:59',
    [string]$MineCode = ''
)

$ErrorActionPreference = 'Stop'

function New-BuildDir {
    $dir = Join-Path $env:TEMP ('runqian_dataset_' + [Guid]::NewGuid().ToString('N'))
    New-Item -ItemType Directory -Force -Path $dir | Out-Null
    return $dir
}

function Get-RunqianClasspath([string]$BuildDir) {
    return @(
        $BuildDir,
        'D:\Program Files\raqsoft\report\classes',
        'D:\Program Files\raqsoft\report\lib\*',
        'D:\Program Files\raqsoft\report\web\webapps\demo\WEB-INF\lib\*',
        'D:\Program Files\raqsoft\report\web\webapps\demo\WEB-INF\classes',
        'D:\Program Files\raqsoft\report\web\tomcat\lib\*',
        'D:\Program Files\raqsoft\common\jdbc\*'
    ) -join ';'
}

function Write-JavaSources([string]$BuildDir) {
    $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    $inspectSource = @'
import com.raqsoft.report.ide.usermodel.ReportEditor;
import com.raqsoft.report.ide.usermodel.ReportModel;
import com.raqsoft.report.usermodel.DataSetConfig;
import com.raqsoft.report.usermodel.DataSetMetaData;
import com.raqsoft.report.usermodel.SQLDataSetConfig;

public class InspectRaqsoftReport {
    public static void main(String[] args) throws Exception {
        ReportEditor editor = new ReportEditor();
        editor.loadReport(args[0]);
        ReportModel model = editor.getReportModel();
        DataSetMetaData metaData = model.getDataSetMetaData();
        for (int i = 0; i < metaData.getDataSetConfigCount(); i++) {
            DataSetConfig config = metaData.getDataSetConfig(i);
            String sql = "";
            if (config instanceof SQLDataSetConfig) {
                sql = ((SQLDataSetConfig) config).getSQL();
            }
            System.out.println("DATASET\t" + config.getName() + "\t" + config.getDataSourceName() + "\t" + sql.length());
            System.out.println(sql.replace("\r", "").replace("\n", "\\n"));
        }
    }
}
'@
    [System.IO.File]::WriteAllText((Join-Path $BuildDir 'InspectRaqsoftReport.java'), $inspectSource, $utf8NoBom)

    $updateSource = @'
import com.raqsoft.report.ide.usermodel.ReportEditor;
import com.raqsoft.report.ide.usermodel.ReportModel;
import com.raqsoft.report.usermodel.DataSetConfig;
import com.raqsoft.report.usermodel.DataSetMetaData;
import com.raqsoft.report.usermodel.SQLDataSetConfig;
import java.io.File;
import java.nio.charset.Charset;
import java.nio.file.Files;

public class UpdateRunqianReportFromSqlDir {
    public static void main(String[] args) throws Exception {
        File[] sqlFiles = new File(args[1]).listFiles();
        if (sqlFiles == null || sqlFiles.length == 0) {
            throw new IllegalStateException("No SQL files found in: " + args[1]);
        }
        ReportEditor editor = new ReportEditor();
        editor.loadReport(args[0]);
        ReportModel model = editor.getReportModel();
        DataSetMetaData metaData = model.getDataSetMetaData();
        Charset utf8 = Charset.forName("UTF-8");
        for (File sqlFile : sqlFiles) {
            if (!sqlFile.isFile() || !sqlFile.getName().endsWith(".sql")) {
                continue;
            }
            String name = sqlFile.getName().substring(0, sqlFile.getName().length() - 4);
            DataSetConfig config = metaData.getDataSetConfig(name);
            if (config == null || !(config instanceof SQLDataSetConfig)) {
                throw new IllegalStateException("SQL dataset not found: " + name);
            }
            String sql = new String(Files.readAllBytes(sqlFile.toPath()), utf8);
            ((SQLDataSetConfig) config).setSQL(sql);
            config.setDataSourceName("matrix_cloud");
        }
        if (!editor.saveReport(args[0])) {
            throw new IllegalStateException("saveReport returned false");
        }
    }
}
'@
    [System.IO.File]::WriteAllText((Join-Path $BuildDir 'UpdateRunqianReportFromSqlDir.java'), $updateSource, $utf8NoBom)
}

function Compile-Java([string]$BuildDir, [string]$Classpath) {
    javac -encoding UTF-8 -cp $Classpath (Join-Path $BuildDir 'InspectRaqsoftReport.java') (Join-Path $BuildDir 'UpdateRunqianReportFromSqlDir.java')
}

function Invoke-Inspect([string]$BuildDir, [string]$Classpath, [string]$Report) {
    return java -cp $Classpath InspectRaqsoftReport $Report
}

function Convert-SqlValue([object]$Value) {
    if ($null -eq $Value -or [string]$Value -eq '') {
        return 'NULL'
    }
    return "'" + ([string]$Value).Replace("'", "''") + "'"
}

function Get-ParamsForDataset([string]$Name, [int]$PlaceholderCount) {
    $p = New-Object System.Collections.Generic.List[object]
    if ($Name -eq 'buy') {
        for ($i = 0; $i -lt 3; $i++) { $p.Add($MineCode); $p.Add($MineCode); $p.Add($StartDate); $p.Add($EndDate) }
        for ($i = 0; $i -lt 3; $i++) { $p.Add($MineCode); $p.Add($MineCode); $p.Add($StartYear); $p.Add($EndYear) }
    } elseif ($Name -eq 'other') {
        for ($i = 0; $i -lt 7; $i++) { $p.Add($MineCode); $p.Add($MineCode); $p.Add($StartDate); $p.Add($EndDate) }
    } elseif ($Name -eq 'otherYear') {
        for ($i = 0; $i -lt 7; $i++) { $p.Add($MineCode); $p.Add($MineCode); $p.Add($StartYear); $p.Add($EndYear) }
    } elseif ($Name -eq 'buyMonthSum') {
        for ($i = 0; $i -lt 3; $i++) { $p.Add($StartDate); $p.Add($EndDate) }
    } elseif ($Name -eq 'buyYearSum') {
        for ($i = 0; $i -lt 3; $i++) { $p.Add($StartYear); $p.Add($EndYear) }
    } elseif ($Name -eq 'otherMonthSum') {
        for ($i = 0; $i -lt 7; $i++) { $p.Add($StartDate); $p.Add($EndDate) }
    } elseif ($Name -eq 'otherYearSum') {
        for ($i = 0; $i -lt 7; $i++) { $p.Add($StartYear); $p.Add($EndYear) }
    } else {
        throw "Unknown dataset: $Name"
    }
    if ($p.Count -ne $PlaceholderCount) {
        throw "$Name parameter count mismatch: sql=$PlaceholderCount generated=$($p.Count)"
    }
    return $p
}

function Expand-Sql([string]$Sql, [System.Collections.Generic.List[object]]$Params) {
    $script:__RunqianParamIdx = 0
    $expanded = [regex]::Replace($Sql, '\?', {
        param($m)
        $value = Convert-SqlValue $Params[$script:__RunqianParamIdx]
        $script:__RunqianParamIdx = $script:__RunqianParamIdx + 1
        return $value
    })
    if ($script:__RunqianParamIdx -ne $Params.Count) {
        throw "Replacement mismatch: used=$script:__RunqianParamIdx params=$($Params.Count)"
    }
    return $expanded
}

function Resolve-OutputPath([string]$PathValue) {
    if ([System.IO.Path]::IsPathRooted($PathValue)) {
        return [System.IO.Path]::GetFullPath($PathValue)
    }
    return [System.IO.Path]::GetFullPath((Join-Path (Get-Location) $PathValue))
}

function Parse-InspectLines([string[]]$Lines) {
    $items = New-Object System.Collections.Generic.List[object]
    for ($i = 0; $i -lt $Lines.Count; $i++) {
        if ($Lines[$i].StartsWith('DATASET' + "`t")) {
            $parts = $Lines[$i].Split("`t")
            $sql = ''
            if ($i + 1 -lt $Lines.Count) {
                $sql = $Lines[$i + 1].Replace('\n', "`n")
            }
            $items.Add([pscustomobject]@{ Name = $parts[1]; DataSource = $parts[2]; Sql = $sql })
        }
    }
    return $items
}

if (-not (Test-Path -LiteralPath $ReportPath)) {
    throw "Report not found: $ReportPath"
}

$buildDir = New-BuildDir
try {
    Write-JavaSources $buildDir
    $cp = Get-RunqianClasspath $buildDir
    Compile-Java $buildDir $cp

    if ($Mode -eq 'inspect') {
        if (-not $OutPath) { throw '-OutPath is required for inspect mode' }
        $lines = Invoke-Inspect $buildDir $cp $ReportPath
        $outFull = Resolve-OutputPath $OutPath
        New-Item -ItemType Directory -Force -Path (Split-Path $outFull -Parent) | Out-Null
        $lines | Set-Content -LiteralPath $outFull -Encoding UTF8
        Write-Output $outFull
    } elseif ($Mode -eq 'update') {
        if (-not $SqlDir) { throw '-SqlDir is required for update mode' }
        java -cp $cp UpdateRunqianReportFromSqlDir $ReportPath $SqlDir
        Write-Output "updated=$ReportPath"
    } elseif ($Mode -eq 'expand') {
        if (-not $OutPath) { throw '-OutPath is required for expand mode' }
        $lines = Invoke-Inspect $buildDir $cp $ReportPath
        $items = Parse-InspectLines $lines
        $md = New-Object System.Collections.Generic.List[string]
        $md.Add("# Runqian dataset SQL - expanded parameters")
        $md.Add('')
        $md.Add('| Param | Value |')
        $md.Add('|---|---|')
        $md.Add("| startDate | $StartDate |")
        $md.Add("| endDate | $EndDate |")
        $md.Add("| startYear | $StartYear |")
        $md.Add("| endYear | $EndYear |")
        $md.Add("| mineCode | $(if ($MineCode -eq '') { 'NULL' } else { $MineCode }) |")
        $md.Add('')
        foreach ($item in $items) {
            $count = ([regex]::Matches($item.Sql, '\?')).Count
            $params = Get-ParamsForDataset $item.Name $count
            $expanded = Expand-Sql $item.Sql $params
            $paramOrder = ($params | ForEach-Object { Convert-SqlValue $_ }) -join ', '
            $md.Add("## $($item.Name)")
            $md.Add('')
            $md.Add("- datasource: ``$($item.DataSource)``")
            $md.Add("- parameter count: $($params.Count)")
            $md.Add("- parameter order: $paramOrder")
            $md.Add('')
            $md.Add('```sql')
            $md.Add($expanded.Trim())
            $md.Add('```')
            $md.Add('')
        }
        $outFull = Resolve-OutputPath $OutPath
        New-Item -ItemType Directory -Force -Path (Split-Path $outFull -Parent) | Out-Null
        $md | Set-Content -LiteralPath $outFull -Encoding UTF8
        Write-Output $outFull
    }
} finally {
    if (Test-Path -LiteralPath $buildDir) {
        Remove-Item -LiteralPath $buildDir -Recurse -Force
    }
}
