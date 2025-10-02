Write-Output "======================================"
Write-Output "     Influence OS by Black Aqua India Pvt Ltd"
Write-Output "======================================"
Write-Output "`nStarting script to close all recent apps..." 

Start-Sleep -Seconds 1
for ($i = 1; $i -le 3; $i++) {
    Write-Output "`n$i of 3"
    $devices = adb devices | Select-String "device$" | ForEach-Object { ($_ -split '\s+')[0] }
    foreach ($device in $devices) {
        Write-Output "Closing recent apps on device: $device"
        adb -s $device shell input keyevent KEYCODE_HOME
        Start-Sleep -Milliseconds 100  # Small delay
        adb -s $device shell input keyevent KEYCODE_APP_SWITCH
        Start-Sleep -Milliseconds 100  # Small delay
        adb -s $device shell input tap 350 1450
        Start-Sleep -Milliseconds 100  # Small delay
    }
    Write-Output "All apps cleared on all devices! - $i"
    Start-Sleep -Seconds 1  # Small delay before next iteration
}

Write-Output "`nAll apps cleared on all devices!"
Write-Output "======================================"
Write-Output "     Influence OS by Black Aqua India Pvt Ltd"
Write-Output "======================================"
