# Display company branding at the start
Write-Output "============================================"
Write-Output "  Influence OS by Black Aqua India Pvt Ltd  "
Write-Output "============================================"
Write-Output "`nStarting device unlock script..."
Start-Sleep -Seconds 1

# Repeat the whole process 3 times
for ($iteration = 1; $iteration -le 3; $iteration++) {
    Write-Output "`n=== $iteration of 3 ===`n"

    # Get list of connected devices
    $devices = adb devices | Select-String "device$" | ForEach-Object { ($_ -split '\s+')[0] }

    if ($devices.Count -eq 0) {
        Write-Output "No devices connected."
        Read-Host "Press Enter to exit..."
        exit
    }

    foreach ($device in $devices) {
        Write-Output ""
        Write-Output "Checking device: $device"

        # Get current lock status
        $lockStatus = adb -s $device shell dumpsys window | Select-String "mCurrentFocus"
        $wakeStatus = adb -s $device shell dumpsys power | Select-String "mWakefulness="

        Write-Output "Lock Status: $lockStatus"
        Write-Output "Wake Status: $wakeStatus"

        # Logic to determine the device state
        if ($lockStatus -match "com.motorola.launcher3" -or $lockStatus -match "com.android.launcher3") {
            Write-Output "Device is already unlocked. No action needed."
        }
        elseif ($lockStatus -match "NotificationShade" -and $wakeStatus -match "Awake") {
            Write-Output "Device is locked but awake. Swiping up to unlock..."
            adb -s $device shell input swipe 500 1500 500 500
        }
        elseif ($lockStatus -match "NotificationShade" -and $wakeStatus -match "Dozing") {
            Write-Output "Device is locked and asleep. Pressing power button and swiping up..."
            adb -s $device shell input keyevent 26  # Press Power Button
            Start-Sleep -Seconds 1
            adb -s $device shell input swipe 500 1500 500 500  # Swipe up to unlock
        }
        else {
            Write-Output "Unknown state for device $device. No action taken."
        }
    }

    Write-Output "`nDevices Unlocked - $iteration"
    Start-Sleep -Seconds 1  # Optional pause before next iteration
}

# Final branding at the end
Write-Output "`nScript execution completed!"
Write-Output "============================================"
Write-Output "  Influence OS by Black Aqua India Pvt Ltd  "
Write-Output "============================================"
