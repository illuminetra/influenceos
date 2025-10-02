Write-Output "======================================"
Write-Output "     Influence OS by Black Aqua India Pvt Ltd"
Write-Output "======================================"

# Get list of connected devices
$devices = adb devices | Select-String "device$" | ForEach-Object { ($_ -split "`t")[0] }

if ($devices.Count -eq 0) {
    Write-Output "No ADB devices found!"
    exit
}

# Initialize next run times for each device
$deviceSchedule = @{}
foreach ($device in $devices) {
    $deviceSchedule[$device] = (Get-Date)  # Start immediately
}

Write-Output "Starting lightweight device loop..."

while ($true) {
    $now = Get-Date

    foreach ($device in $devices) {
        if ($now -ge $deviceSchedule[$device]) {
            $timestamp = $now.ToString("HH:mm:ss")
            Write-Output "[$timestamp] | Device: $device | Updating startup.txt"

            # Ensure directory exists
            adb -s $device shell "mkdir -p /storage/emulated/0/blackaqualocal"

            # Overwrite startup.txt with '1'
            adb -s $device shell "echo 1 > /storage/emulated/0/blackaqualocal/startup.txt"

            # Schedule next run with random delay (15–30 minutes)
            $delayMinutes = Get-Random -Minimum 15 -Maximum 30
            $deviceSchedule[$device] = $now.AddMinutes($delayMinutes)

            $nextRun = $deviceSchedule[$device].ToString("HH:mm:ss")
            Write-Output "[$timestamp] | Device: $device | Next run in $delayMinutes min (at $nextRun)"
        }
    }

    # Sleep a short interval to avoid tight loop
    Start-Sleep -Seconds 10
}
