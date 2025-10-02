Write-Output "============================================"
Write-Output "  Influence OS by Black Aqua India Pvt Ltd  "
Write-Output "============================================"

# Set tap coordinates
$x = 500
$y = 400

# Get list of connected devices
$devices = adb devices | Select-String "device$" | ForEach-Object { ($_ -split "`t")[0] }

if ($devices.Count -eq 0) {
    Write-Output "No devices connected."
    Read-Host "Press Enter to exit..."
    exit
}

foreach ($device in $devices) {
    Write-Output ""
    Write-Output "Running on device: $device"

    # Start the Automate flow
    adb -s $device shell am start -a android.intent.action.VIEW -d "content://com.llamalab.automate.provider/flows/124"

    # Wait a bit for the window to load
    Start-Sleep -Seconds 2

    # Tap the screen at the specified coordinates
    adb -s $device shell input tap $x $y
}

Write-Output "`nScript execution completed!"
Write-Output "============================================"
Write-Output "  Influence OS by Black Aqua India Pvt Ltd  "
Write-Output "============================================"
