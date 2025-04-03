param (
    [string]$Target = "127.0.0.1",       # Địa chỉ IP hoặc hostname cần quét
    [string]$Mode = "",                 # Chế độ quét: Popular, WellKnown, Unknown, Custom, File
    [string]$Ports = "",                # Danh sách cổng nhập thủ công (VD: "22,80,443")
    [string]$PortFile = "",             # File TXT chứa danh sách cổng (mỗi cổng 1 dòng)
    [int]$Timeout = 100,                # Thời gian timeout (milliseconds)
    [string]$OutputFile = ""            # Xuất kết quả ra file (nếu cần)
)

# Danh sách cổng phổ biến
$PopularPorts = @(21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 3306, 3389, 8080, 5900, 2525, 1723, 465, 587, 993, 995, 636, 8443, 8888, 25565, 5000, 67, 68)

# Cổng well-known (1-1023)
$WellKnownPorts = 1..1023

# Cổng unknown (ngẫu nhiên từ 1024-65535, chọn 50 cổng)
$UnknownPorts = Get-Random -InputObject (1024..65535) -Count 50

# Xác định danh sách cổng cần quét
switch ($Mode) {
    "Popular"   { $PortsToScan = $PopularPorts }
    "WellKnown" { $PortsToScan = $WellKnownPorts }
    "Unknown"   { $PortsToScan = $UnknownPorts }
    "Custom"    { 
        if ($Ports -ne "") {
            $PortsToScan = $Ports -split "," | ForEach-Object { [int]$_ }
        } else {
            Write-Host "❌ Bạn cần nhập danh sách cổng bằng -Ports `"22,80,443`"" -ForegroundColor Red
            exit
        }
    }
    "File" {
        if (Test-Path $PortFile) {
            $PortsToScan = Get-Content $PortFile | ForEach-Object { [int]$_ }
        } else {
            Write-Host "❌ Không tìm thấy file: $PortFile" -ForegroundColor Red
            exit
        }
    }
    default {
        Write-Host "❌ Chế độ không hợp lệ! Chọn: Popular, WellKnown, Unknown, Custom, File." -ForegroundColor Red
        exit
    }
}

function Scan-Port {
    param (
        [string]$Host,
        [int]$Port,
        [int]$Timeout
    )

    $tcpClient = New-Object System.Net.Sockets.TcpClient
    $asyncResult = $tcpClient.BeginConnect($Host, $Port, $null, $null)
    $wait = $asyncResult.AsyncWaitHandle.WaitOne($Timeout, $false)

    if ($wait -and $tcpClient.Connected) {
        $result = "Cổng $Port mở trên $Host"
        Write-Output $result
        $tcpClient.Close()
        return $result
    } else {
        return $null
    }
}

# Kiểm tra kết nối mạng
if (-not (Test-Connection -ComputerName $Target -Count 1 -Quiet)) {
    Write-Host "❌ Không thể kết nối đến $Target" -ForegroundColor Red
    exit
}

Write-Host "`n🔎 Đang quét chế độ $Mode trên $Target..." -ForegroundColor Cyan
$Results = @()

foreach ($port in $PortsToScan) {
    $scanResult = Scan-Port -Host $Target -Port $port -Timeout $Timeout
    if ($scanResult) {
        $Results += $scanResult
    }
}

Write-Host "`n✅ Quét hoàn tất!" -ForegroundColor Green

# Xuất kết quả ra file nếu được chỉ định
if ($OutputFile -ne "") {
    $Results | Out-File -FilePath $OutputFile -Encoding UTF8
    Write-Host "📂 Kết quả đã lưu vào: $OutputFile" -ForegroundColor Yellow
}
